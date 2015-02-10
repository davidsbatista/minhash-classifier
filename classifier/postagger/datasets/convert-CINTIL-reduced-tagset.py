#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import fileinput
import codecs

mappings = dict()


def load_mappings():
    f_mappings = codecs.open("convert-tageset.txt", encoding='utf-8')
    for line in f_mappings:
        orig,new = line.split('\t')
        mappings[orig] = new.strip()
    f_mappings.close()


def main():
    load_mappings()
    f_file = codecs.open(sys.argv[1], encoding='utf-8')
    for line in f_file:
        if len(line) != 1:
            parts = line.split('\t')
            word = parts[0]
            pos_tag = parts[1].strip()
            entity_tag = parts[2].strip()
            try:
                print (word+'\t'+mappings[pos_tag]+'\t'+entity_tag.strip()).encode("utf8")
            except Exception, e:
                print e
                print line
                sys.exit(0)
        else:
            print ""
    f_file.close()

if __name__ == "__main__":
    main()
