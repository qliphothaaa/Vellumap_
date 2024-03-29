from model.data_serialize_object import DataSerialize
from model.change_pic import imageToStr
from collections import OrderedDict

#the main object for map object
class MapBackground():
    def __init__(self, pic_name, rate=1.0, x = 0.0, y = 0.0, pic_str=''):
        self.pic_name = pic_name
        self.rate = rate
        self.x = x
        self.y = y
        self.path_name = './pic/' + self.pic_name
        if pic_str =='':
            self.pic_str = imageToStr(self.path_name)
        else:
            self.pic_str = pic_str

    ###############################getter and setter
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



    ################method sql
    def generateSqlForAdd(self):
        sql = "insert into background values (?, ?, ?, ?, ?);"  
        return (sql,(self.pic_name, self.x, self.y, self.rate, self.pic_str))

    def generateSqlForUpdate(self):
        sql = "Update background set x = ?, y = ?, size_rate = ? where (name = ?);"  
        return (sql,(self.x, self.y, self.rate, self.pic_name))

    def generateSqlForDelete(self):
        #sql = "Delete from background where(name = '%s');" % self.pic_name
        sql = "Delete from background;"
        return sql


    ################method serialize
    def serialize(self):
        return OrderedDict([
                    ('pic_name', self.pic_name),
                    ('rate', self.rate),
                    ('x', self.x),
                    ('y', self.y),
                    ('pic_str', self.pic_str)
                    ])


    def deserialize(self, data):
        self.pic_name = data['pic_name']
        self.rate = data['rate']
        self.x = data['x']
        self.y = data['y']
        self.pic_str = data['pic_str']

    ################end


if __name__ == "__main__":
    mb = MapBackground('test')
    mb.setPixMapFromStorage('full')



