import unittest
from model.map_object import MapObject
from model.map_object_type import ObjectType
#ahahahahaha
class TestMapObject(unittest.TestCase):
    def setUp(self):
        self.testType = ObjectType('typetree', 'red', 'rect', 100, 100)
        self.testType2 = ObjectType('typeBuilding', 'green', 'ell', 50, 50)
        self.testObject = MapObject('forest', self.testType, 'tree1', False)
        self.testObject2 = MapObject('building', self.testType2, 'as', False)
        self.testObject3 = MapObject('building', self.testType2, 'as2', False)
        self.testObject.setId(0)
        self.testObject2.setId(1)
        self.testObject3.setId(2)

    def test_getAttribute(self):
        self.assertEqual(self.testType.getAttribute(), ('red', 'rect', 100,100))
        self.assertEqual(self.testType2.getAttribute(), ('green', 'ell', 50,50))

    def test_getSize(self):
        self.assertEqual(self.testType.getSize(), (100,100))
        self.assertEqual(self.testType2.getSize(), (50,50))

    def test_getObjects(self):
        self.assertEqual(self.testType.getObjects(), [self.testObject])
        self.assertEqual(self.testType2.getObjects(), [self.testObject2, self.testObject3])

    def test_removeMapObjectConnection(self):
        self.testType.removeMapObjectConnection(self.testObject)
        self.assertEqual(self.testType.getObjects(), [])

    def test_addMapObjectConnection(self):
        self.testType.addMapObjectConnection(self.testObject2)
        self.assertEqual(self.testType.getObjects(), [self.testObject, self.testObject2])


    def test_update(self):
        self.assertEqual(self.testType.getAttribute(), ('red', 'rect', 100,100))
        self.testType.update('new name', 'ell', 'black', 40,40)
        self.assertEqual(self.testType.getAttribute(), ('black', 'ell', 40,40))



if __name__ == '__main__':
    unittest.main()
    
