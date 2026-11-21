"""Regression checks for missing API observations and token/pair identity."""
import unittest

from analyze import cohort, trending_transitions


def snapshot(round_number, ids=None, status=200):
    rec = {'status': status, 'response_end_utc': f'2026-11-21T11:0{round_number}:00+00:00'}
    if ids is not None:
        rec['payload'] = {'data': [{'id': x} for x in ids]}
    return {'round': round_number, 'responses': {'trending': rec}}


class SnapshotAnalysisTests(unittest.TestCase):
    def test_429_is_missing_not_empty_ranking(self):
        valid, transitions = trending_transitions([
            snapshot(0, ['a', 'b']), snapshot(1, None, 429), snapshot(2, ['b', 'c'])])
        self.assertEqual([s['round'] for s in valid], [0, 2])
        self.assertEqual(len(transitions), 1)
        self.assertEqual(transitions[0]['elapsed_seconds'], 120)
        self.assertEqual(transitions[0]['retention'], 0.5)
        self.assertEqual(transitions[0]['jaccard'], 1 / 3)

    def test_no_successful_rankings_produce_no_transitions(self):
        valid, transitions = trending_transitions([snapshot(0, None, 429)])
        self.assertEqual(valid, [])
        self.assertEqual(transitions, [])

    def test_multiple_pairs_do_not_duplicate_token_cohort(self):
        pair = {'chainId': 'solana', 'baseToken': {'address': 'mint'}, 'pairAddress': 'one',
                'liquidity': {'usd': 100}, 'priceUsd': '1', 'pairCreatedAt': 1795255200000}
        pair2 = dict(pair, pairAddress='two', liquidity={'usd': 200})
        data = {'responses': {'pairs_0': {'payload': [pair, pair2], 'response_end_utc': '2026-11-21T11:00:00+00:00'}}}
        result = cohort(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['pair'], 'two')


if __name__ == '__main__':
    unittest.main()
