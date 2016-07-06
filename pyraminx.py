# Pyraminx random state generator
import random

def randomCycle(nums):
  '''
  Randomly scrambles nums in cycle, e.g.
  1234->3412
  '''
  idx = random.randint(0, len(nums) - 1)
  return nums[idx:] + nums[:idx]

def arePermsEqualParity(perm0, perm1):
  '''
  Check if perm0 and perm1 are of the same parity
  '''
  perm1 = perm1[:]
  transCount = 0
  for loc in range(len(perm0) - 1):
    p0 = perm0[loc]
    p1 = perm1[loc]
    if p0 != p1:
      sloc = perm1[loc:].index(p0)+loc
      perm1[loc], perm1[sloc] = p0, p1
      transCount += 1
  return transCount % 2 == 0

def randomEvenPermutation(nums):
  '''
  Generate random even permutation of nums
  '''
  while True:
    permutation = nums[:]
    random.shuffle(permutation)
    if arePermsEqualParity(permutation, nums):
      return nums

def randomState():
  '''
  Random state generator
  The idea is to generate a random permutation of the first 7 blocks
  Then determine the orientations
  '''
  rtn = randomCycle([flr, lrf, rfl]) + randomCycle([fdl, dlf, lfd]) + randomCycle([fdr, drf, rfd]) + randomCycle([rld, ldr, drl])
  pieces = randomEvenPermutation([[fr, rf], [lf, fl], [df, fd], [rl, lr], [dr, rd], [dl, ld]])
  swapCount = 0
  for piece in pieces[:-1]:
    if random.randint(0, 1):
      rtn += piece[::-1]
      swapCount += 1
    else:
      rtn += piece
  if swapCount % 2:
    rtn += pieces[-1][::-1]
  else:
    rtn += pieces[-1]
  return tuple(rtn)

def randomScramble():
  while True:
    # Generate random state
    state = randomState()
    # Solve the random state
    scramble = shortest_path(I, state)
    if scramble and len(scramble) >= 6:
      rtn = ''.join([quarter_twists_names[move] for move in scramble])
      for i, move in enumerate(['l', 'r', 'b', 'u']):
        tmp = random.randint(0, 2)
        if tmp == 1:
          rtn += move
        if tmp == 2:
          rtn += move + '\''
      return rtn

# Centers
flr = 0
lrf = 1
rfl = 2
fdl = 3
dlf = 4
lfd = 5
fdr = 6
drf = 7
rfd = 8
rld = 9
ldr = 10
drl = 11
# Edges
fr = 12
rf = 13
lf = 14
fl = 15
df = 16
fd = 17
rl = 18
lr = 19
dr = 20
rd = 21
dl = 22
ld = 23

'''
A permutation p on 0,1,...,n-1 is represented as
a list of length n-1.  p[i] = j means of course
that p maps i to j.

When operating on a list c (e.g. a list of length
24 of colors), then  p * c
is the rearranged list of colors:
   (p * c)[i] = c[p[i]]    for all i
Thus, p[i] is the location of where the color of
position i will come from; p[i] = j means that
the color at position j moves to position i.
'''

####################################################
### Permutation operations
####################################################

def perm_apply(perm, position):
  '''
  Apply permutation perm to a list position (e.g. of faces).
  Face in position p[i] moves to position i.
  '''
  return tuple([position[i] for i in perm])

def perm_inverse(p):
  '''
  Return the inverse of permutation p.
  '''
  n = len(p)
  q = [0]*n
  for i in range(n):
    q[p[i]] = i
  return tuple(q)

###################################################
### Make standard permutations of faces
###################################################
# Identity: equal to (0, 1, 2, ..., 23).
I = (flr, lrf, rfl, fdl, dlf, lfd, fdr, drf, rfd, rld, ldr, drl, fr, rf, lf, fl, df, fd, rl, lr, dr, rd, dl, ld)

# Front face rotated clockwise.
U = (rfl, flr, lrf, fdl, dlf, lfd, fdr, drf, rfd, rld, ldr, drl, rl, lr, fr, rf, df, fd, lf, fl, dr, rd, dl, ld)
Ui = perm_inverse(U)
L = (flr, lrf, rfl, lfd, fdl, dlf, fdr, drf, rfd, rld, ldr, drl, fr, rf, dl, ld, fl, lf, rl, lr, dr, rd, fd, df)
Li = perm_inverse(L)
R = (flr, lrf, rfl, fdl, dlf, lfd, drf, rfd, fdr, rld, ldr, drl, df, fd, lf, fl, rd, dr, rl, lr, rf, fr, dl, ld)
Ri = perm_inverse(R)
B = (flr, lrf, rfl, fdl, dlf, lfd, fdr, drf, rfd, drl, rld, ldr, fr, rf, lf, fl, df, fd, dr, rd, ld, dl, lr, rl)
Bi = perm_inverse(B)

# All 6 possible moves (assuming that the lower-bottom-right cubie
# stays fixed).
moves = (U, Ui, L, Li, R, Ri, B, Bi)

quarter_twists_names = {}
quarter_twists_names[U] = 'U'
quarter_twists_names[Ui] = 'U\''
quarter_twists_names[L] = 'L'
quarter_twists_names[Li] = 'L\''
quarter_twists_names[R] = 'R'
quarter_twists_names[Ri] = 'R\''
quarter_twists_names[B] = 'B'
quarter_twists_names[Bi] = 'B\''

def shortest_path(start, end):
  '''
  Using 2-way BFS, finds the shortest path from start_position to
  end_position. Returns a list of moves. 

  You can use the rubik.quarter_twists move set.
  Each move can be applied using rubik.perm_apply
  '''
  forwardParent = {}
  backwardParent = {}
  forwardParent[start] = (None, None)
  backwardParent[end] = (None, None)
  forwardLevel = [start]
  backwardLevel = [end]
  levelCount = 0
  def retrievePath(state):
    '''
    Get the moves with state as intermediate state
    '''
    rtn = []
    tmp = state
    while state != start:
      state, move = forwardParent[state]
      rtn.append(move)
    rtn = rtn[::-1]
    state = tmp
    while state != end:
      state, move = backwardParent[state]
      rtn.append(move)
    return rtn
  while forwardLevel and backwardLevel and levelCount <= 6:
    levelCount += 1
    # Update the level
    frontier = []
    for state in forwardLevel:
      if state in backwardParent:
        return retrievePath(state)
      for move in moves:
        neighbor = perm_apply(move, state)
        if neighbor not in forwardParent:
          forwardParent[neighbor] = (state, move)
          frontier.append(neighbor)
    forwardLevel = frontier[:]
    frontier = []
    for state in backwardLevel:
      if state in forwardParent:
        return retrievePath(state)
      for move in moves:
        neighbor = perm_apply(perm_inverse(move), state)
        if neighbor not in backwardParent:
          backwardParent[neighbor] = (state, move)
          frontier.append(neighbor)
    backwardLevel = frontier[:]
  return None

print(randomScramble())
