import unittest
import sys
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from model.graphics_management import GraphicsManagement
from tests.fake_db import FakeDB

class TestGraphicsManagement(unittest.TestCase):
    app = QApplication(sys.argv)
    def setUp(self):
        self.graphics_management = GraphicsManagement()
        self.map_object1 = MagicMock()
        self.map_object1.getPosition = MagicMock(return_value = (3,3))
        self.map_object1.object_id = 3
        

    def test_generateGraphics(self):
        self.assertEqual(len(self.graphics_management.graphics),0)
        self.graphics_management.generateGraphics(self.map_object1, 'red', 'tri', 20, 20)
        self.assertEqual(len(self.graphics_management.graphics), 1)
        self.assertTrue(3 in self.graphics_management.graphics)
        self.assertEqual(self.graphics_management.graphics[3].shape, 'tri')
        self.assertEqual(self.graphics_management.graphics[3].width, 20)
        self.assertEqual(self.graphics_management.graphics[3].height, 20)
            

    def test_getGraphics(self):
        self.graphics_management.generateGraphics(self.map_object1, 'red', 'tri', 20, 20)
        #TC1
        self.assertNotEqual(self.graphics_management.getGraphics(3), None)
        self.assertEqual(self.graphics_management.getGraphics(3).shape, 'tri')
        self.assertEqual(self.graphics_management.getGraphics(3).width , 20)
        #TC2
        self.assertEqual(self.graphics_management.getGraphics(4), None)



    def test_removeGraphics(self):
        self.graphics_management.generateGraphics(self.map_object1, 'red', 'tri', 20, 20)
        self.assertTrue(3 in self.graphics_management.graphics)
        #TC1
        self.graphics_management.removeGraphics(3)
        self.assertEqual(len(self.graphics_management.graphics),0)
        self.assertFalse(3 in self.graphics_management.graphics)
        #TC2
        with self.assertRaisesRegex(KeyError, "cannot find the graphic"):
            self.graphics_management.removeGraphics(4)

    def test_updateGraphics(self):
        self.graphics_management.generateGraphics(self.map_object1, 'red', 'tri', 20, 20)
        #TC1
        self.graphics_management.updateGraphics(3, 'black', 'rec', 10, 40)
        self.assertEqual(self.graphics_management.getGraphics(3).shape, 'rec')
        self.assertEqual(self.graphics_management.getGraphics(3).width, 10)
        self.assertEqual(self.graphics_management.getGraphics(3).height, 40)
        #TC2
        with self.assertRaisesRegex(KeyError, "cannot find the graphic"):
            self.graphics_management.updateGraphics(4,'#232323', 'ell', 34, 65)

    def test_hideGraphics(self):
        #TC1
        self.graphics_management.generateGraphics(self.map_object1, 'red', 'tri', 20, 20)
        self.assertTrue(self.graphics_management.getGraphics(3).isVisible())
        self.graphics_management.hideGraphics({3})
        self.assertFalse(self.graphics_management.getGraphics(3).isVisible())
        #TC2
        self.assertEqual(self.graphics_management.hideGraphics(set()), None)
        #TC3
        with self.assertRaisesRegex(ValueError, "input should be set"):
            self.graphics_management.hideGraphics([3])
        #TC4
        with self.assertRaisesRegex(KeyError, "cannot find the graphic"):
            self.graphics_management.hideGraphics({1})


    def test_showGraphics(self):
        #TC1
        self.graphics_management.generateGraphics(self.map_object1, 'red', 'tri', 20, 20)
        self.assertTrue(self.graphics_management.getGraphics(3).isVisible())
        self.graphics_management.hideGraphics({3})
        self.assertFalse(self.graphics_management.getGraphics(3).isVisible())
        self.graphics_management.showGraphics({3})
        self.assertTrue(self.graphics_management.getGraphics(3).isVisible())
        #TC2
        self.assertEqual(self.graphics_management.hideGraphics(set()), None)
        #TC3
        with self.assertRaisesRegex(ValueError, "input should be set"):
            self.graphics_management.hideGraphics([3])
        #TC4
        with self.assertRaisesRegex(KeyError, "cannot find the graphic"):
            self.graphics_management.hideGraphics({1})
if __name__ == '__main__':
    unittest.main()


