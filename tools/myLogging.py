# coding = utf-8

import logging
import os
import time


class FrameLog:
    def __init__(self):
        # 创建日志器
        self.logger = logging.getLogger('my')
        # 设置日志输出级别
        self.logger.setLevel(level=logging.DEBUG)
        # 设置日志路径以及日志文件名
        self.log_time = time.strftime('%Y_%m_%d')
        self.log_path = os.getcwd() + '/Logs/'
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        self.log_name = self.log_path + self.log_time + '.log'
        self.format = logging.Formatter(fmt='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s',
                                        datefmt='%Y-%m-%d %H:%M:%S %a')
        self.filter = logging.Filter(name='my')

    def set_filehandler(self):
        # 创建文件处理器
        self.file_handler = logging.FileHandler(self.log_name, mode='a', encoding='utf-8')
        # 处理器设置日志输出级别
        self.file_handler.setLevel(logging.DEBUG)
        # 处理器添加格式器
        self.file_handler.setFormatter(self.format)
        # 添加过滤器
        self.file_handler.addFilter(self.filter)
        # 日志器添加文件处理器
        self.logger.addHandler(self.file_handler)
        # 关闭打开的文件
        self.file_handler.close()

    def set_cmd_handler(self):
        # 创建命令行处理器
        self.cmd_handler = logging.StreamHandler()
        # 处理器设置日志输出级别
        self.cmd_handler.setLevel(logging.DEBUG)
        # 处理器添加格式器
        self.cmd_handler.setFormatter(self.format)
        # 添加过滤器
        self.file_handler.addFilter(self.filter)
        # 日志器添加文件处理器
        self.logger.addHandler(self.cmd_handler)
        # 关闭打开的文件
        self.cmd_handler.close()

    def log(self):
        if not self.logger.handlers:
            self.set_filehandler()
            self.set_cmd_handler()
        # 返回日志器
        return self.logger


if __name__ == '__main__':
    log = FrameLog().log()
    log.info('info')
    log.error('error')
    log.debug('debug')
    log.warning('warning')
    log.critical('严重级别')

    baidu_url = 'https://www.baidu.com/'
    log.info('开始打开百度{}'.format(baidu_url))
    log.info('关闭浏览器')
