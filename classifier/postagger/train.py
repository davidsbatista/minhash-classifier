#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dsbatista'

import pickle
from mxpost import MaxentPosTagger
from nltk.corpus import ConllCorpusReader


def demo(corpus, num_sents):
    """
    Loads a few sentences from the Brown corpus or the Wall Street Journal
    corpus, trains them, tests the tagger's accuracy and tags an unseen
    sentence.

    @type corpus: C{str}
    @param corpus: Name of the corpus to load, either C{brown} or C{treebank}.

    @type num_sents: C{int}
    @param num_sents: Number of sentences to load from a corpus. Use a small
    number, as training might take a while.
    """
    if corpus.lower() == "brown":
        from nltk.corpus import brown
        tagged_sents = brown.tagged_sents()[:num_sents]

    elif corpus.lower() == "treebank":
        from nltk.corpus import treebank
        tagged_sents = treebank.tagged_sents()[:num_sents]

    elif corpus.lower() == "floresta":
        from nltk.corpus import floresta
        tagged_sents = floresta.tagged_sents()[:num_sents]

    elif corpus.lower() == "cintil":
        print "Loading CINTIL"
        #column_types = ['ignore','words','ignore','ignore','pos','ignore']
        #cintil = ConllCorpusReader('/home/dsbatista/cintil/','cintil-fixed.conll',column_types)
        column_types = ['words', 'pos', 'ignore']
        #cintil = ConllCorpusReader('/home/dsbatista/extract-publico-relationships/pos-tagger','cintil-fixed.conll',column_types)
        cintil = ConllCorpusReader('/home/dsbatista/Dropbox/pt-relationships/classifier/postagger/datasets', 'cintil-fixed-reduced.conll', column_types)
        tagged_sents = cintil.tagged_sents()[:num_sents]

    else:
        print "Please load either the 'brown' or the 'treebank' corpus."

    #size = int(len(tagged_sents) * 0.1)
    #train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
    train_sents = cintil.tagged_sents()
    test_sents = cintil.tagged_sents()
    print train_sents,test_sents
    maxent_tagger = MaxentPosTagger()
    maxent_tagger.train(train_sents)
    maxent_tagger.evaluate(test_sents)

    """
    print "tagger accuracy (test %i sentences, after training %i):" % \
        (size, (num_sents - size)), maxent_tagger.evaluate(test_sents)
    print "\n\n"
    print "classify unseen sentence: ", maxent_tagger.tag(["Isto", "é", "bastante","rápido", "!"])
    print "\n\n"
    print "show the 40 most informative features:"
    print maxent_tagger.classifier.show_most_informative_features(40)
    """

    f_model = open('test.pkl', "wb")
    pickle.dump(maxent_tagger, f_model, 1)
    f_model.close()

if __name__ == '__main__':
    demo("cintil", 100)

