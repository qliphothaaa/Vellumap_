class ObjectType():
    def __init__(self, type_name, color, shape, width, height):
        self.type_name = type_name
        self.color = color
        self.shape = shape
        self.width = width
        self.height = height
        self.objects_id_set = set()

    def getAttribute(self):
        return (self.color, self.shape, self.width, self.height)
    
    def getObjectIdSet(self):
        return self.objects_id_set

    def update(self, color, shape, width, height):
        self.color = color
        self.shape = shape
        self.width = width
        self.height = height

    def addObjectId(self, object_id):
        self.objects_id_set.add(object_id)

    def removeObjectId(self, object_id):
        self.objects_id_set.remove(object_id)

        

    def generateSqlForAdd(self):
        sql = "insert into type values('%s', '%s', '%s', '%s', '%s')" % (self.type_name, self.shape, self.color, self.width, self.height)
        return sql

    def generateSqlForUpdate(self):
        sql = "Update type set Shape = '%s', color = '%s', width = '%s', height = '%s' where name ='%s'" % (self.shape, self.color, self.width, self.height, self.type_name)
        return sql

    def generateSqlForDelete(self):
        sql = "Delete from type where (name = '%s')" % self.type_name
        return sql
