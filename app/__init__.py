import pickle

from config import VERBS
from config import POS_TAGGER
from config import KNN
from config import N_SIGS
from config import N_BANDS

from flask import Flask

from classifier.postagger import mxpost
from classifier.LocalitySensitiveHashing import LocalitySensitiveHashing

print "Loading PoS-tagger", POS_TAGGER
f_model = open(POS_TAGGER, "rb")
pos_tagger = pickle.load(f_model)
f_model.close()

print "Loading verbs", VERBS
f_verbs = open(VERBS, "rb")
verbs = pickle.load(f_verbs)
f_verbs.close()

print "Creating REDIS connection"
lsh = LocalitySensitiveHashing(N_BANDS, N_SIGS, KNN, True)

app = Flask(__name__)
app.config.from_object('config')

print "Server ready!"

from app import views