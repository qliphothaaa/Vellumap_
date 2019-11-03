import unittest
from model.object_type import ObjectType
from tests.fake_db import FakeDB


class TestType(unittest.TestCase):
    def setUp(self):
        self.db = FakeDB('test')
        self.data1 = ( 'type1', 'green', 'ell', 30, 40 )
        self.Type1 = ObjectType(*self.data1) 
        self.Type1.objects_id_set = {1,2,3}
            

    def tearDown(self):
        self.db.clear('type')

    def test_getAttribute(self):
        self.assertEqual(self.Type1.getAttribute(), self.data1[1:])

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
        #self.assertRaises(TypeError, self.Type1.update, (*test_data02), msg="" )
        with self.assertRaisesRegex(TypeError, 'the width should be int or float'):
            self.Type1.update(*test_data02)
        with self.assertRaisesRegex(TypeError, 'the height should be int or float'):
            self.Type1.update(*test_data03)
        with self.assertRaisesRegex(TypeError, 'the color should be string'):
            self.Type1.update(*test_data04)
        with self.assertRaisesRegex(TypeError, 'the shape should be string'):
            self.Type1.update(*test_data05)

        with self.assertRaisesRegex(ValueError, 'bad value'):
            self.Type1.update(*test_data06)
        with self.assertRaisesRegex(ValueError, 'bad value'):
            self.Type1.update(*test_data07)
        with self.assertRaisesRegex(ValueError, 'bad value'):
            self.Type1.update(*test_data08)
        with self.assertRaisesRegex(ValueError, 'bad value'):
            self.Type1.update(*test_data09)


    def test_getObjectIdSet(self):
        self.assertEqual(self.Type1.getObjectIdSet(), {1,2,3})
        

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
        with self.assertRaisesRegex(TypeError, "id should be int"):
            self.Type1.removeObjectId('asdf')
        with self.assertRaisesRegex(KeyError, "can't find id"):
            self.Type1.removeObjectId(234)
        

        
    def test_generateSqlForAdd(self):
        self.db.accessDatabase(self.Type1.generateSqlForAdd())
        self.assertEqual(self.db.viewData('shape', 'name', self.Type1.type_name, 'type'), 'ell')

    def test_generateSqlForUpdate(self):
        self.db.accessDatabase(self.Type1.generateSqlForAdd())
        data_new = ('black', 'rec', 20, 20)
        self.Type1.update(*data_new)
        self.db.accessDatabase(self.Type1.generateSqlForUpdate())
        self.assertEqual(self.db.viewData('shape', 'name', self.Type1.type_name, 'type'), 'rec')

    def test_generateSqlForDelete(self):
        self.db.accessDatabase(self.Type1.generateSqlForAdd())
        self.db.accessDatabase(self.Type1.generateSqlForDelete())
        self.assertEqual(self.db.viewDataAll('type'),[])
        
if __name__ == '__main__':
    unittest.main()


