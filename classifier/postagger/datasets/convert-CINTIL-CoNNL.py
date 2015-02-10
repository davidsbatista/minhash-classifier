#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import fileinput
import codecs
import nltk


def load_contractions():
    global l
    l = ['-lhe_/CL','-lhe_/CL','-lhe_/CL','-lhe_/CL','-me_/CL','-me_/CL','-me_/CL','-te_/CL','-te_/CL','-te_/CL']
    global contraccoes
    global contraccoes_desfeitas
    contraccoes = []
    contraccoes_desfeitas = []
    f_sentences = codecs.open("contracoes.txt", encoding='utf-8')
    for line in f_sentences:
        contraccoes.append(line.strip())
    f_sentences.close()

    f_sentences = codecs.open("contracoes-desfeitas.txt", encoding='utf-8')
    for line in f_sentences:
        contraccoes_desfeitas.append(line.strip())


def main():
    load_contractions()

    tags = [u"/CJ", u"/ADV", u"/LADV", u"/LPRS", u"/DGT", u"/LPREP", u"/LITJ", u"/LCJ", u"/DA#", u"/UM#", u"/DEM#", u"/REL#", u"/REL[", u"/REL/", u"/PNM", u"/PADR", u"/PPA#", u"/VAUX#", u"/V#", u"/PPT", u"/INF#", u"/INFAUX#", u"/GER", u"/GERAUX#", u"/CN#", u"/CN", u"/ADJ#", u"/QNT#", u"/QNT/", u"/QNT[", u"/WD#", u"/ORD#", u"/POSS#", u"/DM", u"/CARD#", u"/MTH", u"/PRS", u"STT#", u"IND#", u"/DEM/", u"/ADJ/", u"/ITJ", "/DEM[", u"/EADR[", u"/CL#", u"/DFR", u"/LDFR", u"/INT[", u"/INT/", u"/SYB[", u"/INT#", u"/UNIT#", u"/IA#", u"/IA/", u"/MGT", u"/NP", u"/EXC[", u"/LTR", u"/EOE", u"/LD", u"/PP", u"/IND[", u"/IND/", u"/DL", u"/LREL", u"/EMP[", u"/LQD", u"/PL[", u"/CL/", u"/STT", u"/LCN", u"/EL[", u"/TERMN", u"/SC", u"/V[",u"/VAUX[",u"/INF[",u"/INFAUX[",u"/LADV", u"LCJ1", u"LPREP", u"LPRS1"]

    f_sentences = codecs.open(sys.argv[1], encoding='utf-8')
    for line in f_sentences:
        if line.startswith('<p ') or line.startswith('<s '):
            if line.startswith('<p '):
                print "\n",
            clean = re.sub('<(s|p)[^>]*>', '', line)
            sentence = clean.strip()
            parts = sentence.split(' ')
            parts = parts[:-1]

            # Resolve contractions and ciclics
            verbs = [u'/GER', u'/INF', u'/PPA', u'/V', u'/VAUX']

            for i in range(0,len(parts)):
                if i<len(parts)-1:
                    if parts[i]==u'Esta_/DEM#fs[O]' and parts[i+1] == u'outra/QNT#fs[O]':
                        parts[i] =  u'Esta/DEM#fs[O]'

                    # resolve: disse-lhe, fugiu-se, etc.
                    if any(verb in parts[i] for verb in verbs) and parts[i+1].startswith("-") and "/CL" in parts[i+1]:
                        verb = parts[i].split('/')[0]
                        reflexive = parts[i+1].split('/')[0]
                        if verb.endswith('#'):
                            verb = verb[:-1]

                        if "-CL-" not in verb:
                            pos = parts[i].split("/")[-1].split("#")[0]
                            tag = parts[i+1].split("[")[1][:-1]
                            contr = (verb+reflexive)
                            if "/GER" in parts[i]:
                                pos = pos.split("[")[0]
                            parts[i] = contr+"/"+pos+"["+tag+"]"
                            del parts[i+1]

                        else:
                            pos = parts[i].split("/")[-1].split("#")[0]
                            tag = parts[i+1].split("[")[1][:-1]
                            splits = verb.split("-CL-")
                            if splits[0].endswith('#'): splits[0] = splits[0][:-1]
                            parts[i] = splits[0]+reflexive+"-"+splits[1]+"/"+pos+"["+tag+"]"

                    elif ('_/' in parts[i]) or (parts[i] in l):
                        if "#" not in parts[i] and "#" not in parts[i+1]:
                            contr = parts[i].split('[')[0]+' '+parts[i+1].split('[')[0]
                            tag = parts[i].split('[')[1][:-1]

                        elif "#" not in parts[i] and "#" in parts[i+1]:
                            contr = parts[i].split('[')[0]+' '+parts[i+1].split('#')[0]
                            tag = parts[i].split('[')[1][:-1]

                        elif "#" in parts[i] and "#" in parts[i+1]:
                            contr = parts[i].split('#')[0]+' '+parts[i+1].split('#')[0]
                            tag = parts[i].split('#')[1][4:-1]


                        # there are a few annotations BUGS/errors, fix them
                        if tag == '0':
                            tag='O'

                        # de[I]_/PREP[I-ORG]
                        if tag == 'I]_/PRE':
                            tag = 'I-ORG'

                        try:
                            c = contraccoes.index(contr)
                            contr_desf = contraccoes_desfeitas[c]
                            parts[i] = contr_desf+"/"+tag
                            del parts[i+1]
                        except Exception, e:
                            print "Error", e
                            print contr.encode("utf8")
                            sys.exit(0)

            # print word per line with POS and tag information, CoNNL format
            ignore = ['<i>', '</i>', "<t>", "</t>", "*//PNT[O]"]
            for p in parts:
                if p in ignore:
                    continue

                # hard-coded fixes
                if p == u"Rochefoucauld/PNM[I]":
                    p = "Rochefoucauld/PNM[I-PER]"

                if p == "off/OFF/PREP[O]":
                    p = "off/CN[O]"

                if "/PREP" in p and ("/CN" not in p and "/V" not in p):
                    if "PREP[" in p:
                        try:
                            word, info = p.split("/")
                            pos = "PREP"
                            tag = info[info.find('['):]
                            tag = tag[1:-1]
                            print (word+'\t'+pos+'\t'+tag).encode("utf8")
                        except Exception, e:
                            print parts
                            print "t", p
                            sys.exit(0)

                    elif "PREP/" in p:
                        word,pos,tag = p.split("/")
                        print (word+'\t'+pos+'\t'+tag).encode("utf8")

                elif any(substring in p for substring in tags):
                    parts = p.split("/")
                    word = parts[0]
                    other = parts[-1]

                    # "/" symbol
                    # "//SYB[I-WRK] 
                    # "//SYB[I-ORG]
                    # etc.
                    if p.startswith("/"): word = "/"

                    if '#' in other: 
                        pos = other[:other.find('#')]
                    elif "[" in other: 
                        pos = pos = other[:other.find('[')]

                    if ('#' in other) or ("[" in other): 
                        tag = other[other.find('['):]
                        tag = tag[1:-1]
                    else:
                        pos = parts[1]
                        tag = parts[2]

                    if tag == 'I-WR':
                        tag = 'I-WRK'

                    print (word+'\t'+pos+'\t'+tag).encode("utf8")

                elif "/PNT" in p:
                    if p.startswith("//"):
                       pnt = '/'
                       tag = p[6:-1]

                    elif p=='\**//PNT[O]':
                         pnt = " * "
                         tag = "O"

                    elif p=='\*/*//PNT[O]':
                         pnt = " / "
                         tag = "O"

                    elif p=="/*//PNT[O]":
                         pnt = "/ "
                         tag = "O"

                    elif p=="\*//PNT[O]":
                         pnt = " /"
                         tag = "O"

                    elif p=='\*"/"/PNT[O]':
                         pnt = ' \"/\"'
                         tag = "O"

                    else:
                        # blank space on the left: '\*'
                        # blank space on the right: '*/'
                        # add blank spaces
                        o = re.sub(r"(\\\*)", " ", p)
                        o = re.sub(r"(\*\/)", " ", o)
                        try:
                            pnt,tag = o.split("/")
                            tag = tag[4:-1]
                        except:
                            print "error"
                            print p.encode("utf8")
                            sys.exit(0)

                    print pnt.encode("utf8")+'\t'+'PNT'+'\t'+tag.encode("utf8")

                else:
                    print "no match",p.encode("utf8").strip(),
                    sys.exit(0)

if __name__ == "__main__":
    main()
