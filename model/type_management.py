from model.object_type import ObjectType
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
            width = float(types_model[i][3])
            height = float(types_model[i][4])
            self.map_object_types[name] = ObjectType(name,color,shape,width,height)


    def removeTypeByName(self, type_name):
        targetType = self.getTypeByName(type_name)
        remove_set = targetType.getObjectIdSet()
        self.accessDataBase(targetType.generateSqlForDelete())
        del self.map_object_types[type_name]
        return remove_set

    def getObjectSetByName(self, type_name):
        targetType = self.getTypeByName(type_name)
        return targetType.getObjectIdSet()
        

    def createType(self, type_name, shape, color, width, height):
        if type_name in self.map_object_types:
            raise KeyError('Type exist')
        if not shape in ('rect', 'tri', 'ell'):
            raise ValueError('bad shape')
        self.map_object_types[type_name] = ObjectType(type_name, color, shape, width, height)
        self.accessDataBase(self.map_object_types[type_name].generateSqlForAdd())

    def updateType(self, type_name, shape, color, width, height): 
        if not shape in ('rect', 'tri', 'ell'):
            raise ValueError('bad shape')
        targetType = self.getTypeByName(type_name)
        targetType.update(color, shape, width, height)
        update_set = targetType.getObjectIdSet()
        self.accessDataBase(targetType.generateSqlForUpdate())
        return update_set


    def addObjectConnection(self, type_name, object_id):
        targetType = self.getTypeByName(type_name)
        targetType.addObjectId(object_id)

    def removeObjectConnection(self, type_name, object_id):
        targetType = self.getTypeByName(type_name)
        if not isinstance(object_id, int):
            raise TypeError('id should be int')
        if not object_id in targetType.objects_id_set:
            raise KeyError('id does not exist')
        targetType.removeObjectId(object_id)

    def getTypeAttributeByName(self, type_name):
        targetType = self.getTypeByName(type_name)
        return targetType.getAttribute()

    def removeAllType(self):
        self.map_object_types.clear()

    def getTypeNameList(self):
        return (list(self.map_object_types.keys()))

    def getTypeByName(self, type_name):
        if not isinstance(type_name, str):
            raise TypeError("type name should be str")
        if not type_name in self.map_object_types:
            raise KeyError("Type does not exist")
        targetType = self.map_object_types[type_name]
        return targetType


