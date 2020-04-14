# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-14 12:39:01
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 16:53:45

from flask import jsonify, request
from . import api
from ..utils import google_search

@api.route('/google/')
def google():
    query = request.args.get('q')
    if query is None:
        return jsonify({'status': '400', 'message': 'No search query provided', 'results': [], 'pages': 0, 'keyword': ''})
    try:
        page = int(request.args.get('page', 0))
    except:
        return jsonify({'status': '400', 'message': 'Invalid page num', 'results': [], 'pages': 0, 'keyword': query})
    results = google_search(word=str(query), pn=int(page))
    try:
        pages = len(results[1])
        results = results[0]
    except IndexError:
        results = []
        pages = 0
    return jsonify({'status': '200', 'message': 'Success', 'results': results, 'pages': pages, 'keyword': query})