# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-12 15:36:23
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 11:27:50

from flask import render_template, request, redirect, url_for
from ..utils import google_search
from . import google


@google.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('google.search', q=request.form.get('query'), page=0))
    return render_template('google/index.html')

@google.route('/s/')
def search():
    word = request.args.get('q')
    page = int(request.args.get('page', 0))
    return render_template('google/search.html', keyword=word, cur=page + 1)

@google.route('/s/s/')
def search_s():
    word = request.args.get('q')
    page = int(request.args.get('page', 0))
    results = google_search(word=word, pn=page)
    pages = results[1]
    results = results[0]
    return render_template('google/search_s.html', results=results, pages=pages, keyword=word, cur=page + 1)
