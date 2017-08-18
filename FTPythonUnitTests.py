import unittest
import FTPython
import sys
import ftplib as ft


class ConnectionTestCases(unittest.TestCase):

    def setUp(self):
        if FTPython.ftp_connection is not None:
            FTPython.ftp_connection.close()
            FTPython.ftp_connection = None

    def tearDown(self):
        if FTPython.ftp_connection is not None:
            FTPython.ftp_connection.close()
            FTPython.ftp_connection = None

    def test_good_connection(self):
        FTPython.connect("babbage.cs.pdx.edu", 8000, "test_user", "test")
        self.assertTrue(FTPython.ftp_connection is not None)

    def test_bad_port(self):
        FTPython.connect("babbage.cs.pdx.edu", 800, "test_user", "test")
        self.assertRaises(ft.all_errors)

    def test_bad_server(self):
        FTPython.connect("bad", 8000, "test_user", "test")
        self.assertRaises(ft.all_errors)

    def test_bad_password(self):
        FTPython.connect("babbage.cs.pdx.edu", 8000, "test_user", "bad")
        self.assertRaises(ft.all_errors)

    def test_bad_username(self):
        FTPython.connect("babbage.cs.pdx.edu", 8000, "bad", "test")
        self.assertRaises(ft.all_errors)


class ParseInputTestCases(unittest.TestCase):
    std_in = None
    std_out = None

    def setUp(self):
        self.std_in = sys.stdin
        self.std_out = sys.stdout

    def tearDown(self):
        sys.stdin = self.std_in
        sys.stdout = self.std_out

    def test_connect_bad_input(self):
        sys.stdin = open("test_connection_bad_input.txt", 'r')
        FTPython.parse_input()
        self.assertRaises(ValueError)
