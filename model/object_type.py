from model.data_serialize_object import DataSerialize
from collections import OrderedDict

class ObjectType(DataSerialize):
    def __init__(self, type_name='', color='', shape='', width=1, height=1):
        super().__init__()
        self.type_name = type_name
        self.color = color
        self.shape = shape
        self.width = width
        self.height = height
        self.objects_id_set = set()

    ###############################getter and setter

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        if not isinstance(value, str):
            raise TypeError('color should be string(input:%s)'%value)
        self._color = value

    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self, value):
        if not isinstance(value, str):
            raise TypeError('shape should be string(input:%s)'%value)
        self._shape = value

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if not isinstance(value, int):
            if not isinstance(value,float):
                raise TypeError('width should be int or float(input:%s)'%value)
        if value <= 0:
            raise ValueError ("width should bigger then 0(input:%s)"%value)
        self._width = value

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if not isinstance(value, int):
            if not isinstance(value,float):
                raise TypeError('height should be int or float(input:%s)'%value)
        if value <= 0:
            raise ValueError("height should bigger then 0(input:%s)"%value)
        self._height = value

    ################method

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

    ################method sql

    def generateSqlForAdd(self):
        sql = "insert into type values(?, ?, ?, ?, ?)" 
        return (sql,(self.type_name, self.shape, self.color, self.width, self.height))

    def generateSqlForUpdate(self):
        sql = "Update type set Shape = ?, color = ?, width = ?, height = ? where name = ?"  
        return (sql, (self.shape, self.color, self.width, self.height, self.type_name))

    def generateSqlForDelete(self):
        sql = "Delete from type where (name = ?)"  
        return (sql, self.type_name)

    ################method serialize

    def serialize(self):
        return OrderedDict([
                ('name', self.type_name),
                ('color', self.color),
                ('shape', self.shape),
                ('width', self.width),
                ('height', self.height),
            ])


    def deserialize(self, data):
        self.type_name = data['name']
        self.color = data['color']
        self.shape = data['shape']
        self.width = data['width']
        self.height = data['height']

    ################end
