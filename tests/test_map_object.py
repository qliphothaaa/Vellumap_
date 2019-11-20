import unittest
from model.map_object import MapObject
from tests.fake_db import FakeDB


class TestMapObject(unittest.TestCase):
    def setUp(self):
        self.obj1 = MapObject(1, 'test1', 'typetree', 10.0, 10.0, 'aaaa')
        self.db = FakeDB('test')

    def tearDown(self):
        self.db.clear('objectgraphic')
        self.db.clear('objectdescription')

    def test_getPosition(self):
        self.assertEqual(self.obj1.getPosition(), (10.0, 10.0))

    def test_getObjectInfo(self):
        self.assertEqual(self.obj1.getObjectInfo(), (1, 'test1', 'typetree', 10, 10, 'aaaa'))

    def test_generateSqlForAdd(self):
        sql = self.obj1.generateSqlForAdd()
        self.db.accessDatabase(sql)
        self.assertEqual(self.db.viewData('type', 'name', 'test1', 'ObjectGraphic'), 'typetree')
        self.assertAlmostEqual(self.db.viewData('x', 'name', 'test1', 'ObjectGraphic'), 10)
        self.assertAlmostEqual(self.db.viewData('y', 'name', 'test1', 'ObjectGraphic'), 10)
        
    def test_generateSqlForRename(self):
        self.assertEqual(self.obj1.generateSqlForRename(), "Update ObjectGraphic set Name = 'test1' where (id = 1);")

    def test_generateSqlForAddDiscription(self):
        sql = self.obj1.generateSqlForAddDiscription()
        self.assertEqual(self.obj1.generateSqlForAddDiscription(), "insert into ObjectDescription values (1, 'aaaa');")
        self.db.accessDatabase(sql)
        self.assertEqual(self.db.viewData('Description', 'id', 1, 'ObjectDescription'), 'aaaa')

            
    def test_generateSqlForChangeDescription(self):
        self.db.accessDatabase(self.obj1.generateSqlForAddDiscription())
        self.assertEqual(self.db.viewData('Description', 'id', 1, 'ObjectDescription'), 'aaaa')
        self.obj1.description = 'asdf'
        self.db.accessDatabase(self.obj1.generateSqlForChangeDescription())
        self.assertEqual(self.db.viewData('Description', 'id', 1, 'ObjectDescription'), 'asdf')

    def test_generateSqlForUpdatePosition(self):
        self.db.accessDatabase(self.obj1.generateSqlForAdd())
        self.assertAlmostEqual(self.db.viewData('x', 'name', 'test1', 'ObjectGraphic'), 10)
        self.assertAlmostEqual(self.db.viewData('y', 'name', 'test1', 'ObjectGraphic'), 10)
        self.obj1.object_id = self.db.viewData('id', 'name', 'test1', 'ObjectGraphic')
        self.obj1.x = 10.0
        self.obj1.y = 234.0
        self.db.accessDatabase(self.obj1.generateSqlForUpdatePosition())
        self.assertAlmostEqual(self.db.viewData('x', 'name', 'test1', 'ObjectGraphic'), 10)
        self.assertAlmostEqual(self.db.viewData('y', 'name', 'test1', 'ObjectGraphic'), 234)

    def test_generateSqlForDelete(self):
        self.assertEqual(self.obj1.generateSqlForDelete(), "Delete from ObjectGraphic where(id = 1);")

    def test_generateSqlForDeleteDescription(self):
        self.assertEqual(self.obj1.generateSqlForDeleteDescription(), "Delete from ObjectDescription where(id = 1);")


if __name__ == '__main__':
    unittest.main()






        

