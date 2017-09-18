#!/usr/bin/env python
# coding=utf-8

from form import TextQueryInput
from flask import url_for, render_template, request, redirect
from app import app
from . import ELASTIC


@app.route('/', methods=['POST'])
def index():
    index_form = TextQueryInput(request.form)
    if index_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=index_form.keyword.data, page_num=1))
    return render_template('index.html', form=index_form)


@app.route('/s/<keyword>/<int:page_num>', methods=['GET', 'POST'])
def search_result(keyword, page_num):
    if page_num < 1:
        page_num = 1
    r = ELASTIC.search(keyword, page_num)
    query_form = TextQueryInput(request.form)
    if query_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=query_form.keyword.data, page_num=1))
    query_form.keyword.data = keyword
    return render_template('result.html',
                           keyword=keyword,
                           result_num=c.result_count,
                           result_time=c.take_time,
                           google_results=c.google_result,
                           zhihu_results=c.zhihu_result,
                           current_page=page_num,
                           query_form=query_form)