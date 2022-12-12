from tools import execSql, tool
from tools.tgClient import priClient

client = priClient.client
db = execSql.ReadSQL()


def addItem(args: list, user_id: str) -> (str, bool):
    # 增加众筹 <title> <link> <money> <datetime>
    if len(args) < 4:
        return '参数不足', False
    title = args[0]
    link = args[1]
    money = args[2]
    if not (0 < float(money) < 100) or ('.' in money and len(money.split('.')[-1]) > 2):
        return '金额异常，超出范围（0~999.99）', False
    datetime = args[3]
    _id = db.getIdFromSponsor(link)
    if _id != 0:
        if checkAuth(_id, user_id):
            return '已添加过相同资源，编号为%s' % _id, False
        else:
            db.joinItem(_id, user_id)
            return '该资源已由他人发起众筹，已为你自动参与', True
    status, rep = db.insertItem(title, link, user_id, money, datetime)
    if not status:
        tool.isError(rep, args)
        return '未知错误，已通知管理员', False
    return '编号为%s' % db.getIdFromSponsor(link), True


def delItem(args: list, user_id: str):
    if len(args) < 1:
        return '参数不足', False
    _id = args[0]
    if not checkAuth(_id, user_id):
        return '非法权限', False
    else:
        status, rep = db.delSponsor(_id)
        if not status:
            tool.isError(rep, args)
            return '未知错误，已通知管理员', False
        return '删除成功', True


def finishItem(args: list, user_id: str, cover: bool) -> (str, bool):
    # 发车 <id> <link> <pwd> <password>
    if len(args) < 4:
        return '参数不足', False
    _id = args[0]
    link = args[1]
    pwd = args[2]
    password = args[3]
    if not checkAuth(_id, user_id):
        return '非法权限', False
    # 校验是否已发车
    IsFinish = db.isFinish(_id)
    if not cover and IsFinish:
        return '该资源已发车，如需修改，请使用 #强制发车 ', False
    status, rep = db.toFinish(_id, link, pwd, password, cover and IsFinish)
    if not status:
        tool.isError(rep, args)
        return '未知错误，已通知管理员', False
    return '发车成功', True


def getAllItem(args: list, user_id: str) -> (str, bool):
    limit = '10'
    if len(args) > 1:
        limit = args[0]
    itemList = db.getAllFromSponsor(user_id, limit)
    if len(itemList) == 0:
        return '未查询到你发起的众筹', False
    else:
        rep = ''
        for item in itemList:
            title = item[0]
            _id = item[1]
            rep += '\n%s 编号%s' % (title, _id)
        return rep, True


def checkAuth(_id: str, user_id: str) -> bool:
    # 校验操作者权限
    user = db.getUserFromSponsor(_id)
    return user == user_id or user_id == priClient.master


def joinItem(args: list, user_id: str):
    if len(args) < 1:
        return '参数不足', False
    _id = args[0]
    if checkAuth(_id, user_id):
        return '你是发起者，无需参与众筹', False
    status, rep = db.joinItem(_id, user_id)
    if not status:
        tool.isError(rep, args)
        return '未知错误，已通知管理员', False
    return '参加成功', True


def exitItem(args: list, user_id: str):
    if len(args) < 1:
        return '参数不足', False
    _id = args[0]
    # 已发车的众筹不允许退出
    status = int(db.getStatusById(_id))
    if status:
        return '已发车的众筹不允许退出', False
    status, rep = db.exitItem(_id, user_id)
    if not status:
        tool.isError(rep, args)
        return '未知错误，已通知管理员', False
    return '退出成功', True


def getAllJoin(args: list, user_id: str):
    limit = '10'
    if len(args) > 1:
        limit = args[0]
    itemList = db.getAllFromJoin(user_id, limit)
    if len(itemList) == 0:
        return '未查询到你参与的众筹', False
    else:
        rep = ''
        for item in itemList:
            _id = item[0]
            title = db.getTitleById(_id)
            num = db.getNumById(_id)
            rep += f'\n{title} 编号{_id} 当前参与人数{num}'
        return rep, True


async def getItemByWd(args: list, limit: int) -> (str, bool):
    if len(args) < 1:
        return '参数不足', False
    wd = args[0]
    itemList = db.getItemByWd(wd)
    if len(itemList) == 0:
        return '未查询到符合条件的众筹', False
    else:
        rep = ''
        # TODO 搜索时显示完整信息以及参与人数和预估金额
        for item in itemList:
            title = item[0]
            link = item[1]
            author = await client.get_entity(int(item[2]))
            money = float(item[3])
            fDate = item[4]
            num = int(item[5])
            status = int(item[6])
            if limit is not None and limit == status:
                continue
            strStatus = '未发车'
            if status:
                strStatus = '已发车'
            _id = item[7]
            avgMoney = format(money / num, '.2f')
            rep += f'\n编号{_id} {title} {link} 发起者：#{author.username} 总金额：{money}元 发车日期：{fDate} {strStatus} 上车人数：{num} 预估金额：{avgMoney}'
        return rep, True


def getUrlByid(args: list) -> (str, bool):
    if len(args) < 1:
        return '参数不足', False
    _id = args[0]
    url = db.getUrlById(_id)
    return url, True


def getAllJoinById(args: list) -> list:
    _id = args[0]
    tmpList = db.getAllFromJoinById(_id)
    userList = []
    for item in tmpList:
        userList.append(item[0])
    return userList
