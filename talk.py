
import requests, sys,json
import ssl
import itchat
# itchat.auto_login(enableCmdQR=True)  # 这里需要你人工手机扫码登录
que = []

headers = {'content-type': 'application/json;charset=UTF-8'}
# url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&grant_type=client_credentials&client_id=y62Mvz0WiGKflUcGxrs1Cuxj&client_secret=Nwgb1MxIduU7sA14IVKW6CThRuA6iL0X'
# url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&grant_type=client_credentials&client_id=y62Mvz0WiGKflUcGxrs1Cuxj&client_secret=Nwgb1MxIduU7sA14IVKW6CThRuA6iL0X'
url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=6OxYrUsikwNmdkysvzXCVfxE&client_secret=t0DASvc0PIPt28KFQDvMZK3bZWG46YgV'


# request = requests.post(url,headers=headers)
request = requests.get(url,headers=headers)
content = request.text
if (content):
    dic = json.loads(content)
access_token = dic.get("access_token")

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    que.clear()
    que.append(msg['Text'])
    if que:
        print("收到消息：   " + que[0])
        itchat.send(que[0], xiaohao)
        post_data = '{"version":"2.0","sessionId":"service-session-id-1564725848057-b8b432886c094e6894aeb6ba393f482a",' \
                            '"request":{"query":"%s","user_id":"88888"},"SYS_REMEMBERED_SKILLS":"1057","bot_id":"72142",' \
                        '"log_id":"4de8dc00-b4d9-11e9-8e8c-e7e03a055294","source":"KEYBOARD","type":"TEXT",' \
                        '"bot_session":""}' % que[0]
        new_url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token
        req = requests.post(new_url,post_data.encode('utf-8'),headers=headers)
        res = req.text
        if (res):
            res = json.loads(res)
            result = res.get("result").get("response").get("action_list")[0].get("say")
            if result:
                itchat.send(result,xiaohao)
                print("send: "+result)
                return result

itchat.auto_login(hotReload=True)
# friend_list = itchat.get_friends(update=True)  # 第一个是自己
# friend_list = friend_list[1:]
# for friend in friend_list:
#     print(friend)
# name = itchat.search_friends(name=u'ai君君')
try:
    name = itchat.search_friends(name=u'a小号')
    xiaohao = name[0]["UserName"]
    itchat.run()
except:
    pass

# while 1:
#     que = input(">>>: ")
#     post_data = '{"version":"2.0","sessionId":"service-session-id-1564725848057-b8b432886c094e6894aeb6ba393f482a",' \
#                 '"request":{"query":"%s","user_id":"88888"},"SYS_REMEMBERED_SKILLS":"1057","bot_id":"72147",' \
#                 '"log_id":"4de8dc00-b4d9-11e9-8e8c-e7e03a055294","source":"KEYBOARD","type":"TEXT",' \
#                 '"bot_session":""}' % que
#     new_url = 'https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token=' + access_token
#     req = requests.post(new_url,post_data.encode('utf-8'),headers=headers)
#     res = req.text
#     if (res):
#         res = json.loads(res)
#         print(res.get("result").get("response").get("action_list")[0].get("say"))
