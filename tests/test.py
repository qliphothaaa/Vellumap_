import unittest
from model.map_object import MapObject
from model.map_object_type import ObjectType
 
class TestMapObject(unittest.TestCase):
    def setUp(self):
        self.testType = ObjectType('typetree', 'red', 'rect', 100, 100)
        self.testType2 = ObjectType('typeBuilding', 'green', 'ell', 50, 50)
        self.testObject = MapObject('forest', self.testType, 'tree1', False)
        self.testObject2 = MapObject('building', self.testType2, 'as', False)
        self.testObject.setId(0)
        self.testObject2.setId(1)

    def test_getMapInfo(self):
        self.assertEqual(self.testObject.getMapInfo(), (0,'tree1','typetree', '100', '100', 0.0, 0.0, 1)) 
        self.assertEqual(self.testObject2.getMapInfo(), (1,'as','typeBuilding', '50', '50', 0.0, 0.0, 1)) 

    def test_getPosition(self):
        self.assertEqual(self.testObject.getPosition(), (0, 0))
        self.assertEqual(self.testObject2.getPosition(), (0, 0))

    def test_generateSqlForRename(self):
        self.assertEqual(self.testObject.generateSqlForRename('asd'), "Update ObjectGraphic set Name = 'asd' where (id = '0');")
        self.assertEqual(self.testObject2.generateSqlForRename('asdf'), "Update ObjectGraphic set Name = 'asdf' where (id = '1');")

    def test_generateSqlForDelete(self):
        self.assertEqual(self.testObject.generateSqlForDelete(), "Delete from ObjectGraphic where(id = '0');")
        self.assertEqual(self.testObject2.generateSqlForDelete(), "Delete from ObjectGraphic where(id = '1');")

    def test_generateSqlForPosition(self):
        self.assertEqual(self.testObject.generateSqlForUpdatePosition(30, 30), "Update ObjectGraphic set X = %e, y = %e where (id = '0');"% (30, 30))
        self.assertEqual(self.testObject2.generateSqlForUpdatePosition(3, 3), "Update ObjectGraphic set X = %e, y = %e where (id = '1');"% (3, 3))



if __name__ == '__main__':
    unittest.main()
    
