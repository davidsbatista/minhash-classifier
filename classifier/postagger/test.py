#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import pickle
import sys

tokenizer =  r'\w+(?:-\w+)+|\d+(?:[:|/]\d+)+|\d+(?:[.]?[oaºª°])+|\w+\'\w+|\d+(?:[,|.]\d+)*\%?|[\w+\.-]+@[\w\.-]+|https?://[^\s]+|\w+'


def extract_reverb_patterns(text_tokenized):
    tagged = tagger.tag(text_tokenized)
    for tag in tagged:
        print '/'.join(tag),
    print "\n",

    patterns = []

    for i in range(0, len(tagged)):
        word = tagged[i]
        # if the word is a verb
        if word[1] == 'verb':
                pattern = tagged[i][0]
                if i < len(tagged)-2:
                    # ReVerb
                    j = i+1
                    while (j < (len(tagged)-2) and (
                        tagged[j][1] == 'adjective' or   # adjectivs
                        tagged[j][1] == 'adverb' or      # adverbs
                        tagged[j][1] == 'determiner' or  # adverbs
                        tagged[j][1] == 'verb' or        # verbs
                        tagged[j][1] == 'noun')):        # noun
                            pattern += '_'+tagged[j][0]
                            j += 1

                    # must end in a proposition
                    if j < (len(tagged)-2) and tagged[j][1] == "preposition":
                        pattern += '_'+tagged[j][0]+'_RVB'
                        patterns.append(pattern)

                    # negation detection
                    if (i-1 > 0) and (tagged[i-1][0] == u"não" or
                                      tagged[i-1][0] == u"nunca" or
                                      tagged[i-1][0] == u"jamais"):
                            neg_pattern = tagged[i-1][0]+'_'+pattern+'_RVB'
                            patterns.append(neg_pattern)

    for p in patterns:
        print p
    print "\n",


def process(sentence):
    tokens = re.findall(tokenizer, sentence.decode("utf8"), flags=re.UNICODE)
    extract_reverb_patterns(tokens)


def main():
    global tagger
    print "Loading PoS tagger\n"
    f_model = open(sys.argv[1], "rb")
    tagger = pickle.load(f_model)
    f_model.close()

    sentence1 = """As acções do Banco Espírito Santo (BES) voltaram a negociar-se em bolsa."""
    sentence2 = """Após ter suspendido a negociação dos títulos do banco."""
    sentence3 = """O Governo de Ricardo foi acusado por um deputado do PS."""
    sentence4 = """João fez duras críticas a Carlos Carvalhas."""
    sentence5 = """Passos Coelho não fez qualquer tipo de declaração."""
    sentence6 = """Passos Coelho chegou a Lisboa e não fez qualquer tipo de declação."""

    process(sentence1)
    process(sentence2)
    process(sentence3)
    process(sentence4)
    process(sentence5)
    process(sentence6)


if __name__ == "__main__":
    main()