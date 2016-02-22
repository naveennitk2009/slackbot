__author__ = 'naveenkumar'
import requests
import copy
import datetime
import json
from django.core.mail import EmailMultiAlternatives


class SlackBot(object):
    def __init__(self, settings):
        self._TOKEN = settings['TOKEN']
        self._BASE_ENDPOINT = "https://slack.com"
        self._PARAMS = {'token': self._TOKEN}


    def get_imc_list(self):
        url = self._BASE_ENDPOINT + "/api/im.list"
        res = requests.get(url, params=self._PARAMS)
        return json.loads(res.text).get('ims')

    def get_user_info(self, id):
        url = self._BASE_ENDPOINT + "/api/users.info"
        params = copy.deepcopy(self._PARAMS)
        params.update({'user': id})
        res = requests.get(url, params=params)
        return json.loads(res.text).get('user')

    def get_messages_from_imc(self,imc_id):
        url = self._BASE_ENDPOINT + "/api/im.history"
        params = copy.deepcopy(self._PARAMS)
        date = datetime.datetime.now() - datetime.timedelta(days=2)
        timestamp = totimestamp(date)
        params.update({
            'channel': imc_id,
            'oldest': timestamp,
            'count': 1000
        })
        res = requests.get(url, params=params)
        return json.loads(res.text)

    def get_messages_from_imcs(self):
        im_messages = []
        imc_list = self.get_imc_list()
        for imc in imc_list:
            user_info = self.get_user_info(imc.get('user'))
            im_id = imc.get('id')
            messages = self.get_messages_from_imc(im_id)
            messages_to_send = []
            for message in reversed(messages.get('messages')):
                messages_to_send.append(message.get('text'))
            im_messages.append({
                'user': {
                    'name': user_info.get('name') if user_info.get('name') is not None else user_info.get('profile').get('real_name')
                },
                'messages': messages_to_send
            })
        body = ""
        for item in im_messages:
            body = body + '{name} - {res}\n'.format(name=item['user']['name'], res=item['messages'])

        #print(im_messages)
        subject = "SLACK CHAT: " + datetime.datetime.now().strftime("%d %m %Y")
        send_to = ["naveen.nitk2009@gmail.com"]
        msg = EmailMultiAlternatives(subject, json.dumps(body),
                            "myslackbot@slackbot.com", send_to)
        msg.send()
        return

def totimestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    # return td.total_seconds()
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6




# if __name__ == "__main__":
#     sbot = SlackBot(settings={'TOKEN': "xoxp-2526871921-13207990918-16823177588-bb0c66d389"})
#     sbot.get_messages_from_imcs()