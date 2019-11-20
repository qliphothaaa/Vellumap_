import sqlite3
class FakeDB():
    def __init__(self, db_name):
        self.db_name = './db/%s.db' % db_name
        self.result = None

    def viewData(self, result, aim, aim_value ,table_name):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        sql = "select %s from %s where %s = '%s'"% (result, table_name, aim, aim_value)
        #sql = "select * from %s"% (table_name)
        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        conn.close()
        if result == []:
            return result
        else:
            return result[0][0]

    def viewDataAll(self, table_name):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        #sql = "select %s from %s where %s = '%s'"% (result, table_name, aim, aim_value)
        sql = "select * from %s"% (table_name)
        cur.execute(sql)
        result = cur.fetchall()

        conn.commit()
        conn.close()
        if result == []:
            return result
        else:
            return result
        

    def accessDatabase(self, sql):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()


    def clear(self, table_name):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        cur.execute("delete from %s" % table_name)
        conn.commit()
        conn.close()

        


if __name__ == '__main__':
    db = FakeDB('newMap')

