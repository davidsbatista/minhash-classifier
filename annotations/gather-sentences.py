#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os
import re
import fileinput
import codecs

tokenizer =  r'\w+(?:-\w+)+|\d+(?:[:|/]\d+)+|\d+(?:[.]?[oaºª°])+|\w+\'\w+|\d+(?:[,|.]\d+)*\%?|[\w+\.-]+@[\w\.-]+|https?://[^\s]+|\w+'

relationships = []

class Relationship:
    def __init__(self,_name,_arg1,_arg2,_words):
        self.name = _name
        self.args1 = _arg1
        self.args2 = _arg2
        self.words = _words


class Instance:
    def __init__(self,_arg1Type,_arg2Type,_BEF,_BET,_AFT):
        self.arg1Type = _arg1Type
        self.arg2Type = _arg2Type
        self.BEF = _BEF
        self.BET = _BET
        self.AFT = _AFT


def readSeeds(data):
    f = codecs.open(data, encoding='utf-8')
    for line in f:
        if line.startswith('relation'):
            rel = line.split(":")[1].strip()

        if line.startswith('arg1'):
             tmp = line.split(":")[1].split(",")
             args1 = [ x.strip() for x in tmp]

        if line.startswith('arg2'):
             tmp = line.split(":")[1].split(",")
             args2 = [ x.strip() for x in tmp]

        if line.startswith('words'):
            tmp_words = line.split(":")[1].split(",")
            words = [ x.strip() for x in tmp_words]

            # build Relationship object and apend it to the list
            relation = Relationship(rel,args1,args2,words)
            relationships.append(relation)

    f.close()


def findMatches(line):
    # extract contexts (i.e., BEFORE,BETWEEN,AFTER) and entities types
    regex = re.compile('<[A-Z]+>[^<]+</[A-Z]+>',re.U)
    matches = []

    for m in re.finditer(regex,line):
        matches.append(m)

    for x in range(0,len(matches)-1):
        if x == 0:
            start = 0
        if x>0:
            start = matches[x-1].end()

        try:
            end = matches[x+2].start()
        except:
            end = len(line)-1

        before = line[ start :matches[x].start()]
        between = line[matches[x].end():matches[x+1].start()]
        after = line[matches[x+1].end(): end ]
        ent1 = matches[x].group()
        ent2 = matches[x+1].group()

        arg1Match = re.match("<[A-Z]+>",ent1)
        arg2Match = re.match("<[A-Z]+>",ent2)

        arg1Type = arg1Match.group()[1:-1]
        arg2Type = arg2Match.group()[1:-1]

        """
        print ent1.encode("utf8")
        print ent2.encode("utf8")
        print arg1Type
        print arg2Type
        print before.encode("utf8")
        print between.encode("utf8")
        print after.encode("utf8")
        print "\n"
        """

        # try to match with any seed words
        between_words = re.findall(tokenizer, between.lower(), flags = re.UNICODE)
        if len(between_words)>10: continue
        else:
            i = Instance(arg1Type,arg2Type,before,between,after)
            if (checkForRelationship(i,line)):
                print line.encode("utf8")
                break;


def checkForRelationship(i,sentence):
    for r in relationships:
        if (i.arg1Type in r.args1 and i.arg2Type in r.args2):
            # tokenize words in bef,bet,aft
            all_words = i.BEF + i.BET + i.AFT
            tokens = re.findall(tokenizer, all_words.lower(), flags = re.UNICODE)
            if len(set(tokens).intersection(set(r.words)))>0:
                return True


def main():
    readSeeds(sys.argv[1])
    f = codecs.open(sys.argv[2], encoding='utf-8')
    for line in f:
        if len(line)<=500:
            findMatches(line)
    f.close()




if __name__ == "__main__":
    main()




