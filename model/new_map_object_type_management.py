from model.new_map_object_type import ObjectType
from model.data_access_object import DataAccess

class TypesManagement(DataAccess):
    def __init__(self, map_name):
        self.map_object_types = {}
        self.map_name = map_name

    def loadTypes(self):
        types_model = self.viewData('type')
        for i in range(types_model.rowCount()):
            name = types_model.record(i).value('name')
            color = types_model.record(i).value('color')
            shape = types_model.record(i).value('shape')
            width = types_model.record(i).value('width')
            height = types_model.record(i).value('height')
            self.map_object_types[name] = ObjectType(name,color,shape,width,height)

    def loadNewType(self, type_name):
        types_model = self.viewData('type')
        for i in range(types_model.rowCount()):
            if types_model.record(i).value('name')==type_name:
                name = types_model.record(i).value('name')
                color = types_model.record(i).value('color')
                shape = types_model.record(i).value('shape')
                width = types_model.record(i).value('width')
                height = types_model.record(i).value('height')
                self.map_object_types[name] = ObjectType(name,color,shape,width,height)


    def removeTypeByName(self, type_name):
        targetType = self.map_object_types[type_name]
        self.accessDataBase(
        del self.map_object_types[type_name]
        #return remove_list

    def getTypeAttributeByName(self, type_name):
        targetType = self.map_object_types[type_name]
        return targetType.getAttribute()

    


        
        

        

