#!/usr/bin/env python
# coding=utf-8

from flask_wtf import Form
from wtforms import StringField, SubmitField, validators
from db import REDIS


class TextQueryInput(Form):
    keyword = StringField(u'在10000个资源中搜索',
                          validators=[validators.DataRequired(),
                                      validators.Length(1, 40)],
                          render_kw={'placeholder':('在' + str(REDIS.count()) + '个资源中搜索').decode('utf-8')})
    submit = SubmitField(u'搜索')
