import re
#object type, contain a prototype description of object
DEBUG = False
class ObjectType():
    def __init__(self, type_name, color, shape, width, height):

        self.type_name = type_name
        self.color = color
        self.shape = shape
        self.width = width
        self.height = height
        self.object_name_base = re.sub('^type','',self.type_name)

        self.objects = []


    '''
    def remove(self):
        if DEBUG: print('TYPE: remove object it self')
        self.objects = []
        self = None
    '''


    '''
    def getObjects(self):
        return self.objects
    '''

    def getSize(self):
        if DEBUG: print('TYPE: get width and height of type')
        return (self.width, self.height)

    def getAttribute(self):
        return (self.color, self.shape, self.width, self.height)


    def removeMapObjectConnection(self,map_object):
        if DEBUG: print('TYPE: remove object from type')
        self.objects.remove(map_object)

    def addMapObjectConnection(self, map_object):
        if DEBUG: print('TYPE: add object to type')
        self.objects.append(map_object)

    def update(self, type_name, shape, color, width, height):
        if DEBUG: print('TYPE: update type attribute')
        self.type_name = type_name
        self.color = color
        self.shape = shape
        self.width = width
        self.height = height


