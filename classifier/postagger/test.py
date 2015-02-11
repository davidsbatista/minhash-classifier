#!/usr/bin/env python
# -*- coding: utf-8 -*-

import StringIO
import codecs
import re
import pickle
import sys
from Sentence import Sentence

tokenizer =  r'\w+(?:-\w+)+|\d+(?:[:|/]\d+)+|\d+(?:[.]?[oaºª°])+|\w+\'\w+|\d+(?:[,|.]\d+)*\%?|[\w+\.-]+@[\w\.-]+|https?://[^\s]+|\w+'


def extract_reverb_patterns_ptb(text):

    """
    Extract ReVerb relational patterns
    http://homes.cs.washington.edu/~afader/bib_pdf/emnlp11.pdf

    # extract ReVerb patterns:
    # V | V P | V W*P
    # V = verb particle? adv?
    # W = (noun | adj | adv | pron | det)
    # P = (prep | particle | inf. marker)
    """

    # remove the tags and extract tokens
    text_no_tags = re.sub(r"</?[A-Z]+>", "", text)
    tokens = re.findall(tokenizer, text_no_tags.decode("utf8"), flags=re.UNICODE)

    # tag tokens with pos-tagger
    tagged = tagger.tag(tokens)
    patterns = []
    patterns_tags = []
    i = 0
    limit = len(tagged)-1
    tags = tagged

    """
    verb = ['VB', 'VBD', 'VBD|VBN', 'VBG', 'VBG|NN', 'VBN', 'VBP', 'VBP|TO', 'VBZ', 'VP']
    adverb = ['RB', 'RBR', 'RBS', 'RB|RP', 'RB|VBG', 'WRB']
    particule = ['POS', 'PRT', 'TO', 'RP']
    noun = ['NN', 'NNP', 'NNPS', 'NNS', 'NN|NNS', 'NN|SYM', 'NN|VBG', 'NP']
    adjectiv = ['JJ', 'JJR', 'JJRJR', 'JJS', 'JJ|RB', 'JJ|VBG']
    pronoun = ['WP', 'WP$', 'PRP', 'PRP$', 'PRP|VBP']
    determiner = ['DT', 'EX', 'PDT', 'WDT']
    adp = ['IN', 'IN|RP']
    """

    verb = ['verb', 'verb_past']
    word = ['noun', 'adjective', 'adverb', 'determiner', 'pronoun']
    particule = ['preposition']

    """
    conjunction
    electronic
    interjection
    numeral
    punctuation
    symbol

    adjective
    adverb
    determiner
    noun
    preposition
    pronoun
    verb
    verb_past
    """

    while i <= limit:
        tmp = StringIO.StringIO()
        tmp_tags = []

        # a ReVerb pattern always starts with a verb
        if tags[i][1] in verb:
            tmp.write(tags[i][0]+' ')
            t = (tags[i][0], tags[i][1])
            tmp_tags.append(t)
            i += 1

            # V = verb particle? adv? (also capture auxiliary verbs)
            while i <= limit and (tags[i][1] in verb or tags[i][1] in word):
                tmp.write(tags[i][0]+' ')
                t = (tags[i][0], tags[i][1])
                tmp_tags.append(t)
                i += 1

            # W = (noun | adj | adv | pron | det)
            while i <= limit and (tags[i][1] in word):
                tmp.write(tags[i][0]+' ')
                t = (tags[i][0], tags[i][1])
                tmp_tags.append(t)
                i += 1

            # P = (prep | particle | inf. marker)
            while i <= limit and (tags[i][1] in particule):
                tmp.write(tags[i][0]+' ')
                t = (tags[i][0], tags[i][1])
                tmp_tags.append(t)
                i += 1

            # add the build pattern to the list collected patterns
            patterns.append(tmp.getvalue())
            patterns_tags.append(tmp_tags)
        i += 1

    return patterns, patterns_tags


def extract_patterns(text):
    patterns, patterns_tags = extract_reverb_patterns_ptb(text)
    if len(patterns) > 0:
        for pattern in patterns_tags:
            for tag in pattern:
                print '/'.join(tag).encode("utf8"),
            print "\n"
        print "\n"


def process(sentence):

    s = Sentence(sentence)

    for rel in s.relationships:
        """
        print rel.ent1
        print rel.ent2
        print rel.before
        print rel.between
        print rel.after
        """
        extract_patterns(rel.before)
        extract_patterns(rel.between)
        extract_patterns(rel.after)


    """
    if len(patterns) > 0:
        for pattern in patterns_tags:
            # detect passive-voice
            for i in range(0, len(pattern)):
                passive_voice = False
                if pattern[i][1].startswith('v'):
                    try:
                        inf = verbs[pattern[i][0]]
                        if inf in ['ser', 'estar', 'ter', 'haver'] and i+2 <= len(pattern)-1:
                            if (pattern[-2][1] == 'verb_past' or pattern[-2][1] == 'adjectiv') and pattern[-1][0] == 'por':
                                passive_voice = True
                    except KeyError:
                        continue

                if passive_voice is True:
                    #print "passive voice:",
                    for tag in pattern:
                        print '/'.join(tag).encode("utf8"),
                    print "\n"
    """


def main():
    global verbs
    print "Loading Label-Delaf"
    verbs_conj = open('../verbs/verbs_conj.pkl', "r")
    verbs = pickle.load(verbs_conj)
    verbs_conj.close()

    global tagger
    print "Loading PoS tagger\n"
    f_model = open(sys.argv[1], "rb")
    tagger = pickle.load(f_model)
    f_model.close()

    #f_sentences = codecs.open(sys.argv[2], encoding='utf-8')
    f_sentences = codecs.open(sys.argv[2])
    for line in f_sentences:
        process(line)
    f_sentences.close()

    """
    sentence1 = "As acções do Banco Espírito Santo (BES) voltaram a negociar-se em bolsa."
    sentence2 = "Após ter suspendido a negociação dos títulos do banco."
    sentence3 = "O Governo de Ricardo foi acusado por um deputado do PS."
    sentence4 = "João fez duras críticas a Carlos Carvalhas."
    sentence5 = "Passos Coelho não fez qualquer tipo de declaração."
    sentence6 = "Passos Coelho chegou a Lisboa e não fez qualquer tipo de declação."
    process(sentence1)
    process(sentence2)
    process(sentence3)
    process(sentence4)
    process(sentence5)
    process(sentence6)
    """


if __name__ == "__main__":
    main()