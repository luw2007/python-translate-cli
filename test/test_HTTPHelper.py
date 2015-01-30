from unittest import TestCase
from pytrans.request import HTTPHelper
from pytrans.compat import u

class TestHTTPHelper(TestCase):
    def test_post(self):
        r = HTTPHelper('https://passport.baidu.com/v2/api/\?login')
        status, text = r.post(dict(username='admin', password='admin'))
        self.assertTrue(status)
        self.assertIn('passport.baidu.com', text.decode('gbk'))
        r.close()

    def test_get(self):
        r = HTTPHelper('https://github.com/luw2007')
        status, text = r.get()
        self.assertTrue(status)
        self.assertIn('luw2007', text.decode('utf8'))
        r.close()

        r = HTTPHelper('http://www.baidu.com')
        status, text = r.get()
        self.assertTrue(status)
        self.assertIn('baidu', text.decode('gbk'))
        r.close()