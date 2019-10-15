class ObjectType():
    def __init__(self, type_name, color, shape, width, height):
        self.type_name = type_name
        self.color = color
        self.shape = shape
        self.height = height

    def getSize(self):
        return (self.width, self.height)

    def getAttribute(self):
        return (self.color, self.shape, self.width, self.height)
    
    def getObjectIdList(self):
        return self.objects_id_list




        
