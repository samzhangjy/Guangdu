# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-14 11:35:31
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 12:38:16

from . import main
from flask import render_template, request, jsonify


@main.app_errorhandler(404)
def not_found(e):
    if request.path.startswith('/api'):
        return jsonify({'status': '404', 'message':'Not found'}), 404
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    if request.path.startswith('/api'):
        return jsonify({'status': '500', 'message':'Internal server error'}), 500
    return render_template('errors/500.html'), 500
