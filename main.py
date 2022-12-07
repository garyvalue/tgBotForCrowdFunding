import json

import socks
from telethon import TelegramClient, events

config_path = './config.json'
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


def onMessage(text: str):
    pass


@client.on(events.NewMessage())
async def event_handler(event):
    await event.reply(event.message.message)


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(client_main())
