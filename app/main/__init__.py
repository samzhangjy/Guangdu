# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-14 11:07:21
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 11:39:10

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors