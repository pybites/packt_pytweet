import unittest

from packt import title_match, hashify


class TestPackt(unittest.TestCase):

    def setUp(self):
        self.filters = 'Python Django Flask'.split()
        self.python_title = "Python 3 Web Development Beginner's Guide"
        self.flask_title = 'Learning Flask Framework'
        self.aws_title = 'Learning AWS'
        self.css_title = 'Responsive Web Design with HTML5 and CSS3 - Second Edition'

    def test_title_match(self):
        self.assertTrue(title_match(self.python_title, filters=self.filters))
        self.assertTrue(title_match(self.flask_title, filters=self.filters))
        self.assertFalse(title_match(self.aws_title, filters=self.filters))
        self.assertFalse(title_match(self.css_title, filters=self.filters))

    def test_hashify(self):
        py_hashtag = "#Python 3 Web Development Beginner's Guide"
        flask_hashtag = 'Learning #Flask Framework'
        self.assertEqual(hashify(self.python_title, filters=self.filters), py_hashtag)
        self.assertEqual(hashify(self.flask_title, filters=self.filters), flask_hashtag)
        self.assertEqual(hashify(self.aws_title, filters=self.filters), self.aws_title)
        self.assertEqual(hashify(self.css_title, filters=self.filters), self.css_title)


if __name__ == '__main__':
    unittest.main()
