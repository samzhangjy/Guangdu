# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-14 11:09:21
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 17:53:28

from flask import render_template
from . import main
import os

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/docs/')
def docs():
    return render_template('docs.html')

@main.route('/about/')
def about():
    return render_template('about.html')
