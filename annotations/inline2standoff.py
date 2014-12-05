#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import re
import fileinput
import codecs

ent = re.compile('<[A-Z]+>[^<]+</[A-Z]+>',re.U)
span_id = int(0)
offset = int(0)
ent_span = dict()

def parseFile(data):
    f = codecs.open(data, encoding='utf-8')
    for line in f:
        findMatches(ent,line)


def findMatches(regex,line):
    global span_id
    global offset
    entities = []

    for match in re.finditer(regex,line):
        etype = line[int(match.start())+1:int(match.start()+4)]
        begin = match.start()+5
        end = match.end()-6
        entity = line[begin:end]
        e = (etype,entity)
        entities.append(e)

    line = re.sub(r"<[A-Z]+>|</[A-Z]+>", "", line)

    for e in entities:

        # see if entity id already exists
        # or create a new one
        """
        try:
            span_id = ent_span[e[1]]
        except:
            span_id = len(ent_span)+1
            ent_span[e[1]] = span_id
        """
        span_id += 1
        start = line.index(e[1])
        end = start + len(e[1])
        print "T"+str(span_id)+'\t'+e[0].encode("utf8")+' '+str(start+offset)+' '+str(end+offset)+'\t'+(e[1].encode("utf8"))
    offset += len(line)


def main():
    parseFile(sys.argv[1])

if __name__ == "__main__":
    main()
