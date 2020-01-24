import requests
from bs4 import BeautifulSoup

target = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579579384&enterid=1579579384&from=groupmessage&isappinstalled=0'
req = requests.get(url=target)
req.encoding = 'urf-8'
html = req.text
soup = BeautifulSoup(html, 'html.parser')
cities = soup.find('div', {'class': 'areaBox___3jZkr'})
# 每个省
protocols = cities.find_all('div')
data = {}

for i in protocols:
    try:
        first = i.find('div', {'class': 'areaBlock1___3V3UU'})
        content = first.find_all('p')
        name = content[0].get_text()
        num = content[1].get_text()
        print(num)
        if num == "":
            num = 0
        data['{}'.format(name)] = num
        print('疫情：', name, '确诊', num, '例')
    except AttributeError as e:
        continue
print(data)