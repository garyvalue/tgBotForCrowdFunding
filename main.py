import time

import telethon.tl.types as tgType
from telethon import events

import tools.tool
from tools import onMessage
from tools.myLogging import FrameLog
from tools.tgClient import priClient

# 配置处理开始
# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

client = priClient.client
log = FrameLog().log()
# 用于记录用户上一次操作时间
timeMap = {}


# 配置处理结束


# 展示登陆的信息
def show_my_inf(me):
    log.info(f"-----****************-----\nName:{me.username}\nId:{me.id}\n-----login successful-----")


async def client_main():
    log.debug("-client-main-")
    me = await client.get_me()
    show_my_inf(me)
    entity = await client.get_entity(priClient.master)
    await client.send_message(entity, 'Hello,my master')
    await client.run_until_disconnected()


# 返回值为本次操作与上次操作的时间间隔
def canContinue(user_id) -> (bool, int):
    nowTime = int(time.time())
    lastTime = timeMap.get(user_id, 0)
    if lastTime == 0:
        timeMap[user_id] = nowTime
        return True, 0
    else:
        diffTime = nowTime - lastTime
        if diffTime <= 1:
            return False, 1 - diffTime
        else:
            timeMap[user_id] = nowTime
            return True, 0


# 指令统一处理
async def notifyFinish(args: list, userList: list):
    _id = args[0]
    link = args[1]
    pwd = args[2]
    password = args[3]
    strReply = f'编号{_id}已发车\n链接：{link}\n提取码：{pwd}\n密码：{password}'
    for user in userList:
        entity = await client.get_entity(user)
        await client.send_message(entity, strReply)


async def onAction(text: str, user_id: str) -> str:
    status, waitTime = canContinue(user_id)
    log.info(f'用户{user_id}执行指令：{text} 放行：{status}')
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
        # Todo 批量发车
        # 返回所有上车用户
        if status:
            userList = onMessage.getAllJoinById(fullCmd[1:])
            await notifyFinish(fullCmd[1:], userList)
    elif cmd == '#我发起的众筹':
        reply, status = onMessage.getAllItem(fullCmd[1:], user_id)
    elif cmd == '#参加众筹' or cmd == '#参与众筹':
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
        reply, status = await onMessage.getItemByWd(fullCmd[1:], limit)
    elif cmd == '#查询链接':
        reply, status = onMessage.getUrlByid(fullCmd[1:])
    return tools.tool.reReply(reply, status, user_id)


@client.on(events.NewMessage())
async def event_handler(event):
    # 获取message内容
    raw_text = event.message.message
    if raw_text.find('#') == 0 or raw_text.find('/') == 0:
        log.debug(f'接到消息：{event.message}')
        # 判断消息来源是群组还是私聊
        isPrivate = True
        if type(event.message.peer_id) == tgType.PeerChannel:
            isPrivate = False
        if isPrivate:
            user_id = str(event.message.peer_id.user_id)
        else:
            user_id = str(event.message.from_id.user_id)
        if raw_text == '#帮助' or raw_text == '/help':
            await event.reply('https://telegra.ph/%E6%8C%87%E4%BB%A4%E8%AF%B4%E6%98%8E-12-10')
            return
        replyMsg = await onAction(raw_text, user_id)
        await event.reply(replyMsg)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(client_main())
