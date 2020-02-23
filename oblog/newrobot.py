import json
import requests
import traceback
from werobot import WeRoBot


class TulingAutoReply:

    def __init__(self, tuling_key, tuling_url):
        self.key = tuling_key
        self.url = tuling_url

    def my_reply(self, unicode_str):
        body = {'key': self.key, 'info': unicode_str.encode('utf-8')}
        r = requests.post(self.url, data=body)
        r.encoding = 'utf-8'
        resp = r.text
        if resp is None or len(resp) == 0:
            return None
        try:
            js = json.loads(resp)
            if js['code'] == 100000:
                return js['text'].replace('', 'n')
            elif js['code'] == 200000:
                return js['url']
            else:
                return None
        except Exception:
            traceback.print_exc()
            return None



auto_reply = TulingAutoReply('bce36f0e23d44ef694f3843743552375', 'http://openapi.tuling123.com/openapi/api/v2')  # key和url从图灵机器人网站上申请得到

robot = WeRoBot(enable_session=False,
                token='ssjsecrettoken980612ssj',
                APP_ID='wx3200e87d6dd9eddd',
                APP_SECRET='3aade7b8bbf9cb305b076a1d2d0e4a71')

@robot.handler
def hell(message):
    rep = auto_reply.my_reply(message)
    return rep