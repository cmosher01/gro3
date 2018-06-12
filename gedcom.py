#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import io
import argparse
import functools
import itertools

class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []
    def __repr__(self):
        return repr(self.data)
    def __iter__(self):
        yield self
        for c in itertools.chain(*map(iter, self.children)):
            yield c
    def add(self, c):
        self.children.append(c)
        c.parent = self
        # TODO self.verify(parent==None) ???
        return self
    def verify(self, top=True):
        if top:
            assert not n.parent
        for c in self.children:
            assert c.parent == self
            c.verify(top=False)
    def to_tuple(self):
        return (self.data, tuple([c.to_tuple() for c in self.children]))
    def str_deep(self, lv=0):
        ret = '.'*2*lv+repr(self)+'\n'
        for c in self.children:
            ret += c.str_deep(lv+1)
        return ret
    def mutate(self, f):
        self.data = f(self.data)
        for c in self.children:
            c.mutate(f)
    def mutate_c(self, f):
        self.data = f(self.data, self.children)
        for c in self.children:
            c.mutate_c(f)




PTR = '@'



def gv(n):
    return n.data[0]

def pv(a,n):
    r,pn,pv = a
    if pv < gv(n):
        pn = pn.children[-1]
    elif gv(n) < pv:
        while gv(n) <= gv(pn):
            pn = pn.parent
    return (r,pn.add(n),gv(n))

def unp(p):
    'inverse of str.partition'
    return p[0]+p[1]+p[2]

def is_ptr(s):
    return s.startswith(PTR) and not s.startswith(PTR+PTR)

def conc_cont(d, c):
    i = 0
    n = len(c)
    x,tag,val = d
    while i < n:
        ctag = c[i].data[1]
        if ctag == 'CONC' or ctag == 'CONT':
            sep = '\n' if ctag == 'CONT' else ''
            val = val+sep+c[i].data[2]
            del c[i]
            n = n-1
        else:
            i = i+1
    return (x,tag,val)





e = 'latin-1'
s = io.TextIOWrapper(sys.stdin.buffer, encoding=e)

s = map(str.strip, s)

# level numbers
s = map(lambda n: n.partition(' '), s)
s = map(lambda n: Node((int(n[0]),n[2])), s)

# build tree structure based on levels
n = Node((-1,''))
n,__,__ = functools.reduce(pv, s, (n,n,0))
n.mutate(lambda n: n[1]) # remove level numbers


# ID
n.mutate(lambda n: n.partition(' '))
n.mutate(lambda n: (n[0].strip(PTR),n[2]) if is_ptr(n[0]) else (None,unp(n)))

# tag
n.mutate(lambda n: (n[0],n[1].partition(' ')))
n.mutate(lambda n: (n[0],n[1][0],n[1][2]))



n.mutate_c(conc_cont)

# value (or pointer)
n.mutate(lambda n: (n[0],n[1])+((None,n[2]) if is_ptr(n[2]) else (n[2],None)))

# empty (or whitespace-only) string value --> None
n.mutate(lambda n: (n[0],n[1],n[2].strip() if n[2] else None,n[3]))

# @ptr@ --> ptr
n.mutate(lambda n: (n[0],n[1],n[2],n[3].strip(PTR) if n[3] else None))

# @@ in values --> @
n.mutate(lambda n: (n[0],n[1],n[2].replace(PTR+PTR,PTR) if n[2] else None,n[3]))



print(n.str_deep())
