#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import sys


def main():

    sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    f_txt = open(sys.argv[1])
    sentences = sent_tokenizer.tokenize(f_txt.read())
    f_txt.close()
    for s in sentences:
        print s

if __name__ == "__main__":
    main()
