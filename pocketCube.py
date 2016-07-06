# Random scramble generator
# Generate a random state
# Solve it
import random

def randomState():
  '''
  Random state generator
  The idea is to generate a random permutation of the first 7 blocks
  Then determine the orientations
  '''
  permutation = [x * 3 + random.randint(0, 2) for x in range(7)]
  # Fix the permutation so sum is multiply of 3
  if sum(permutation) % 3 == 1:
    if permutation[0] % 3 == 0:
      permutation[0] += 2
    else:
      permutation[0] -= 1
  elif sum(permutation) % 3 == 2:
    if permutation[0] % 3 != 2:
      permutation[0] += 1
    else:
      permutation[0] -= 2
  random.shuffle(permutation)
  rtn = []
  for piece in permutation:
    rtn.append(piece)
    rtn.append(piece + 1 if piece % 3 != 2 else piece - 2)
    rtn.append(piece + 2 if piece % 3 == 0 else piece - 1)
  rtn += [bdr, drb, rbd]
  return tuple(rtn)

def randomScramble():
  while True:
    # Generate random state
    state = randomState()
    # Solve the random state
    scramble = shortest_path(I, state)
    if scramble and len(scramble) >= 4:
      break
  rtn = ''
  for move in scramble:
    rtn += quarter_twists_names[move]
  return rtn

# flu refers to the front face (because f is first) of the cubie that
# has a front face, a left face, and an upper face.
# yob refers to the colors yellow, orange, blue that are on the
# respective faces if the cube is in the solved position.
flu = 0 # (0-th cubie; front face)
luf = 1 # (0-th cubie; left face)
ufl = 2 # (0-th cubie; up face)

fur = 3 # (1-st cubie; front face)
urf = 4 # (1-st cubie; up face)
rfu = 5 # (1-st cubie; right face)

fdl = 6 # (2-nd cubie; front face)
dlf = 7 # (2-nd cubie; down face)
lfd = 8 # (2-nd cubie; left face)

frd = 9 #  (3-rd cubie; front face)
rdf = 10 # (3-rd cubie; right face)
dfr = 11 # (3-rd cubie; down face)

bul = 12 # (4-th cubie; back face)
ulb = 13 # (4-th cubie; up face)
lbu = 14 # (4-th cubie; left face)

bru = 15 # (5-th cubie; back face)
rub = 16 # (5-th cubie; right face)
ubr = 17 # (5-th cubie; up face)

bld = 18 # (6-th cubie; back face)
ldb = 19 # (6-th cubie; left face)
dbl = 20 # (6-th cubie; down face)

bdr = 21 # (7-th cubie; back face)
drb = 22 # (7-th cubie; down face)
rbd = 23 # (7-th cubie; right face)

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

def perm_twice(p):
  '''
  Apply the same permutation twice
  '''
  return perm_apply(p, p)

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
I = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr, bul, ulb, lbu, bru, rub, ubr, bld, ldb, dbl, bdr, drb, rbd)

F = (fdl, dlf, lfd, flu, luf, ufl, frd, rdf, dfr, fur, urf, rfu, 
     bul, ulb, lbu, bru, rub, ubr, bld, ldb, dbl, bdr, drb, rbd)
Fi = perm_inverse(F)
F2 = perm_twice(F)
L = (ulb, lbu, bul, fur, urf, rfu, ufl, flu, luf, frd, rdf, dfr,
     dbl, bld, ldb, bru, rub, ubr, dlf, lfd, fdl, bdr, drb, rbd)
Li = perm_inverse(L)
L2 = perm_twice(L)
U = (rfu, fur, urf, rub, ubr, bru, fdl, dlf, lfd, frd, rdf, dfr,
     luf, ufl, flu, lbu, bul, ulb, bld, ldb, dbl, bdr, drb, rbd)
Ui = perm_inverse(U)
U2 = perm_twice(U)

# All 6 possible moves (assuming that the lower-bottom-right cubie
# stays fixed).
moves = (F, Fi, F2, L, Li, L2, U, Ui, U2)

quarter_twists_names = {}
quarter_twists_names[F] = 'F'
quarter_twists_names[Fi] = 'F\''
quarter_twists_names[F2] = 'F2'
quarter_twists_names[L] = 'L'
quarter_twists_names[Li] = 'L\''
quarter_twists_names[L2] = 'L2'
quarter_twists_names[U] = 'U'
quarter_twists_names[Ui] = 'U\''
quarter_twists_names[U2] = 'U2'

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
  while forwardLevel and backwardLevel and levelCount <= 7:
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
