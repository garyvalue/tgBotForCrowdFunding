def reReply(reply:str, status:bool) -> str:
    if status:
        return '执行成功，%s' % reply
    else:
        return '执行失败，%s' % reply

def isError(rep):
    # Todo 报错信息转发给主人
    pass