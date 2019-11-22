import unittest
import sys
from PyQt5.QtWidgets import QApplication
from tests.fake_db import FakeDB
from model.scene import Scene

class TestScene(unittest.TestCase):
    app = QApplication(sys.argv)
    def setUp(self):
        self.db = FakeDB('test')
        self.dbAddType()
        self.dbAddObject()
        self.scene = Scene('test')


    def dbAddType(self):
        data1 = ( 'type1', 'ell', 'green', 10, 10 )
        data2 = ( 'type2', 'rect', 'yellow', 20, 20 )
        data3 = ( 'type3', 'tri', 'black', 30, 30)
        type_list = [data1, data2, data3]
        for item in type_list:
            self.db.accessDatabase("insert into type values ('%s', '%s', '%s', %s, %s);"% (*item,))

    def dbAddObject(self):
        Object1 = ( 'test1', 10.0, 10.0, 'type2', 'test1Description')
        Object2 = ( 'test2',  320,  302, 'type1', 'test2Description')
        Object3 = ( 'test3',  500,  400, 'type3', 'test3Description')
        object_list = [Object1, Object2, Object3]
        for item in object_list:
            self.db.accessDatabase("insert into ObjectGraphic values (null, '%s', %s, %s, '%s');"% (*item[:4],))

        self.id1 = self.db.viewData('id', 'name', 'test1', 'ObjectGraphic')
        self.id2 = self.db.viewData('id', 'name', 'test2', 'ObjectGraphic')
        self.id3 = self.db.viewData('id', 'name', 'test3', 'ObjectGraphic')

        self.db.accessDatabase("insert into ObjectDescription values(%s, '%s')" % (self.id1, Object1[4]))
        self.db.accessDatabase("insert into ObjectDescription values(%s, '%s')" % (self.id2, Object2[4]))
        self.db.accessDatabase("insert into ObjectDescription values(%s, '%s')" % (self.id3, Object3[4]))

        self.db.accessDatabase("insert into Background values ('img.jpg', 5, 5, 5)")


    def tearDown(self):
        self.db.clear('objectgraphic')
        self.db.clear('objectdescription')
        self.db.clear('type')
        self.db.clear('background')


    def test_initManagements(self):
        self.assertEqual(len(self.scene.graphics_management.graphics), 3)
        self.assertNotEqual(self.scene.types_management, None)
        self.assertNotEqual(self.scene.object_management, None)
        self.assertNotEqual(self.scene.graphics_management, None)
        self.assertEqual(len(self.scene.types_management.map_object_types), 3)
        self.assertEqual(len(self.scene.object_management.map_objects), 3)
        self.assertEqual(len(self.scene.graphics_management.graphics), 3)
        self.assertTrue(self.id1 in self.scene.types_management.getObjectSetByName('type2'))
        self.assertTrue(self.id2 in self.scene.types_management.getObjectSetByName('type1'))
        self.assertTrue(self.id3 in self.scene.types_management.getObjectSetByName('type3'))
    

    def test_loadGraphics(self):
        item_id_list = []
        for item in self.scene.gr_scene.items():
            if item.object_id > 0:
                item_id_list.append(item.object_id)
        for object_id in item_id_list:
            self.assertTrue(object_id in self.scene.object_management.map_objects)
            self.assertTrue(object_id in self.scene.graphics_management.graphics)

    def test_removeObject(self):
        self.scene.removeObject(self.id1)
        self.assertEqual(self.scene.types_management.getObjectSetByName('type2'),set())
        self.assertEqual(self.scene.types_management.getObjectSetByName('type1'), {self.id2})
        self.assertEqual(self.scene.types_management.getObjectSetByName('type3'), {self.id3})
        self.scene.removeObject(self.id3)
        self.assertEqual(self.scene.types_management.getObjectSetByName('type3'), set())

        self.assertTrue(self.id2 in self.scene.object_management.map_objects)
        self.assertFalse(self.id1 in self.scene.object_management.map_objects)
        self.assertFalse(self.id3 in self.scene.object_management.map_objects)

        self.assertTrue(self.id2 in self.scene.graphics_management.graphics)
        self.assertFalse(self.id1 in self.scene.graphics_management.graphics)
        self.assertFalse(self.id3 in self.scene.graphics_management.graphics)

        item_id_list = []
        for item in self.scene.gr_scene.items():
            item_id_list.append(item.object_id)
        item_id_list.remove(-1)
        item_id_list.remove(-2)
        self.assertEqual(item_id_list, [self.id2])
        self.assertEqual(self.db.viewDataAll('objectgraphic'),[(self.id2, 'test2', 320, 302, 'type1')])
        self.assertEqual(self.db.viewData('type', 'name', 'test1', 'objectgraphic'), [])
        self.assertEqual(self.db.viewData('Description', 'id', self.id2, 'ObjectDescription'), 'test2Description')
        self.assertEqual(self.db.viewData('Description', 'id', self.id3, 'ObjectDescription'), [])


    def test_updatePosition(self):
        self.scene.updatePosition(self.id1, 1.0, 1.0)
        self.assertEqual(self.scene.object_management.map_objects[self.id1].x, 1)
        self.assertEqual(self.scene.object_management.map_objects[self.id1].y, 1)
        self.assertEqual(self.db.viewData('x', 'id', self.id1, 'ObjectGraphic'), 1)
        self.assertEqual(self.db.viewData('y', 'id', self.id1, 'ObjectGraphic'), 1)


    def test_createNewObject(self):
        object_id = self.scene.createNewObject('type2', 23, 67)
        object_type_data = self.scene.types_management.getTypeAttributeByName('type2')
        obj = self.scene.object_management.getObjectById(object_id)
        self.assertEqual(obj.object_type_name, 'type2')
        self.assertEqual(obj.x, 23)
        self.assertEqual(obj.y, 67)
        self.assertTrue(object_id in self.scene.types_management.getObjectSetByName('type2'))
        self.assertTrue(object_id in self.scene.graphics_management.graphics)

    def test_renameObject(self):
        self.scene.renameObject(self.id1, 'rename')
        self.assertEqual(self.scene.object_management.getObjectById(self.id1).object_name, 'rename')

    def test_changeDescription(self):
        self.scene.changeDescription(self.id1, 'changeDescription')
        self.assertEqual(self.scene.object_management.getObjectById(self.id1).description, 'changeDescription')

    def test_removeType(self):
        self.assertEqual(self.scene.removeType('type1'), {self.id2})
        self.assertFalse(self.id2 in self.scene.object_management.map_objects)
        self.assertFalse(self.id2 in self.scene.graphics_management.graphics)
        item_id_list = []
        for item in self.scene.gr_scene.items():
            item_id_list.append(item.object_id)
        self.assertFalse(self.id2 in item_id_list)

    def test_createNewType(self):
        self.scene.createNewType('typeNew', 'rect', '#fasdfa', 40, 20)
        self.assertEqual(self.scene.types_management.getTypeAttributeByName('typeNew'), ('#fasdfa', 'rect', 40, 20))

    def test_updateType(self):
        data1 = ( 'type1', 'ell', 'green', 10, 10 )
        self.scene.updateType('type1', 'tri', 'white', 20,100)
        self.assertEqual(self.scene.graphics_management.graphics[self.id2].width, 20)
        self.assertEqual(self.scene.graphics_management.graphics[self.id2].height, 100)
        self.assertEqual(self.scene.graphics_management.graphics[self.id2].shape, 'tri')

    def test_getTypeNameList(self):
        self.assertEqual(self.scene.getTypeNameList(), ['type1','type2','type3'])
        self.scene.createNewType('typeNew', 'rect', '#fasdfa', 40, 20)
        self.assertEqual(self.scene.getTypeNameList(), ['type1','type2','type3','typeNew'])

    def test_filterGraphicsByType(self):
        self.scene.filterGraphicsByType('type1', False)
        self.assertEqual(self.scene.graphics_management.graphics[self.id2].isVisible(), False)
        self.assertEqual(self.scene.graphics_management.graphics[self.id3].isVisible(), True)
        self.scene.filterGraphicsByType('type1', True)
        self.assertEqual(self.scene.graphics_management.graphics[self.id2].isVisible(), True)

if __name__ == '__main__':
    unittest.main()

