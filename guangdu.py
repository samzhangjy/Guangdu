# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-10 20:05:03
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-10 20:05:07

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
