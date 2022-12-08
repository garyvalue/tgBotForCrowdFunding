from tools import execSql

db = execSql.ReadSQL()


def addItem(args: list, user_id: str) -> (str, bool):
    # 增加众筹 <tltle> <link> <money> <datetime>
    if len(args) < 4:
        return '参数不足', False
    title = args[0]
    link = args[1]
    money = args[2]
    if not (0 < float(money) < 100) or ('.' in money and len(money.split('.')[-1]) > 2):
        return '金额异常，超出范围（0~999.99）', False
    datetime = args[3]

    _id = db.getId(link)
    if _id != 0:
        # Todo 如果不是本人添加，自动上车
        return '已添加过相同资源，编号为%s' % _id, False
    status, rep = db.insertItem(title, link, user_id, money, datetime)
    if not status:
        # Todo 报错信息转发给主人
        return rep, False
    return '编号为%s' % db.getId(link), True
