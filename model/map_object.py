from model.data_serialize_object import DataSerialize
from collections import OrderedDict

class MapObject(DataSerialize):
    def __init__(self, object_id, object_name, object_type_name, x, y, description='nothing'):
        super().__init__()
        self.object_id = object_id
        self.object_name = object_name
        self.object_type_name = object_type_name

        self.x = x
        self.y = y
        self.description = description

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError('the description should be string')
        if len(value)>100:
            raise ValueError('description too long')
        self._description = value
    
    @property
    def object_type_name(self):
        return self._object_type_name
    @object_type_name.setter
    def object_type_name(self, value):
        if not isinstance(value, str):
            raise TypeError('the type_name should be string')
        self._object_type_name = value
    
    @property
    def object_id(self):
        return self._object_id
    @object_id.setter
    def object_id(self, value):
        if not isinstance(value, int):
            raise TypeError('the id should be int')
        self._object_id = value

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        if not isinstance(value, float):
            raise TypeError('the x should be float')
        self._x = value

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        if not isinstance(value, float):
            raise TypeError('the y should be float or float')
        self._y = value



    def getPosition(self):
        return (self.x, self.y)

    def getObjectInfo(self):
        object_id = self.object_id
        name = self.object_name
        type_name = self.object_type_name
        x = self.x
        y = self.y
        description = self.description
        return (object_id, name, type_name, x, y, description)



    def generateSqlForRename(self):
        sql = "Update ObjectGraphic set Name = '%s' where (id = %d);" % (self.object_name, self.object_id)
        return sql

    def generateSqlForChangeDescription(self):
        sql = "Update ObjectDescription set Description = '%s' where (id = %d);" % (self.description, self.object_id)
        return sql

    def generateSqlForUpdatePosition(self):
        sql = "Update ObjectGraphic set X = %e, y = %e where (id = %d);" % (self.x, self.y, self.object_id)
        return sql

    def generateSqlForAdd(self):
        sql = "insert into ObjectGraphic values (%d, '%s', %e, %e, '%s');" % (self.object_id, self.object_name, self.x, self.y, self.object_type_name)
        return sql

    def generateSqlForAddDiscription(self):
        sql = "insert into ObjectDescription values (%d, '%s');" % (self.object_id, self.description)
        return sql

    def generateSqlForDelete(self):
        sql = "Delete from ObjectGraphic where(id = %d);" % self.object_id
        return sql

    def generateSqlForDeleteDescription(self):
        sql = "Delete from ObjectDescription where(id = %d);" % self.object_id
        return sql

    def serialize(self):
        return OrderedDict([
                ('id', self.id),
                ('object_id', self.object_id),
                ('name', self.object_name),
                ('type', self.object_type_name),
                ('x', self.x),
                ('y', self.y),
                ('description', self.description)
            ])


    def deserialize(self, data, hashmap={}):
        raise NotImplemented()

    

        
