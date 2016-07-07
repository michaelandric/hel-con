#!/usr/bin/python

from itertools import product

a = []
n = 18

for i in range(1, 1+n):
    a.append([i, i+n])

alist = list(product(*a))

set_n = len(alist)/2.

np.savetxt('perm_mat_a.txt', np.array(alist[:int(set_n)]), fmt='%d')

flip_alist = np.flipud(np.array(alist[int(set_n):]))
np.savetxt('perm_mat_b.txt', flip_alist, fmt='%d')

