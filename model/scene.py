from model.graphics_scene import QMapGraphicsScene
from model.object_management import ObjectsManagement
from model.type_management import TypesManagement
from model.graphics_management import GraphicsManagement
from model.graphics_background import QMapGraphicsBackground
from model.background import MapBackground
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import traceback
import json

class Scene(QObject):
    ErrorSignal = pyqtSignal(str)
    def __init__(self, map_name):
        super().__init__()
        self.mapName = map_name

        self.object_management = ObjectsManagement(map_name)
        self.types_management = TypesManagement(map_name)
        self.graphics_management = GraphicsManagement()

        self.max_id = self.object_management.max_id
        self.initUI()


    def initUI(self):
        self.gr_scene = QMapGraphicsScene(self)
        self.gr_scene.setGrScene(15000, 15000)
        self.initManagements()
        self.loadGraphics()

    def debug(func):
        def wrapper(self, *args, **kwargs):
            try:
                func(self, *args, **kwargs)
                print("Execute: %s: %s" % (self.__class__.__name__ ,func.__name__))
            except:
                print("Error execute: %s" % func.__name__)
                #print(kwargs)
                self.ErrorSignal.emit(traceback.format_exc())
        return wrapper

    @debug
    def initManagements(self):
        for object_id in self.object_management.map_objects:
            map_object = self.object_management.map_objects[object_id]
            object_type_data = self.types_management.getTypeAttributeByName(map_object.object_type_name)
            self.types_management.addObjectConnection(map_object.object_type_name, object_id)
            self.graphics_management.generateGraphics(map_object, *object_type_data)

    @debug
    def importBackground(self, name, x, y, size):
        self.object_management.addBackground(name,size, x, y)
        self.loadBackgroundGraphics()

    @debug
    def loadGraphics(self):
        self.gr_scene.clear()
        self.loadBackgroundGraphics()

        for object_id in self.graphics_management.graphics:
            self.gr_scene.addItem(self.graphics_management.graphics[object_id])

    @debug
    def loadBackgroundGraphics(self):
        self.gr_scene.clearBackground()
        if (self.object_management.map_background):
            mb = self.object_management.map_background
            mbg = QMapGraphicsBackground(mb)
            self.gr_scene.addBackgroundItem(mbg)


    @debug
    def removeBackground(self):
        self.gr_scene.clearBackground()
        self.object_management.removeBackground()


    @debug
    def removeObject(self, object_id):
        type_name = self.object_management.removeObjectById(object_id)
        self.types_management.removeObjectConnection(type_name, object_id)
        self.gr_scene.removeItem(self.graphics_management.getGraphics(object_id))
        self.graphics_management.removeGraphics(object_id)


    @debug
    def createNewObject(self, type_name, x, y):
        object_type_data = self.types_management.getTypeAttributeByName(type_name)
        object_id = self.object_management.createNewObject(type_name, float(x), float(y))
        self.types_management.addObjectConnection( type_name, object_id)
        map_object = self.object_management.getObjectById(object_id)
        self.graphics_management.generateGraphics(map_object, *object_type_data)
        self.gr_scene.addItem(self.graphics_management.getGraphics(object_id))
        return object_id


        
    @debug
    def removeType(self, type_name):
        object_id_set = self.types_management.removeTypeByName(type_name)
        for i in object_id_set:
            self.gr_scene.removeItem(self.graphics_management.getGraphics(i))
            self.object_management.removeObjectById(i)
            self.graphics_management.removeGraphics(i)
        return object_id_set


    @debug
    def updateType(self, type_name, shape, color, width, height):
        object_id_set = self.types_management.updateType(type_name, shape, color, width, height)
        object_type_data = (color, shape, width, height)
        for object_id in object_id_set:
            self.graphics_management.updateGraphics(object_id, *object_type_data)


    @debug
    def filterGraphicsByType(self, type_name, state):
        id_set = self.types_management.getObjectSetByName(type_name)
        if (state):
            self.graphics_management.showGraphics(id_set)
        else:
            self.graphics_management.hideGraphics(id_set)


    def getTypeNameList(self):
        name_list = self.types_management.getTypeNameList()
        return name_list

    @debug
    def renameObject(self, object_id, object_name):
        self.object_management.renameObject(object_id, object_name)

    @debug
    def changeDescription(self, object_id, desciription):
        self.object_management.changeDescription(object_id, desciription)

    @debug
    def updatePosition(self, object_id, x, y):
        self.object_management.updatePosition(object_id, x, y)

    @debug
    def createNewType(self, type_name, shape, color, width, height):
        self.types_management.createType(type_name, shape, color, width, height)


    @debug
    def saveToDB(self):
        self.object_management.saveToDB()
        self.types_management.saveToDB()



    @debug
    def saveAsJson(self):
        filename = "json/" + self.mapName + ".json.txt"
        with open (filename, "w") as file:
            objects_data = self.object_management.collectData()
            type_data = self.types_management.collectData()
            dictMerge =type_data.copy()
            dictMerge.update(objects_data)
            file.write( json.dumps( dictMerge, indent=4))

        print('saving successful')

    def loadFromJson(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            #then do something with data
           


    def saveAsImg(self):
        print("save as img")



