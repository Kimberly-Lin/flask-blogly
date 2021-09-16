from app import app
from unittest import TestCase
from models import db, connect_db, User

app.config["TESTING"] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

#create DB blogly test and populate
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'

connect_db(app)
db.create_all()

class BlogTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        test_user = User(first_name='Davis',last_name='Test',img='')
        db.session.add(test_user)
        db.session.commit()
        self.test_user_id = test_user.id

    def tearDown(self):
        """Stuff to do after every test."""
        User.query.delete()


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