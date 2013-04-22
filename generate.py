import itertools
import argparse

keys = list('cdefgab')

def powerset(s):
    for i in xrange(min(5, len(s))+1):
        for combo in itertools.permutations(s,i):
            yield "".join(combo)


def with_rest(left_hand, right_hand):
    needs_rest = left_hand if len(left_hand) == min(len(left_hand), len(right_hand)) else right_hand
    no_rest = left_hand if len(left_hand) == max(len(left_hand), len(right_hand)) else right_hand
    rests = len(no_rest) - len(needs_rest)
    needs_rest = needs_rest + ['-'] * rests
    for keys in itertools.permutations(needs_rest):
        yield (list(keys), right_hand) \
            if len(left_hand) == min(len(left_hand), len(right_hand)) \
            else (left_hand, list(keys))

def both_hands(bass, treble):
    both_hands = list(itertools.product(powerset(bass), powerset(treble)))
    for left_hand, right_hand in both_hands:
        if left_hand and right_hand:
            left_hand, right_hand = (list(left_hand), list(right_hand))
            if len(left_hand) != len(right_hand):
                for left_hand, right_hand in with_rest(left_hand, right_hand):
                    yield right_hand or ['-'] * len(left_hand), left_hand or ['-'] * len(right_hand)
                continue
            yield right_hand or ['-'] * len(left_hand), left_hand or ['-'] * len(right_hand)

def generate(bass=keys, treble=keys, _filter=None):
    for left_hand, right_hand in both_hands(bass, treble):
        if _filter:
            if list(_filter) in (left_hand, right_hand):
                print 'TREBLE: %s' % left_hand
                print 'BASS: %s' % right_hand
                print '-'*50
        else:
            print 'TREBLE: %s' % left_hand
            print 'BASS: %s' % right_hand
            print '-'*50

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Pianoo')
    parser.add_argument(
        '--bass',
        type=str
    )
    parser.add_argument(
        '--treble',
        type=str
    )
    parser.add_argument(
        '--filter',
        type=str
    )
    args = parser.parse_args()
    generate(args.bass, args.treble, args.filter)