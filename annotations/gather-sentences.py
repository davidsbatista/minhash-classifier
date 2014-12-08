#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import codecs
from classifier.Sentence import Sentence

tokenizer =  r'\w+(?:-\w+)+|\d+(?:[:|/]\d+)+|\d+(?:[.]?[oaºª°])+|\w+\'\w+|\d+(?:[,|.]\d+)*\%?|[\w+\.-]+@[\w\.-]+|https?://[^\s]+|\w+'


class RelationshipType:
    def __init__(self, _name, _arg1, _arg2, _words):
        self.name = _name
        self.args1 = _arg1
        self.args2 = _arg2
        self.words = _words


def read_sentiwords(data):
    words = list()
    f = codecs.open(data, encoding='utf-8')
    for line in f:
        words.apped(line.strip())
    f.close()
    return words


def read_seed_words(data):
    relationships = list()
    f = codecs.open(data, encoding='utf-8')
    for line in f:
        if line.startswith('relation'):
            rel = line.split(":")[1].strip()

        if line.startswith('arg1'):
            tmp = line.split(":")[1].split(",")
            args1 = [x.strip() for x in tmp]

        if line.startswith('arg2'):
            tmp = line.split(":")[1].split(",")
            args2 = [x.strip() for x in tmp]

        if line.startswith('words'):
            tmp_words = line.split(":")[1].split(",")
            words = [x.strip() for x in tmp_words]

            # build Relationship object and apend it to the list
            relation = RelationshipType(rel, args1, args2, words)
            relationships.append(relation)
    f.close()
    return relationships


def find_matches(line, relationships, positive, negative):
    sentence = Sentence(line)

    for rel in sentence.relationships:

        for r in relationships:
            # check if the arguments type match
            if rel.arg1type in r.args1 and rel.arg2type in r.args2:

                # tokenize words in bef,bet,aft
                bef = re.findall(tokenizer, rel.before .lower(), flags=re.UNICODE)
                bet = re.findall(tokenizer, rel.between.lower(), flags=re.UNICODE)
                aft = re.findall(tokenizer, rel.after.lower(), flags=re.UNICODE)

                # try to match with any seed words
                all_words = bef + bet + aft

                print all_words

                tokens = re.findall(tokenizer, all_words.lower(), flags=re.UNICODE)
                if len(set(tokens).intersection(set(r.words))) > 0:
                    print line.encode("utf8")

                elif len(set(tokens).intersection(set(positive))) > 0:
                    print line.encode("utf8")

                elif len(set(tokens).intersection(set(negative))) > 0:
                    print line.encode("utf8")


def main():
    relationships = read_seed_words(sys.argv[1])
    positive = read_sentiwords("positive.txt")
    negative = read_sentiwords("negative.txt")
    f = codecs.open(sys.argv[2], encoding='utf-8')
    for line in f:
        find_matches(line, relationships, positive, negative)
    f.close()


if __name__ == "__main__":
    main()




