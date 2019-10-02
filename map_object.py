from map_graphics_object import QMapGraphicsObject
from data_access_object import DataAccess
DEBUG = False
#the main object for map object
class MapObject(DataAccess):
    def __init__(self, mapName, objectType, objectName, isCreate=True):

        self.id = None
        self.objectName = objectName
        self.x = 0
        self.y = 0
        self.objectType = objectType
        self.size = 1

        self.mapName = mapName
        self.isCreate = isCreate
        self.tableName = 'ObjectGraphic'

        #add grpahic to graphic scene
        self.grMapObject = QMapGraphicsObject(self, *(objectType.getAttribute()))

        self.objectType.addMapObjectConnection(self)

        #add self data to database
        if isCreate:
            self.accessDataBase(self.generateSqlForAdd())
            self.id = int(self.accessDatabaseforId(self.tableName))

    def __str__(self):
        return ('<object: %s, %s >' % (self.objectName, self.objectType))

        
    def getMapInfo(self):
        if DEBUG: print('OBJECT: get object info')
        id = self.getId()
        name = self.objectName
        typeName = self.objectType.getName()
        width = str(self.objectType.getSize()[0])
        height = str(self.objectType.getSize()[1])
        position = self.getPosition()
        size = self.size
        return (id, name, typeName, width, height, *position, size)

    def updateGr(self, color, shape, width, height):
        self.grMapObject.setColor(color)
        self.grMapObject.setShape(shape)
        self.grMapObject.setWidth(width)
        self.grMapObject.setHeight(height)


    def remove(self):
        if DEBUG: print('OBJECT: remove object it self')
        self.grMapObject = None
        self.objectType.removeMapObjectConnection(self)
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
        self.objectName = name

    def getName(self):
        if DEBUG: print('OBJECT: get name of object')
        return self.objectName

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
        sql = "insert into ObjectGraphic values (null,'%s',%e, %e,'%s',%e);" % (self.objectName, *(self.getPosition()), self.objectType.typeName, 1.0)
        return sql

    def generateSqlForDelete(self):
        if DEBUG: print('OBJECT: connect to database, op:delete object')
        sql = "Delete from ObjectGraphic where(id = '%s');" % self.id
        return sql

    def generateSqlForUpdatePosition(self,x,y):
        if DEBUG: print('OBJECT: connect to database, op:update position')
        sql = "Update ObjectGraphic set X = %e, y = %e where (id = '%s');" % (x, y, self.id)
        return sql


