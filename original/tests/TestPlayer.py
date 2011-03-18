from unittest import TestCase

from Player import Player

class TestPlayer(TestCase):

  def setUp(self):
    self.player = Player()

  def testInit(self):
    self.failUnless(self.player)
    self.failUnlessEqual(self.player.name, Player.NAME_DEFAULT)

  def testShoot(self):
    self.player.shoot()
    pass

  def testMoveForwardOn(self):
    self.player.moveForwardOn()
    forwardOn = self.player.isForwardOn()
    self.failUnless(forwardOn)

  def testMoveForwardOff(self):
    self.player.moveForwardOn()
    before = self.player.isForwardOn()
    self.player.moveForwardOff()
    after = self.player.isForwardOn()
    self.failUnless(before == True)
    self.failUnless(after == False)

  def testIsForwardOn(self):
    forwardOn = self.player.isForwardOn()
    self.failIf(Player.FORWARD_DEFAULT)

  def testRotateLeftOn(self):
    self.player.rotateLeftOn()
    rotateLeftOn = self.player.isRotateLeftOn()
    self.failUnless( isinstance(rotateLeftOn, bool) )
    self.failUnless(rotateLeftOn == True)
    #TODO: add tests for checking that the event was sent

  def testRotateLeftOff(self):
    self.player.rotateLeftOn()
    self.player.rotateLeftOff()
    rotateLeftOn = self.player.isRotateLeftOn()
    self.failUnless( isinstance(rotateLeftOn, bool) )
    self.failUnless(rotateLeftOn == False)
    #TODO: add tests for checking that the event was sent

  def testIsRotateLeftOn(self):
    isRotateLeftOn = self.player.isRotateLeftOn()
    self.failUnless( isinstance(isRotateLeftOn, bool) )

  def testRotateRightOn(self):
    self.player.rotateRightOn()
    rotateRightOn = self.player.isRotateRightOn()
    self.failUnless( isinstance(rotateRightOn, bool) )
    self.failUnless(rotateRightOn == True)
    #TODO: add tests for checking that the event was sent

  def testRotateRightOff(self):
    self.player.rotateRightOn()
    self.player.rotateRightOff()
    rotateRightOn = self.player.isRotateRightOn()
    self.failUnless( isinstance(rotateRightOn, bool) )
    self.failUnless(rotateRightOn == False)
    #TODO: add tests for checking that the event was sent

  def testIsRotateRightOn(self):
    isRotateRightOn = self.player.isRotateRightOn()
    self.failUnless( isinstance(isRotateRightOn, bool) )
