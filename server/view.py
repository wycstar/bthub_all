#!/usr/bin/env python
# coding=utf-8

from form import TextQueryInput
from flask import url_for, render_template, redirect, flash
from server import SITE
from server import ELASTIC


@SITE.route('/', methods=['GET', 'POST'])
def index():
    index_form = TextQueryInput()
    if index_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=index_form.keyword.data, page_num=1))
    return render_template('index.html', form=index_form)


@SITE.route('/s/<keyword>/<int:page_num>', methods=['GET', 'POST'])
def search_result(keyword, page_num):
     r = ELASTIC.search(keyword, page_num)
     if r is None:
         flash(u'asdfasdfasdf')
     print r
     query_form = TextQueryInput()
     if query_form.validate_on_submit():
         return redirect(url_for('search_result', keyword=query_form.keyword.data, page_num=1))
     return render_template('result.html',
                            query_form=query_form,
                            keyword=keyword,
                            result_num=r.get('total') if r is not None else 0,
                            result_time=r.get('took') if r is not None else 0,
                            results=r.get('result') if r is not None else 0)
#                            zhihu_results=c.zhihu_result,
#                            current_page=page_num,
#                            query_form=query_form)


@SITE.route('/hash/<h>', methods=['GET'])
def result_detail(h):
    query_form = TextQueryInput()
    if query_form.validate_on_submit():
        return redirect(url_for('search_result', keyword=query_form.keyword.data, page_num=1))
    return render_template('detail.html',
                           query_form=query_form)
