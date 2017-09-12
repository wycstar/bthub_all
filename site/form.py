#!/usr/bin/env python
# coding=utf-8

from flask_wtf import Form
from wtforms import StringField, SubmitField, validators


class TextQueryInput(Form):
    keyword = StringField(u'', validators=[validators.DataRequired(),
                                          validators.Length(1, 40)])
    submit = SubmitField(u'搜 索')
