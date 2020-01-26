import requests
from bs4 import BeautifulSoup
from selenium import webdriver

target = 'https://3g.dxy.cn/newh5/view/pneumonia?scene=2&clicktime=1579579384&enterid=1579579384&from=groupmessage&isappinstalled=0'
req = requests.get(url=target)
req.encoding = 'urf-8'
html = req.text
option = webdriver.ChromeOptions()
option.add_argument('headless')  # 设置option,后台运行
option.add_argument('--no-sandbox')
driver = webdriver.Chrome(chrome_options=option)
driver.get(target)
js = "var q=document.documentElement.scrollTop=1500"
driver.execute_script(js)
selenium_page = driver.page_source
soup = BeautifulSoup(selenium_page, 'html.parser')
protocols = soup.find('div', {'class': 'areaBox___3jZkr'})
# protocols = soup.find('div', {'class': 'wrapper___3xhNP'})
print(protocols)
# 每个省
cities = protocols.find_all('div')
data = {}

for i in cities:
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