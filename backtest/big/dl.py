import sys
from huggingface_hub import snapshot_download, HfApi
S=sys.argv[1]
snapshot_download("jocry/Pumpfun_Memecoin_Corpus",repo_type="dataset",local_dir=f"{S}/datasets/jocry",max_workers=4)
snapshot_download("pumpdatafun/pump-fun-trades-sample",repo_type="dataset",local_dir=f"{S}/datasets/pumpdatafun",allow_patterns=["README.md","data/*","events/*","launches/*","graduations/*","*.json"],max_workers=4)
print("DONE")
