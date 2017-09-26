#!/usr/bin/env python
# coding=utf-8

from form import TextQueryInput
from flask import url_for, render_template, redirect, request
from server import SITE, ELASTIC, SERVER
from db import MONGO
import re


@SITE.route('/', methods=['GET', 'POST'])
def index():
    index_form = TextQueryInput()
    if index_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=index_form.keyword.data.replace(' ', '+'), page_num=1))
    return render_template('index.html', form=index_form)


@SITE.route('/s/<keyword>/<int:page_num>', methods=['GET', 'POST'])
def search_result(keyword, page_num):
    query_form = TextQueryInput()
    r = ELASTIC.search(keyword.replace('+', ' '), page_num, request.args.get('sort'), request.args.get('order'))
    if query_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=query_form.keyword.data.replace(' ', '+'), page_num=1))
    return render_template('result.html',
                           query_form=query_form,
                           keyword=keyword,
                           result_num=r.get('total'),
                           result_time=r.get('took'),
                           results=r.get('result'),
                           current_page=page_num)


@SITE.route('/hash/<h>', methods=['GET', 'POST'])
def result_detail(h):
    query_form = TextQueryInput()
    r = MONGO.get(h)
    f, s = ELASTIC._convert(r['f'])
    # 测试热度绘图
    import random
    import datetime
    p = [random.randint(0, 10) for _ in range(14)]
    # 测试完毕
    if query_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=query_form.keyword.data, page_num=1))
    return render_template('detail.html',
                           query_form=query_form,
                           name=r['n'],
                           files=f,
                           size=s,
                           date=r['d'],
                           mag='magnet:?xt=urn:btih:' + r['_id'],
                           likes=ELASTIC.analyze(r['n']),
                           chart_date=[(datetime.datetime.utcnow() - datetime.timedelta(days=x)).strftime("%m-%d") for x in range(14, 0, -1)],
                           chart_data=p,
                           vote=r.get('g'))


@SERVER.on('message', namespace='/push')
def handle_message(message):
    print message


@SERVER.on('like', namespace='/push')
def handle_like(message):
    print 'like {0}'.format(message)
    if re.search(r'^[0-9a-fA-F]+$', message) and len(message) == 40:
        MONGO.like(message)


@SERVER.on('unlike', namespace='/push')
def handle_like(message):
    print 'unlike {0}'.format(message)
    if re.search(r'^[0-9a-fA-F]+$', message) and len(message) == 40:
        MONGO.unlike(message)
