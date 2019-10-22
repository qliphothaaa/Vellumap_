import unittest
from model.object_management import ObjectsManagement
from tests.fake_db import FakeDB


class TestObjectManagmeent(unittest.TestCase):
    def setUp(self):
        Object1 = ( 'test1', 10.0, 10.0,'tree', 'test1Description')
        Object2 = ( 'test2',  320, 302,'human', 'test2Description')
        self.db = FakeDB('test')
        self.db.accessDatabase("insert into ObjectGraphic values (null, '%s', %s, %s, '%s');"% (*Object1[:4],))
        self.db.accessDatabase("insert into ObjectGraphic values (null, '%s', %s, %s, '%s');"% (*Object2[:4],))
        self.id1 = self.db.viewData('id', 'name', 'test1', 'ObjectGraphic')
        self.id2 = self.db.viewData('id', 'name', 'test2', 'ObjectGraphic')
        self.db.accessDatabase("insert into ObjectDescription values(%s, '%s')" % (self.id1, Object1[4]))
        self.db.accessDatabase("insert into ObjectDescription values(%s, '%s')" % (self.id2, Object2[4]))

        self.object_management = ObjectsManagement('test')
        pass


    def tearDown(self):
        self.db.clear('objectgraphic')
        self.db.clear('objectdescription')

    def test_loadObjects(self):
        self.assertTrue(self.id1 in self.object_management.map_objects)
        self.assertTrue(self.id2 in self.object_management.map_objects)

    def test_loadBackground(self):
        self.assertEqual(self.object_management.map_background.pic_name, 'img.jpg');
        self.assertEqual(self.object_management.map_background.x, 5);
        self.assertEqual(self.object_management.map_background.y, 5);
        self.assertEqual(self.object_management.map_background.rate, 5);

    def test_renameObject(self):
        self.assertEqual(self.object_management.map_objects[self.id1].object_name, 'test1')
        self.assertEqual(self.object_management.map_objects[self.id2].object_name, 'test2')

        self.object_management.renameObject(self.id1, 'rename1')
        self.assertEqual(self.object_management.map_objects[self.id1].object_name, 'rename1')
        self.assertEqual(self.db.viewData('name', 'id', self.id1, 'objectgraphic'), 'rename1')

        self.object_management.renameObject(self.id2, 'rename2')
        self.assertEqual(self.object_management.map_objects[self.id2].object_name, 'rename2')
        self.assertEqual(self.db.viewData('name', 'id', self.id2, 'objectgraphic'), 'rename2' )

    def test_changeDescription(self):
        self.assertEqual(self.object_management.map_objects[self.id1].description, 'test1Description')
        self.assertEqual(self.object_management.map_objects[self.id2].description, 'test2Description')

        self.object_management.changeDescription(self.id1, 'changeDescri1')
        self.assertEqual(self.object_management.map_objects[self.id1].description, 'changeDescri1')
        self.assertEqual(self.db.viewData('description', 'id', self.id1, 'objectdescription'), 'changeDescri1')

        self.object_management.changeDescription(self.id2, 'changeDescri2')
        self.assertEqual(self.object_management.map_objects[self.id2].description, 'changeDescri2')
        self.assertEqual(self.db.viewData('description', 'id', self.id2, 'objectdescription'), 'changeDescri2')

    def test_updatePosition(self):
        self.assertEqual(self.object_management.map_objects[self.id1].x, 10.0)
        self.assertEqual(self.object_management.map_objects[self.id1].y, 10.0)
        self.assertEqual(self.object_management.map_objects[self.id2].x, 320.0)
        self.assertEqual(self.object_management.map_objects[self.id2].y, 302.0)
        self.object_management.updatePosition(self.id1, 20, 30)
        self.object_management.updatePosition(self.id2, 200, 300)
        self.assertEqual(self.object_management.map_objects[self.id1].x, 20.0)
        self.assertEqual(self.object_management.map_objects[self.id1].y, 30.0)
        self.assertEqual(self.object_management.map_objects[self.id2].x, 200.0)
        self.assertEqual(self.object_management.map_objects[self.id2].y, 300.0)
        self.assertEqual(self.db.viewData('x', 'id', self.id1, 'objectgraphic'), 20)
        self.assertEqual(self.db.viewData('x', 'id', self.id2, 'objectgraphic'), 200)
        self.assertEqual(self.db.viewData('y', 'id', self.id1, 'objectgraphic'), 30)
        self.assertEqual(self.db.viewData('y', 'id', self.id2, 'objectgraphic'), 300)

    def test_createNewObject(self):
        self.assertEqual(len(self.object_management.map_objects), 2)
        object_id = self.object_management.createNewObject('typeHell', 33, 34)
        self.assertTrue(object_id in self.object_management.map_objects)
        self.assertEqual(self.object_management.map_objects[object_id].x, 33)
        self.assertEqual(self.object_management.map_objects[object_id].y, 34)
        self.assertEqual(self.object_management.map_objects[object_id].object_type_name, 'typeHell')
        self.assertEqual(self.object_management.map_objects[object_id].object_name, 'Hell_unnamed')
        self.assertEqual(self.object_management.map_objects[object_id].description, 'nothing')
        self.assertEqual(len(self.object_management.map_objects), 3)

        self.assertEqual(self.db.viewData('x', 'id', object_id, 'objectgraphic') , 33)
        self.assertEqual(self.db.viewData('y', 'id', object_id, 'objectgraphic') , 34)
        self.assertEqual(self.db.viewData('type', 'id', object_id, 'objectgraphic') , 'typeHell')
        self.assertEqual(self.db.viewData('name', 'id', object_id, 'objectgraphic') , 'Hell_unnamed')
        self.assertEqual(self.db.viewData('description', 'id', object_id, 'objectdescription') , 'nothing')

    def test_removeObjectById(self):
        self.assertEqual(len(self.object_management.map_objects), 2)
        type_name = self.object_management.removeObjectById(self.id1)
        self.assertEqual(type_name, 'tree')
        self.assertFalse(self.id1 in self.object_management.map_objects)
        self.assertEqual(len(self.object_management.map_objects), 1)

        self.assertEqual(self.db.viewData('name', 'id', self.id1, 'objectgraphic') , [])
        self.assertEqual(self.db.viewData('name', 'id', self.id2, 'objectgraphic') , 'test2')

        self.assertEqual(len(self.object_management.map_objects), 1)
        type_name = self.object_management.removeObjectById(self.id2)
        self.assertEqual(type_name, 'human')
        self.assertFalse(self.id2 in self.object_management.map_objects)
        self.assertEqual(len(self.object_management.map_objects), 0)

        self.assertEqual(self.db.viewData('name', 'id', self.id1, 'objectgraphic') , [])
        self.assertEqual(self.db.viewData('name', 'id', self.id2, 'objectgraphic') , [])


    def test_clearAllObject(self):
        self.assertEqual(len(self.object_management.map_objects), 2)
        self.object_management.clearAllObject()
        self.assertEqual(len(self.object_management.map_objects), 0)
        self.assertEqual(self.object_management.map_background, None)
        self.assertEqual(self.db.viewData('name', 'id', self.id1, 'objectgraphic') , 'test1')
        self.assertEqual(self.db.viewData('name', 'id', self.id2, 'objectgraphic') , 'test2')

    def test_getObjectById(self):
        object1 = self.object_management.getObjectById(self.id1)
        object2 = self.object_management.getObjectById(self.id2)
        object1.object_name = 'test1'
        object1.x = 10
        object1.y = 10
        object1.object_type_name = 'tree'
        object2.object_name = 'test2'
        object1.x = 320
        object1.y = 302
        object1.object_type_name = 'human'

    '''
    def test_addBackground(self):

        pass

    def test_removeBackground(self):
        pass
    '''

if __name__ == '__main__':
    unittest.main()
