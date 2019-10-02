from model.map_graphics_scene import QMapGraphicsScene
from model.map_object import MapObject
from model.map_object_type import ObjectType
from model.data_access_object import DataAccess
from PyQt5.QtSql import *
DEBUG = False
#The main scene that contain all things
class Scene(DataAccess):
    def __init__(self, map_name):
        super().__init__()
        self.object_types = []
        self.objects = []
        self.map_name = map_name
        self.scene_width = 6400
        self.scene_height = 6400
        self.initUI()

    def initUI(self):
        if DEBUG: print('SCENE:init gr_scene')
        self.gr_scene = QMapGraphicsScene(self)
        self.gr_scene.setGrScene(self.scene_width, self.scene_height)

        self.clearTypes()
        self.loadType()
        self.loadObject()

    def createNewObject(self, type_name):
        ObjectType = self.getTypeByName(type_name)
        mapObject = MapObject(self.map_name, ObjectType, ObjectType.object_name_base+'_unnamed') 
        self.addObjectConnection(mapObject)
        ObjectType.addMapObjectConnection(mapObject)
        self.gr_scene.addItem(mapObject.grMapObject)


    def addObjectConnection(self, obj):
        if DEBUG: print('SCENE:add object to Scene')
        self.objects.append(obj)

    def removeObjectConnection(self, obj):
        if DEBUG: print('SCENE:remove object from Scene')
        self.objects.remove(obj)

    def removeObjectById(self, object_id):
        if DEBUG: print('SCENE:remove object it self')
        item = self.getObjectById(object_id)
        self.gr_scene.removeItem(item.grMapObject)
        self.removeObjectConnection(item)
        item.remove()

    def getObjectById(self, object_id):
        if DEBUG: print('SCENE:find object by id')
        for item in self.objects:
            if item.getId() == object_id:
                return item

    def addType(self, object_type):
        if DEBUG: print('SCENE:add type to Scene')
        self.object_types.append(object_type)

    def removeTypeConnection(self, object_type):
        if DEBUG: print('SCENE:remove type from Scene')
        self.object_types.remove(object_type)

    def getTypeByName(self, type_name):
        if DEBUG: print('SCENE:find type by name')
        for item in self.object_types:
            if item.getName() == type_name:
                return item

    def removeTypeByName(self, type_name):
        if DEBUG: print('SCENE:remove type it self')
        item = self.getTypeByName(type_name)
        self.removeTypeConnection(item)
        for obj in item.getObjects():
            self.gr_scene.removeItem(obj.grMapObject)
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
            object_type = self.getTypeByName(model.record(i).value('type'))
            object_name = model.record(i).value('name')
            object_id = model.record(i).value('id')
            object_x = model.record(i).value('x')
            object_y = model.record(i).value('y')

            mapObject = MapObject(self.map_name, object_type, object_name,False)
            mapObject.setId(object_id)
            self.gr_scene.addItem(mapObject.grMapObject)
            self.addObjectConnection(mapObject)
            mapObject.setPosition(object_x, object_y)
            

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
                self.addType(ObjectType(name,color, shape,width,height))
                return


    def updateType(self, type_name):
        if DEBUG: print('SCENE:update object grpahic and type attribute after update type in database')
        if DEBUG: print('updateType')
        model = self.viewData('type')
        item = self.getTypeByName(type_name)
        for i in range(model.rowCount()):
            if model.record(i).value('name') == type_name:
                databaseRecord = model.record(i)
                item.update(databaseRecord.value('name'), databaseRecord.value('shape'), databaseRecord.value('color'), databaseRecord.value('width'), databaseRecord.value('height'))
                for obj in item.getObjects():
                    obj.updateGr(*(item.getAttribute()))


    def renameObject(self, id, newName):
        for i in self.objects:
            if i.getId() == id:
                i.setName(newName)

