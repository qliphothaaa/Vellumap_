#from PyQt5.QtSql import *
import sys
import sqlite3
DEBUG = False
class DataAccess():
    def __init__(self):
        self.map_name = ''

    #read database return model
    '''
    def viewData(self, table_name):
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.map_name)
            db.open()
        model = QSqlTableModel()
        model.setTable(table_name)
        model.select()
        return model
    '''

    def viewData(self, table_name):
        conn = sqlite3.connect('./db/%s.db' % self.map_name)
        cur = conn.cursor()
        sql = "select * from %s" % (table_name)
        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        conn.close()
        return result


    '''
    #operation to change database
    def accessDataBase(self,sql):
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.map_name)
            db.open()
        query = QSqlQuery()
        try: 
            query.exec_(sql)
        except:
            print("Sql error in cud: ", sys.exc_info()[0])
        db.commit()
    '''
    def accessDataBase(self, sql):
        conn = sqlite3.connect('./db/%s.db' % self.map_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()



    '''
    def accessDatabaseforId(self, table_name):
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.map_name)
            db.open()
        sql = "select seq from sqlite_sequence where name='%s'" % table_name
        query = QSqlQuery()
        try:
            query.exec_(sql)
            query.next()
        except:
            print("Sql error find id: ", sys.exc_info()[0])

        return query.value(0)
    '''
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



           
