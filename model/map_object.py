from model.map_graphics_object import QMapGraphicsObject
from model.data_access_object import DataAccess
DEBUG = False
#the main object for map object
class MapObject(DataAccess):
    def __init__(self, map_name, object_type, object_name, is_create=True):

        self.id = None
        self.object_name = object_name
        self.x = 0
        self.y = 0
        self.object_type = object_type
        self.size = 1

        self.map_name = map_name
        self.is_create = is_create
        self.tableName = 'ObjectGraphic'

        #add grpahic to graphic scene
        self.grMapObject = QMapGraphicsObject(self, *(object_type.getAttribute()))

        self.object_type.addMapObjectConnection(self)

        #add self data to database
        if is_create:
            self.accessDataBase(self.generateSqlForAdd())
            self.id = int(self.accessDatabaseforId(self.tableName))

    def __str__(self):
        return ('<object: %s, %s >' % (self.object_name, self.object_type))

        
    def getMapInfo(self):
        if DEBUG: print('OBJECT: get object info')
        id = self.getId()
        name = self.object_name
        type_name = self.object_type.getName()
        width = str(self.object_type.getSize()[0])
        height = str(self.object_type.getSize()[1])
        position = self.getPosition()
        size = self.size
        return (id, name, type_name, width, height, *position, size)

    def updateGr(self, color, shape, width, height):
        self.grMapObject.setColor(color)
        self.grMapObject.setShape(shape)
        self.grMapObject.setWidth(width)
        self.grMapObject.setHeight(height)


    def remove(self):
        if DEBUG: print('OBJECT: remove object it self')
        self.grMapObject = None
        self.object_type.removeMapObjectConnection(self)
        self.accessDataBase(self.generateSqlForDelete())

    def getPosition(self):
        if DEBUG: print('OBJECT: get position of object')
        self.x = self.grMapObject.scenePos().x()
        self.y = self.grMapObject.scenePos().y()
        return (self.x,self.y)

    def updatePosition(self, x, y):
        if DEBUG: print('OBJECT: update position of object')
        self.accessDataBase(self.generateSqlForUpdatePosition(x,y))

    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.grMapObject.setPos(x, y)

    def setName(self, name):
        if DEBUG: print('OBJECT: new name to the object:(%s)'%name)
        self.accessDataBase(self.generateSqlForRename(name))
        self.object_name = name

    def getName(self):
        if DEBUG: print('OBJECT: get name of object')
        return self.object_name

    def setId(self, objectId):
        self.id = objectId

    def getId(self):
        return self.id

    def generateSqlForRename(self, name):
        if DEBUG: print('OBJECT: connect to database, op:update Name:%s'%name)
        sql = "Update ObjectGraphic set Name = '%s' where (id = '%d');" % (name, self.id)
        return sql

    def generateSqlForAdd(self):
        if DEBUG: print('OBJECT: connect to database, op:add object')
        sql = "insert into ObjectGraphic values (null,'%s',%e, %e,'%s',%e);" % (self.object_name, *(self.getPosition()), self.object_type.type_name, 1.0)
        return sql

    def generateSqlForDelete(self):
        if DEBUG: print('OBJECT: connect to database, op:delete object')
        sql = "Delete from ObjectGraphic where(id = '%s');" % self.id
        return sql

    def generateSqlForUpdatePosition(self,x,y):
        if DEBUG: print('OBJECT: connect to database, op:update position')
        sql = "Update ObjectGraphic set X = %e, y = %e where (id = '%s');" % (x, y, self.id)
        return sql


