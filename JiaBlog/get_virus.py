import requests
from bs4 import BeautifulSoup

target = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579579384&enterid=1579579384&from=groupmessage&isappinstalled=0'
req = requests.get(url=target)
req.encoding = 'urf-8'
html = req.text
soup = BeautifulSoup(html, 'html.parser')
cities = soup.find('div', {'class': 'descBox___3dfIo'})
protocols = cities.find_all('p')
data = {}

for i in protocols:
    try:
        content = i.find('span').get_text()
        name = content[:3].replace(" ", "")
        content = content.replace(" ", "")
        num = 0
        try:
            num_start = content.index('诊')
            num_end = content.find('例')
            num = content[num_start + 1:num_end]
            data['{}'.format(name)] = num
        except:
            pass
        print('疫情：', name, '确诊', num, '例')
    except AttributeError as e:
        continue
print(data)