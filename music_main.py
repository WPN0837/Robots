import requests
from bs4 import BeautifulSoup
import re
import json
import pymysql
import os.path

import song
import playlist
import get_comments
import connection_mysql
def entry_playlist(purl):
	id=purl[-10:]
	purl="http://music.163.com/api/playlist/detail?id={}&upd".format(id)
	headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'connection': 'keep-alive', 'cache-control': 'no-cache','Referer': 'http://music.163.com/'}
	s=BeautifulSoup(requests.get(purl,headers=headers).content,'html.parser')
	pl=json.loads(s.text)['result']
	pid=pl['id']
	pname=pl['name']
	pcreator=pl['creator']['nickname']
	c=connection_mysql.connect()
	try:
		if c.wplaylist(playlist.playlist(pid,pname,pcreator)):
			print('歌单信息录入成功 '+pname)
			for i in pl['tracks']:
				if c.wsong(song.song(i['id'],i['name'],"")):
					print('歌曲信息录入成功 '+i['name'])
				else:
					print('此歌曲信息已存在 '+i['name'])
		else:
			print('歌单信息已存在 '+pname)
	except Exception:
		print('music_main出现异常')
	finally:
		c.connect_close()
def get_songcomment_from_mysql():
	headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36','referer':'http://music.163.com/'}
	params="2n/JkBvSvikOEjdeEO/EE+m4AD1+hmIZlnFEG+Bm8X2kevh85tQb+z1s8nF0eUCEvJMREM7WyWEBLzoGbQ/+yrMyZInoY058rzeBIFmdPVvQFC2yjVbC2Ttypz/UCRshSoDf2j0XvbKYp0BHPAPlU04/K9LcKWIJqMM73+kzKtIOpVIh0ycwxwF1HXyaKDdkKb108Tw6cDVI6uw0DMo+/gDPPAU+3uifFBHIif99Uto="
	encSecKey="92922bae658c6edaad6cf41234c5f3e4cf170e8cc492459ab84f106e2cfa43c1daef630d8344f87860c894dcc4b1bc075a6307590eeada0c4e5cd880926d30a85aef76cd94f4044bccfeafd50bcf6a473201fb3869e5337ecd1ac6e7fb5cee9ba175cd59ef1b8d299990a35b15eb8d81f27031030191aa11acc895742a643f4f"
	data={'params':params,'encSecKey':encSecKey}
	
	
	c=connection_mysql.connect()
	try:
		res=c.get_song()
		if len(res)==0:
			return 0
		for i in res:
			print(i[0])
			r=requests.post("http://music.163.com/weapi/v1/resource/comments/R_SO_4_{0}?csrf_token=".format(i[0]),headers=headers,data=data)
			comments_json=json.loads(r.text)
			hot_comments=comments_json['hotComments']
			Path="d:/comments/{0}.txt".format(i[1])
			if not os.path.isfile(Path):
				with open(Path,'w',encoding='utf-8') as file:
					for each in hot_comments:
						file.write(each['user']['nickname']+'\n')
						file.write(each['content']+'\n')
						file.write('................................\n\n')
	except Exception:
		print('music_main出现异常',Exception)
	finally:
		c.connect_close()
if __name__=='__main__':
	print('1.爬取歌单')
	print('2.爬取数据库存储的歌曲评论')
	num=int(input('请选择:'))
	if num==1:
		url=input("url:")
		entry_playlist(url)
	elif num==2:
		get_songcomment_from_mysql()
	else:
		print('功能不存在')		
		
#先加上try catch finally  保证最后数据库连接能关闭
#及时抛出异常，如当存在主键已存在问题时可以：歌单；关闭或跳过这个歌单   歌曲：跳过这个歌曲录入下一首歌曲id
