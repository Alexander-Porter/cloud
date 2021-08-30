import os
import hashlib
import requests
import base64
import json
import time
scan=['E:/music']
fixer=['mp3','lrc']
userope='Alexander-Porter/cloud'
db='D:/nex.json'
def fileListFunc(filePathList,fixList,bool):
    fileList = []
    for filePath in filePathList:
        for top, dirs, nondirs in os.walk(filePath):
            for item in nondirs:
                path=os.path.join(top, item)
                try:
                  if(path.split(".")[1] in fixList):
                    with open(path, 'rb') as fp:
                      data = fp.read()
                    file_md5= hashlib.md5(data).hexdigest()   
                    if bool:
                      datas={'path':path,'sign':file_md5}
                    else:
                      datas=path
                    fileList.append(datas)
                except:
                  pass
    return fileList


def file2base64(path):
    with open(path, 'rb') as f:
      data_b64 = base64.b64encode(f.read()).decode('utf-8')
    return data_b64

def upload_file(path):
    file_name = path['path'].split('/')[1].replace('\\','/')
    dir=(os.path.dirname(file_name))
    raw=requests.get('https://ghapi.snakekiss.com/repos/'+userope+'/contents/'+dir,headers = {"Authorization": "token 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"})
    if raw.status_code==404:
      sha=False
    else:
      l=raw.json()
      try:sha=[x['sha'] for x in l if x['path']==file_name][0]
      except:
        sha=False
        print(file_name+'Error')
    print(file_name)    
    url = "https://ghapi.snakekiss.com/repos/"+userope+"/contents/"+file_name  # 用户名、库名、路径
    headers = {"Authorization": "token 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"}
    content = file2base64(path['path'])
    data = {
        "message": "message",
        "committer": {
            "name": "x",
            "email": "user@163.com"
        },
        "content": content
    }
    if (sha):
      data['sha']=sha
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers)
    print(raw.status_code,req.status_code)
with open (db,'r') as f:
  _list=json.loads(f.read())
file_list=fileListFunc(scan,fixer,True)
n=[]
has_done=[]
for i in file_list:
  if (_list.count(i)==0):
    n.append(i)
for i in n:
  upload_file(i)
  has_done.append(i)
  with open (db,'w') as f:
    f.write(json.dumps(has_done))

while True:
  need=[]
  _file_list=fileListFunc(scan,fixer,True)
  for i in _file_list:
    if (file_list.count(i)==0):
      print('修改或新增'+i['path'])
      need.append(i)
  file_list=fileListFunc(scan,fixer,True)
  with open (db,'w') as f:
    f.write(json.dumps(file_list))
  for g in need:
    upload_file(g)
  print('30s')
  time.sleep(30)