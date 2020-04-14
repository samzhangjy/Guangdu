# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-12 15:34:31
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-12 15:41:12

from flask import Blueprint

google = Blueprint('google', __name__, url_prefix='/google/')

from . import views