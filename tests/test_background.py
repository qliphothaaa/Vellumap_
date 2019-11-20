import unittest
from model.background import MapBackground
from tests.fake_db import FakeDB


class TestBackground(unittest.TestCase):
    def setUp(self):
        self.background1 =  MapBackground('full.jpg', 2.0, 0.0, 0.0)
        self.db = FakeDB('test')

    def tearDown(self):
        self.db.clear('background')

    def test_generateSqlForAdd(self):
        self.db.accessDatabase(self.background1.generateSqlForAdd()) 
        self.assertEqual(self.db.viewData('size_rate', 'name', 'full.jpg', 'background'), 2)
        self.assertEqual(self.db.viewData('x', 'name', 'full.jpg', 'background'), 0)
        self.assertEqual(self.db.viewData('y', 'name', 'full.jpg', 'background'), 0)


    def test_generateSqlForUpdate(self):
        self.db.accessDatabase(self.background1.generateSqlForAdd()) 
        self.background1.rate = 10.0
        self.background1.x = 100.0
        self.background1.y = 100.0
        self.assertEqual(self.db.viewData('size_rate', 'name', 'full.jpg', 'background'),2)
        self.assertEqual(self.db.viewData('x', 'name', 'full.jpg', 'background'),0)
        self.assertEqual(self.db.viewData('y', 'name', 'full.jpg', 'background'),0)
        self.db.accessDatabase(self.background1.generateSqlForUpdate()) 
        self.assertEqual(self.db.viewData('size_rate', 'name', 'full.jpg', 'background'),10)
        self.assertEqual(self.db.viewData('x', 'name', 'full.jpg', 'background'),100)
        self.assertEqual(self.db.viewData('y', 'name', 'full.jpg', 'background'),100)


    def test_generateSqlForDelete(self):
        self.db.accessDatabase(self.background1.generateSqlForAdd()) 
        self.assertEqual(len(self.db.viewDataAll('background')), 1)
        self.db.accessDatabase(self.background1.generateSqlForDelete()) 
        self.assertEqual(self.db.viewData('size_rate', 'name', 'full.jpg', 'background'), [])
        self.assertEqual(self.db.viewDataAll('background'), [])

if __name__ == '__main__':
    unittest.main()
