from model.map_graphics_scene import QMapGraphicsScene
from model.map_object import MapObject
from model.map_object_type import ObjectType
from model.data_access_object import DataAccess
from model.map_background import MapBackground
from model.map_graphics_background import QMapGraphicsBackground
from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
DEBUG = False
#The main scene that contain all things
class Scene(DataAccess):
    def __init__(self, map_name):
        super().__init__()

        self.object_types = []
        self.objects = []

        self.map_name = map_name
        self.to_create = ''
        self.initUI()
        

    def initUI(self):
        if DEBUG: print('SCENE:init gr_scene')
        self.gr_scene = QMapGraphicsScene(self)
        self.gr_scene.setGrScene(15000, 15000)


        self.loadBackground('yiji.jpg', 10)

    def setTempTypeName(self, type_name):
        if (self.to_create == type_name):
            self.to_create = ''
        else:
            self.to_create = type_name

    def loadBackground(self, pic_name, rate):
        if (pic_name is not ''):
            self.clearObjects()
            self.clearTypes()
            mapBackground = MapBackground(pic_name, rate)
            self.mapBackgroundGraphic = QMapGraphicsBackground(mapBackground.getPathName(), mapBackground.getSize())
            self.gr_scene.addItem(self.mapBackgroundGraphic)
            self.loadType()
            self.loadObject()


    def loadBackgroundFromDatabase(self):
        model = self.viewData('Background')
        pixmap_name = model.record(0).value('name')
        pixmap = model.record(0).value('pic')

    def addObjectConnection(self, obj):
        self.objects.append(obj)

    def removeObjectConnection(self, obj):
        self.objects.remove(obj)

    def addTypeConnection(self, object_type):
        self.object_types.append(object_type)

    def removeTypeConnection(self, object_type):
        self.object_types.remove(object_type)

    def getObjectById(self, object_id):
        if DEBUG: print('SCENE:find object by id')
        for item in self.objects:
            if item.id == object_id:
                return item
        
    def getTypeByName(self, type_name):
        if DEBUG: print('SCENE:find type by name')
        for object_type in self.object_types:
            if object_type.type_name == type_name:
                return object_type
        

    def removeObjectById(self, object_id):
        if DEBUG: print('SCENE:remove object it self')
        map_object = self.getObjectById(object_id)
        object_type = self.getTypeByName(map_object.object_type_name)

        object_type.removeMapObjectConnection(map_object.id)
        self.removeObjectConnection(map_object)
        self.gr_scene.removeItem(map_object.grMapObject) 
        map_object.remove()  #map_object remove from db


    def removeTypeByName(self, type_name):
        if DEBUG: print('SCENE:remove type it self')
        object_type = self.getTypeByName(type_name)
        objects_list = object_type.objects[:]
        for object_id in objects_list:
            self.removeObjectById(object_id)
        self.removeTypeConnection(object_type)
        object_type = None
                


    def clearTypes(self):
        if DEBUG: print('SCENE:reset all type in Scene')
        self.object_types = []
        

    def clearObjects(self):
        if DEBUG: print('SCENE:reset all object in Scene')
        self.objects = []
        self.gr_scene.clear()


    def loadObject(self):
        model = self.viewData('ObjectGraphic')
        model2 = self.viewData('ObjectDescription')
        for i in range(model.rowCount()):
            object_type_name = model.record(i).value('type')
            object_name = model.record(i).value('name')
            object_id = model.record(i).value('id')
            object_x = model.record(i).value('x')
            object_y = model.record(i).value('y')
            description = model2.record(i).value('description')
            object_type = self.getTypeByName(object_type_name)

            mapObject = MapObject(self.map_name, object_type_name, object_name,False, description)
            object_type_data = object_type.getAttribute()
            mapObject.generateGraphic(*object_type_data)
            mapObject.id = object_id
            object_type.addMapObjectConnection(object_id)
            self.addObjectConnection(mapObject)

            mapObject.setPosition(object_x, object_y)
            self.gr_scene.addItem(mapObject.grMapObject)
            

    def loadType(self):
        if DEBUG: print('SCENE:load type from database to Scene')
        model = self.viewData('type')
        for i in range(model.rowCount()):
            name = model.record(i).value('name')
            color = model.record(i).value('color')
            shape = model.record(i).value('shape')
            width = model.record(i).value('width')
            height = model.record(i).value('height')
            self.addTypeConnection(ObjectType(name,color,shape,width,height))
            


    def loadNewType(self, type_name):
        if DEBUG: print('SCENE:load new type when new type add to database')
        model = self.viewData('type')
        for i in range(model.rowCount()):
            if model.record(i).value('name')==type_name:
                name = model.record(i).value('name')
                color = model.record(i).value('color')
                shape = model.record(i).value('shape')
                width = model.record(i).value('width')
                height = model.record(i).value('height')
                self.addTypeConnection(ObjectType(name,color, shape,width,height))


    def updateType(self, type_name):
        if DEBUG: print('SCENE:update object grpahic and type attribute after update type in database')
        model = self.viewData('type')
        object_type = self.getTypeByName(type_name)
        for i in range(model.rowCount()):
            if model.record(i).value('name') == type_name:
                databaseRecord = model.record(i)
                object_type.update(databaseRecord.value('name'), databaseRecord.value('shape'), databaseRecord.value('color'), databaseRecord.value('width'), databaseRecord.value('height'))
                for obj in self.objects:
                    if obj.object_type_name == type_name:
                        obj.updateGr(*(object_type.getAttribute()))


    def renameObject(self, id, newName):
        for i in self.objects:
            if i.id == id:
                i.updateNameToDatabase(newName)

    def changeDescriptionObject(self, id, description):
        for i in self.objects:
            if i.id == id:
                i.updateDescriptionToDatabase(description)


    def getTypeNameList(self):
        list = []
        for object_type in self.object_types:
            list.append(object_type.type_name)
        return list

    def convertRealPosToMapPos(self, width, height, real_x, real_y):
        map_x = real_x - width/2
        map_y = real_y - height/2
        return (map_x, map_y)

    def convertMapPosToRealPos(self, width, height, map_x, map_y):
        real_x = map_x + width/2
        real_y = map_y - height/2
        return (real_x, real_y)

    def createNewObject(self, real_x, real_y):
        if (self.to_create != ''):
            object_type = self.getTypeByName(self.to_create)
        else:
            return 0
        width = object_type.width 
        height = object_type.height
        print(width)
        map_x, map_y = self.convertRealPosToMapPos(width, height, real_x, real_y)
        if (isinstance(object_type, type(None))):
            pass
        else:
            mapObject = MapObject(self.map_name, object_type.type_name, object_type.object_name_base+'_unnamed') 
            object_type_data =  object_type.getAttribute()
            mapObject.generateGraphic(*object_type_data)
            self.addObjectConnection(mapObject)
            object_type.addMapObjectConnection(mapObject.id)
            mapObject.setPosition(map_x, map_y)
            mapObject.updatePositionToDatabase(map_x, map_y)
            self.gr_scene.addItem(mapObject.grMapObject)
