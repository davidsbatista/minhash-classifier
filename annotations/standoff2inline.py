#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import fileinput
import codecs

entities = dict()
relationships = []

class Entity:
    def __init__(self,_term,_name,_etype,_start,_end):
        self.term = _term
        self.name = _name
        self.etype = _etype
        self.start = _start
        self.end = _end


class Relationship:
    def __init__(self,_rel,_rel_type,_arg1,_arg2):
        self.rel = _rel
        self.rel_type = _rel_type
        self.arg1 = _arg1
        self.arg2 = _arg2


def findSentBegin(sentences,index):
    index = index-1
    while sentences[index]!='\n':
        index = index -1
    return index


def main():
    txt = sys.argv[1]
    ann = sys.argv[2]
    
    # read standoff annotations into Entity and Relationship objects
    f_ann = codecs.open(ann, encoding='utf-8')
    for line in f_ann:
        if line.startswith("T"):
            term = line.split('\t')[0]
            entity = line.split('\t')[-1]
            data = line.split('\t')[1]
            etype,start,end = data.split(' ')
            e = Entity(term,entity.strip(),etype,int(start),int(end))
            entities[e.term] = e

        if line.startswith("R"):
            rel = line.split('\t')[0]
            data = line.split('\t')[1]
            rel_type,arg1,arg2 = data.split(' ')
            r = Relationship(rel,rel_type,arg1,arg2)
            relationships.append(r)
    f_ann.close()

    # read sentences files as a whole, because of the standoff annotations
    f_txt = codecs.open(txt, encoding='utf-8')
    sentences = f_txt.read()
    f_txt.close()

    # generates the sentences with inline XML annotations
    id = 0
    for r in relationships:
        # gets the arguments of the relationship and the semantic type
        arg1 = r.arg1.split(":")[1]
        arg2 = r.arg2.split(":")[1]
        entity1 = entities[arg1.strip()]
        entity2 = entities[arg2.strip()]
        e1type = entity1.etype
        e2type = entity2.etype

        # calculates standoff annotations relatives to the sentence with the relationship and not the whole .txt file
        sentence_begin = findSentBegin(sentences,entity1.start)
        sentence_end = sentences.find("\n", entity2.end)
        sentence =  sentences[sentence_begin:sentence_end]

        # checks the order of the arguments in the relationship
        args_reversed = False
        ent1_start = sentence.find(entity1.name)
        ent2_start = sentence.find(entity2.name)
        if (entity2.start<entity1.start):
            args_reversed = True

        # writes the sentence with inline XML annotations and the relationship type with the arguments order
        if (args_reversed==True):
            ent2_start = sentence.find(entity2.name)
            sentence = sentence[:ent2_start] + '<'+entity2.etype+'>' + entity2.name + '</'+entity2.etype+'>' + sentence[ent2_start+len(entity2.name):]
            ent1_start = sentence.find(entity1.name)
            sentence = sentence[:ent1_start] + '<'+entity1.etype+'>' + entity1.name + '</'+entity1.etype+'>' + sentence[ent1_start+len(entity1.name):]
        else:
            ent1_start = sentence.find(entity1.name)
            sentence = sentence[:ent1_start] + '<'+entity1.etype+'>' + entity1.name + '</'+entity1.etype+'>' + sentence[ent1_start+len(entity1.name):]
            ent2_start = sentence.find(entity2.name)
            sentence = sentence[:ent2_start] + '<'+entity2.etype+'>' + entity2.name + '</'+entity2.etype+'>' + sentence[ent2_start+len(entity2.name):]

        print sentence.strip().encode("utf8")
        if (args_reversed==True):
            print "relation:"+r.rel_type.encode("utf8")+"(Arg2,Arg1)\n"
        else:
            print "relations:"+r.rel_type.encode("utf8")+"(Arg1,Arg2)\n"
        id+=1

if __name__ == "__main__":
    main()
