#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import codecs
import pickle

import MinHash
from Relationship import Relationship
from FeatureExtractor import FeatureExtractor
from LocalitySensitiveHashing import LocalitySensitiveHashing

N_BANDS = 10
N_SIGS = 100
KNN = 7
USE_REDIS = True


def classify_sentences(data_file, extractor):
    relationships = []
    f_sentences = codecs.open(data_file, encoding='utf-8')
    for line in f_sentences:
        if len(line) > 1:
            sentence = line.strip()
            rel = Relationship(None, sentence, None)

            # extract features/shingles
            features = extractor.extract_features(rel)
            shingles = features.getvalue().strip().split(' ')

            # calculate min-hash sigs
            sigs = MinHash.signature(shingles, N_SIGS)
            rel.sigs = sigs

            relationships.append(rel)

    f_sentences.close()
    return relationships


def classify_relationship(rel):
    lsh = LocalitySensitiveHashing(N_BANDS, N_SIGS, KNN, USE_REDIS)
    types = lsh.classify(rel)
    print "\n"
    print rel.sentence
    print types


def load_training_sentences(data_file, extractor):
    relationships = []
    sentence = None
    rel_identifier = 0
    f_sentences = codecs.open(data_file, encoding='utf-8')
    f_features = open('features.txt', 'w')

    for line in f_sentences:
        sys.stdout.write('.')
        if not re.match('^relation', line):
            sentence = line.strip()
        else:
            rel_type = line.strip().split(':')[1]
            rel = Relationship(rel_identifier, sentence, rel_type)

            # extract features/shingles
            features = extractor.extract_features(rel)
            shingles = features.getvalue().strip().split(' ')

            # write shingles to StringIO
            f_features.write(rel_type + '\t')
            for shingle in shingles:
                f_features.write(shingle.encode("utf8") + ' ')
            f_features.write('\n')

            # calculate min-hash sigs
            sigs = MinHash.signature(shingles, N_SIGS)
            rel.sigs = sigs
            rel.identifier = rel_identifier

            rel_identifier += 1
            relationships.append(rel)

    f_sentences.close()
    f_features.close()

    return relationships


def load_shingles(shingles_file):
    """
    Parses already extracted shingles from a file.
    File format is: relaltionship_type tab_char and
    shingles separated by an empty space (\s)
    """
    relationships = []
    rel_identifier = 0
    f_shingles = codecs.open(shingles_file, encoding='utf-8')

    for line in f_shingles:
        sys.stdout.write('.')
        rel_type, shingles_string = line.split('\t')
        shingles = shingles_string.strip().split(' ')

        # calculate min-hash sigs
        sigs = MinHash.signature(shingles, N_SIGS)

        rel = Relationship(rel_identifier, None, rel_type)
        rel.sigs = sigs
        rel.identifier = rel_identifier

        relationships.append(rel)
        rel_identifier += 1
    f_shingles.close()

    return relationships


def main():

    ###########################
    # CLASSIFY A NEW SENTENCE
    ###########################
    # argv[1] - true
    # argv[2] - bands file
    # argv[3] - dict (sigs->sentence_id) file
    # argv[4] - sentence to classify

    if sys.argv[1] == 'true':

        print "Loading PoS tagger"
        model = open('postagger/cintil-reduced-tagset.pkl', "rb")
        pos_tagger = pickle.load(model)
        model.close()

        print "Loading verbs conjugations"
        f_verbs = open('verbs/verbs_conj.pkl', "rb")
        verbs = pickle.load(f_verbs)
        f_verbs.close()

        extractor = FeatureExtractor(pos_tagger, verbs)
        # read sentences from file
        # create a relationship object
        # extract features/shingles and calculate min-hash sigs
        relationships = classify_sentences(sys.argv[2], extractor)

        # find the closests neighbours
        lsh = LocalitySensitiveHashing(N_BANDS, N_SIGS, KNN, USE_REDIS)
        for r in relationships:
            types = lsh.classify(r)
            print "\n"
            print r.sentence
            print types

    ############################
    # INDEX TRAINING INSTANCES #
    ############################
    # argv[1] - false
    # argv[2] - training data file (example: train_data.txt)

    elif sys.argv[1] == 'false':
        # calculate min-hash sigs (from already extracted shingles) index in bands
        if os.path.isfile("features.txt"):
            print "Calculating min-hash sigs from features.txt file"
            relationships = load_shingles('features.txt')
            print "\n"
            print "Indexing ", len(relationships), "relationships"
            print "MinHash Signatures: ", N_SIGS
            print "Bands             : ", N_BANDS
            print "Sigs per Band     : ", N_SIGS / N_BANDS
            lsh = LocalitySensitiveHashing(N_BANDS, N_SIGS, KNN, USE_REDIS)
            lsh.create()
            for r in relationships:
                lsh.index(r)

        # load sentences, extract features, calculate min-hash sigs, index in bands
        else:
            print "Loading PoS tagger"
            model = open('postagger/cintil-reduced-tagset.pkl', "rb")
            pos_tagger = pickle.load(model)
            model.close()

            print "Loading verbs conjugations"
            f_verbs = open('verbs/verbs_conj.pkl', "rb")
            verbs = pickle.load(f_verbs)
            f_verbs.close()

            extractor = FeatureExtractor(pos_tagger, verbs)
            print "Extracting features from training data and calculating min-hash sigs"
            relationships = load_training_sentences(sys.argv[2], extractor)
            print "\n"
            print "Indexing ", len(relationships), "relationships"
            print "MinHash Signatures: ", N_SIGS
            print "Bands             : ", N_BANDS
            lsh = LocalitySensitiveHashing(N_BANDS, N_SIGS, KNN, USE_REDIS)
            lsh.create()
            for r in relationships:
                lsh.index(r)


if __name__ == "__main__":
    main()