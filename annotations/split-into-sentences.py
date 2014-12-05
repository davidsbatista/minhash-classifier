#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import fileinput
import nltk.data

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def main():
    out_file = open(sys.argv[1]+".sentences","w")

    for line in fileinput.input():
        parts = line.split('\t')
        if len(parts)==5:
            category = parts[0]
            if category in ['MUNDO','ECONOMIA','SOCIEDADE','POLITICA']:
                date = parts[1]
                url = parts[2]
                title = parts[3]
                text = parts[4]
                text = title + '. ' + text
                for sentence in sent_detector.tokenize(text.strip()):
                    out_file.write(sentence+'\n')

    out_file.close()

if __name__ == "__main__":
    main()
