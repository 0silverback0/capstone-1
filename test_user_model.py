import os
from unittest import TestCase

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///testting-hiphop"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """ test user model """

    def setUp(self):
        """ add test data """

        db.drop_all()
        db.create_all()

        testuser = User.signup('test1', 'password', 'https://bit.ly/3ihhSWp')
        uid = 100
        testuser.id = uid

        testuser2 = User.signup('test2', 'password2', 'https://bit.ly/3ihhSWp')
        uid2 = 101
        testuser2.id = uid2 

        db.session.commit()

        u1 = User.query.get(testuser.id)
        u2 = User.query.get(testuser2.id)

        self.u1 = u1
        self.uid1 = uid

        self.u2 = u2
        self.uid2 = uid2

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """ test the model """

        user = User (username="user", password="hashed", img_url='https://bit.ly/3ihhSWp')

        db.session.add(user)
        db.session.commit()

        self.assertEqual(len(user.followers), 0)
        self.assertEqual(len(user.post), 0)

    def test_user_follows(self):
        """ test user follows is working """

        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEquals(len(self.u1.following), 1)
        self.assertIn(self.u2, self.u1.following)
        self.assertIn(self.u1, self.u2.followers)

    def test_signup(self):
        """ test valid signup """
        tester = User.signup(username="tester", password="tester1", img_url="https://bit.ly/3ihhSWp")

        uid = 107
        tester.id = uid
        db.session.commit()

        test_user = User.query.get(uid)

        self.assertEquals(test_user.username, 'tester')
        self.assertNotEqual(test_user.password, 'tester1')
        self.assertEqual(test_user.img_url, 'https://bit.ly/3ihhSWp')

    def test_login(self):
        """ test valid login """
        user = User.login(self.u1.username, self.u1.password)

        self.assertIsNotNone(user)

    def test_bad_signup(self):
        """ test a bad login """
        user = User.login(self.u1.username, self.u1.password)

        self.assertFalse(user)