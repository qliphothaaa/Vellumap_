from model.new_map_object_type import ObjectType
from model.data_access_object import DataAccess

class TypesManagement(DataAccess):
    def __init__(self, map_name):
        self.map_object_types = {}
        self.map_name = map_name
        self.loadTypes()

    def loadTypes(self):
        types_model = self.viewData('type')
        for i in range(len(types_model)):
            name = types_model[i][0]
            color = types_model[i][2]
            shape = types_model[i][1]
            width = types_model[i][3]
            height = types_model[i][4]
            self.map_object_types[name] = ObjectType(name,color,shape,width,height)


    def removeTypeByName(self, type_name):
        targetType = self.map_object_types[type_name]
        remove_set = targetType.getObjectIdSet()
        self.accessDataBase(targetType.generateSqlForDelete())
        del self.map_object_types[type_name]
        return remove_set

    def getObjectSetByName(self, type_name):
        targetType = self.map_object_types[type_name]
        return targetType.getObjectIdSet()
        

    def createType(self, type_name, shape, color, width, height):
        self.map_object_types[type_name] = ObjectType(type_name, color, shape, width, height)
        self.accessDataBase(self.map_object_types[type_name].generateSqlForAdd())

    def updateType(self, type_name, shape, color, width, height): 
        targetType = self.map_object_types[type_name]
        targetType.update(color, shape, width, height)
        update_set = targetType.getObjectIdSet()
        self.accessDataBase(targetType.generateSqlForUpdate())
        return update_set


    def addObjectConnection(self, type_name, object_id):
        targetType = self.map_object_types[type_name]
        targetType.addObjectId(object_id)

    def removeObjectConnection(self, type_name, object_id):
        targetType = self.map_object_types[type_name]
        targetType.removeObjectId(object_id)

    def getTypeAttributeByName(self, type_name):
        targetType = self.map_object_types[type_name]
        return targetType.getAttribute()

    def removeAllType(self):
        self.map_object_types.clear()

    def getTypeNameList(self):
        return (list(self.map_object_types.keys()))

