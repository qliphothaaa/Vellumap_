from model.map_graphics_scene import QMapGraphicsScene
from model.map_object import MapObject
from model.map_object_type import ObjectType
from model.data_access_object import DataAccess
from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
DEBUG = False
#The main scene that contain all things
class Scene(DataAccess):
    def __init__(self, map_name):
        super().__init__()
        self.object_types = []
        self.objects = []
        self.map_name = map_name
        self.scene_width = 15000
        self.scene_height = 15000
        self.to_create = ''
        self.initUI()
        

    def initUI(self):
        if DEBUG: print('SCENE:init gr_scene')
        self.gr_scene = QMapGraphicsScene(self)
        self.gr_scene.setGrScene(self.scene_width, self.scene_height)

        self.clearTypes()
        self.loadType()
        self.loadObject()

    def setTempTypeName(self, type_name):
        if (self.to_create == type_name):
            self.to_create = ''
        else:
            self.to_create = type_name


    def createNewObject(self, real_x, real_y):
        if (self.to_create != ''):
            ObjectType = self.getTypeByName(self.to_create)
        else:
            return 0

        width, height = ObjectType.getSize()
        map_x, map_y = self.convertRealPosToMapPos(width, height, real_x, real_y)
        print(map_x, map_y)
        if (isinstance(ObjectType, type(None))):
            print("not exist")
        else:
            mapObject = MapObject(self.map_name, ObjectType, ObjectType.object_name_base+'_unnamed') 
            self.addObjectConnection(mapObject)
            ObjectType.addMapObjectConnection(mapObject)
            mapObject.setPosition(map_x, map_y)
            mapObject.updatePosition(map_x, map_y)
            self.gr_scene.addItem(mapObject.grMapObject)
        #print(self.to_create)


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

    def getObjectXYById(self, object_id):
        for item in self.objects:
            if item.getId() == object_id:
                return item.getPosition()

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

    '''
    def drawCross(self, x, y):
        self.removeCross()
        outlinePen = QPen(Qt.white)
        outlinePen.setWidth(5)
        self.line = self.gr_scene.addLine(x, y-30, x, y+30, outlinePen)
        self.line2 = self.gr_scene.addLine(x-30, y, x+30, y, outlinePen)

    def removecross(self):
        if (self.line==None and self.line2==None):
            pass
        else:
            self.gr_scene.removeItem(self.line)
            self.gr_scene.removeItem(self.line2)
    '''



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

    def changeDescriptionObject(self, id, description):
        for i in self.objects:
            if i.getId() == id:
                i.setDescription(description)



    def convertRealPosToMapPos(self, width, height, real_x, real_y):
        map_x = real_x - width/2
        map_y = real_y - height/2
        return (map_x, map_y)

    def convertMapPosToRealPos(self, width, height, map_x, map_y):
        real_x = map_x + width/2
        real_y = map_y - height/2
        return (real_x, real_y)



