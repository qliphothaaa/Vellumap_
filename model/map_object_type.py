import re
#object type, contain a prototype description of object
DEBUG = False
class ObjectType():
    def __init__(self, type_name, default_color, shape, width, height):

        self.type_name = type_name
        self.default_color = default_color
        self.shape = shape
        self.width = width
        self.height = height
        self.object_name_base = re.sub('^type','',self.type_name)

        self.objects = []


    def __str__(self):
        return self.shape
    def remove(self):
        if DEBUG: print('TYPE: remove object it self')
        self.objects = []
        self = None

    def getName(self):
        return self.type_name

    def getColor(self):
        return self.default_color

    def getShape(self):
        return self.shape

    def getObjects(self):
        return self.objects

    def getSize(self):
        if DEBUG: print('TYPE: get width and height of type')
        return (self.width, self.height)

    def getAttribute(self):
        color = self.getColor()
        shape = self.getShape()
        width = self.getSize()[0]
        height = self.getSize()[1]
        return (color, shape, width, height)


    def removeMapObjectConnection(self,obj):
        if DEBUG: print('TYPE: remove object from type')
        self.objects.remove(obj)

    def addMapObjectConnection(self, mapObject):
        if DEBUG: print('TYPE: add object to type')
        self.objects.append(mapObject)

    def update(self, type_name, shape, color, width, height):
        if DEBUG: print('TYPE: update type attribute')
        self.type_name = type_name
        self.default_color = color
        self.shape = shape
        self.width = width
        self.height = height


