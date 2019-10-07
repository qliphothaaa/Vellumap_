from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from model.data_access_object import DataAccess
DEBUG = False
#the main object for map object
class MapBackground(DataAccess):
    def __init__(self, picture_name, rate ):
        self.pic_name = picture_name     
        self.rate = rate
        self.path_name = './pic/' + self.pic_name
        reader = QImageReader(self.path_name)
        self.size = reader.size() * self.rate

    def getSize(self):
        return self.size

    def getPathName(self):
        return self.path_name

    def getRate(self):
        return self.rate
        






