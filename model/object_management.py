import re
import copy
from model.map_object import MapObject
from model.data_access_object import DataAccess
from model.background import MapBackground
from collections import OrderedDict

class ObjectsManagement(DataAccess):
    def __init__(self, map_name):
        self.map_objects = {}
        self.deleted_objects = []
        self.map_background = None
        self.deleted_background = None
        self.map_name = map_name
        self.max_id = 0

        self.update_id = set()
        self.add_id = set()
        #self.delete_id = set()

        self.loadObjects()
        self.loadBackground()


    def loadObjects(self):
        object_model = self.viewData('ObjectGraphic')
        description_model = self.viewData('ObjectDescription')
        for i in range(len(object_model)):
            object_id = object_model[i][0]
            if object_id > self.max_id:
                self.max_id = object_id
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
            x = background_model[i][1]
            y = background_model[i][2]
            rate = background_model[i][3]
            self.map_background = MapBackground( pic_name, rate, x, y)

    def renameObject(self, object_id, new_name):
        if not isinstance(new_name, str):
            raise TypeError("the name should be str")
        if new_name is '':
            raise ValueError("name is empty")
        if len(new_name) > 10:
            raise ValueError("name should be less then 10 char")

        targetObject = self.getObjectById(object_id)
        targetObject.object_name = new_name

        self.update_id.add(object_id)
        #self.accessDataBase(targetObject.generateSqlForRename())

    def changeDescription(self, object_id, description):
        if not isinstance(description, str):
            raise TypeError("the name should be str")
        if description is '':
            raise ValueError("description is empty")
        if len(description) > 100:
            raise ValueError("description should be less then 100 char")
        targetObject = self.getObjectById(object_id)
        targetObject.description = description
        self.update_id.add(object_id)
        #self.accessDataBase(targetObject.generateSqlForChangeDescription())

    def updatePosition(self, object_id, x, y):
        if not isinstance(x,int) and not isinstance(y,int):
            if not isinstance(x, float) and not isinstance(y, float):
                raise ValueError("position should be int or float")
        targetObject = self.getObjectById(object_id)
        targetObject.x = float(x)
        targetObject.y = float(y)
        self.update_id.add(object_id)
        #self.accessDataBase(targetObject.generateSqlForUpdatePosition())

    def createNewObject(self, type_name, x, y):
        object_name = re.sub('^type','',type_name) + '_unnamed'
        mapObject = MapObject(self.max_id+1, object_name, type_name, x, y)

        #self.accessDataBase(mapObject.generateSqlForAdd())
        #object_id = int(self.accessDatabaseforId('ObjectGraphic'))
        #mapObject.object_id = object_id
        #self.accessDataBase(mapObject.generateSqlForAddDiscription())

        self.map_objects[mapObject.object_id] = mapObject
        self.max_id += 1
        self.add_id.add(mapObject.object_id)

        return mapObject.object_id


    def addBackground(self, pic_name, rate, x=0, y=0):
        if not self.map_background is None:
            self.removeBackground()
        self.map_background = MapBackground( pic_name, rate, x, y)

    def removeBackground(self):
        #self.accessDataBase(self.map_background.generateSqlForDelete())
        self.deleted_background = copy.deepcopy(self.map_background)
        self.map_background = None

    def removeObjectById(self, object_id):
        targetObject = self.getObjectById(object_id)
        type_name = targetObject.object_type_name
        self.deleted_objects.append(copy.deepcopy(self.map_objects[object_id]))
        del self.map_objects[object_id]

        if object_id in self.add_id:
            self.add_id.remove(object_id)
        elif object_id in self.update_id:
            self.update_id.remove(object_id)
        return type_name

    def clearAllObject(self):
        self.map_objects.clear()
        self.map_background = None

    def getObjectById(self, object_id):
        if not isinstance(object_id, int):
            raise TypeError("the id should be int")
        if not object_id in self.map_objects:
            raise KeyError("can't find id")
        return self.map_objects[object_id]

    def saveToDB(self):
        for object_id in self.add_id:
            target_object = self.getObjectById(object_id)
            self.accessDataBase(target_object.generateSqlForAdd())
            self.accessDataBase(target_object.generateSqlForAddDiscription())

        for object_id in self.update_id:
            target_object = self.getObjectById(object_id)
            self.accessDataBase(target_object.generateSqlForUpdatePosition())
            self.accessDataBase(target_object.generateSqlForChangeDescription())
            self.accessDataBase(target_object.generateSqlForRename())

        for map_object in self.deleted_objects:
            self.accessDataBase(map_object.generateSqlForDelete())
            self.accessDataBase(map_object.generateSqlForDeleteDescription())

        if self.map_background:
            self.accessDataBase(self.map_background.generateSqlForDelete())
            self.accessDataBase(self.map_background.generateSqlForAdd())
            self.accessDataBase(self.map_background.generateSqlForUpdate())
        else:
            if self.deleted_background:
                self.accessDataBase(self.deleted_background.generateSqlForDelete())

        self.clearTempSet()

    def clearTempSet(self):
        self.add_id.clear()
        self.update_id.clear()
        self.deleted_objects.clear()
        self.deleted_background = None

    def collectData(self):
        objects = []
        if self.map_background:
            background_data = self.map_background.serialize()
        else:
            background_data = OrderedDict([('pic_name','None')])

        for map_object in self.map_objects.values():
            objects.append(map_object.serialize())

        return OrderedDict([
                ('background', background_data),
                ('map_objects', objects)
            ])


