import unittest
import os
import uuid
import shutil
import urllib
from unittest.mock import patch

from savepic import unique_filename
from savepic import setup_dir
from savepic import match_header
from savepic import save_image
from savepic import download_files

class TestSavingImage(unittest.TestCase):

    sample = [("one", "two"), ("two", "three")]

    def test_unique_filename_punctuation_removed(self):
        self.assertEqual(unique_filename('http://bla.com/pic.png'), 'httpbla.compic.png')

    def test_unique_filename_alpha_left(self):
        self.assertNotEqual(unique_filename('http://www.abc.net.au/news/image/9404150-3x2-700x467.jpg'),
                            unique_filename('http://www.zyx.net.au/news/image/9404150-3x2-700x467.jpg'))

    def test_unique_filename_num_left(self):
        self.assertNotEqual(unique_filename('http://www.abc.net.au/news/image/9404150-3x2-800x467.jpg'),
                            unique_filename('http://www.abc.net.au/news/image/9404150-3x2-100x467.jpg'))

    def test_setup_dir_correct_path(self):
        newDir = str(uuid.uuid4().hex)
        self.assertEqual(setup_dir(newDir), newDir)
        self.assertTrue(os.path.isdir(newDir))
        os.rmdir(newDir)

    def test_setup_dir_is_folder(self):
        newDir = str(uuid.uuid4().hex)
        setup_dir(newDir)
        self.assertTrue(os.path.isdir(newDir))
        os.rmdir(newDir)

    def test_match_header_find_correct(self):
        self.assertTrue(match_header(self.sample, "two", "three"))

    def test_match_header_dont_find_incorrect(self):
        self.assertFalse(match_header(self.sample, "two", "one"))

    def test_match_header_nonexistent_header(self):
        self.assertRaises(ValueError, match_header, self.sample, "four", "one")

    def test_match_header_wrong_structure(self):
        self.assertRaises(ValueError, match_header, ["three", "four"], "four", "one")


    def test_save_image_from_url(self):
        url = 'http://www.abc.net.au/news/image/9404150-3x2-700x467.jpg'
        self.assertTrue(save_image(url, setup_dir('test'), 60))
        shutil.rmtree('test')

    def test_save_image_url_not_an_image(self):
        notPic = 'https://github.com/mooromets'
        self.assertFalse(save_image(notPic, setup_dir('test'), 60))
        shutil.rmtree('test')

    def test_save_image_wrong_url(self):
        notValidUrl = 'https://github.com/mooromets/no.pic.jpg'
        self.assertRaises(urllib.error.HTTPError, save_image,notValidUrl, setup_dir('test'), 60)
        shutil.rmtree('test')

    @patch('savepic.save_image')
    def test_save_download_files_ok(self, mock_save):
        mock_save.return_value = True
        self.assertEqual(download_files(list(range(50))), 50)

    @patch('savepic.save_image')
    def test_save_download_files_not_downloaded(self, mock_save):
        mock_save.return_value = False
        self.assertEqual(download_files(list(range(50))), 0)

    @patch('savepic.save_image')
    def test_save_download_files_exception_on_download(self, mock_save):
        mock_save.side_effect = Exception('file not saved')
        self.assertEqual(download_files(list(range(50))), 0)


if __name__ == '__main__':
    unittest.main()
