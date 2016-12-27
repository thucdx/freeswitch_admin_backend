import unittest

from user import User


class UserTest(unittest.TestCase):
    def testParse(self):
        user = User.parse("11;sofia/internal/1019@35.165.245.123;ce840628-de39-4044-8be1-6c937e51325f;1019;1019;hear"
                          "|speak|video;0;0;0;100")
        self.assertEquals(user.id, '11')
        self.assertEquals(user.caller_name, '1019')
        self.assertEquals(user.status, "hear|speak|video")
        self.assertEquals(user.uuid, 'ce840628-de39-4044-8be1-6c937e51325f')
        self.assertEquals(user.caller_number, '1019')
        self.assertEquals(user.caller_name, '1019')

    def test_is_admin_01(self):
        user = User.parse("11;sofia/internal/1019@35.165.245.123;ce840628-de39-4044-8be1-6c937e51325f;1019;1019;hear"
                          "|speak|video|moderator;0;0;0;100")
        self.assertEquals(user.id, '11')
        self.assertTrue(user.is_admin())

    def test_is_admin_02(self):
        user = User.parse(
            "11;sofia/internal/1019@35.165.245.123;ce840628-de39-4044-8be1-6c937e51325f;1019;1019;hear"
            "|speak|video;0;0;0;100")
        self.assertEquals(user.id, '11')
        self.assertFalse(user.is_admin())
