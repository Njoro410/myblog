from turtle import title
import unittest
from app.models import Comments, Posts, User
from flask_login import current_user
from app import db


class TestComments(unittest.TestCase):

    def setUp(self):
        self.user_Brian = User(
            firstname='Brian', lastname='Njoroge', password='siriyako', email='test@user.com', bio='hooray')
        self.post = Posts(title='This is the title', sub_title='yeees')
        self.comment = Comments(comment="this is that")

    def tearDown(self):
            Posts.query.delete()
            User.query.delete()
            Comments.query.delete()

    def test_instance(self):
            self.assertTrue(isinstance(self.new_comment, Comments))

    def test_check_instance_variables(self):
            self.assertEquals(self.new_comment.comment, 'this is that')
            
    def test_save_comment(self):
            self.new_comment.save_comment()
            self.assertTrue(len(Comments.query.all()) > 0)

