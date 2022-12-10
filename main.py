import json
import os
import time

import socks
from telethon import TelegramClient, events

import tools.tool
from tools import onMessage

current_directory = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_directory, 'config.json')

# 配置处理开始
# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)
api_id = config.get('api_id')
api_hash = config.get('api_hash')
bot_token = config.get('bot_token')
master = config.get('master')
proxy_port = config.get('proxy_port')
if proxy_port is not None:
    client = TelegramClient('anon', api_id, api_hash, proxy=(socks.SOCKS5, 'localhost', proxy_port)).start(
        bot_token=bot_token)
else:
    client = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

# 用于记录用户上一次操作时间
timeMap = {}


# 配置处理结束


# 展示登陆的信息
def show_my_inf(me):
    print("-----****************-----")
    print("Name:", me.username)
    print("ID:", me.id)
    print("-----login successful-----")


async def client_main():
    print("-client-main-")
    me = await client.get_me()
    show_my_inf(me)
    entity = await client.get_entity(master)
    await client.send_message(entity, 'Hello,my master')
    await client.run_until_disconnected()


# 返回值为本次操作与上次操作的时间间隔
def canContinue(user_id) -> (bool, int):
    return True, 0
    nowTime = int(time.time())
    lastTime = timeMap.get(user_id, 0)
    if lastTime == 0:
        timeMap[user_id] = nowTime
        return True, 0
    else:
        diffTime = nowTime - lastTime
        if diffTime <= 30:
            return False, 30 - diffTime
        else:
            timeMap[user_id] = nowTime
            return True, 0
    # Todo 限流，根据发车次数减少指令操作间隔


# 指令统一处理
def onAction(text: str, user_id: str) -> str:
    status, waitTime = canContinue(user_id)
    if not status:
        return '还需等待%d秒后才可执行操作' % waitTime
    fullCmd = text.split(' ')
    cmd = fullCmd[0]
    status = False
    reply = '无对应指令'
    if cmd == '#增加众筹':
        reply, status = onMessage.addItem(fullCmd[1:], user_id)
    elif cmd == '#删除众筹':
        reply, status = onMessage.delItem(fullCmd[1:], user_id)
    elif cmd == '#发车' or cmd == '#强制发车':
        reply, status = onMessage.finishItem(fullCmd[1:], user_id, cmd == '#强制发车')
        # Todo 发车成功后，通知所有成员
    elif cmd == '#我发起的众筹':
        reply, status = onMessage.getAllItem(fullCmd[1:], user_id)
    elif cmd == '#参加众筹':
        reply, status = onMessage.joinItem(fullCmd[1:], user_id)
    elif cmd == '#退出众筹':
        reply, status = onMessage.exitItem(fullCmd[1:], user_id)
    elif cmd == '#我参与的众筹':
        reply, status = onMessage.getAllJoin(fullCmd[1:], user_id)
    elif cmd == '#搜索' or cmd == '#搜索已发车' or cmd == '#搜索未发车':
        limit = None
        if cmd == '#搜索已发车':
            limit = 1
        elif cmd == '#搜索未发车':
            limit = 0
        reply, status = onMessage.getItemByWd(fullCmd[1:],limit)
    return tools.tool.reReply(reply, status)


@client.on(events.NewMessage())
async def event_handler(event):
    # 获取message内容
    raw_text = event.message.message
    user_id = str(event.message.peer_id.user_id)
    if raw_text.find('#') == 0 or raw_text.find('/') == 0:
        replyMsg = onAction(raw_text, user_id)
        await event.reply(replyMsg)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(client_main())
