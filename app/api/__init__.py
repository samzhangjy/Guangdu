# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-14 11:01:56
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 12:41:25

from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from . import baidu, google