import unittest
from model.map_object import MapObject
from model.map_object_type import ObjectType

class TestMapObject(unittest.TestCase):
    def setUp(self):
        self.testObject1 = MapObject('map1', 'type_tree', 'asdf', False, 'descr1')
        self.testObject2 = MapObject('map2', 'type_build', 'as2', False)
        self.testObject1.id = 1
        self.testObject2.id = 2
        self.testObject1.generateGraphic('color1', 'rec', 34, 54)
        self.testObject2.generateGraphic('color2', 'ell', 89, 12)
        self.testObject1.setPosition(12, 43)
        self.testObject2.setPosition(223, 9845)

    def test_init(self):
        self.assertEqual(self.testObject1.id, 1)
        self.assertEqual(self.testObject1.object_name, 'asdf')
        self.assertEqual(self.testObject1.x,12)
        self.assertEqual(self.testObject1.y,43)
        self.assertEqual(self.testObject1.width, 34)
        self.assertEqual(self.testObject1.height, 54)
        self.assertEqual(self.testObject1.object_type_name, 'type_tree')
        self.assertEqual(self.testObject1.description, 'descr1')
        self.assertEqual(self.testObject1.map_name, 'map1')
        self.assertEqual(self.testObject1.table_name, 'ObjectGraphic')

    def test_getinfo(self):
        self.assertEqual(self.testObject1.getObjectInfo(), (1, 'asdf','type_tree', '34', '54', 12, 43, 'descr1'))

    def test_updateGr(self):
        self.testObject1.updateGr('red', 'rect', 100, 300)
        self.assertEqual(self.testObject1.grMapObject.shape, 'rect')
        self.assertEqual(self.testObject1.grMapObject.width, 100)
        self.assertEqual(self.testObject1.grMapObject.height, 300)

if __name__ == '__main__':
    unittest.main()
