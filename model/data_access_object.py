#from PyQt5.QtSql import *
import sys
import sqlite3
DEBUG = False
class DataAccess(object):
    def __init__(self):
        self.id = id(self)

    #read database return model

    def viewData(self, table_name):
        conn = sqlite3.connect('./db/%s.db' % self.map_name)
        cur = conn.cursor()
        result = ''

        try:
            sql = "select * from %s" % (table_name)
            cur.execute(sql)
            result = cur.fetchall()
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            print('fail to access database, rollback now')
            conn.rollback()
        cur.close()
        conn.close()
        return result


    def accessDataBase(self, sql, attr):
        conn = sqlite3.connect('./db/%s.db' % self.map_name)
        cur = conn.cursor()
        try:
            cur.execute(sql, attr)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
            print('fail to access database, rollback now')
            conn.rollback()
        cur.close()
        conn.close()

    def serialize(self):
        raise NotImplemented()


    def deserialize(self, data, hashmap={}):
        raise NotImplemented()



if __name__ == '__main__':
    db = DataAccess()
    db.map_name = 'newMap'
    re = db.viewData('type')
    print(re)



           
