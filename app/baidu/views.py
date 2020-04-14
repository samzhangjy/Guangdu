# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-10 20:06:43
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 11:28:00

from . import baidu
from flask import render_template, request, redirect, url_for, abort, make_response, session
from app.utils import baidu_search, google_search


@baidu.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        q = request.form.get('query')
        pn = request.args.get('page')
        if pn is None:
            pn = 0
        return redirect(url_for('baidu.search', q=q, page=pn))
    return render_template('baidu/index.html')


@baidu.route('/s/', methods=['GET', 'POST'])
def search():
    q = request.args.get('q')
    pn = int(request.args.get('page', 0))
    return render_template('baidu/search.html', keyword=q, cur=pn)
    
@baidu.route('/s/s/', methods=['GET', 'POST'])
def search_s():
    q = request.args.get('q')
    pn = int(request.args.get('page', 0))
    results = baidu_search(word=str(q), pn=int(pn))
    try:
        pages = results[1]
        results = results[0]
    except IndexError:
        results = []
        pages = 0
    pages_ = []
    for i in range(0, pages):
        pages_.append(i)
    return render_template('baidu/search_s.html', keyword=q, results=results, pages=pages_, cur=pn)
