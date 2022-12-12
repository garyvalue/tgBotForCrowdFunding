import datetime
import os
import sqlite3

import tools.const as const

db_path = './data/data.db'


class ReadSQL:
    def __init__(self, database=None):
        if not os.path.exists('./data'):
            os.mkdir('./data')
        if database is None:
            database = db_path
        self.database = database
        existDb = os.path.exists(database)
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        if not existDb:
            self.cur.execute(const.createSqlSponsor)
            self.cur.execute(const.createSqlFinish)
            self.cur.execute(const.createSqlJoin)
            self.conn.commit()

    # 发起众筹，返回值分别为执行状态和异常原因
    def insertItem(self, title: str, link: str, author: str, money: str, date: str) -> (bool, str):
        try:
            self.cur.execute(const.insertSponsorSql % (title, link, author, money, date, 0))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return False, repr(e)
        except sqlite3.OperationalError as e:
            return False, repr(e)
        return True, None

    def getIdFromSponsor(self, link: str):
        self.cur.execute('select id from "sponsor" where link="%s"' % link)
        rep = self.cur.fetchone()
        if rep is not None:
            return rep[0]
        else:
            return 0

    def getUserFromSponsor(self, _id: str):
        self.cur.execute('select author from "sponsor" where id="%s"' % _id)
        rep = self.cur.fetchone()
        if rep is not None:
            return rep[0]
        else:
            return '0'

    def delSponsor(self, _id):
        try:
            self.cur.execute(const.delSponsorSql % _id)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return False, repr(e)
        except sqlite3.OperationalError as e:
            return False, repr(e)
        return True, None

    def getAllFromSponsor(self, user_id: str, limit: int) -> list:
        self.cur.execute(
            'select title,id from "sponsor" where author="%s" order by id desc limit "%s"' % (user_id, limit))
        rep = self.cur.fetchall()
        if rep is None:
            return []
        else:
            return rep

    def isFinish(self, _id):
        self.cur.execute('select * from "finish" where id="%s"' % _id)
        rep = self.cur.fetchone()
        if rep is not None:
            return True
        else:
            return False

    def toFinish(self, _id: str, link: str, pwd: str, password: str, cover: bool):
        try:
            if not cover:
                self.cur.execute(
                    const.insertFinishSql % (_id, link, pwd, password, datetime.datetime.now().strftime("%Y-%m-%d")))
                self.cur.execute(const.finishSponsorSql % _id)
            else:
                self.cur.execute(const.updateFinishSql % (_id, link, pwd, password))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return False, repr(e)
        except sqlite3.OperationalError as e:
            return False, repr(e)
        return True, None

    def delFinish(self, _id):
        try:
            self.cur.execute(const.delFinishSql % _id)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return False, repr(e)
        except sqlite3.OperationalError as e:
            return False, repr(e)
        return True, None

    def joinItem(self, _id: int, user_id: str) -> (bool, str):
        try:
            self.cur.execute(const.joinItemSql % (_id, user_id))
            self.cur.execute(const.setJoinNumSql % (int(self.getNumById(_id)) + 1, _id))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return False, repr(e)
        except sqlite3.OperationalError as e:
            return False, repr(e)
        return True, None

    def exitItem(self, _id: int, user_id: str) -> (bool, str):
        try:
            self.cur.execute(const.exitItemSql % (_id, user_id))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return False, repr(e)
        except sqlite3.OperationalError as e:
            return False, repr(e)
        return True, None

    def getAllFromJoin(self, user_id: str, limit: int) -> list:
        self.cur.execute(
            'select id from "join" where user="%s" order by id desc limit "%s"' % (user_id, limit))
        rep = self.cur.fetchall()
        if rep is None:
            return []
        else:
            return rep

    def getTitleById(self, _id) -> str:
        self.cur.execute(
            'select title from "sponsor" where id="%s"' % _id)
        return self.cur.fetchone()[0]

    def getStatusById(self, _id) -> str:
        self.cur.execute(
            'select status from "sponsor" where id="%s"' % _id)
        return self.cur.fetchone()[0]

    def getNumById(self, _id) -> str:
        self.cur.execute('select count(*) from "join" where id="%s"' % _id)
        return self.cur.fetchone()[0]

    def getItemByWd(self, wd: str):
        strSQl = f'select * from "sponsor" where title like "%{wd}%"'
        self.cur.execute(strSQl)
        rep = self.cur.fetchall()
        if rep is None:
            return []
        else:
            return rep

    def getMaxId(self) -> int:
        self.cur.execute('select max(id) from "91hot"')
        return self.cur.fetchone()[0]

    def closeDb(self):
        self.conn.commit()
        self.conn.close()
        return

    def getUrlById(self, _id) -> str:
        self.cur.execute(f'select link from "sponsor" where id={_id}')
        return self.cur.fetchone()[0]

    def getAllFromJoinById(self, _id) -> list:
        self.cur.execute(f'select user from "finish" where id={_id}')
        return self.cur.fetchall()


if __name__ == '__main__':
    test = ReadSQL('./data/data.db')
    test.getMaxId()
    test.closeDb()
