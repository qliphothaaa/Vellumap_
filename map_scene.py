from map_graphics_scene import QMapGraphicsScene
from map_object import MapObject
from map_object_type import ObjectType
from data_access_object import DataAccess
from PyQt5.QtSql import *
DEBUG = False
#The main scene that contain all things
class Scene(DataAccess):
    def __init__(self, mapName):
        super().__init__()
        self.object_types = []
        self.objects = []
        self.mapName = mapName
        self.scene_width = 6400
        self.scene_height = 6400
        self.initUI()

    def initUI(self):
        if DEBUG: print('SCENE:init grScene')
        self.grScene = QMapGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

        self.clearTypes()
        self.loadType()
        self.loadObject()

    def createNewObject(self, typeName):
        ObjectType = self.getTypeByName(typeName)
        mapObject = MapObject(self.mapName, ObjectType, ObjectType.objectNameBase+'unnamed') 
        self.addObjectConnection(mapObject)
        ObjectType.addMapObjectConnection(mapObject)
        self.grScene.addItem(mapObject.grMapObject)


    def addObjectConnection(self, obj):
        if DEBUG: print('SCENE:add object to Scene')
        self.objects.append(obj)

    def removeObjectConnection(self, obj):
        if DEBUG: print('SCENE:remove object from Scene')
        self.objects.remove(obj)

    def removeObjectById(self, objectId):
        if DEBUG: print('SCENE:remove object it self')
        item = self.getObjectById(objectId)
        self.grScene.removeItem(item.grMapObject)
        self.removeObjectConnection(item)
        item.remove()

    def getObjectById(self, objectId):
        if DEBUG: print('SCENE:find object by id')
        for item in self.objects:
            if item.getId() == objectId:
                return item

    def addType(self, object_type):
        if DEBUG: print('SCENE:add type to Scene')
        self.object_types.append(object_type)

    def removeTypeConnection(self, object_type):
        if DEBUG: print('SCENE:remove type from Scene')
        self.object_types.remove(object_type)

    def getTypeByName(self, typeName):
        if DEBUG: print('SCENE:find type by name')
        for item in self.object_types:
            if item.getName() == typeName:
                return item

    def removeTypeByName(self, typeName):
        if DEBUG: print('SCENE:remove type it self')
        item = self.getTypeByName(typeName)
        self.removeTypeConnection(item)
        for obj in item.getObjects():
            self.grScene.removeItem(obj.grMapObject)
        item.remove()

    def clearTypes(self):
        if DEBUG: print('SCENE:reset all type in Scene')
        self.object_types = []

    def clearObjects(self):
        if DEBUG: print('SCENE:reset all object in Scene')
        self.objects = []

    def loadObject(self):
        model = self.viewData('ObjectGraphic')
        for i in range(model.rowCount()):
            objectType = self.getTypeByName(model.record(i).value('type'))
            objectName = model.record(i).value('name')
            objectId = model.record(i).value('id')
            objectX = model.record(i).value('x')
            objectY = model.record(i).value('y')

            mapObject = MapObject(self.mapName, objectType, objectName,False)
            mapObject.setId(objectId)
            self.grScene.addItem(mapObject.grMapObject)
            self.addObjectConnection(mapObject)
            mapObject.setPosition(objectX, objectY)
            

    def loadType(self):
        if DEBUG: print('SCENE:load type from database to Scene')
        model = self.viewData('type')
        for i in range(model.rowCount()):
            name = model.record(i).value('name')
            color = model.record(i).value('color')
            shape = model.record(i).value('shape')
            width = model.record(i).value('width')
            height = model.record(i).value('height')
            self.addType(ObjectType(name,color,shape,width,height))
            


    def loadNewType(self, typeName):
        if DEBUG: print('SCENE:load new type when new type add to database')
        model = self.viewData('type')
        for i in range(model.rowCount()):
            if model.record(i).value('name')==typeName:
                name = model.record(i).value('name')
                color = model.record(i).value('color')
                shape = model.record(i).value('shape')
                width = model.record(i).value('width')
                height = model.record(i).value('height')
                self.addType(ObjectType(name,color, shape,width,height))
                return


    def updateType(self, typeName):
        if DEBUG: print('SCENE:update object grpahic and type attribute after update type in database')
        if DEBUG: print('updateType')
        model = self.viewData('type')
        item = self.getTypeByName(typeName)
        for i in range(model.rowCount()):
            if model.record(i).value('name') == typeName:
                databaseRecord = model.record(i)
                item.update(databaseRecord.value('name'), databaseRecord.value('shape'), databaseRecord.value('color'), databaseRecord.value('width'), databaseRecord.value('height'))
                for obj in item.getObjects():
                    obj.updateGr(*(item.getAttribute()))


    def renameObject(self, id, newName):
        for i in self.objects:
            if i.getId() == id:
                i.setName(newName)

