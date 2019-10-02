from PyQt5.QtSql import *
import sys
DEBUG = False
class DataAccess():
    def __init__(self):
        pass

    #read database return model
    def viewData(self, table_name):
        if DEBUG: print('try to access database, R')
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

    #operation to change database
    def accessDataBase(self,sql):
        if DEBUG: print('try to access database, CUD')
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






           
