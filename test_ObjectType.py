import unittest
from model.map_object_type import ObjectType
 
class TestType(unittest.TestCase):
    def setUp(self):
        self.testType = ObjectType('typetree', 'red', 'rect', 100, 100)
        self.testType2 = ObjectType('typeBuilding', 'green', 'ell', 50, 50)
        self.testType.addMapObjectConnection(12)
        self.testType2.addMapObjectConnection(234)
        

    def test_init(self):
        self.assertEqual(self.testType.type_name, ('typetree'))
        self.assertEqual(self.testType.color, ('red'))
        self.assertEqual(self.testType.shape, ('rect'))
        self.assertEqual(self.testType.width, 100)
        self.assertEqual(self.testType.height, 100)
        self.assertEqual(self.testType.objects, [12])

        self.assertEqual(self.testType2.type_name, ('typeBuilding'))
        self.assertEqual(self.testType2.color, ('green'))
        self.assertEqual(self.testType2.shape, ('ell'))
        self.assertEqual(self.testType2.width, 50)
        self.assertEqual(self.testType2.height, 50)
        self.assertEqual(self.testType2.objects, [234])


    def test_getSize(self):
        self.assertEqual(self.testType.getSize(), (100,100))
        self.assertEqual(self.testType2.getSize(), (50,50))

    def test_getAttribute(self):
        self.assertEqual(self.testType.getAttribute(), ('red', 'rect', 100, 100))
        self.assertEqual(self.testType2.getAttribute(), ('green', 'ell', 50, 50))

    def test_addConnection(self):
        self.testType.addMapObjectConnection(12)
        self.assertEqual(self.testType.objects, [12,12])
        self.testType2.addMapObjectConnection(234)
        self.assertEqual(self.testType2.objects, [234,234])

    def test_removeConnection_success(self):
        self.testType.removeMapObjectConnection(12)
        self.assertEqual(self.testType.objects, [])
        self.testType2.removeMapObjectConnection(234)
        self.assertEqual(self.testType2.objects, [])

    def test_update(self):
        self.testType.update('aaa', '','#2342', '23', '54')
        self.assertEqual(self.testType.type_name, 'aaa')
        self.assertEqual(self.testType.color, '#2342')
        self.assertEqual(self.testType.shape, '')
        self.assertEqual(self.testType.width, '23')
        self.assertEqual(self.testType.height, '54')

if __name__ == '__main__':
    unittest.main()
    
