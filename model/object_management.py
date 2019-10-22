import re
from model.new_map_object import MapObject
from model.data_access_object import DataAccess
from model.map_background import MapBackground

class ObjectsManagement(DataAccess):
    def __init__(self, map_name):
        self.map_objects = {}
        self.map_background = None
        self.map_name = map_name
        self.loadObjects()
        self.loadBackground()


    def loadObjects(self):
        object_model = self.viewData('ObjectGraphic')
        description_model = self.viewData('ObjectDescription')
        for i in range(len(object_model)):
            object_id = object_model[i][0]
            object_name = object_model[i][1]
            object_type_name = object_model[i][4]
            object_x = object_model[i][2]
            object_y = object_model[i][3]
            description = description_model[i][1]
            mapObject = MapObject(object_id, object_name, object_type_name, object_x, object_y, description)
            self.map_objects[object_id] = mapObject

    def loadBackground(self):
        background_model = self.viewData('background')
        for i in range(len(background_model)):
            pic_name = background_model[i][0]
            rate = background_model[i][3]
            x = background_model[i][1]
            y = background_model[i][2]
            self.map_background = MapBackground( pic_name, rate, x, y)




    def renameObject(self, object_id, new_name):
        targetObject = self.map_objects[object_id]
        targetObject.object_name = new_name
        self.accessDataBase(targetObject.generateSqlForRename())

    def changeDescription(self, object_id, description):
        targetObject = self.map_objects[object_id]
        targetObject.description = description
        self.accessDataBase(targetObject.generateSqlForChangeDescription())

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
        self.accessDataBase(mapObject.generateSqlForAddDiscription())
        self.map_objects[object_id] = mapObject
        return object_id

    def addBackground(self, pic_name, rate, x=0, y=0):
        if (self.map_background is None):
            self.map_background = MapBackground( pic_name, rate, x, y)
            self.accessDataBase(self.map_background.generateSqlForAdd())

    def removeBackground(self):
        self.accessDataBase(self.map_background.generateSqlForDelete())
        self.map_background = None

        

    def removeObjectById(self, object_id):
        targetObject = self.map_objects[object_id]
        type_name = targetObject.object_type_name
        self.accessDataBase(targetObject.generateSqlForDelete())
        self.accessDataBase(targetObject.generateSqlForDeleteDescription())
        del self.map_objects[object_id]
        return type_name

    def clearAllObject(self):
        self.map_objects.clear()
        self.map_background = None

    def getObjectById(self, object_id):
        return self.map_objects[object_id]


