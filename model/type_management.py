from model.object_type import ObjectType
from model.data_access_object import DataAccess
from collections import OrderedDict
import copy,re, json

class TypesManagement(DataAccess):
    def __init__(self, map_name):
        super().__init__()
        self.map_object_types = {}
        self.map_name = map_name
        #print("TM: %s" % map_name)

        self.deleted_types = []
        self.updated_type_names = set()
        self.added_type_names = set()

        mapExtension = re.split('\.', self.map_name)[-1]
        if mapExtension == "db":
            self.loadTypes()
        elif mapExtension == "json":
            self.loadJsonFile(self.map_name)

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
        #self.accessDataBase(targetType.generateSqlForDelete())

        self.deleted_types.append(copy.deepcopy(self.map_object_types[type_name]))
        del self.map_object_types[type_name]

        if type_name in self.added_type_names:
            self.added_type_names.remove(type_name)
        elif type_name in self.updated_type_names:
            self.updated_type_names.remove(type_name)

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
        #self.accessDataBase(self.map_object_types[type_name].generateSqlForAdd())
        self.added_type_names.add(type_name)

    def updateType(self, type_name, shape, color, width, height): 
        if not shape in ('rect', 'tri', 'ell'):
            raise ValueError('bad shape')
        targetType = self.getTypeByName(type_name)
        targetType.update(color, shape, width, height)
        update_set = targetType.getObjectIdSet()
        #self.accessDataBase(targetType.generateSqlForUpdate())
        self.updated_type_names.add(type_name)
        
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

    def saveToDB(self):
        for type_name in self.added_type_names:
            target_type = self.getTypeByName(type_name)
            self.accessDataBase(*target_type.generateSqlForAdd())

        for type_name in self.updated_type_names:
            target_type = self.getTypeByName(type_name)
            self.accessDataBase(*target_type.generateSqlForUpdate())

        for type_ in self.deleted_types:
            self.accessDataBase(*type_.generateSqlForDelete())
            del type_

        self.deleted_types.clear()
        self.updated_type_names.clear()
        self.added_type_names.clear()

    def collectData(self):
        types = []
        for object_type in self.map_object_types.values():
            types.append(object_type.serialize())

        return OrderedDict([
                ('object_types', types)
            ])

    def loadJsonFile(self, data):
        with open('./json/'+data, "r") as file:
            raw_data = file.read()
            data = json.loads(raw_data, encoding='utf-8')
            
            for i in data['object_types']:
                name = i['name']
                object_type = ObjectType()
                object_type.deserialize(i)
                self.map_object_types[name] = object_type
