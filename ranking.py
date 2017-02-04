#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import json
import bottle
import bottle_mysql
from bottle import *

app = bottle.Bottle()
config = json.load(open('./config.json','r'))
plugin = bottle_mysql.Plugin(dbuser=config['dbuser'],
							dbpass=config['dbpass'],
							dbname=config['dbname'],
							dbport=config['dbport'], 
							dbhost=config['dbhost'])
app.install(plugin)

def check(username, password):
	if username == 'admin' and password == 'password':
		return True
	else:
		return False

#トップページ
@app.route('/')
def toppage(db):
	db.execute('select * from ranking order by id')
	return template('./templates/top', itr=db.fetchall())

@app.route('/new/', method='get')
@auth_basic(check)
def new_get():
	return template('./templates/new')

@app.route('/new/', method='post')
def new_post(db):
	name = request.forms.get('name')
	comment = request.forms.get('comment')
	db.execute('insert into ranking(name, comment) values(%s,%s)', (name, comment))
	return 'OK'

@app.route('/add/', method='get')
def add_get():
	abort(405, 'めそっどのっとあらうど')

@app.route('/add/', method='post')
def add_post(db):
	name = request.forms.get('name')
	score = request.forms.get('score')
	ranking_id = request.forms.get('ranking_id')
	times = time.strftime("%Y/%m/%d %H:%M:%S")
	db.execute('insert into score(ranking_id, name, score, time) values(%s,%s,%s,%s)', (ranking_id, name, score, times))
	return 'OK'

@app.route('/show/<id:int>')
def show(db, id):
	db.execute('select name,score,time from score where ranking_id=%s order by score desc;',(id,))
	itr = db.fetchall()
	if(not itr):
		abort(404, '指定したランキングが見つかりません.')
	db.execute('select name, comment from ranking where id=%s', (id,))
	rank = db.fetchone()
	return template('./templates/show', itr=itr, rank=rank)

@app.route('/test/')
@auth_basic(check)
def test():
	return template('./templates/test')

#静的ファイル
@app.route('/static/<filepath:path>')
def statics(filepath):
	return static_file(filepath, root='./static')

if(__name__=='__main__'):
	app.run(host="0.0.0.0", port=80)
