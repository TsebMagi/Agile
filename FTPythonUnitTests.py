import unittest
import FTPython


class ConnectionTestCases(unittest.TestCase):

    def setUp(self):
        FTPython.connect("babbage.cs.pdx.edu", 8000, "test_user", "test")
        self.assertTrue(FTPython.ftp_connection is not None)

    def tearDown(self):
        if FTPython.ftp_connection is not None:
            FTPython.ftp_connection.close()
            FTPython.ftp_connection = None

    def test_good_connection(self):
        FTPython.connect("babbage.cs.pdx.edu", 8000, "test_user", "test")
        self.assertTrue(FTPython.ftp_connection is not None)

    def test_bad_port(self):
        FTPython.connect("babbage.cs.pdx.edu", 800, "test_user", "test")
        self.assertTrue(FTPython.ftp_connection is None)

    def test_bad_server(self):
        FTPython.connect("bad", 8000, "test_user", "test")
        self.assertTrue(FTPython.ftp_connection is None)

    def test_bad_password(self):
        FTPython.connect("babbage.cs.pdx.edu", 8000, "test_user", "bad")
        self.assertTrue(FTPython.ftp_connection is None)

    def test_bad_username(self):
        FTPython.connect("babbage.cs.pdx.edu", 8000, "bad", "test")
        self.assertTrue(FTPython.ftp_connection is None)
