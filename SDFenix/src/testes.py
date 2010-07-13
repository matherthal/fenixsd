'''
Created on 13/07/2010

@author: Rondon
'''
import unittest

from messenger import Messenger
from message import Message


class Test(unittest.TestCase):


    def testMessenger(self):
        msg = Message(None,None,None,None,None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMessenger']
    unittest.main()