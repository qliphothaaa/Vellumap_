from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
#the main object for map object
class MapBackground():
    def __init__(self, pic_name, rate=1.0, x = 0, y = 0):
        self.pic_name = pic_name
        self.rate = rate
        self.x = x
        self.y = y
        self.setPixmap()

    def setPixmap(self):
        self.path_name = './pic/' + self.pic_name
        reader = QImageReader(self.path_name)
        self.size = reader.size() * self.rate

    '''
    def __str__(self):
        return (self.pic_name + ' ' + str(self.rate) + ' ' + str(self.x) + ' ' + str(self.y))
    '''


    def generateSqlForAdd(self):
        sql = "insert into background values ('%s',%e, %e, %e);" % (self.pic_name, self.x, self.y, self.rate)
        return sql

    def generateSqlForUpdate(self):
        sql = "Update background set x = %e, y = %e, size_rate = %e where (name = '%s');" % (self.x, self.y, self.rate, self.pic_name)
        return sql

    def generateSqlForDelete(self):
        sql = "Delete from background where(name = '%s');" % self.pic_name
        return sql



if __name__ == "__main__":
    mb = MapBackground('test')
    mb.setPixMapFromStorage('full')



