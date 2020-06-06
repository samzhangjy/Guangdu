# -*- coding: utf-8 -*-
# @Author: Sam Zhang
# @Date:   2020-04-14 11:09:21
# @Last Modified by:   Sam Zhang
# @Last Modified time: 2020-04-14 17:53:28

from flask import render_template, request, current_app, send_from_directory
from . import main
import os
from pytube import YouTube
from uuid import uuid1

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/docs/')
def docs():
    return render_template('docs.html')

@main.route('/about/')
def about():
    return render_template('about.html')

@main.route('/youtube/')
def youtube():
    id = request.args.get('id')
    video_url = 'https://www.youtube.com/watch?v=%s' % id
    youtube = YouTube(video_url)
    video = youtube.streams.filter(res='720p', mime_type='video/mp4')[0]
    uuid = str(uuid1()) + '.mp4'
    path = video.download(os.path.abspath('./app/static'), filename=uuid)
    print(os.system('cd ./app/static&&ls'))
    return send_from_directory('./app/static', uuid)
