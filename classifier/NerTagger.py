#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import ner
import StringIO
import sys
from xml.dom.minidom import parseString


def main():
    tagger = NerTagger()
    tagged = tagger.tag_document(sys.argv[1])
    for t in tagged:
        print t


class NerTagger:

    def __init__(self):
        self.tagger = ner.SocketNER(host='localhost', port=9191)
        self.sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        self.punctuation = [".", ", ", "!", "?", "; ", ":"]

    def tag_document(self, document):
        f_txt = open(document)
        sentences = self.sent_tokenizer.tokenize(f_txt.read())
        f_txt.close()
        tagged_document = []
        for sentence in sentences:
            # tag text, one sentence at the time
            document = StringIO.StringIO()
            labeled_text = self.tagger.tag_text(sentence)
            tagged_text = self.add_tags(self, labeled_text)
            document.write(tagged_text)
            tagged_text = document.getvalue().encode("utf8")
            tagged_document.append(tagged_text.strip())

        return tagged_document

    @staticmethod
    def add_tags(self, labeled_tokens):
        try:
            dom = parseString('<root>' + labeled_tokens.encode("utf8") + '</root>')
            tokens = dom.getElementsByTagName('wi')
            text = StringIO.StringIO()
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
                if tag_type != 'I-PER' and previous_type == 'B-PER':
                    text.write('</PER>')
                elif tag_type != 'I-ORG' and previous_type == 'B-ORG':
                    text.write('</ORG>')
                elif tag_type != 'I-LOC' and previous_type == 'B-LOC':
                    text.write('</LOC>')
                elif tag_type != 'I-MSC' and previous_type == 'B-MSC':
                    text.write('</MSC>')

                # end of multi-word entity
                if tag_type == 'O' and previous_type != 'O':
                    end_tag = ''
                    if tag_type == 'O' and previous_type == 'I-PER':
                        end_tag = '</PER>'
                    elif tag_type == 'O' and previous_type == 'I-ORG':
                        end_tag = '</ORG>'
                    elif tag_type == 'O' and previous_type == 'I-LOC':
                        end_tag = '</LOC>'
                    elif tag_type == 'O' and previous_type == 'I-MSC':
                        end_tag = '</MSC>'

                    if word in self.punctuation:
                        text.write(end_tag+word)
                    else:
                        text.write(end_tag+' '+word)

                # ex: B-LOC,I-LOC,B-LOC
                elif tag_type.startswith("B") and previous_type.startswith("I"):
                    text.write('</'+previous_type.split("-")[1]+'> <'+tag_type.split("-")[1]+">" + word)

                # sentence ends in a multi-word or single entity
                elif tokens.index(token) == len(tokens)-1 and tag_type!='O':
                    if tag_type == 'I-PER': text.write(' '+word+'</PER>')
                    if tag_type == 'I-LOC': text.write(' '+word+'</LOC>')
                    if tag_type == 'I-ORG': text.write(' '+word+'</ORG>')
                    if tag_type == 'I-MSC': text.write(' '+word+'</MSC>')
                    if tag_type == 'B-PER': text.write(' <PER>'+word+'</PER>')
                    if tag_type == 'B-LOC': text.write(' <LOC>'+word+'</LOC>')
                    if tag_type == 'B-ORG': text.write(' <ORG>'+word+'</ORG>')
                    if tag_type == 'B-MSC': text.write(' <MSC>'+word+'</MSC>')

                # inside a multi-word entity
                elif tag_type == 'I-PER': text.write(' '+word)
                elif tag_type == 'I-LOC': text.write(' '+word)
                elif tag_type == 'I-ORG': text.write(' '+word)
                elif tag_type == 'I-MSC': text.write(' '+word)

                # start of a new entity
                elif tag_type == 'B-ORG': text.write(' <ORG>'+word)
                elif tag_type == 'B-PER': text.write(' <PER>'+word)
                elif tag_type == 'B-LOC': text.write(' <LOC>'+word)
                elif tag_type == 'B-MSC': text.write(' <MSC>'+word)

                # not part of an entity
                elif tag_type == 'O':
                    if word in self.punctuation:
                        text.write(word)
                    elif word == """``""":
                        text.write(' "')
                    elif word == """''""":
                        text.write('"')
                    else: text.write(' '+word)

                previous_type = tag_type

            return text.getvalue()

        except Exception, e:
            print "XML parsing"+'\t'+e.message+'\n'


if __name__ == "__main__":
    main()
