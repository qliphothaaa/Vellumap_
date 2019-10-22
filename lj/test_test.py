import unittest
from unittest.mock import patch
from test import it

class TestMapObject(unittest.TestCase):

    def test_foo(self):
        with patch('test.it.ppp') as mocked_ppp:
            mocked_ppp.return_value = 'ddddddddddd'

            a = it()
            self.assertEqual(a.foo(), 'ddddddddddd')
        


if __name__ == '__main__':
    unittest.main()
