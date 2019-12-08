import unittest
from collections import OrderedDict
from model.background import MapBackground
from tests.fake_db import FakeDB


class TestBackground(unittest.TestCase):
    def setUp(self):
        self.background1 =  MapBackground('full.jpg', 2.0, 0.0, 0.0)

    def tearDown(self):
        self.background1 =  MapBackground('full.jpg', 2.0, 0.0, 0.0)

    def test_generateSqlForAdd(self):
        self.assertEqual(self.background1.generateSqlForAdd(), ("insert into background values (?, ?, ?, ?, ?);",('full.jpg', 0.0, 0.0,2.0,self.background1.pic_str)))


    def test_generateSqlForUpdate(self):
        self.assertEqual(self.background1.generateSqlForUpdate(), ("Update background set x = ?, y = ?, size_rate = ? where (name = ?);",(0.0, 0.0,2.0, 'full.jpg')))


    def test_generateSqlForDelete(self):
        self.assertEqual(self.background1.generateSqlForDelete(), "Delete from background;")

    def test_serialize(self):
        self.assertEqual(self.background1.serialize(), OrderedDict([('pic_name','full.jpg'),('rate',2.0),('x',0.0),('y', 0.0),('pic_str', self.background1.pic_str)]))

    def test_deserialize(self):
        data = {'pic_name':'img.jpg', 'rate':1.0, 'x': 0.1, 'y':0.4, 'pic_str':'asdf'}
        

        self.assertEqual(self.background1.pic_name, 'full.jpg')
        self.assertEqual(self.background1.rate, 2.0)
        self.assertEqual(self.background1.x, 0.0)
        self.assertEqual(self.background1.y, 0.0)

        self.background1.deserialize(data)

        self.assertEqual(self.background1.pic_name, 'img.jpg')
        self.assertEqual(self.background1.rate, 1.0)
        self.assertEqual(self.background1.x, 0.1)
        self.assertEqual(self.background1.y, 0.4)
        self.assertEqual(self.background1.pic_str, 'asdf')

        with self.assertRaises(ValueError):
            self.background1.pic_name = 'asdf.png'


if __name__ == '__main__':
    unittest.main()
