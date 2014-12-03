#!/bin/bash

STANFORD_NER_JAR=/home/dsbatista/pt-ner/stanford-ner-2014-01-04.jar
CLASSIFIER=/home/dsbatista/pt-ner/ner-model-ptBIO.ser

java -mx10g -cp $STANFORD_NER_JAR edu.stanford.nlp.ie.NERServer -loadClassifier $CLASSIFIER -port 9191 -outputFormat xml
