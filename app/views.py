import codecs

from flask import render_template, redirect, flash
from forms import TextForm

from app import app, verbs, pos_tagger, LocalitySensitiveHashing
from app import app, lsh
from config import N_SIGS

from classifier import MinHash
from classifier.FeatureExtractor import FeatureExtractor
from classifier.Relationship import Relationship


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/classified')
def read_classified():
    classified_sents = codecs.open("/home/dsbatista/rel-eXtractor/output_classifer.txt", encoding='utf-8')
    count = 0
    sentences = []
    for line in classified_sents:
        if count == 100:
            return render_template("output.html", sentences=sentences)
        if line == '\n':
            t = (sentence, arg1, arg2, relation)
            sentences.append(t)
            sentence = None
            relation = None
            arg1 = None
            arg2 = None
            count += 1
        else:
            if line.startswith("relation:"):
                relation = line.strip()
            elif line.startswith("<"):
                if arg1 == '':
                    arg1 = line.strip()
                else:
                    arg2 = line.strip()
            else:
                sentence = line
    classified_sents.close()


@app.route('/text', methods=['GET', 'POST'])
def classify():
    form = TextForm()
    if form.validate_on_submit():
        #flash('Text to process = "%s" ' % form.text_area.data)

        sentence = form.text_area.data
        print "creating relationship object"
        rel = Relationship(None, sentence, None)

        print "extrating shingles"
        # extract features/shingles
        extractor = FeatureExtractor(pos_tagger, verbs)
        #extractor = FeatureExtractor(None, None)
        features = extractor.extract_features(rel)
        shingles = features.getvalue().strip().split(' ')

        print shingles

        print "calculating min-hash sigs"
        # calculate min-hash sigs
        sigs = MinHash.signature(shingles, N_SIGS)
        rel.sigs = sigs

        print "classifying"
        rel_type = lsh.classify(rel)

        print "classified as :", rel_type

        return render_template('classified.html', rel_type=rel_type, sentence=sentence)

    return render_template('text.html', title='Extract Relationships', form=form)