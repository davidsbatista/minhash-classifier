# -*- coding: utf-8 -*-

import StringIO
import re
import sys

from nltk import ngrams
from nltk.corpus import stopwords


class FeatureExtractor:

    def __init__(self, _pos_tagger=None, _verbs=None):
        self.TOKENIZER= r'\,|\(|\)|\w+(?:-\w+)+|\d+(?:[:|/]\d+)+|\d+(?:[.]?[oaºª°])+|\w+\'\w+|\d+(?:[,|.]\d+)*\%?|[\w+\.-]+@[\w\.-]+|https?://[^\s]+|\w+'
        self.CONTEXT_WINDOW = 3
        self.N_GRAMS_SIZE = 4
        self.ambiguous = ['deputado', 'eurodeputado']
        self.aux_verbs = ['ter', 'haver', 'ser', 'estar']
        self.stop = stopwords.words('portuguese')
        if _pos_tagger:
            self.pos_tagger = _pos_tagger
        else:
            self.pos_tagger = None
        if _verbs:
            self.verbs = _verbs
        else:
            self.verbs = None

    def extract_features(self, rel):
        features = StringIO.StringIO()

        # calculate the size of each context, i.e., the number of tokens
        try:
            before_tokens = re.findall(self.TOKENIZER, rel.before, flags=re.UNICODE)
            between_tokens = re.findall(self.TOKENIZER, rel.between, flags=re.UNICODE)
            after_tokens = re.findall(self.TOKENIZER, rel.after, flags=re.UNICODE)
        except TypeError:
			print rel.sentence
			sys.exit(0) 

        # conside only a window of size 'tokens_window' tokens
        before_tokens = before_tokens[0 - self.CONTEXT_WINDOW:]
        after_tokens = after_tokens[:self.CONTEXT_WINDOW]

        # add entities type
        features.write(rel.arg1type + '_ARG1 ')
        features.write(rel.arg2type + '_ARG2 ')

        # biggest context is a feature
        if len(before_tokens) >= max(len(between_tokens), len(after_tokens)):
            features.write("LARGER_BEF ")

        if len(after_tokens) >= max(len(between_tokens), len(before_tokens)):
            features.write("LARGER_AFT ")

        if len(between_tokens) >= max(len(after_tokens), len(before_tokens)):
            features.write("LARGER_BET ")

        # mark if contexts are empty as a feature
        if len(before_tokens) == 0:
            features.write("EMPTY_BEF ")
        if len(after_tokens) == 0:
            features.write("EMPTY_AFT ")
        if len(between_tokens) == 0:
            features.write("EMPTY_BET ")

        # extract n-grams from contexts
        self.extract_ngrams(' '.join(before_tokens), "BEF", features)
        self.extract_ngrams(' '.join(between_tokens), "BET", features)
        self.extract_ngrams(' '.join(after_tokens), "AFT", features)

        """
        # if less or equal to '4' extract nouns
        if len(between_tokens) < 4:
            self.extract_nouns(between_tokens, features)

        # extract every word between the two entities
        print "extracting nouns"
        self.extract_tokens(between_tokens, features)
        """

        # extract ReVerb patterns
        if self.pos_tagger:
            self.extract_patterns(before_tokens, "BEF", features)
            self.extract_patterns(between_tokens, "BET", features)
            self.extract_patterns(after_tokens, "AFT", features)

        return features

    def extract_ngrams(self, text, context, features):
        chrs = ['_' if c == ' ' else c for c in text]
        for g in ngrams(chrs, self.N_GRAMS_SIZE):
            features.write(''.join(g) + '_' + context + ' ')

    def extract_tokens(self, text_tokenized, features):
        for i in range(0, len(text_tokenized)):
            if text_tokenized[i].encode("utf8") not in self.stop:
                features.write(text_tokenized[i] + '_BET ')

    @staticmethod
    def extract_nouns(self, text_tokenized, features):
        tagged = self.pos_tagger.tag(text_tokenized)
        patterns = []
        # if the word is a noun
        for i in range(0, len(tagged)):
            word = tagged[i]
            if word[1] == 'noun':
                patterns.append(word[0] + '_NOUN_BET')

        for p in patterns:
            features.write(p + ' ')

    def extract_patterns(self, text_tokenized, context, features):
        tagged = self.pos_tagger.tag(text_tokenized)
        patterns = []

        for i in range(0, len(tagged)):
            word = tagged[i]
            # if the word is a verb
            if word[1] == 'verb':
                    patterns.append(tagged[i][0] + "_VERB_" + context)
                    pattern = tagged[i][0]
                    if i < len(tagged)-2:
                        # ReVerb
                        j = i+1
                        while (j < (len(tagged)-2) and (
                            tagged[j][1] == 'adjective' or   # adjectives
                            tagged[j][1] == 'adverb' or      # adverbs
                            #tagged[j][1] == 'determiner' or  # determiner
                            tagged[j][1] == 'verb' or        # verbs
                            tagged[j][1] == 'noun')):        # noun
                                pattern += '_'+tagged[j][0]
                                j += 1

                        #print pattern
                        #print tagged[j-1]
                        #print "j", j
                        #print "len(tagged)-2", len(tagged)-2

                        # must end in a proposition or determiner
                        if j < (len(tagged)-2) and (tagged[j][1] == "preposition" or tagged[j][1] == "determiner"):
                            pattern += '_'+tagged[j][0]+'_'
                            pattern += context+'_RVB'
                            patterns.append(pattern)

                        # negation detection
                        if (i-1 > 0) and (tagged[i-1][0] == u"não" or
                                          tagged[i-1][0] == u"nunca" or
                                          tagged[i-1][0] == u"jamais"):
                                neg_pattern = tagged[i-1][0]+'_'+pattern
                                neg_pattern += context+'_RVB'
                                patterns.append(neg_pattern)

                    # just a verb
                    else:
                        pattern += '_'+context+'_RVB'
                        patterns.append(pattern)

        for p in patterns:
            #print p.encode("utf8")
            features.write(p + ' ')

        """
        print "text: ", text_tokenized
        print "pos:  ", tagged
        patterns = []
        for i in range(0, len(tagged)):
            word = tagged[i]
            # if the word is a verb
            if word[1] == 'verb' and word[0] not in self.ambiguous:
                # add verb
                patterns.append(word[0] + '_VRB')

                # add verb normalized
                if word[0] in verbs:
                    vrb_norm = verbs[word[0]]
                    if vrb_norm not in self.aux_verbs:
                        patterns.append(vrb_norm + '_VRB_NORM')
                        patterns.append(vrb_norm + '_VRB_NORM')
                        patterns.append(vrb_norm + '_VRB_NORM')
        """

