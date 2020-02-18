from flaskblog import create_app, db, mail
from flaskblog.models import Images
from flaskblog.gallery.utils import save_picture, delete_picture, save_zip
from flaskblog.gallery.forms import UploadPictureForm
import os
import unittest
from coverage import coverage

cov = coverage(branch=True, omit=['tests.py'])
cov.start()

app = create_app()

class TestCase(unittest.TestCase):
    def setUp(self):

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests/test.db'

        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


    ############ HELPER METHODS ################

    def register(self, username, email, password, confirm_password):
        return self.app.post(
            '/register',
            data=dict(username=username, email=email, password=password, confirm_password=confirm_password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def logout(self):
        return self.app.post(
            '/logout',
            follow_redirects=True
        )

    ############ TEST CASES ####################

    def test_valid_registration(self):
        response = self.register('Hansen', 'hansen10@live.ca', 'testpw', 'testpw')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created for Hansen', response.data)

    def test_invalid_registration(self):
        response = self.register('Hansen', 'hansen10@live.ca', 'testpw', 'invalidconfirmation')
        self.assertIn(b'Field must be equal to password', response.data)

    def test_duplicate_email_registration(self):
        response = self.register('Hansen', 'hansen10@live.ca', 'testpw', 'testpw')
        self.assertEqual(response.status_code, 200)
        response = self.register('Hansen', 'hansen10@live.ca', 'testpw', 'testpw')
        self.assertIn(b'That email is taken', response.data)


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_add_single_image_to_db(self):
        # See if database can add image
        i = Images(image_file='test.jpg', description='test', user_id='12')
        with app.app_context():
            db.session.add(i)
            db.session.commit()
            self.assertEqual(Images.query.get(1).image_file, 'test.jpg')


    def test_delete_single_image_from_db(self):
        i = Images(image_file='test.jpg', description='test', user_id='12')
        with app.app_context():
            db.session.add(i)
            db.session.commit()
            self.assertEqual(Images.query.get(1).image_file, 'test.jpg')


if __name__ == "__main__":
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(os.getcwd(), "/flaskblog/tests/tmp/coverage/index.html"))
    cov.html_report(directory='flaskblog/tests/tmp/coverage')
    cov.erase()

