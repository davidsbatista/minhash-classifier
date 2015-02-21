#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dsbatista'

import cPickle
from mxpost import MaxentPosTagger
from nltk.corpus import ConllCorpusReader
from sklearn.cross_validation import KFold


def train_k_fold(sentences):
    kf = KFold(len(sentences), 5)
    overall_results = dict()
    overall_results['adjective'] = 0
    overall_results['adverb'] = 0
    overall_results['conjunction'] = 0
    overall_results['determiner'] = 0
    overall_results['electronic'] = 0
    overall_results['interjection'] = 0
    overall_results['noun'] = 0
    overall_results['numeral'] = 0
    overall_results['preposition'] = 0
    overall_results['pronoun'] = 0
    overall_results['punctuation'] = 0
    overall_results['symbol'] = 0
    overall_results['verb'] = 0
    overall_results['verb_past'] = 0

    fold = 0
    for train_index, test_index in kf:
        print "\nFOLD", fold
        train = []
        test = []

        print "TRAIN", train_index, len(train_index)
        print "TEST", test_index, len(test_index)

        for index in train_index:
            train.append(sentences[index])

        for index in test_index:
            test.append(sentences[index])

        maxent_tagger = MaxentPosTagger()
        print "Training"
        maxent_tagger.train(train)
        print "Testing"
        correct_tags, total_tags = maxent_tagger.evaluate(test)

        for tag in correct_tags:
            print tag, ':\t'+str(correct_tags[tag]/float(total_tags[tag]))
            overall_results[tag] += correct_tags[tag]/float(total_tags[tag])

        print "Saving generated model"
        f_model = open('pos-tagger_'+str(fold)+'_.pkl', "wb")
        cPickle.dump(maxent_tagger, f_model, 1)
        f_model.close()

        fold += 1

    print "\nAccuracy on", kf.n_folds
    for tag in overall_results:
        print tag, overall_results[tag] / float(kf.n_folds)


def train_all(sentences):
    maxent_tagger = MaxentPosTagger()
    print "Training"
    maxent_tagger.train(sentences)
    print "Saving generated model"
    f_model = open('pos-tagger_all_.pkl', "wb")
    cPickle.dump(maxent_tagger, f_model, 1)
    f_model.close()


def main():
    directory = "/home/dsbatista/PycharmProjects/minhash-classifier/classifier/postagger/datasets"
    columns = ['words', 'pos', 'ignore']
    print "Reading CINTIL corpus"
    cintil = ConllCorpusReader(directory, 'CINTIL-CoNNL-reduced-past-verbs.txt', columns)
    #cintil = ConllCorpusReader(directory, 'CINTIL-CoNNL-format.txt', columns)
    sentences = cintil.tagged_sents()
    sentences = sentences[0:100]
    print len(sentences), " sentences loaded"
    train_all(sentences)

    """
    print "\n\n"
    print "classify unseen sentence: ", maxent_tagger.tag(["Isto", "é", "bastante", "rápido", "!"])
    print "\n\n"
    print "show the 40 most informative features:"
    print maxent_tagger.classifier.show_most_informative_features(40)
    """

if __name__ == '__main__':
    main()