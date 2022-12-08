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
            self.cur.execute(const.createSql)
            self.conn.commit()

    # 发起众筹，返回值分别为执行状态和异常原因
    def insertItem(self, title: str, link: str, author: str, money: str, date: str) -> (bool, str):
        try:
            self.cur.execute(const.insertSql % (title, link, author, money, date, 0))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return False, repr(e)
        except sqlite3.OperationalError as e:
            return False, repr(e)
        return True, None

    def getId(self, link: str):
        self.cur.execute('select id from "item" where link="%s"' % link)
        rep = self.cur.fetchone()
        if rep is not None:
            return rep[0]
        else:
            return 0

    def getMaxId(self) -> int:
        self.cur.execute('select max(id) from "91hot"')
        return self.cur.fetchone()[0]

    def closeDb(self):
        self.conn.commit()
        self.conn.close()
        return


if __name__ == '__main__':
    test = ReadSQL('./data/data.db')
    test.getMaxId()
    test.closeDb()
