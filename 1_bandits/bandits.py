# %% Define environment

import numpy as np
from numpy.random import rand, randint
import matplotlib.pyplot as plt

# bandits = [(1, 1), (5, 10), (-3, 15), (15, 2), (-24, 3)]


def environment(a, bandits):
    assert 0 <= a < len(bandits)
    mean, dev = bandits[a]
    return mean + (rand() * 2 - 1) * dev


# %% Decision policy

# example: q = [1, 2, 3, 4, 5]
def greedy(q):
    # # assert len(q) > 0
    # if len(q) == 0:
    #     return -1
    # elif len(q) == 1:
    #     return 0
    # else:
    #     maxval = q[0]
    #     maxindex = 0
    #     for i in range(1, len(q)):
    #         if maxval < q[i]:
    #             maxval = q[i]
    #             maxindex = i
    #     return maxindex
    return np.argmax(q)

def softmax(q, t):
    q = [x/t for x in q]
    softmax_values = np.exp(q) / np.sum(np.exp(q), axis=0)

    precalculated_values = []
    precalculated_values.append(softmax_values[0])
    for i in range(1, len(softmax_values)):
        precalculated_values.append(precalculated_values[i-1] + softmax_values[i])

    picker = rand()
    for i in range(len(precalculated_values) - 1):
        first = precalculated_values[i]
        second = precalculated_values[i+1]
        if(first < picker and picker < second ):
            return i + 1
    return 0 # ako nije između prvog i drugog znači da je manji od prvog

def eps_greedy(q, eps=0.1):
    if rand() < eps:
        # choose random action
        return randint(0, len(q))
    else:
        # choose greedy action
        return greedy(q)


greedy([1, 2])
softmax([3.0, 1.0, 0.2], 10)

# %% Learning algorithm


def learn(q, a, r, p=0.9):
    # q(a)_novo = p * q(a)_staro + (1-p)*r
    assert 0 <= a < len(q)
    q[a] = p * q[a] + (1 - p) * r
    return q.copy()


q = [1, 2, 3, 4, 5]
learn(q, 1, 102, 0.5)

# %% Main loop -- Learning & Acting

bandits = [(1, 1), (5, 10), (-3, 15), (15, 2), (-24, 3)]

# q = []
# for b in bandits:
#     q.append(0)
q = [0 for b in bandits]
# q = [1, 5, -3, 15, -24]

actions = []
rewards = []
qs = [q]

for k in range(1000):
    # body of the main learning loop
    # a = eps_greedy(q, 0.2) # test epsilon 
    a = softmax(q, 10)
    r = environment(a, bandits)
    q = learn(q, a, r)
    # logging functions
    actions.append(a)
    rewards.append(r)
    qs.append(q)

# actions

plt.plot(actions, ".")

# %% Plotting

q0 = [q[0] for q in qs]
q1 = [q[1] for q in qs]
q2 = [q[2] for q in qs]
q3 = [q[3] for q in qs]
q4 = [q[4] for q in qs]

plt.plot(q0, "b", label="q0")
plt.plot(q1, "r", label="q1")
plt.plot(q2, "g", label="q2")
plt.plot(q3, "k", label="q3")
plt.plot(q4, "m", label="q4")
plt.legend()
plt.grid()

# %%
