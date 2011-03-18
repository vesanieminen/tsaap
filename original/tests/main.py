import sys
sys.path.append('src')

import unittest

from TestGame import TestGame
from TestShip import TestShip
from TestPlayer import TestPlayer
from TestUtils import TestUtils
from TestEvent import TestEvent

def suite():
  suite = unittest.TestSuite() 
  suite.addTest( unittest.makeSuite(TestGame) )
  suite.addTest( unittest.makeSuite(TestShip) )
  suite.addTest( unittest.makeSuite(TestPlayer) )
  suite.addTest( unittest.makeSuite(TestUtils) )
  suite.addTest( unittest.makeSuite(TestEvent) )
  return suite

if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())

