import unittest
from model.object_management import ObjectsManagement
from tests.fake_db import FakeDB


class TestObjectManagmeent(unittest.TestCase):
    def setUp(self):
        Object1 = ( 'obj2', 200, 200,'type1', 'obj2Description')
        self.db = FakeDB('test')
        self.db.accessDatabase("insert into ObjectGraphic values (null, '%s', %s, %s, '%s');"% (*Object1[:4],))
        self.db.accessDatabase("insert into Background values ('full.jpg', 0.0, 0.0, 5.0)")
        id1 = self.db.viewData('id', 'name', 'obj2', 'ObjectGraphic')
        self.db.accessDatabase("insert into ObjectDescription values(%s, '%s')" % (id1, Object1[4]))
        self.object_management = ObjectsManagement('test')

    def tearDown(self):
        self.db.clear('objectgraphic')
        self.db.clear('objectdescription')
        self.db.clear('background')

    def test_loadObjects(self):
        id1 = self.db.viewData('id', 'name', 'obj2', 'ObjectGraphic')
        self.assertTrue(id1 in self.object_management.map_objects)
        self.assertEqual(self.object_management.map_objects[id1].object_name , 'obj2')
        self.assertEqual(self.object_management.map_objects[id1].x ,200)
        self.assertEqual(self.object_management.map_objects[id1].y ,200)
        self.assertEqual(self.object_management.map_objects[id1].description ,'obj2Description')
        self.assertEqual(self.object_management.map_objects[id1].object_type_name,'type1')

    def test_loadBackground(self):
        self.assertEqual(self.object_management.map_background.pic_name, 'full.jpg');
        self.assertEqual(self.object_management.map_background.x, 0);
        self.assertEqual(self.object_management.map_background.y, 0);
        self.assertEqual(self.object_management.map_background.rate, 5);

    def test_renameObject(self):
        id1 = self.db.viewData('id', 'name', 'obj2', 'ObjectGraphic')
        self.assertEqual(self.object_management.map_objects[id1].object_name, 'obj2')
        
        #TC1
        self.object_management.renameObject(id1, 'newname')
        self.assertEqual(self.object_management.map_objects[id1].object_name, 'newname')
        self.assertEqual(self.db.viewData('name', 'id', id1, 'objectgraphic'), 'newname')
        #TC2
        with self.assertRaisesRegex(ValueError, 'name is empty'):
            self.object_management.renameObject(id1, '')
        #TC3
        with self.assertRaisesRegex(KeyError, "can't find id"):
            self.object_management.renameObject(45, 'newname')
        #TC4
        with self.assertRaisesRegex(TypeError, 'id should be int'):
            self.object_management.renameObject('asdf', 'newname')
        #TC5
        with self.assertRaisesRegex(ValueError, 'name should be less then 10 char'):
            self.object_management.renameObject(id1, '12345678901')

    def test_changeDescription(self):
        id1 = self.db.viewData('id', 'name', 'obj2', 'ObjectGraphic')
        self.assertEqual(self.object_management.map_objects[id1].description, 'obj2Description')

        #TC1
        self.object_management.changeDescription(id1, 'newdescription')
        self.assertEqual(self.object_management.map_objects[id1].description, 'newdescription')
        self.assertEqual(self.db.viewData('description', 'id', id1, 'objectdescription'), 'newdescription')
        #TC2
        with self.assertRaisesRegex(ValueError, 'description is empty'):
            self.object_management.changeDescription(id1, '')
        #TC3
        with self.assertRaisesRegex(KeyError, "can't find id"):
            self.object_management.changeDescription(3, 'newdescription')
        #TC4
        with self.assertRaisesRegex(TypeError, 'id should be int'):
            self.object_management.changeDescription('asdf', 'newdescription')
        #TC5
        with self.assertRaisesRegex(ValueError, 'description should be less then 100 char'):
            self.object_management.changeDescription(id1, 'a'*101)

    def test_updatePosition(self):
        id1 = self.db.viewData('id', 'name', 'obj2', 'ObjectGraphic')
        self.assertEqual(self.object_management.map_objects[id1].x, 200.0)
        self.assertEqual(self.object_management.map_objects[id1].y, 200.0)

        #TC1
        self.object_management.updatePosition(id1, 20, 20)
        self.assertEqual(self.object_management.map_objects[id1].x, 20)
        self.assertEqual(self.object_management.map_objects[id1].y, 20)
        self.assertEqual(self.db.viewData('x', 'id',id1, 'objectgraphic'), 20)
        self.assertEqual(self.db.viewData('y', 'id',id1, 'objectgraphic'), 20)
        #TC2
        with self.assertRaisesRegex(KeyError, "can't find id"):
            self.object_management.updatePosition(3, 20, 20)
        #TC3
        with self.assertRaisesRegex(TypeError, 'id should be int'):
            self.object_management.updatePosition('asdf', 20, 20)
        #TC4
        with self.assertRaisesRegex(ValueError, 'position should be int or float'):
            self.object_management.updatePosition(id1, 'asdf', 'asdf')

    def test_createNewObject(self):
        object_id = self.object_management.createNewObject('type1', 100.0, 100.0)
        self.assertTrue(object_id in self.object_management.map_objects)
        self.assertEqual(self.object_management.map_objects[object_id].x, 100)
        self.assertEqual(self.object_management.map_objects[object_id].y, 100)
        self.assertEqual(self.object_management.map_objects[object_id].object_type_name, 'type1')
        self.assertEqual(self.object_management.map_objects[object_id].object_name, '1_unnamed')
        self.assertEqual(self.object_management.map_objects[object_id].description, 'nothing')

        self.assertEqual(self.db.viewData('x', 'id', object_id, 'objectgraphic') , 100)
        self.assertEqual(self.db.viewData('y', 'id', object_id, 'objectgraphic') , 100)
        self.assertEqual(self.db.viewData('type', 'id', object_id, 'objectgraphic') , 'type1')
        self.assertEqual(self.db.viewData('name', 'id', object_id, 'objectgraphic') , '1_unnamed')
        self.assertEqual(self.db.viewData('description', 'id', object_id, 'objectdescription') , 'nothing')

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
        with self.assertRaisesRegex(ValueError, 'cannot find the pic'):
            self.object_management.addBackground(*data2)

        with self.assertRaisesRegex(TypeError, 'rate should be float'):
            self.object_management.addBackground(*data3)

        with self.assertRaisesRegex(TypeError, 'position should be float'):
            self.object_management.addBackground(*data4)
        

    def test_removeBackground(self):
        self.assertNotEqual(self.object_management.map_background, None)
        self.object_management.removeBackground()
        self.assertEqual(self.object_management.map_background, None)


    def test_removeObjectById(self):
        id1 = self.db.viewData('id', 'name', 'obj2', 'ObjectGraphic')
        self.assertEqual(len(self.object_management.map_objects), 1)
        type_name = self.object_management.removeObjectById(id1)
        self.assertFalse(id1 in self.object_management.map_objects)
        self.assertEqual(len(self.object_management.map_objects), 0)

        with self.assertRaisesRegex(KeyError, "can't find id"):
            self.object_management.removeObjectById(3)
        with self.assertRaisesRegex(TypeError, 'id should be int'):
            self.object_management.removeObjectById('asf')


    def test_clearAllObject(self):
        self.assertEqual(len(self.object_management.map_objects), 1)
        self.object_management.clearAllObject()
        self.assertEqual(len(self.object_management.map_objects), 0)
        self.assertEqual(self.object_management.map_background, None)

    def test_getObjectById(self):
        id1 = self.db.viewData('id', 'name', 'obj2', 'ObjectGraphic')

        self.assertEqual(self.object_management.getObjectById(id1).object_name, 'obj2')
        with self.assertRaisesRegex(KeyError, "can't find id"):
            self.object_management.getObjectById(3)
        with self.assertRaisesRegex(TypeError, 'id should be int'):
            self.object_management.getObjectById('asf')

if __name__ == '__main__':
    unittest.main()
