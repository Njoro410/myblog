import unittest
from app.models import Quote


class QuoteTest(unittest.TestCase):
    """
    test class to test the bahaviour of Quote class
    """

    def setUp(self):

        '''
        Set up method that will run before every Test
        '''
        self.new_quote = Quote('brian','get some sleep')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote, Quote))
