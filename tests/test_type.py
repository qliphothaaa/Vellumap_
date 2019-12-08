import unittest
from collections import OrderedDict
from model.object_type import ObjectType

class TestType(unittest.TestCase):
    def setUp(self):
        self.data1 = ( 'type1', 'green', 'ell', 30, 40 )
        self.Type1 = ObjectType(*self.data1)
        self.Type1.objects_id_set = {1,2,3}

    def tearDown(self):
        self.Type1 = ObjectType(*self.data1)
        self.Type1.objects_id_set = {1,2,3}

    def test_getAttribute(self):
        self.assertEqual(self.Type1.getAttribute(), self.data1[1:])

    def test_getObjectIdSet(self):
        self.assertEqual(self.Type1.getObjectIdSet(), {1,2,3})

    def test_update(self):
        test_data01 = ('black', 'rec', 20, 20)
        test_data02 = ('black', 'rec', '20', 20)
        test_data03 = ('black', 'rec', 20, '20')
        test_data04 = (23, 'rec', 20, 20)
        test_data05 = ('black', 4, 20, 20)
        test_data06 = ('black', 'rec', 0, 20)
        test_data07 = ('black', 'rec', 20, 0)
        test_data08 = ('black', 'rec', -1, 20)
        test_data09 = ('black', 'rec', 20, -1)
        self.Type1.update(*test_data01 )
        self.assertEqual(self.Type1.getAttribute(),test_data01)
        with self.assertRaises(TypeError):
            self.Type1.update(*test_data02 )
        with self.assertRaises(TypeError):
            self.Type1.update(*test_data03 )
        with self.assertRaises(TypeError):
            self.Type1.update(*test_data04 )
        with self.assertRaises(TypeError):
            self.Type1.update(*test_data05 )
        with self.assertRaises(ValueError):
            self.Type1.update(*test_data06 )
        with self.assertRaises(ValueError):
            self.Type1.update(*test_data07 )
        with self.assertRaises(ValueError):
            self.Type1.update(*test_data08 )
        with self.assertRaises(ValueError):
            self.Type1.update(*test_data09 )

    def test_addObjectId(self):
        self.Type1.addObjectId(12)
        self.assertEqual(self.Type1.getObjectIdSet(), {1,2,3,12})
        self.Type1.objects_id_set = {1,2,3}
        with self.assertRaisesRegex(TypeError, 'id should be int'):
            self.Type1.addObjectId('asdf')
        self.Type1.objects_id_set = {1,2,3}
        self.Type1.addObjectId(1)
        self.assertEqual(self.Type1.getObjectIdSet(), {1,2,3})

    def test_removeObjectId(self):

        self.Type1.removeObjectId(1)
        self.assertEqual(self.Type1.getObjectIdSet(), {2,3})
        with self.assertRaises(TypeError):
            self.Type1.removeObjectId('asdf')
        with self.assertRaises(KeyError):
            self.Type1.removeObjectId(234)

    def test_generateSqlForAdd(self):
        self.assertEqual(self.Type1.generateSqlForAdd(), ("insert into type values(?, ?, ?, ?, ?)",('type1', 'ell', 'green', 30, 40)))

    def test_generateSqlForUpdate(self):
        self.assertEqual(self.Type1.generateSqlForUpdate(), ("Update type set Shape = ?, color = ?, width = ?, height = ? where name = ?",('ell', 'green',30,40,'type1')))

    def test_generateSqlForDelete(self):
        self.assertEqual(self.Type1.generateSqlForDelete(), ("Delete from type where (name = ?)",('type1')))



    def test_serialize(self):
        self.assertEqual(self.Type1.serialize(), OrderedDict([('name','type1'),('color','green'),('shape','ell'),('width', 30),('height', 40)]))

    def test_deserialize(self):
        data = {'name':'type2', 'color':'red', 'shape': 'rect', 'width': 10, 'height':10}

        self.type_name = data['name']
        self.color = data['color']
        self.shape = data['shape']
        self.width = data['width']
        self.height = data['height']
        
        self.assertEqual(self.Type1.type_name, 'type1')
        self.assertEqual(self.Type1.color, 'green')
        self.assertEqual(self.Type1.shape, 'ell')
        self.assertEqual(self.Type1.width, 30)
        self.assertEqual(self.Type1.height, 40)

        self.Type1.deserialize(data)

        self.assertEqual(self.Type1.type_name, 'type2')
        self.assertEqual(self.Type1.color, 'red')
        self.assertEqual(self.Type1.shape, 'rect')
        self.assertEqual(self.Type1.width, 10)
        self.assertEqual(self.Type1.height, 10)
