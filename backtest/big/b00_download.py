"""Fetch frozen public input revisions, verifying size and LFS SHA-256.

Usage: python b00_download.py SCRATCH [--october] [--snapshots]
No downloaded Python, pickle or executable is run. Data stay outside Git.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

HF='https://huggingface.co'
REVISIONS={
 'jocry/Pumpfun_Memecoin_Corpus':'bd8aed6452fb81665a74e6c308323f2c825dc82a',
 'pumpdatafun/pump-fun-trades-sample':'c3a429fcd65f15e9ea1feca8a174e617b7e8f396',
}


def request(url):
    return urlopen(Request(url,headers={'User-Agent':'DetourResearch/1.0'}),timeout=120)


def download(repo,dest,select,workers,manifest_name):
    revision=REVISIONS[repo]
    with request(f'{HF}/api/datasets/{repo}/tree/{revision}?recursive=true&limit=1000') as r:
        if r.headers.get('Link'): raise RuntimeError('Paginated tree: explicitly handle pagination before downloading')
        tree=json.load(r)
    entries=[x for x in tree if x['type']=='file' and select(x['path'])]
    if not entries: raise RuntimeError('No selected input files')
    dest.mkdir(parents=True,exist_ok=True)
    def fetch(e):
        name=e['path'];rel=Path(name)
        if rel.is_absolute() or '..' in rel.parts: raise ValueError('Unsafe repository path')
        path=dest/rel;path.parent.mkdir(parents=True,exist_ok=True)
        expected=(e.get('lfs') or {}).get('oid')
        if expected: expected=expected.removeprefix('sha256:')
        if path.exists() and path.stat().st_size==e['size']:
            with path.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
            if not expected or digest==expected:
                return dict(path=name,size=e['size'],sha256=digest,expected_sha256=expected,cached=True)
        last=None
        for attempt in range(3):
            try:
                tmp=path.with_name(path.name+'.part');h=hashlib.sha256()
                url=f'{HF}/datasets/{repo}/resolve/{revision}/{quote(name)}?download=true'
                with request(url) as r,tmp.open('wb') as f:
                    while block:=r.read(1024*1024): f.write(block);h.update(block)
                digest=h.hexdigest()
                if tmp.stat().st_size!=e['size']: raise ValueError('Size mismatch')
                if expected and expected!=digest: raise ValueError('LFS SHA-256 mismatch')
                tmp.replace(path);print('verified',repo,name,flush=True)
                return dict(path=name,size=e['size'],sha256=digest,expected_sha256=expected)
            except Exception as ex:
                last=ex;print('retry',name,attempt+1,type(ex).__name__,flush=True)
        raise RuntimeError(f'Download failed: {name}') from last
    # Always fetch documentation before analytical inputs.
    docs=[e for e in entries if e['path'].endswith('.md')]
    records=[fetch(e) for e in docs]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        records.extend(pool.map(fetch,[e for e in entries if e not in docs]))
    manifest=dict(repo=repo,revision=revision,finished_at=datetime.now(timezone.utc).isoformat(),files=records)
    (dest/manifest_name).write_text(json.dumps(manifest,indent=2),encoding='utf-8')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('scratch')
    p.add_argument('--october',action='store_true');p.add_argument('--snapshots',action='store_true')
    p.add_argument('--workers',type=int,default=4);a=p.parse_args()
    if not 1<=a.workers<=16: p.error('workers must be between 1 and 16')
    base=Path(a.scratch).resolve()/'datasets'
    names={'README.md','KNOWN_ISSUES.md','tokens.parquet','migrations.parquet',
           'postgard_snapshots.parquet','postgard_outcomes.parquet'}
    if a.snapshots: names.add('snapshots.parquet')
    download('jocry/Pumpfun_Memecoin_Corpus',base/'jocry',
             lambda s:s in names or s.startswith('trades/'),a.workers,'download_manifest.json')
    if a.october:
        download('pumpdatafun/pump-fun-trades-sample',base/'pumpdatafun',
                 lambda s:s!='.gitattributes' and not s.startswith('signatures/'),
                 a.workers,'validation_download_manifest.json')
