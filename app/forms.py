# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
#from wtforms.validators import DataRequired


class TextForm(Form):
    text = StringField('text')
    default = '<PER>Zé</PER> é membro do grupo <ORG>Ovos Podres</ORG>'.decode("utf8")
    text_area = TextAreaField("TextArea", default=default)
