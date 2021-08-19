import os
from unittest import TestCase
from datetime import datetime
from models import db, User, Post

os.environ['DATABASE_URL'] = "postgresql:///testting-hiphop"

from app import app

db.create_all()

class TestPostModel(TestCase):
    """ test post model """

    def setUp(self):
        """ setup post test """

        db.drop_all()
        db.create_all()

        test_user = User.signup('testuser', 'pasword', 'https://bit.ly/3ihhSWp')
        uid = 201
        test_user.id = uid

        test_post = Post(user_id=test_user.id, text='test text', timestamp=datetime.utcnow())
        pid = 202
        test_post.id = pid

        u = User.query.get(uid)
        p = Post.query.get(pid)

        self.u = u
        self.u_id = uid

        self.p = p
        self.p_id = pid


        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_vaild_post(self):
        """ test valid post """
        test_post = Post(user_id=self.u.id, text='test text', timestamp=datetime.utcnow())
        timestamp = test_post.timestamp
        u = User.query.get(self.u_id)
        u.post.append(test_post)
        db.session.commit()
        
        self.assertTrue(test_post)
        self.assertEqual(test_post.user_id, self.u_id)
        self.assertEqual(test_post.text, 'test text')
        self.assertEqual(test_post.timestamp, timestamp)
        self.assertIn(test_post, self.u.post)

