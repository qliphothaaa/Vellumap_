import unittest
from tests.fake_db import FakeDB
from collections import OrderedDict
from model.type_management import TypesManagement

class TestTypesManagmeent(unittest.TestCase):
    def setUp(self):
        self.db = FakeDB('test')
        self.db.clear('type')
        data1 = ( 'type1', 'ell', 'green', 100, 100 )
        data2 = ( 'type2', 'rec', '#393939', 50, 50 )
        type_list = [data1, data2]
        for item in type_list:
            self.db.accessDatabase("insert into type values ('%s', '%s', '%s', %s, %s);"% (*item,))
        self.type_management = TypesManagement('test.db')
        self.type_management.map_object_types['type1'].objects_id_set = {1}

    def tearDown(self):
        self.db.clear('type')

    def test_loadTypes(self):
        self.assertEqual(list(self.type_management.map_object_types.keys()), ['type1','type2'])
        self.assertEqual(self.type_management.map_object_types['type1'].shape,'ell' )
        self.assertEqual(self.type_management.map_object_types['type1'].color,'green' )
        self.assertEqual(self.type_management.map_object_types['type1'].width,100 )
        self.assertEqual(self.type_management.map_object_types['type1'].height,100 )
        self.assertEqual(self.type_management.map_object_types['type2'].shape,'rec' )
        self.assertEqual(self.type_management.map_object_types['type2'].color,'#393939' )
        self.assertEqual(self.type_management.map_object_types['type2'].width,50 )
        self.assertEqual(self.type_management.map_object_types['type2'].height,50 )

    def test_removeTypeByName(self):
        self.assertEqual(self.type_management.removeTypeByName('type1'), {1})
        self.assertFalse('type1' in self.type_management.map_object_types)
        with self.assertRaises(KeyError):
            self.type_management.removeTypeByName('type3')
        with self.assertRaises(TypeError):
            self.type_management.removeTypeByName(2)
        

    def test_getObjectSetByName(self):
        self.assertEqual(self.type_management.getObjectSetByName('type1'), {1})
        self.assertEqual(self.type_management.getObjectSetByName('type2'), set())
        with self.assertRaises(KeyError):
            self.type_management.getObjectSetByName('type3')
        with self.assertRaises(TypeError):
            self.type_management.getObjectSetByName(2)


    def test_createType(self):
        #TC1
        data1 = ['type4', 'tri', '#234252', 23, 23]
        data2 = ['type1', 'tri', '#234252', 23, 23]
        data3 = ['type5', 'asd', '#234252', 23, 23]
        data4 = ['type5', 'tri', '#234252', -1, -1]
        self.type_management.createType(*data1)
        self.assertEqual(list(self.type_management.map_object_types.keys()), ['type1','type2','type4'])
        self.assertEqual(self.type_management.map_object_types['type4'].color,'#234252' )
        self.assertEqual(self.type_management.map_object_types['type4'].shape,'tri' )
        self.assertEqual(self.type_management.map_object_types['type4'].width, 23 )
        self.assertEqual(self.type_management.map_object_types['type4'].height,23 )
        '''
        self.assertEqual(self.db.viewData('color', 'name', 'type4', 'type'), '#234252')
        self.assertEqual(self.db.viewData('shape', 'name', 'type4', 'type'), 'tri')
        self.assertEqual(self.db.viewData('width', 'name', 'type4', 'type'), 23)
        self.assertEqual(self.db.viewData('height', 'name', 'type4', 'type'), 23)
        '''
        #TC2
        with self.assertRaises(KeyError):
            self.type_management.createType(*data2)
        #TC3
        with self.assertRaises(ValueError):
            self.type_management.createType(*data3)
        #TC4
        with self.assertRaises(ValueError):
            self.type_management.createType(*data4)


    def test_updateType(self): 
        #TC1
        data1 = ['type1','ell', 'blue', 2, 56]
        data2 = ['type3','ell', 'blue', 2, 56]
        data3 = ['type1','asd', 'blue', 2, 56]
        data4 = ['type1','ell', 'blue', -1, -1]
        self.assertEqual(self.type_management.updateType( *data1), {1})
        self.assertEqual(self.type_management.map_object_types['type1'].color,'blue' )
        self.assertEqual(self.type_management.map_object_types['type1'].shape,'ell' )
        self.assertEqual(self.type_management.map_object_types['type1'].width, 2 )
        self.assertEqual(self.type_management.map_object_types['type1'].height,56 )
        #TC2
        with self.assertRaises(KeyError):
            self.type_management.updateType(*data2)
        #TC3
        with self.assertRaises(ValueError):
            self.type_management.updateType(*data3)
        #TC4
        with self.assertRaises(ValueError):
            self.type_management.updateType(*data4)
    def test_addObjectConnection(self):
        #TC1
        self.type_management.addObjectConnection('type1', 23)
        self.assertEqual(self.type_management.getObjectSetByName('type1'), {1,23})
        #TC2
        with self.assertRaises(TypeError):
            self.type_management.addObjectConnection('type1', '98')
        #TC3
        with self.assertRaises(KeyError):
            self.type_management.addObjectConnection('type3',45)

    def test_removeObjectConnection(self):
        #TC1
        self.type_management.removeObjectConnection('type1',1)
        self.assertEqual(self.type_management.getObjectSetByName('type1'), set())
        #TC2
        with self.assertRaises(TypeError):
            self.type_management.removeObjectConnection('type1','39')
        #TC3
        with self.assertRaises(KeyError):
            self.type_management.removeObjectConnection('type1',3)
        #TC4
        with self.assertRaises(KeyError):
            self.type_management.removeObjectConnection('type3',1)

    def test_getTypeAttributeByName(self):
        data1 = ( 'type1', 'green', 'ell',100, 100 )
        #TC1
        self.assertEqual(self.type_management.getTypeAttributeByName('type1'),data1[1:])
        #TC2
        with self.assertRaises(KeyError):
            self.type_management.getTypeAttributeByName('type3')
        
    def test_removeAllType(self):
        self.type_management.removeAllType()
        self.assertEqual(self.type_management.map_object_types, {})

    def test_getTypeNameList(self):
        self.assertEqual(self.type_management.getTypeNameList(), ['type1','type2'])


    def test_saveToDB(self):
        data1 = ['type4', 'tri', '#234252', 23, 23]
        self.type_management.createType(*data1)

        self.assertEqual(self.db.viewData('color', 'name', 'type4', 'type'), [])
        self.assertEqual(self.db.viewData('shape', 'name', 'type4', 'type'), [])
        self.assertEqual(self.db.viewData('width', 'name', 'type4', 'type'), [])
        self.assertEqual(self.db.viewData('height', 'name', 'type4', 'type'), [])

        self.type_management.saveToDB()

        self.assertEqual(self.db.viewData('color', 'name', 'type4', 'type'), '#234252')
        self.assertEqual(self.db.viewData('shape', 'name', 'type4', 'type'), 'tri')
        self.assertEqual(self.db.viewData('width', 'name', 'type4', 'type'), 23)
        self.assertEqual(self.db.viewData('height', 'name', 'type4', 'type'), 23)

    def test_collectData(self):

        data1 = ( 'type1', 'ell', 'green', 100, 100 )
        data2 = ( 'type2', 'rec', '#393939', 50, 50 )

        types = []

        types.append( OrderedDict([('name','type1'),('color','green'),('shape','ell'),('width',100.0),('height',100.0 )]))
        types.append( OrderedDict([('name','type2'),('color','#393939'),('shape','rec'),('width',50.0),('height',50.0 )]))

        result = OrderedDict([
            ('object_types', types),
            ])

        self.assertEqual(self.type_management.collectData(), result)

    def test_loadJsonFile(self):
        '''
        {
            "object_types": [
                {
                    "name": "type23",
                    "color": "black",
                    "shape": "tri",
                    "width": 11.0,
                    "height": 11.0
                },
                {
                    "name": "type12",
                    "color": "white",
                    "shape": "rec",
                    "width": 44.0,
                    "height": 44.0
                }
            ],
        }
        '''
        self.type_management.loadJsonFile('test.json')

        self.assertEqual(self.type_management.map_object_types['type23'].color, 'black')
        self.assertEqual(self.type_management.map_object_types['type23'].shape,'tri' )
        self.assertEqual(self.type_management.map_object_types['type23'].width, 11)
        self.assertEqual(self.type_management.map_object_types['type23'].height, 11)

        self.assertEqual(self.type_management.map_object_types['type12'].color,'white' )
        self.assertEqual(self.type_management.map_object_types['type12'].shape,'rec' )
        self.assertEqual(self.type_management.map_object_types['type12'].width, 44 )
        self.assertEqual(self.type_management.map_object_types['type12'].height,44 )


if __name__ == '__main__':
    unittest.main()


