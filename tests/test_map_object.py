import unittest
from model.map_object import MapObject
from collections import OrderedDict
#from tests.fake_db import FakeDB

class TestMapObject(unittest.TestCase):
    def setUp(self):
        self.obj1 = MapObject(1, 'test1', 'typetree', 10.0, 10.0, 'aaaa')

    def tearDown(self):
        self.obj1 = MapObject(1, 'test1', 'typetree', 10.0, 10.0, 'aaaa')

    def test_getPosition(self):
        self.assertEqual(self.obj1.getPosition(), (10.0, 10.0))

    def test_getObjectInfo(self):
        self.assertEqual(self.obj1.getObjectInfo(), (1, 'test1', 'typetree', 10, 10, 'aaaa'))

    def test_generateSqlForRename(self):
        self.assertEqual(self.obj1.generateSqlForRename(), ("Update ObjectGraphic set Name = ? where (id = ?);",('test1', 1)))

    def test_generateSqlForChangeDescription(self):
        self.assertEqual(self.obj1.generateSqlForChangeDescription(), ("Update ObjectDescription set Description = ? where (id = ?);",('aaaa', 1)))

    def test_generateSqlForUpdatePosition(self):
        self.assertEqual(self.obj1.generateSqlForUpdatePosition(), ("Update ObjectGraphic set x = ?, y = ? where (id = ?);",(10.0, 10.0, 1)))

    def test_generateSqlForAdd(self):
        self.assertEqual(self.obj1.generateSqlForAdd(), ("insert into ObjectGraphic values (?, ?, ?, ?, ?);",(1, 'test1', 10.0, 10.0, 'typetree')))

    def test_generateSqlForAddDiscription(self):
        self.assertEqual(self.obj1.generateSqlForAddDiscription(), ("insert into ObjectDescription values (?, ?);",(1, 'aaaa')))

    def test_generateSqlForDelete(self):
        self.assertEqual(self.obj1.generateSqlForDelete(), ("Delete from ObjectGraphic where(id = ?);",(1,)))

    def test_generateSqlForDeleteDescription(self):
        self.assertEqual(self.obj1.generateSqlForDeleteDescription(), ("Delete from ObjectDescription where(id = ?);",(1,)))

    def test_serialize(self):
        self.assertEqual(self.obj1.serialize(), OrderedDict([('object_id',1),('name','test1'),('type','typetree'),('x',10.0),('y',10.0 ),('description','aaaa')]))


    def test_deserialize(self):
        self.assertEqual(self.obj1.object_name, 'test1')
        self.assertEqual(self.obj1.object_type_name, 'typetree')
        self.assertEqual(self.obj1.x, 10)
        self.assertEqual(self.obj1.y, 10)
        self.assertEqual(self.obj1.description, 'aaaa')

        data = {'name':'newname', 'type':'newtype', 'x': 0.0, 'y':0.0, 'description':'bbbb'}

        self.obj1.deserialize(data)

        self.assertEqual(self.obj1.object_name, 'newname')
        self.assertEqual(self.obj1.object_type_name, 'newtype')
        self.assertEqual(self.obj1.x, 0.0)
        self.assertEqual(self.obj1.y, 0.0)
        self.assertEqual(self.obj1.description, 'bbbb')

