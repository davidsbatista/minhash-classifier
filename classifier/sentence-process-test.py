#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
from Relationship import Relationship

__author__ = 'dsbatista'


def main():
    f_sentences = codecs.open(sys.argv[1], encoding='utf-8')
    for line in f_sentences:
            sentence = line.strip()
            rel = Relationship(sentence)
            print rel


if __name__ == "__main__":
    main()