#from PyQt5.QtSql import *
import sys
import sqlite3
DEBUG = False
class DataAccess():
    def __init__(self):
        self.map_name = ''

    #read database return model

    def viewData(self, table_name):
        conn = sqlite3.connect('./db/%s.db' % self.map_name)
        cur = conn.cursor()
        sql = "select * from %s" % (table_name)
        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        conn.close()
        return result


    def accessDataBase(self, sql):
        conn = sqlite3.connect('./db/%s.db' % self.map_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()



    def accessDatabaseforId(self, table_name):
        conn = sqlite3.connect('./db/%s.db' % self.map_name)
        cur = conn.cursor()
        sql = "select seq from sqlite_sequence where name='%s'" % table_name
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()
        conn.close()
        return result[0][0]



if __name__ == '__main__':
    db = DataAccess()
    db.map_name = 'newMap'
    re = db.viewData('type')
    print(re)



           
