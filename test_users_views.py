from unittest import TestCase
import os

from models import db, User #Post, Likes, Follows, Artist

os.environ['DATABASE_URI'] = "postgresql:///testting_hiphop"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTest(TestCase):
    """ test all user views """

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testUser", password='test123', img_url=None)
        self.testuser2 = User.signup(username="testUser2", password='test123', img_url=None)

        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        db.session.commit()

    def tearDown(self):
        """ tear down database after test"""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_show_index(self):
        with self.client as c:
            res = c.get('/', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center m-3">Signup</h1>', str(res.data))

    def test_user_signup_page(self):
        with self.client as c:
            res = c.get('/signup')
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-primary">Signup!</button>', str(res.data))
            self.tearDown()

    def test_user_signup(self):
        with self.client as c:
            res = c.post('/signup')
            self.assertEqual(res.status_code, 200)

    def test_user_login_get(self):
        with self.client as c:
            res = c.get('/login')
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center m-3">Login</h1>', str(res.data))
            res = c.post('/login', data={'username': 'testUser', 'password': 'test123', 'img_url': None}, follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<button class="btn btn-success btn-sm">Edit user</button>', str(res.data))

    def test_all_users(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            res = c.get('/all-users')
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center">Hip Hop Heads</h1>', str(res.data))

    # def test_user_home(self):
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser_id

    #         res = c.get(f'/users/{self.testuser_id}')
    #         self.assertEqual(res.status_code, 200)

    def test_make_post(self):
        with self.client as c:
            res = c.get(f'/post/{self.testuser_id}')

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-primary">Post!</button>', str(res.data))

    def test_user_edit(self):
        with self.client as c:
            res = c.get(f'/user/edit/{self.testuser_id}')

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-success btn-sm">Edit!</button>', str(res.data))

    def test_add_artist(self):
        with self.client as c:
            res = c.get('/add-artist')

            self.assertEqual(res.status_code, 200)
            self.assertIn('<button type="submit" class="btn btn-primary">Add</button>', str(res.data))