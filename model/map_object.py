class MapObject():
    def __init__(self, object_id, object_name, object_type_name, x, y, description='nothing'):
        self.object_id = object_id
        self.object_name = object_name
        self.object_type_name = object_type_name

        self.x = x
        self.y = y
        self.description = description


    def getPosition(self):
        return (self.x, self.y)


    def getObjectInfo(self):
        object_id = self.object_id
        name = self.object_name
        type_name = self.object_type_name
        x = self.x
        y = self.y
        description = self.description
        return (object_id, name, type_name, x, y, description)


    def generateSqlForRename(self):
        sql = "Update ObjectGraphic set Name = '%s' where (id = '%d');" % (self.object_name, self.object_id)
        return sql

    def generateSqlForChangeDescription(self):
        sql = "Update ObjectDescription set Description = '%s' where (id = '%d');" % (self.description, self.object_id)
        return sql



    def generateSqlForUpdatePosition(self):
        sql = "Update ObjectGraphic set X = %e, y = %e where (id = '%s');" % (self.x, self.y, self.object_id)
        return sql



    def generateSqlForAdd(self):
        sql = "insert into ObjectGraphic values (null,'%s',%e, %e,'%s');" % (self.object_name, self.x, self.y, self.object_type_name)
        return sql

    def generateSqlForAddDiscription(self):
        sql = "insert into ObjectDescription values (%d, '%s');" % (self.object_id, self.description)
        return sql



    def generateSqlForDelete(self):
        sql = "Delete from ObjectGraphic where(id = '%s');" % self.object_id
        return sql

    def generateSqlForDeleteDescription(self):
        sql = "Delete from ObjectDescription where(id = '%s');" % self.object_id
        return sql


    

        
