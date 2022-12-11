import json
import os

import socks
from telethon import TelegramClient


class myClient:
    def __init__(self, config: dict):
        self.api_id = config.get('api_id')
        self.api_hash = config.get('api_hash')
        self.bot_token = config.get('bot_token')
        self.master = config.get('master')
        self.proxy_port = config.get('proxy_port')
        if self.proxy_port is not None:
            self.client = TelegramClient('anon', self.api_id, self.api_hash,
                                         proxy=(socks.SOCKS5, 'localhost', self.proxy_port)).start(
                bot_token=self.bot_token)
        else:
            self.client = TelegramClient('anon', self.api_id, self.api_hash).start(bot_token=self.bot_token)

filePath = os.path.dirname(os.path.abspath(__file__))
FatherPath = os.path.abspath(os.path.join(filePath, ".."))
config_path = os.path.join(FatherPath, 'config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)
priClient = myClient(config)