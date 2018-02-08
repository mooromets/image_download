import unittest
import os
import uuid
import shutil
import urllib
from unittest.mock import MagicMock

from savepic import unique_filename
from savepic import setup_dir
from savepic import match_header
from savepic import save_image
from savepic import download_files

class TestSavingImage(unittest.TestCase):

    def test_unique_filename(self):
        self.assertEqual(unique_filename('http://bla.com'), 'httpbla.com')
        self.assertNotEqual(unique_filename('http://www.abc.net.au/news/image/9404150-3x2-700x467.jpg'),
                            unique_filename('http://www.zyx.net.au/news/image/9404150-3x2-700x467.jpg'))
        self.assertNotEqual(unique_filename('http://www.abc.net.au/news/image/9404150-3x2-800x467.jpg'),
                            unique_filename('http://www.abc.net.au/news/image/9404150-3x2-100x467.jpg'))

    def test_setup_dir(self):
        newDir = str(uuid.uuid4().hex)
        setup_dir(newDir)
        self.assertTrue(os.path.isdir(newDir))
        os.rmdir(newDir)


    def test_match_header(self):
        sample = [("one", "two"), ("two", "three")]
        self.assertTrue(match_header(sample, "two", "three"))
        self.assertFalse(match_header(sample, "two", "one"))
        self.assertRaises(ValueError, match_header, sample, "four", "one")
        self.assertRaises(ValueError, match_header, ["three", "four"], "four", "one")


    def test_save_image(self):
        url = 'http://www.abc.net.au/news/image/9404150-3x2-700x467.jpg'
        self.assertTrue(save_image(url, setup_dir('test'), 60))
        notPic = 'https://github.com/mooromets'
        self.assertFalse(save_image(notPic, setup_dir('test'), 60))
        notValidUrl = 'https://github.com/mooromets/no.pic.jpg'
        self.assertRaises(urllib.error.HTTPError, save_image,notValidUrl, setup_dir('test'), 60)
        shutil.rmtree('test')


if __name__ == '__main__':
    unittest.main()
