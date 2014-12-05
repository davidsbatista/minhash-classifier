#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import re
import fileinput
import codecs

ent = re.compile('<[A-Z]+>[^<]+</[A-Z]+>',re.U)


def parseFile(data):
    f = codecs.open(data, encoding='utf-8')
    for line in f:
        if not len(re.findall(ent,line))>2:
            #sys.stdout.write(line.encode("utf8"))
            parts = line.split('\t')
            print re.sub(r"<[A-Z]+>|</[A-Z]+>", "", parts[0]).encode("utf8")
    fileinput.close()


def main():
    parseFile(sys.argv[1])


if __name__ == "__main__":
    main()
