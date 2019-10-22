from model.new_map_object_graphics import QMapObjectGraphics

class GraphicsManagement():
    def __init__(self):
        self.graphics = {}


    def generateGraphics(self, map_object, color, shape, width, height):
        grMapObject = QMapObjectGraphics(map_object, color, shape, width, height)
        grMapObject.setPos(*map_object.getPosition())
        self.graphics[map_object.object_id] = grMapObject

    def getGraphics(self, object_id):
        return self.graphics[object_id]

    def removeGraphics(self, object_id):
        del self.graphics[object_id]


    def updateGraphics(self, object_id, color, shape, width, height):
        self.graphics[object_id].setColor(color)
        self.graphics[object_id].setShape(shape)
        self.graphics[object_id].setWidth(width)
        self.graphics[object_id].setHeight(height)

    def hideGraphics(self, object_id_set):
        for object_id in object_id_set:
            self.graphics[object_id].hide()

    def showGraphics(self, object_id_set):
        for object_id in object_id_set:
            self.graphics[object_id].show()
            

