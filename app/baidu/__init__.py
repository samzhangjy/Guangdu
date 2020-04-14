# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-10 20:06:38
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 11:08:07

from flask import Blueprint

baidu = Blueprint('baidu', __name__, url_prefix='/baidu')

from . import views
