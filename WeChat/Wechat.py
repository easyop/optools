# -*- coding: utf-8 -*-
# * Author        : Zachary  mail : easydevops@163.com
# * Create time   : 2019-05-29 10:22
# * Description   :
import requests
import time
import json


class WeChatApp():
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid

    def _getAccessToken(self):
        '''获取accessToken'''
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        info = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret
        }
        access_token = requests.get(url=url, params=info).json()['access_token']
        return access_token

    def getAccessoken(self):
        try:
            with open(self.agentid + '.accesstoken', 'rt') as f:
                get_time, access_token = f.read().split()
        except:
            with open(self.agentid + '.accesstoken', 'wt') as f:
                access_token = self._getAccessToken()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if cur_time - float(get_time) < 7200:
                return access_token
            else:
                with open(self.agentid + '.accesstoken', 'wt') as f:
                    access_token = self._getAccessToken()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def sendToApp(self, partyid=None, user=None, content=None):
        '''发送消息到应用'''
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.getAccessoken()
        body = {
            "toparty": partyid,
            "touser": user,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": content
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(body), 'utf-8'))
        response = requests.post(url, send_msges).json()
        # response = response.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        #         print (respone["errmsg"])
        return response["errmsg"]

    def createChat(self, chatname, chatid, ower, userlist, ):

        """通过应用创建群聊，创建群聊的应用可见范围需要是根部门"""
        url = "https://qyapi.weixin.qq.com/cgi-bin/appchat/create?access_token=" + self.getAccessoken()
        body = {
            "name": chatname,
            "owner": ower,
            "userlist": userlist,
            "chatid": chatid
        }
        send_msg = (bytes(json.dumps(body), 'utf-8'))
        res = requests.post(url=url, data=send_msg).json()
        return res

    def sendToChat(self, chatid, content):
        """通过应用发送消息到群聊，只有通过应用创建的群聊才能使用此方法"""
        url = " https://qyapi.weixin.qq.com/cgi-bin/appchat/send?access_token=" + self.getAccessoken()
        body = {
            "chatid": chatid,
            "msgtype": "text",
            "text": {"content": content},
            "safe": 0
        }
        send_msgs = (bytes(json.dumps(body), 'utf-8'))
        res = requests.post(url=url, data=send_msgs).json()
        return res


    def sendImageToApp(self, partyid=None, user=None, content=None):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.getAccessoken()
        body = {
            "toparty": partyid,
            "touser": user,
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": content
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(body), 'utf-8'))
        response = requests.post(url, send_msges).json()
        # response = response.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        #         print (respone["errmsg"])
        return response["errmsg"]

    def uploadImage(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token=' + self.getAccessoken() + '&type=image'
        path = '/Users/zachary/workspace/wechat/duola.jpeg'
        files = {'image': open(path, 'rb')}
        response = requests.post(url, files=files).json()

        print(response['media_id'])

    def sendarticleToApp(self, partyid=None, user=None, content=None):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.getAccessoken()
        body = {
            "toparty": partyid,
            "touser": user,
            "msgtype": "news",
            "agentid": self.agentid,
            "news": {
                "articles": [
                    {
                        "title": "我的博客上线啦",
                        "description": "点击链接进入我的博客主页",
                        "url": "http://www.ilinux.tech",
                        "picurl": "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
                    }
                ]
            },
            "safe": "0"
        }

        send_msges = (bytes(json.dumps(body), 'utf-8'))
        response = requests.post(url, send_msges).json()
        return response["errmsg"]

    def createMenu(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token={token}&agentid={agentid}'.format(
            token=self.getAccessoken(), agentid=self.agentid)
        body = {
            "button": [
                {
                    "type": "click",
                    "name": "今日歌曲",
                    "key": "V1001_TODAY_MUSIC"
                },
                {
                    "name": "菜单",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "我的博客",
                            "url": "http://www.ilinux.com/"
                        },
                        {
                            "type": "click",
                            "name": "赞一下我们",
                            "key": "V1001_GOOD"
                        }
                    ]
                }
            ]
        }
        send_msgs = (bytes(json.dumps(body), 'utf-8'))
        res = requests.post(url=url, data=send_msgs).json()
        return res


if __name__ == '__main__':
    #测试信息
    xiaoduola = WeChatApp('ww8a72e32145e84754', 'XE32ecrqwVvOL-XkZlLws1AMd7Trs', '1000002')
    print(xiaoduola.sendToChat(chatid='haha', content='xxx'))


