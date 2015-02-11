#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import gzip
import pickle

verbs = dict()


def load_verbs():
    label = "Label-Delaf_pt_v4_1.dic.utf8.gz"
    f = gzip.open(label, 'rb', 'utf-8')
    for line in f:
        if not line.startswith("%") and line.find(".V")!=-1:
            conjugation, verb = line.split(".V")[0].split(",")
            verbs[conjugation] = verb
    print len(verbs.keys()), "loaded"


def main():
    load_verbs()
    verbs_conj = open('verbsConj.pkl',"wb")
    pickle.dump(verbs, verbs_conj, 1)
    verbs_conj.close()

if __name__ == "__main__":
    main()
