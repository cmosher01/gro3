#!/usr/bin/python3
# -*- coding: utf-8 -*-

import fileinput
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
    return p[0]+p[1]+p[2]

def is_ptr(s):
    return s.startswith(PTR) and not s.startswith(PTR+PTR)



s = fileinput.input()
s = map(str.strip, s)

# level numbers
s = map(lambda n: n.partition(' '), s)
s = map(lambda n: Node((int(n[0]),n[2].strip())), s)

# build tree structure based on levels
n = Node((-1,''))
n,_,_ = functools.reduce(pv, s, (n,n,0))
n.mutate(lambda n: n[1]) # remove level numbers

# ID
n.mutate(lambda n: n.partition(' '))
n.mutate(lambda n: (n[0].strip(PTR),n[2]) if is_ptr(n[0]) else (None,unp(n)))

# tag
n.mutate(lambda n: (n[0],n[1].partition(' ')))
n.mutate(lambda n: (n[0],n[1][0],n[1][2]))

# TODO: CONC
# TODO: CONT

# value (or pointer)
n.mutate(lambda n: (n[0],n[1])+((None,n[2]) if is_ptr(n[2]) else (n[2],None)))

# empty string value --> None
n.mutate(lambda n: (n[0],n[1],n[2] if n[2] else None,n[3]))

# @ptr@ --> ptr
n.mutate(lambda n: (n[0],n[1],n[2],n[3].strip(PTR) if n[3] else None))

# @@ --> @ in values
n.mutate(lambda n: (n[0],n[1],n[2].replace(PTR+PTR,PTR) if n[2] else None,n[3]))



print(n.str_deep())
