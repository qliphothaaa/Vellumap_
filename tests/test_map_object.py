import unittest
from model.map_object import MapObject
from tests.fake_db import FakeDB


class TestMapObject(unittest.TestCase):
    def setUp(self):
        self.Object1 = MapObject(2, 'test1', 'tree', 10.0, 10.0, 'aaaa')
        self.Object2 = MapObject(3, 'test2', 'human', 320, 302,)
        self.db = FakeDB('test')
    def tearDown(self):
        self.db.clear('objectgraphic')
        self.db.clear('objectdescription')
        
    def addTodatabase(self):
        self.db.accessDatabase(self.Object1.generateSqlForAdd())
        self.db.accessDatabase(self.Object2.generateSqlForAdd())
        self.Object1.object_id = self.db.viewData('id', 'name', 'test1', 'ObjectGraphic')
        self.Object2.object_id = self.db.viewData('id', 'name', 'test2', 'ObjectGraphic')
        self.db.accessDatabase(self.Object1.generateSqlForAddDiscription())
        self.db.accessDatabase(self.Object2.generateSqlForAddDiscription())

    def test_getPosition(self):
        self.assertEqual(self.Object1.getPosition(), (10.0, 10.0))
        self.assertEqual(self.Object2.getPosition(), (320, 302))

    def test_getObjectInfo(self):
        self.assertEqual(self.Object1.getObjectInfo(), (2, 'test1', 'tree', 10.0, 10.0, 'aaaa'))
        self.assertEqual(self.Object2.getObjectInfo(), (3, 'test2', 'human', 320, 302, 'nothing'))

    def test_generateSqlForAdd(self):
        self.addTodatabase()
        self.db.accessDatabase(self.Object1.generateSqlForAdd())
        self.db.accessDatabase(self.Object2.generateSqlForAdd())
        self.assertEqual(self.db.viewData('type', 'name', 'test1', 'ObjectGraphic'), 'tree')
        self.assertEqual(self.db.viewData('type', 'name', 'test2', 'ObjectGraphic'), 'human')
        
    def test_generateSqlForRename(self):
        self.addTodatabase()

        self.Object1.object_name = 'test11'
        self.Object2.object_name = 'test22'
        self.db.accessDatabase(self.Object1.generateSqlForRename()) 
        self.db.accessDatabase(self.Object2.generateSqlForRename())

        self.assertEqual(self.db.viewData('type', 'name', 'test11', 'ObjectGraphic'), 'tree')
        self.assertEqual(self.db.viewData('type', 'name', 'test22', 'ObjectGraphic'), 'human')


    def test_generateSqlForAddDiscription(self):
        self.addTodatabase()

        self.db.accessDatabase(self.Object1.generateSqlForAddDiscription())
        self.db.accessDatabase(self.Object2.generateSqlForAddDiscription())
        self.assertEqual(self.db.viewData('Description', 'id', self.Object1.object_id, 'ObjectDescription'), 'aaaa')
        self.assertEqual(self.db.viewData('Description', 'id', self.Object2.object_id, 'ObjectDescription'), 'nothing')

            
    def test_generateSqlForChangeDescription(self):
        self.addTodatabase()
        self.Object1.description = 'asdf'
        self.Object2.description = 'qwer'

        self.db.accessDatabase(self.Object1.generateSqlForChangeDescription())
        self.db.accessDatabase(self.Object2.generateSqlForChangeDescription())
        self.assertEqual(self.db.viewData('Description', 'id', self.Object1.object_id, 'ObjectDescription'), 'asdf')
        self.assertEqual(self.db.viewData('Description', 'id', self.Object2.object_id, 'ObjectDescription'), 'qwer')

    def test_generateSqlForUpdatePosition(self):
        self.addTodatabase()
        self.Object1.x = 10
        self.Object1.y = 234
        self.Object2.x = 11
        self.Object2.y = 20
        self.db.accessDatabase(self.Object1.generateSqlForUpdatePosition())
        self.db.accessDatabase(self.Object2.generateSqlForUpdatePosition())

        self.assertEqual(self.db.viewData('x', 'id', self.Object1.object_id, 'ObjectGraphic'), 10)
        self.assertEqual(self.db.viewData('y', 'id', self.Object1.object_id, 'ObjectGraphic'), 234)
        self.assertEqual(self.db.viewData('x', 'id', self.Object2.object_id, 'ObjectGraphic'), 11)
        self.assertEqual(self.db.viewData('y', 'id', self.Object2.object_id, 'ObjectGraphic'), 20)

    def test_generateSqlForDelete(self):
        self.addTodatabase()
        self.db.accessDatabase(self.Object1.generateSqlForDelete())
        self.db.accessDatabase(self.Object2.generateSqlForDelete())

        self.assertEqual(self.db.viewData( '*', 'id', self.Object1.object_id, 'ObjectGraphic'), [])
        self.assertEqual(self.db.viewData( '*', 'id', self.Object2.object_id, 'ObjectGraphic'), [])

    def test_generateSqlForDeleteDescription(self):
        self.addTodatabase()
        self.db.accessDatabase(self.Object1.generateSqlForDeleteDescription())
        self.db.accessDatabase(self.Object2.generateSqlForDeleteDescription())
        self.assertEqual(self.db.viewData('*', 'id', self.Object1.object_id, 'ObjectDescription'), [])
        self.assertEqual(self.db.viewData('*', 'id', self.Object2.object_id, 'ObjectDescription'), [])


if __name__ == '__main__':
    unittest.main()






        

