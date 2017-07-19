#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re
import io
import argparse
from chardet.universaldetector import UniversalDetector

parser = argparse.ArgumentParser()
parser.add_argument('infile', type=argparse.FileType('rb'))
args = parser.parse_args()

print(args.infile.name)

u = UniversalDetector()
p = re.compile(r'^\d+\s+CHAR\s+(.+)$')
c = ''
with args.infile as f:
    i = 512
    for lin in f:
        lin.rstrip()
        m = p.match(lin.decode('latin-1'))
        if m:
            print(m.group(1))
        u.feed(bytearray(lin))
        i = i-1
        if u.done or i <= 0:
            break
    u.close()
print(u.result)
