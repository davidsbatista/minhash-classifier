#!/bin/bash
java -mx10g -cp stanford-ner-2014-01-04.jar edu.stanford.nlp.ie.NERServer -loadClassifier ner-model-ptBIO.ser -port 9191 -outputFormat xml
