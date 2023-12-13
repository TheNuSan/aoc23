
import os
import time
wd=os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(wd,"aoc_12_1.txt"), "r") as f:
    data = [(a, tuple(int(n) for n in b.split(','))) for a, b in (l.strip().split() for l in f)]


cachehit=0
cachemiss=0

# Recursive function that computes how many combinations can be made that match
# the rule list. For instance: combinations("????.#...#...", (1,1,1,1)) → 3
def combinations(s, r, n, cache):
    # Handle the easy cases:
    #  - if data is in cache, return the cached value
    #  - if rules are empty, return 1 unless there is still a # in the string, then 0
    #  - if string is too small to possibly match the rules, return 0
    if (s, r) in cache:
        global cachehit
        cachehit+=1
        return cache[(s, r)]
    else:
        global cachemiss
        cachemiss+=1
    if(False): return 0
    elif not r: return int('#' not in s)
    elif len(s) < sum(r) + len(r) - 1: return 0
    # We now consider two (or three) different cases:
    #  - if string starts with '.', call combinations() recursively by stripping
    #    the first character and using the same rules.
    #  - if string starts with '#', ensure that there is no '.' in the first
    #    r[0] characters and that the next character, if any, is not a '#',
    #    then call combinations() recursively on the remaining data.
    #  - if string starts with '?', we add the two previous values!
    if s[0] in '.?':
        n += combinations(s[1:], r, 0, cache)
    if s[0] in '#?' and len(s) >= r[0] and '.' not in s[:r[0]] and (len(s) == r[0] or s[r[0]] != '#'):
        n += combinations(s[r[0] + 1:], r[1:], 0, cache)
    cache[(s, r)] = n
    return n

c1=dict()
t = time.process_time()
print(sum(combinations(s, r, 0, c1) for s, r in data))
print("       ",time.process_time()-t)
print("cache size:",len(c1.keys()),"hit:",cachehit,"miss:",cachemiss,"percent:",100*cachehit/(cachehit+cachemiss))

cachehit=0
cachemiss=0

c2=dict()
t = time.process_time()
print(sum(combinations('?'.join([s] * 5), r * 5, 0, c2) for s, r in data))
print("       ",time.process_time()-t)
print("cache size:",len(c2.keys()),"hit:",cachehit,"miss:",cachemiss,"percent:",100*cachehit/(cachehit+cachemiss))


'''
t = time.process_time()
prog=0
for s, r in data:
 prog+=1
 print(prog,combinations('?'.join([s] * 5), r * 5), time.process_time()-t )
#print(sum(combinations('?'.join([s] * 5), r * 5) ))
print("       ",time.process_time()-t)
'''
