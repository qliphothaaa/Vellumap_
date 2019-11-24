from model.data_serialize_object import DataSerialize
from collections import OrderedDict

#the main object for map object
class MapBackground():
    def __init__(self, pic_name, rate=1.0, x = 0, y = 0):
        self.pic_name = pic_name
        self.rate = rate
        self.x = x
        self.y = y
        self.path_name = './pic/' + self.pic_name

    @property
    def pic_name(self):
        return self._pic_name
    @pic_name.setter
    def pic_name(self, value):
        if '.jpg' not in value:
            raise ValueError('cannot find the pic')
        self._pic_name = value

    @property
    def rate(self):
        return self._rate
    @rate.setter
    def rate(self, value):
        if not isinstance(value, float):
            raise TypeError('rate should be float')
        self._rate = value

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        if not isinstance(value, float):
            raise TypeError('position should be float')
        self._x = value

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        if not isinstance(value, float):
            raise TypeError('position should be float')
        self._y = value



    def generateSqlForAdd(self):
        sql = "insert into background values ('%s',%e, %e, %e);" % (self.pic_name, self.x, self.y, self.rate)
        return sql

    def generateSqlForUpdate(self):
        sql = "Update background set x = %e, y = %e, size_rate = %e where (name = '%s');" % (self.x, self.y, self.rate, self.pic_name)
        return sql

    def generateSqlForDelete(self):
        #sql = "Delete from background where(name = '%s');" % self.pic_name
        sql = "Delete from background ;"
        return sql

    def serialize(self):
        return OrderedDict([
                    ('pic_name', self.pic_name),
                    ('rate', self.rate),
                    ('x', self.x),
                    ('y', self.y)
                    ])


    def deserialize(self, data, hashmap={}):
        raise NotImplemented()



if __name__ == "__main__":
    mb = MapBackground('test')
    mb.setPixMapFromStorage('full')



