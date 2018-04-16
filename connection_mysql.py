import pymysql
import os.path
import re

import song
import playlist
class connect:
	def __init__(self):
		try:
			if os.path.isfile('sql.config'):
				file = open('sql.config','r',encoding='utf-8')
				res=file.read()
				host=res.split(',',3)[0].split('=')[1]
				user=res.split(',',3)[1].split('=')[1]
				passwd=res.split(',',3)[2].split('=')[1]
				db=res.split(',',3)[3].split('=')[1]
				file.close()
			else:
				print('sql.config文件不存在')
			self.conn = pymysql.connect(host,user,passwd,db,charset='utf8')
			self.cur = self.conn.cursor()
			self.cur.execute("use music163")
		except Exception :
			print('数据库链接出错或数据库没有music163数据库')
	def create_database(self):#不存在music163数据库，则可以调用此函数创建数据库
		self.cur.execute("create database music163 default character utf8")
		self.cur.execute("use music163")
		self.cur.execute("create table song (id varchar(10)not null,name varchar(100) not null,singer varchar(100),primary key(id))")
		self.cur.execute("create table playlist (id varchar(10)not null,name varchar(40) not null,creator varchar(100),primary key(id))")
	def wsong(self,song):#歌曲名字带有特殊符号的去掉特殊符号
		if self.cur.execute('select * from song where id="%s"'%(song.get_id()))==1:
			return False
		re.sub(r"[/,\,:,*,?,\",<,>,|]","_",song.get_name())#windows中文件名不能存在的字符替换成_
		str1='insert into song values("%s","%s","%s")'%(song.get_id(),song.get_name(),song.get_singer())
		self.cur.execute(str1)
		self.cur.connection.commit()
		return True
	def wplaylist(self,playlist):
		if self.cur.execute('select * from playlist where id="%s"'%(playlist.get_id()))==1:
			return False
		str1='insert into playlist values("%s","%s","%s")'%(playlist.get_id(),playlist.get_name(),playlist.get_creator())
		self.cur.execute(str1)
		self.cur.connection.commit()
		return True
	def get_song(self,str=""):
		if str!="":
			self.cur.execute('select * from song where id='+str)
		else:
			self.cur.execute('select * from song')
		return self.cur.fetchall()
	def connect_close(self):
		self.cur.close()
		self.conn.close()