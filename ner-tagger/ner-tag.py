#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ner
import sys
import StringIO
import fileinput
from nltk.tokenize import sent_tokenize
from datetime import datetime
from xml.dom.minidom import parse, parseString

tagger = ner.SocketNER(host='borat', port=9191)
punctuation = [".",",","!","?",";",":"]

def main():
    f_out_tagged = open(sys.argv[1] + '.tagged','w')
    f_out_errors = open(sys.argv[1] + '.errors','w')
    count = 0
    for line in fileinput.input():
        try:
            section,date,url,title,text = line.split('\t')

            # tag title
            labeled_title =  getLabels(title)
            tagged_title = addTags(labeled_title,url,f_out_errors)

            # tag text, one sentence at the time
            document = StringIO.StringIO()
            for s in sent_tokenize(text):
                labeled_text =  getLabels(s)
                tagged_text = addTags(labeled_text,url,f_out_errors)
                document.write(tagged_text)
            tagged_text = document.getvalue().encode("utf8")

            # writes tagged content to file
            try:
                f_out_tagged.write(section+'\t'+date+'\t'+url+'\t'+tagged_title.encode("utf8")+'\t'+tagged_text+'\n')
            except Exception, e:
                f_out_errors.write(url+'\t'+"writing output"+'\t'+e.message+'\n')

            count+=1
            if (count % 500 == 0):
                f_out_tagged.flush()
                f_out_errors.flush()
                print sys.argv[1],datetime.now(),'\t',count

        except Exception, e:
            f_out_errors.write(url+'\t'+"line parsing"+'\t'+e.message+'\n')

    f_out_tagged.close()
    f_out_errors.close()


def addTags(labeled_tokens,url,f_out_errors):
    try:
        dom = parseString('<root>' + labeled_tokens.encode("utf8") + '</root>')
        tokens = dom.getElementsByTagName('wi')
        text =  StringIO.StringIO()
        previous_type = ''
        for token in tokens:
            tag_type = token.getAttribute("entity")
            word = token.firstChild.nodeValue
            if word == '-LRB-': word = '('
            if word == '-RRB-': word = ')'
            if word == '-LSB-': word = '['
            if word == '-RSB-': word = ']'
            if word == '-LCB-': word = '{'
            if word == '-RCB-': word = '}'

            # entity with just a word
            if   (tag_type != 'I-PER' and previous_type == 'B-PER'): text.write('</PER>')
            elif (tag_type != 'I-ORG' and previous_type == 'B-ORG'): text.write('</ORG>')
            elif (tag_type != 'I-LOC' and previous_type == 'B-LOC'): text.write('</LOC>')
            elif (tag_type != 'I-MSC' and previous_type == 'B-MSC'): text.write('</MSC>')

            # end of multi-word entity
            if (tag_type == 'O' and previous_type != 'O'):
                end_tag = ''
                if   (tag_type == 'O' and previous_type == 'I-PER'): end_tag = '</PER>'
                elif (tag_type == 'O' and previous_type == 'I-ORG'): end_tag = '</ORG>'
                elif (tag_type == 'O' and previous_type == 'I-LOC'): end_tag = '</LOC>'
                elif (tag_type == 'O' and previous_type == 'I-MSC'): end_tag = '</MSC>'

                if word in punctuation: text.write(end_tag+word)
                else: text.write(end_tag+' '+word)

            # ex: B-LOC,I-LOC,B-LOC
            elif (tag_type.startswith("B") and previous_type.startswith("I")):
                text.write('</'+previous_type.split("-")[1]+'> <'+tag_type.split("-")[1]+">" + word)


            # sentence ends in a multi-word or single entity
            elif tokens.index(token)==len(tokens)-1 and tag_type!='O':
                if (tag_type == 'I-PER'): text.write(' '+word+'</PER>')
                if (tag_type == 'I-LOC'): text.write(' '+word+'</LOC>')
                if (tag_type == 'I-ORG'): text.write(' '+word+'</ORG>')
                if (tag_type == 'I-MSC'): text.write(' '+word+'</MSC>')
                if (tag_type == 'B-PER'): text.write(' <PER>'+word+'</PER>')
                if (tag_type == 'B-LOC'): text.write(' <LOC>'+word+'</LOC>')
                if (tag_type == 'B-ORG'): text.write(' <ORG>'+word+'</ORG>')
                if (tag_type == 'B-MSC'): text.write(' <MSC>'+word+'</MSC>')

            # inside a multi-word entity
            elif (tag_type == 'I-PER'): text.write(' '+word)
            elif (tag_type == 'I-LOC'): text.write(' '+word)
            elif (tag_type == 'I-ORG'): text.write(' '+word)
            elif (tag_type == 'I-MSC'): text.write(' '+word)

            # start of a new entity
            elif tag_type == 'B-ORG': text.write(' <ORG>'+word)
            elif tag_type == 'B-PER': text.write(' <PER>'+word)
            elif tag_type == 'B-LOC': text.write(' <LOC>'+word)
            elif tag_type == 'B-MSC': text.write(' <MSC>'+word)

            # not part of an entity
            elif tag_type == 'O':
                if word in punctuation: text.write(word)
                elif word=="""``""" :
                    text.write(' "')
                elif word=="""''""":
                    text.write('"')

                else: text.write(' '+word)

            previous_type = tag_type

        return text.getvalue()

    except Exception, e:
        f_out_errors.write(url+'\t'+"XML parsing"+'\t'+e.message+'\n')


def getLabels(text):
    try:
        tagged_text = tagger.tag_text(text)
        return tagged_text
    except Exception, e:
        print e


if __name__ == "__main__":
    main()
