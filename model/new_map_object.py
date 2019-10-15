class MapObject():
    def __init__(self, object_id, object_name, object_type_name, x, y, description='nothing'):
        self.object_id = None
        self.object_name = object_name
        self.object_type_name = object_type_name

        self.x = 0
        self.y = 0
        self.description = description


    def getObjectInfo(self):
        object_id = self.object_id
        name = self.object_name
        type_name = self.object_type_name
        x = self.x
        y = self.y
        description = self.description
        return (object_id, name, type_name, x, y, description)

    '''
    def getPosition(self):
        return (self.x, self.y)
    '''


    def generateSqlForRename(self):
        sql = "Update ObjectGraphic set Name = '%s' where (id = '%d');" % (self.name, self.id)
        return sql

    def generateSqlForChangeDescription(self):
        if DEBUG: print('OBJECT: connect to database, op:update Name:%s'%name)
        sql = "Update ObjectDescription set Description = '%s' where (id = '%d');" % (self.description, self.id)
        return sql

    def generateSqlForAdd(self):
        if DEBUG: print('OBJECT: connect to database, op:add object')
        sql = "insert into ObjectGraphic values (null,'%s',%e, %e,'%s');" % (self.object_name, self.x, self.y, self.object_type_name)
        return sql

    def generateSqlForAddDiscription(self):
        sql = "insert into ObjectDescription values (%d, '%s');" % (self.id, self.description)
        return sql

    def generateSqlForDelete(self):
        if DEBUG: print('OBJECT: connect to database, op:delete object')
        sql = "Delete from ObjectGraphic where(id = '%s');" % self.id
        return sql

    def generateSqlForDeleteDescription(self):
        if DEBUG: print('OBJECT: connect to database, op:delete object')
        sql = "Delete from ObjectDescription where(id = '%s');" % self.id
        return sql

    def generateSqlForUpdatePosition(self):
        if DEBUG: print('OBJECT: connect to database, op:update position')
        sql = "Update ObjectGraphic set X = %e, y = %e where (id = '%s');" % (self.x, self.y, self.id)
        return sql

    

        
