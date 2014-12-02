#!/usr/bin/env python
# -*- coding: utf-8 -*-


from nltk.corpus.reader.tagged import TaggedCorpusReader
from nltk.corpus.reader.conll import ConllCorpusReader


def main():
        # cintil = TaggedCorpusReader('/home/dsbatista/cintil/','CINTIL-sentences-pos.txt')
        # tagged_sents = cintil.tagged_sents()[:num_sents]

        root = '/home/dsbatista/cintil/'
        column_types = ['ignore','words','ignore','ignore','pos','ignore']

        cintil = ConllCorpusReader('/home/dsbatista/cintil/','cintil-fixed.conll',column_types)
        tagged_sents = cintil.tagged_sents()
        print len(tagged_sents)
        


if __name__ == "__main__":
    main()

