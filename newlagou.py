import requests
import json
import csv
import codecs
import sys
import os.path as op

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Upgrade-Insecure-Requests': '1',
'Referer':'https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95?px=new&yx=10k-15k&city=%E8%A5%BF%E5%AE%89#order',
'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'
}


#设置一个会话
session = requests.session()

# 发送Get请求更新cookie
session.get('https://www.lagou.com/jobs/list_%E6%B5%8B%E8%AF%95?px=new&yx=10k-15k&city=%E8%A5%BF%E5%AE%89#order',headers=headers)

data = {
'first':'true',
'pn':1,
'kd':'测试'
}

#使用更新后的hsession请求Ajax json
rep = session.post('https://www.lagou.com/jobs/positionAjax.json?px=new&yx=10k-15k&city=%E8%A5%BF%E5%AE%89&needAddtionalResult=false',headers=headers,data=data)
# 转换成json格式进行分析，抽取
result = json.loads(rep.content.decode(encoding="utf-8-sig"))

# 请求成功，接下来就是提取想要的信息。
positions=result['content']['positionResult']['result']
#print(positions)
#创建要保存的CSV文件
fields = ['年限','学历','职位','公司','薪水','城市','发布时间']
fd = open(op.join(sys.path[0], 'fjobs.csv'), 'w')
# 解决编码（乱码）问题
fd.write(codecs.BOM_UTF8.decode(encoding="utf-8-sig"))
writer=csv.DictWriter(fd, fields, dialect='excel')
writer.writeheader()
for position in positions:
        jobs={
            '年限':position['workYear'],
            '学历':position['education'],
            '职位':position['positionName'],
            '公司':position['companyFullName'],
            '薪水':position['salary'],
            '城市':position['city'],
            '发布时间':position['createTime']
        }
        print(jobs)
        writer.writerow(jobs)
fd.close()       