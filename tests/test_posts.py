import unittest
from app.models import Posts, User
from flask_login import current_user
from app import db


class TestPosts(unittest.TestCase):

    def setUp(self):
        self.user_Brian = User(
            firstname='Brian', lastname='Njoroge', password='siriyako', email='test@user.com', bio='hooray')
        self.new_post = Posts(title='random thing', sub_title='another random', description='bla bla bla', content="bla bla bla bla", likes=0, dislikes=0,
                              user=self.user_Brian)

    def tearDown(self):
        Posts.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post, Posts))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title, 'random thing')
        self.assertEquals(self.new_post.sub_title, 'another random')
        self.assertEquals(self.new_post.description, 'bla bla bla')
        self.assertEquals(self.new_post.content, 'bla bla bla bla')
        self.assertEquals(self.new_post.likes, 0)
        self.assertEquals(self.new_post.dislikes, 0)
        self.assertEquals(self.new_post.user, self.user_Brian)

    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Posts.query.all()) > 0)

    def test_get_post(self):

        self.new_post.save_post()
        got_posts = Posts.get_post(1)
        self.assertTrue(len(got_posts) == 1)
