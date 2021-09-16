from app import app
from unittest import TestCase
from models import db, connect_db, User, Post
import datetime

app.config["TESTING"] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_ECHO'] = False

#create DB blogly test and populate
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

connect_db(app)
db.drop_all()
db.create_all()

class BlogTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        Post.query.delete()
        User.query.delete()
        self.client = app.test_client()
        test_user = User(first_name='Davis',last_name='Test',img='')
        test_post = Post(title='Test Title',
                        content='Test content',
                        created_at=datetime.datetime.now(), 
                        user_id = test_user.id)

        db.session.add(test_user)
        db.session.add(test_post)

        db.session.commit()

        self.test_user_id = test_user.id
        self.test_post_id = test_post.id       


    def tearDown(self):
        """Stuff to do after every test."""
        db.session.rollback()

    def test_homepage_redirect(self):
        """Ensure landing on home page redirects to users list"""
        with self.client as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Davis Test', html)

    def test_new_user(self):
        with self.client as client:
            resp = client.post('/users/new',
                            data={'first_name': 'FirstTest',
                                  'last_name': 'LastTest',
                                  'image_url': ''  },
                                  follow_redirects=True
                                  )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('FirstTest LastTest', html)

    def test_invalid_create_user_input(self):
        with self.client as client:
            resp = client.post('/users/new',
                            data={'first_name': 'FirstTest',
                                  'last_name': '',
                                  'image_url': ''  },
                                  follow_redirects=True
                                  )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please enter a first and last name', html)

    def test_delete_user(self):
        with self.client as client:
            resp = client.post(f'/users/{self.test_user_id}/delete',
                                  follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
            self.assertNotIn('Davis Test', html)

    def test_create_post(self):
        with self.client as client:
            resp = client.post(f'/users/{self.test_user_id}/posts/new',
                                data = {'title':'Test Post',
                                'content':'This is content for the test post'},
                                  follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Post', html)

    def test_edit_post(self):
        with self.client as client:
            resp = client.post(f'/posts/{self.test_post_id}/edit',
                                data = {'title': 'Edited Title',
                                'content':'Edited content'},
                                  follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edited Title', html)
            self.assertIn('Edited content', html)