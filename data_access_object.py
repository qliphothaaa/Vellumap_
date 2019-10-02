from PyQt5.QtSql import *
import sys
DEBUG = True
class DataAccess():
    def __init__(self):
        pass

    #read database return model
    def viewData(self, tableName):
        if DEBUG: print('try to access database, R')
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()
        model = QSqlTableModel()
        model.setTable(tableName)
        model.select()
        return model

    #operation to change database
    def accessDataBase(self,sql):
        if DEBUG: print('try to access database, CUD')
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()
        query = QSqlQuery()
        try: 
            query.exec_(sql)
        except:
            print("Sql error in cud: ", sys.exc_info()[0])
        db.commit()


    def accessDatabaseforId(self, tableName):
        if QSqlDatabase.contains('qt_sql_default_connection'):
            db = QSqlDatabase.database('qt_sql_default_connection')
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/%s.db' % self.mapName)
            db.open()
        sql = "select seq from sqlite_sequence where name='%s'" % tableName
        query = QSqlQuery()
        try:
            query.exec_(sql)
            query.next()
        except:
            print("Sql error find id: ", sys.exc_info()[0])

        return query.value(0)






           
