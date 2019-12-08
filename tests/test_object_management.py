import unittest, json
from model.object_management import ObjectsManagement
from collections import OrderedDict
from tests.fake_db import FakeDB


class TestObjectManagmeent(unittest.TestCase):
    def setUp(self):
        Object1 = (2, 'obj2', 200, 200,'type1', 'obj2Description')
        self.db = FakeDB('test')
        self.db.accessDatabase("insert into ObjectGraphic values (2, 'obj2', 200, 200, 'type1');")
        self.db.accessDatabase("insert into Background values ('full.jpg', 0.0, 0.0, 5.0,'asdf');")
        self.db.accessDatabase("insert into ObjectDescription values(2, 'obj2Description');")

        self.object_management = ObjectsManagement('test.db')

    def tearDown(self):
        self.db.clear('objectgraphic')
        self.db.clear('objectdescription')
        self.db.clear('background')

    def test_loadObjects(self):
        self.assertTrue(2 in self.object_management.map_objects)
        self.assertEqual(self.object_management.map_objects[2].object_name , 'obj2')
        self.assertEqual(self.object_management.map_objects[2].x ,200)
        self.assertEqual(self.object_management.map_objects[2].y ,200)
        self.assertEqual(self.object_management.map_objects[2].description ,'obj2Description')
        self.assertEqual(self.object_management.map_objects[2].object_type_name,'type1')

    def test_loadBackground(self):
        self.assertEqual(self.object_management.map_background.pic_name, 'full.jpg');
        self.assertEqual(self.object_management.map_background.x, 0);
        self.assertEqual(self.object_management.map_background.y, 0);
        self.assertEqual(self.object_management.map_background.rate, 5);
        self.assertEqual(self.object_management.map_background.pic_str, 'asdf');

    def test_renameObject(self):
        self.assertEqual(self.object_management.map_objects[2].object_name, 'obj2')
        
        #TC1
        self.object_management.renameObject(2, 'newname')
        self.assertEqual(self.object_management.map_objects[2].object_name, 'newname')
        #TC2
        with self.assertRaises(ValueError):
            self.object_management.renameObject(2, '')
        #TC3
        with self.assertRaises(KeyError):
            self.object_management.renameObject(45, 'newname')
        #TC4
        with self.assertRaises(TypeError):
            self.object_management.renameObject('asdf', 'newname')
        #TC5
        with self.assertRaises(ValueError):
            self.object_management.renameObject(2, '12345678901')

    def test_changeDescription(self):
        self.assertEqual(self.object_management.map_objects[2].description, 'obj2Description')

        #TC1
        self.object_management.changeDescription(2, 'newdescription')
        self.assertEqual(self.object_management.map_objects[2].description, 'newdescription')
        #TC2
        '''
        with self.assertRaises(ValueError):
            self.object_management.changeDescription(2, '')
        '''
        #TC3
        with self.assertRaises(KeyError):
            self.object_management.changeDescription(5, 'newdescription')
        #TC4
        with self.assertRaises(TypeError):
            self.object_management.changeDescription('asdf', 'newdescription')
        #TC5
        with self.assertRaises(ValueError):
            self.object_management.changeDescription(2, 'a'*101)

    def test_updatePosition(self):
        self.assertEqual(self.object_management.map_objects[2].x, 200.0)
        self.assertEqual(self.object_management.map_objects[2].y, 200.0)

        #TC1
        self.object_management.updatePosition(2, 20, 20)
        self.assertEqual(self.object_management.map_objects[2].x, 20)
        self.assertEqual(self.object_management.map_objects[2].y, 20)
        #TC2
        with self.assertRaises(KeyError):
            self.object_management.updatePosition(5, 20, 20)
        #TC3
        with self.assertRaises(TypeError):
            self.object_management.updatePosition('asdf', 20, 20)
        #TC4
        with self.assertRaises(ValueError):
            self.object_management.updatePosition(2, 'asdf', 'asdf')

    def test_createNewObject(self):
        object_id = self.object_management.createNewObject('type1', 20.0, 20.0)
        self.assertTrue(object_id in self.object_management.map_objects)
        self.assertEqual(self.object_management.map_objects[object_id].x, 20)
        self.assertEqual(self.object_management.map_objects[object_id].y, 20)
        self.assertEqual(self.object_management.map_objects[object_id].object_type_name, 'type1')
        self.assertEqual(self.object_management.map_objects[object_id].object_name, '1_unnamed')
        self.assertEqual(self.object_management.map_objects[object_id].description, 'nothing')

        with self.assertRaises(ValueError):
            self.object_management.createNewObject('3type1', 20.0, 20.0)


    def test_addBackground(self):
        data1 = ('img.jpg', 5.0, -1.0, -1.0)
        data2 = ('img', 5.0, -1.0, -1.0)
        data3 = ('img.jpg', None, -1.0, -1.0)
        data4 = ('img.jpg', 5.0, None, None)
        self.object_management.addBackground(*data1)
        self.assertEqual(self.object_management.map_background.pic_name, 'img.jpg');
        self.assertEqual(self.object_management.map_background.x, -1);
        self.assertEqual(self.object_management.map_background.y, -1);
        self.assertEqual(self.object_management.map_background.rate, 5);
        with self.assertRaises(ValueError):
            self.object_management.addBackground(*data2)

        with self.assertRaises(TypeError):
            self.object_management.addBackground(*data3)

        with self.assertRaises(TypeError):
            self.object_management.addBackground(*data4)
        

    def test_removeBackground(self):
        self.assertNotEqual(self.object_management.map_background, None)
        self.object_management.removeBackground()
        self.assertEqual(self.object_management.map_background, None)


    def test_removeObjectById(self):
        self.assertEqual(len(self.object_management.map_objects), 1)
        type_name = self.object_management.removeObjectById(2)
        self.assertFalse(2 in self.object_management.map_objects)
        self.assertEqual(len(self.object_management.map_objects), 0)

        with self.assertRaises(KeyError):
            self.object_management.removeObjectById(2)
        with self.assertRaises(TypeError):
            self.object_management.removeObjectById('asf')


    def test_clearAllObject(self):
        self.assertEqual(len(self.object_management.map_objects), 1)
        self.object_management.clearAllObject()
        self.assertEqual(len(self.object_management.map_objects), 0)
        self.assertEqual(self.object_management.map_background, None)

    def test_getObjectById(self):

        self.assertEqual(self.object_management.getObjectById(2).object_name, 'obj2')
        with self.assertRaises(KeyError):
            self.object_management.getObjectById(5)
        with self.assertRaises(TypeError):
            self.object_management.getObjectById('asf')

    def test_saveToDB(self):
        self.object_management.createNewObject('type1', 20.0, 20.0)
        self.object_management.saveToDB()
        self.assertEqual(self.db.viewData('x', 'id', 3, 'objectgraphic'), 20)
        self.assertEqual(self.db.viewData('y', 'id', 3, 'objectgraphic'), 20)
        self.assertEqual(self.db.viewData('type', 'id', 3, 'objectgraphic'), 'type1')

    def test_collectData(self):

        objects = OrderedDict([('object_id',2),('name','obj2'),('type','type1'),('x',200.0),('y',200.0 ),('description','obj2Description')])
        background = OrderedDict([('pic_name','full.jpg'),('rate',5.0),('x',0.0),('y', 0.0),('pic_str', 'asdf')])

        result = OrderedDict([
            ('map_objects', [objects]),
            ('background', background)
            ])
        self.assertEqual(self.object_management.collectData(), result)


    def test_loadJsonFile(self):
        '''
        {
            "map_objects": [
                {
                    "object_id": 23,
                    "name": "asdfasdf",
                    "type": "typeplant",
                    "x": 118.0,
                    "y": 47.0,
                    "description": "asdfasdfasdf"
                }
            ],
            "background": {
                "pic_name": "None"
            }
        }
        '''

        self.object_management.loadJsonFile('test.json')

        object_id=23
        self.assertEqual(self.object_management.map_objects[object_id].x, 118)
        self.assertEqual(self.object_management.map_objects[object_id].y, 47)
        self.assertEqual(self.object_management.map_objects[object_id].object_type_name, 'typeplant')
        self.assertEqual(self.object_management.map_objects[object_id].object_name, 'asdfasdf')
        self.assertEqual(self.object_management.map_objects[object_id].description, 'asdfasdfasdf')

if __name__ == '__main__':
    unittest.main()

