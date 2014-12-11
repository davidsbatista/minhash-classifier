#!/usr/bin/env python

from classifier.postagger import mxpost
from app import app
app.run(debug=True,host= '0.0.0.0')
