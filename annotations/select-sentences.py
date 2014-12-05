#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import fileinput
import codecs

ent = re.compile('<[A-Z]+>[^<]+</[A-Z]+>',re.U)

def main():
    f = codecs.open(sys.argv[1], encoding='utf-8')
    for line in f:
        matches = re.findall(ent,line)
        if len(matches)>1:
            print line.encode("utf-8")

if __name__ == "__main__":
    main()
