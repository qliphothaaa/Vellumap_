from model.object_graphics import QMapObjectGraphics

class GraphicsManagement():
    def __init__(self):
        self.graphics = {}


    def generateGraphics(self, map_object, color, shape, width, height):
        grMapObject = QMapObjectGraphics(map_object, color, shape, width, height)
        x =  map_object.getPosition()[0]
        y =  map_object.getPosition()[1]
        x = x - width/2
        y = y - height/2
        grMapObject.setPos(x, y)
        self.graphics[map_object.object_id] = grMapObject

    def getGraphics(self, object_id):
        try:
            return self.graphics[object_id]
        except(KeyError):
            return None

    def removeGraphics(self, object_id):
        if not object_id in self.graphics:
            raise KeyError('cannot find the graphic')
        del self.graphics[object_id]


    def updateGraphics(self, object_id, color, shape, width, height):
        if not object_id in self.graphics:
            raise KeyError('cannot find the graphic')
        target_graphic = self.getGraphics(object_id)
        target_graphic.setColor(color)
        target_graphic.setShape(shape)
        target_graphic.setWidth(width)
        target_graphic.setHeight(height)
        target_graphic.renewPosition()

    def hideGraphics(self, object_id_set):
        if not isinstance(object_id_set, set):
            raise ValueError('input should be set')
        for object_id in object_id_set:
            if not object_id in self.graphics:
                raise KeyError('cannot find the graphic')
            self.graphics[object_id].hide()

    def showGraphics(self, object_id_set):
        if not isinstance(object_id_set, set):
            raise ValueError('input should be set')
        for object_id in object_id_set:
            if not object_id in self.graphics:
                raise KeyError('cannot find the graphic')
            self.graphics[object_id].show()

    def clear(self):
        self.graphics.clear()
            

