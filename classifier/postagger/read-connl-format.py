#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.corpus.reader.conll import ConllCorpusReader


def main():
        column_types = ['ignore', 'words', 'ignore', 'ignore', 'pos', 'ignore']
        directory = "/home/dsbatista/PycharmProjects/minhash-classifier/classifier/postagger/datasets"
        cintil = ConllCorpusReader(directory, 'cintil-newtags.txt', column_types)
        tagged_sents = cintil.tagged_sents()
        print len(tagged_sents)

if __name__ == "__main__":
    main()

