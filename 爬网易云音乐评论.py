import requests
import json
import os
import re
import urllib
from bs4 import BeautifulSoup
    
def get_songname(url):
    U=url.split('#/')
    url=U[0]+U[1]
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        
        }
    params="2n/JkBvSvikOEjdeEO/EE+m4AD1+hmIZlnFEG+Bm8X2kevh85tQb+z1s8nF0eUCEvJMREM7WyWEBLzoGbQ/+yrMyZInoY058rzeBIFmdPVvQFC2yjVbC2Ttypz/UCRshSoDf2j0XvbKYp0BHPAPlU04/K9LcKWIJqMM73+kzKtIOpVIh0ycwxwF1HXyaKDdkKb108Tw6cDVI6uw0DMo+/gDPPAU+3uifFBHIif99Uto="
    encSecKey="92922bae658c6edaad6cf41234c5f3e4cf170e8cc492459ab84f106e2cfa43c1daef630d8344f87860c894dcc4b1bc075a6307590eeada0c4e5cd880926d30a85aef76cd94f4044bccfeafd50bcf6a473201fb3869e5337ecd1ac6e7fb5cee9ba175cd59ef1b8d299990a35b15eb8d81f27031030191aa11acc895742a643f4f"
    data={
        'params':params,
        'encSecKey':encSecKey
        }
    r=requests.get(url,headers=headers,data=data)
    r.encoding='utf-8'
    song_html=BeautifulSoup(r.text,'html.parser')
    song_data=song_html.find('script',{'type':'application/ld+json'}).string
    song_name=json.loads(song_data)['title']
    r.encoding='utf-8'
    
    return song_name
  
def get_url(url):
    name_id=url.split('=')[1]
    
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'referer':'http://music.163.com/song?id={}'.format(name_id)
        }
    params="2n/JkBvSvikOEjdeEO/EE+m4AD1+hmIZlnFEG+Bm8X2kevh85tQb+z1s8nF0eUCEvJMREM7WyWEBLzoGbQ/+yrMyZInoY058rzeBIFmdPVvQFC2yjVbC2Ttypz/UCRshSoDf2j0XvbKYp0BHPAPlU04/K9LcKWIJqMM73+kzKtIOpVIh0ycwxwF1HXyaKDdkKb108Tw6cDVI6uw0DMo+/gDPPAU+3uifFBHIif99Uto="
    encSecKey="92922bae658c6edaad6cf41234c5f3e4cf170e8cc492459ab84f106e2cfa43c1daef630d8344f87860c894dcc4b1bc075a6307590eeada0c4e5cd880926d30a85aef76cd94f4044bccfeafd50bcf6a473201fb3869e5337ecd1ac6e7fb5cee9ba175cd59ef1b8d299990a35b15eb8d81f27031030191aa11acc895742a643f4f"
    data={
        'params':params,
        'encSecKey':encSecKey
        }
    
    target_url="http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=".format(name_id)

    res=requests.post(target_url,headers=headers,data=data)
    comments_json=json.loads(res.text)
    hot_comments=comments_json['hotComments']
    songname=get_songname(url)
    with open(songname+'.txt','w',encoding='utf-8') as file:
        for each in hot_comments:
            file.write(each['user']['nickname']+'\n')
            file.write(each['content']+'\n')
            file.write('................................\n\n')



    
def main():
    url=input("请输入链接:")
    get_url(url)
   

    
if __name__=="__main__":
    main()
