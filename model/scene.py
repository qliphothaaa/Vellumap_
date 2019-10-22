from model.map_graphics_scene import QMapGraphicsScene
from model.new_map_object_management import ObjectsManagement
from model.new_map_object_type_management import TypesManagement
from model.new_map_object_graphics import QMapObjectGraphics
from model.new_object_graphics_management import GraphicsManagement
from model.map_graphics_background import QMapGraphicsBackground
from model.map_background import MapBackground

class Scene():
    def __init__(self, map_name):
        super().__init__()

        self.object_management = ObjectsManagement(map_name)
        self.types_management = TypesManagement(map_name)
        self.graphics_management = GraphicsManagement()
        self.initUI()


    def initUI(self):
        self.gr_scene = QMapGraphicsScene(self)
        self.gr_scene.setGrScene(15000, 15000)
        self.initManagements()
        self.loadGraphics()

    def loadBackground(self):
        if (self.object_management.map_background):
            mb = self.object_management.map_background
            mbg = QMapGraphicsBackground(mb)
            self.gr_scene.addItem(mbg)



    def initManagements(self):
        for object_id in self.object_management.map_objects:
            map_object = self.object_management.map_objects[object_id]
            object_type_data = self.types_management.getTypeAttributeByName(map_object.object_type_name)
            self.types_management.addObjectConnection(map_object.object_type_name, object_id)
            self.graphics_management.generateGraphics(map_object, *object_type_data)

    def loadGraphics(self):
        self.gr_scene.clear()
        self.loadBackground()
        for object_id in self.graphics_management.graphics:
            self.gr_scene.addItem(self.graphics_management.graphics[object_id])

    def removeObject(self, object_id):
        type_name = self.object_management.removeObjectById(object_id)
        self.types_management.removeObjectConnection(type_name, object_id)
        self.gr_scene.removeItem(self.graphics_management.getGraphics(object_id))
        self.graphics_management.removeGraphics(object_id)

    def updatePosition(self, object_id, x, y):
        self.object_management.updatePosition(object_id, x, y)

    def createNewObject(self, type_name, x, y):
        object_type_data = self.types_management.getTypeAttributeByName(type_name)
        width = object_type_data[2]
        height = object_type_data[3]
        #print('a')
        print(type(width))
        x = x - width/2
        y = y - height/2
        object_id = self.object_management.createNewObject(type_name, x, y)
        self.types_management.addObjectConnection( type_name, object_id)
        map_object = self.object_management.getObjectById(object_id)
        self.graphics_management.generateGraphics(map_object, *object_type_data)
        self.gr_scene.addItem(self.graphics_management.getGraphics(object_id))

    def renameObject(self, object_id, object_name):
        self.object_management.renameObject(object_id, object_name)

    def changeDescription(self, object_id, descirption):
        self.object_management.changeDescription(object_id, descirption)
        
    def removeType(self, type_name):
        object_set = self.types_management.removeTypeByName(type_name)
        for i in object_set:
            self.gr_scene.removeItem(self.graphics_management.getGraphics(i))
            self.object_management.removeObjectById(i)
            self.graphics_management.removeGraphics(i)

    def createNewType(self, type_name, shape, color, width, height):
        self.types_management.createType(type_name, shape, color, width, height)

    def updateType(self, type_name, shape, color, width, height):
        object_id_set = self.types_management.updateType(type_name, shape, color, width, height)
        object_type_data = self.types_management.getTypeAttributeByName(type_name)
        for object_id in object_id_set:
            self.graphics_management.updateGraphics(object_id, *object_type_data)

    def getTypeNameList(self):
        name_list = self.types_management.getTypeNameList()
        return name_list

    def filterGraphicsByType(self, type_name, state):
        id_set = self.types_management.getObjectSetByName(type_name)
        if (state):
            self.graphics_management.showGraphics(id_set)
        else:
            self.graphics_management.hideGraphics(id_set)


        
