import requests
import json

def talk(content):
    url = 'http://www.tuling123.com/openapi/api'
    s =requests.session()
    d = {'key':'bce36f0e23d44ef694f3843743552375','info':content}
    data = json.dumps(d)
    r = s.post(url,data=data)
    text = json.loads(r.text)
    return text['text']