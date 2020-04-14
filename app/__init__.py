# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-10 20:05:32
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 11:17:08

from flask import Flask
from .extensions import *
from uuid import uuid4


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = str(uuid4())

    bootstrap.init_app(app)

    from  .main import main as main_bp
    app.register_blueprint(main_bp)

    from .baidu import baidu as baidu_bp
    app.register_blueprint(baidu_bp)

    from .google import google as google_bp
    app.register_blueprint(google_bp)

    from .api import api as api_bp
    app.register_blueprint(api_bp)

    return app
