from model.new_map_object import MapObject
from model.data_access_object import DataAccess

class ObjectsManagement(DataAccess):
    def __init__(self, map_name):
        self.map_objects = {}
        self.map_name = map_name
        self.loadObjects()


    def loadObjects(self):
        object_model = self.viewData('ObjectGraphic')
        description_model = self.viewData('ObjectDescription')
        for i in range(object_model.rowCount()):
            object_id = object_model.record(i).value('id')
            object_name = object_model.record(i).value('name')
            object_type_name = object_model.record(i).value('type')
            object_x = object_model.record(i).value('x')
            object_y = object_model.record(i).value('y')
            description = description_model.record(i).value('description')
            mapObject = MapObject(object_id, object_name, object_type_name, object_x, object_y, description)
            self.map_objects[object_id] = mapObject


    def renameObject(self, object_id, new_name):
        targetObject = self.map_objects[object_id]
        targetObject.object_name = new_name
        self.accessDataBase(targetObject.generateSqlForRename(new_name))

    def changeDescription(self, object_id, description):
        targetObject = self.map_objects[object_id]
        targetObject.description = description
        self.accessDataBase(targetObject.generateSqlForChangeDescription(description))

    def updatePosition(self, object_id, x, y):
        targetObject = self.map_objects[object_id]
        targetObject.x = x
        targetObject.y = y
        self.accessDataBase(targetObject.generateSqlForUpdatePosition())

    def createNewObject(self, type_name, x, y):
        object_name = re.sub('^type','',type_name) + '_unnamed'
        mapObject = MapObject(-1, object_name, type_name, x, y)
        self.accessDataBase(mapObject.generateSqlForAdd())
        object_id = int(self.accessDatabaseforId('ObjectGraphic'))
        mapObject.object_id = object_id
        self.accessDatabaseforId(mapObject.generateSqlForAddDiscription())
        self.map_objects[object_id] = mapObject

    def removeObjectById(self, object_id):
        targetObject = self.map_objects[object_id]
        self.accessDataBase(targetObject.generateSqlForDelete())
        self.accessDataBase(targetObject.generateSqlForDeleteDescription())
        del self.map_objects[object_id]

    def removeAll(self):
        self.map_objects.clear()

    def getObjectById(self, object_id):
        return self.map_objects[object_id]
