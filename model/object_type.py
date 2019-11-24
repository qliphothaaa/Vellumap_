from model.data_serialize_object import DataSerialize
from collections import OrderedDict

class ObjectType(DataSerialize):
    def __init__(self, type_name, color, shape, width, height):
        super().__init__()
        self.type_name = type_name
        self.color = color
        self.shape = shape
        self.width = width
        self.height = height
        self.objects_id_set = set()

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError('the color should be string')
        self._color = value

    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, value):
        if not isinstance(value, str):
            raise TypeError('the shape should be string')
        self._shape = value

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if not isinstance(value, int):
            if not isinstance(value,float):
                raise TypeError('the width should be int or float')
        if value <= 0:
            raise ValueError ("bad value")
        self._width = value

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            if not isinstance(value,float):
                raise TypeError('the height should be int or float')
        if value <= 0:
            raise ValueError("bad value")
        self._height = value



    def getAttribute(self):
        return (self.color, self.shape, self.width, self.height)
    
    def getObjectIdSet(self):
        return self.objects_id_set

    def update(self, color, shape, width, height):
        self.color = color
        self.shape = shape
        self.width = width
        self.height = height

    def addObjectId(self, object_id):
        if isinstance(object_id, int):
            self.objects_id_set.add(object_id)
        else:
            raise TypeError("id should be int")

    def removeObjectId(self, object_id):
        if isinstance(object_id, int):
            if not object_id in self.objects_id_set:
                raise KeyError("can't find id")
            self.objects_id_set.remove(object_id)
        else:
            raise TypeError("id should be int")

    def generateSqlForAdd(self):
        sql = "insert into type values(?, ?, ?, ?, ?)" 
        return (sql,(self.type_name, self.shape, self.color, self.width, self.height))

    def generateSqlForUpdate(self):
        sql = "Update type set Shape = ?, color = ?, width = ?, height = ? where name = ?"  
        return (sql, (self.shape, self.color, self.width, self.height, self.type_name))

    def generateSqlForDelete(self):
        sql = "Delete from type where (name = ?)"  
        return (sql, self.type_name)

    def serialize(self):
        return OrderedDict([
                ('name', self.type_name),
                ('color', self.color),
                ('shape', self.shape),
                ('width', self.width),
                ('height', self.height),
            ])


    def deserialize(self, data, hashmap={}):
        raise NotImplemented()
