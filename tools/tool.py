from tools.myLogging import FrameLog

log = FrameLog().log()


def reReply(reply: str, status: bool, user_id: str) -> str:
    log.debug(f'用户:{user_id} 状态:{status} 结果：{reply}')
    if status:
        return '执行成功，%s' % reply
    else:
        return '执行失败，%s' % reply


def isError(rep: str, args: list):
    log.error(rep, args)
