#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import fileinput
import codecs

sentences = set()

def main():
    # read files already tagged
    # for each sentence, generate an hash code
    # store hash code in set
    f = codecs.open(sys.argv[1], encoding='utf-8')
    for line in f:
        parts = line.split('\t')
        if len(parts)==2:
            sentence = parts[1]        
            clean = re.sub(r"</?[A-Z]+>", "", sentence)
            #print clean.encode("utf8")
            sentences.add(clean)
    f.close()

    # read file to tag
    f = codecs.open(sys.argv[2], encoding='utf-8')
    # for each sentence generate an hash code
    # if hash code not in set print to annotate
    for line in f:
        clean = re.sub(r"</?[A-Z]+>", "", line)
        if clean not in sentences:
            print line.encode("utf-8"),

if __name__ == "__main__":
    main()
