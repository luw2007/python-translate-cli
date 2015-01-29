from unittest import TestCase
from pytrans.sparse_array import loads
from pytrans.compat import u

class TestLoads(TestCase):
    def test_loads(self):
        self.assertListEqual(loads('[,]'), [None, None])
        self.assertListEqual(loads('[,0]'), [None, 0])
        self.assertListEqual(loads('[0,]'), [0, None])
        self.assertListEqual(loads('[, "\\u4e2d\\u6587"]'), [None, u("中文")])
