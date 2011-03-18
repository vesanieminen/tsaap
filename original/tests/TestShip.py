from unittest import TestCase

from pandac.PandaModules import NodePath, Point3

from Ship import Ship
from Utils import point3ToTuple, tupleLength

class TestShip(TestCase):

  def setUp(self):
    self.ship = Ship()

  def tearDown(self):
    if isinstance(self.ship, NodePath):
      self.ship.visualNode.removeNode()

  def testInit(self):
    self.failUnless(self.ship)
    self.failUnlessEqual(self.ship.name, Ship.NAME_DEFAULT)
    self.failUnless(self.ship.collisionSphere)

  def testGetVisualNode(self):
    node = self.ship.getVisualNode()
    self.failUnless(node)

  def testCreateVisualNode(self):
    self.ship.createVisualNode()
    node = self.ship.getVisualNode()
    self.failUnless( isinstance(node, NodePath) )

  def testIsVisible(self):
    self.ship.createVisualNode()
    self.failUnless( self.ship.isVisible() )

  def testSetCollisionHandler(self):
    f = lambda x, y: 0
    self.ship.setCollisionHandler(f)
    self.failUnlessEqual(self.ship.collisionHandler, f)
    
  def getCollisions(self):
    self.failifEqual(self.ship.collisions, None)
    
  def testSetPos(self):
    pos = (4, 7)
    self.ship.setPos(pos)
    self.failUnlessEqual( self.ship.getPos(), pos )
    
  def testGetPos(self):
    pos = self.ship.getPos()
    self.failUnless( isinstance(pos, tuple) )

  def testGetVel(self):
    vel = self.ship.getVel()
    self.failUnless( isinstance(vel, tuple) )

  def testGetAcc(self):
    acc = self.ship.getAcc()
    self.failUnless( isinstance(acc, float) )

  def testGetHeading(self):
    heading = self.ship.getHeading()
    self.failUnless( isinstance(heading, float) )

  def testShoot(self):
    bullets = self.ship.bullets
    before = len(bullets)
    # In the beginning there are no bullets
    self.failIf(before != 0)
    self.ship.shoot()
    after = len(bullets)
    self.failUnless(before < after)
    self.failUnless(after == 1)
    self.failUnless( bullets[0]['vel'] )
    self.failUnless( bullets[0]['visual'] )
    self.failUnless( bullets[0]['isAlive'] )

  def testBulletHit(self):
    healthBefore = self.ship.health
    self.ship.bulletHit()
    healthAfter = self.ship.health
    self.failUnless(healthBefore > healthAfter)

    # Test that the ship will be destroyed if it's hit enough times
    while(True):
      # Hit with bullets until health is 0
      self.ship.bulletHit()
      if self.ship.health <= 0:
        break
    self.failIf(self.ship.isAlive)

  def testDestroyBullet(self):
    self.ship.shoot()
    bullet = self.ship.bullets[0]
    visual = bullet['visual']
    physical = bullet['physical']
    self.failUnless( len(self.ship.bullets) == 1 )
    self.failUnless(visual)
    self.failUnless(physical)
    self.ship.destroyBullet(bullet)
    self.failUnless( len(self.ship.bullets) == 0 )

  def testDestroy(self):
    before = self.ship.isAlive
    self.ship.destroy()
    after = self.ship.isAlive
    self.failUnless(before == True)
    self.failUnless(after == False)

  def testThrustOn(self):
    before = self.ship.getAcc()
    self.ship.thrustOn()
    after = self.ship.getAcc()
    self.failUnless(before != after)

  def testThrustOff(self):
    self.ship.thrustOn()
    before = self.ship.getAcc()
    self.ship.thrustOff()
    after = self.ship.getAcc()
    self.failUnless(before != after)

  def testRotateLeftOn(self):
    before = self.ship.isRotatingLeft()
    self.ship.rotateLeftOn()
    after = self.ship.isRotatingLeft()
    self.failIf(before == after)
    self.failIf(before == True)
    self.failIf(after == False)

  def testRotateLeftOff(self):
    self.ship.rotateLeftOn()
    before = self.ship.isRotatingLeft()
    self.ship.rotateLeftOff()
    after = self.ship.isRotatingLeft()    
    self.failIf(before == after)
    self.failIf(before == False)
    self.failIf(after == True)

  def testIsRotatingLeft(self):
    isRotatingLeft = self.ship.isRotatingLeft()
    self.failUnless( isinstance(isRotatingLeft, bool) )

  def testRotateRightOn(self):
    before = self.ship.isRotatingRight()
    self.ship.rotateRightOn()
    after = self.ship.isRotatingRight()
    self.failIf(before == after)
    self.failIf(before == True)
    self.failIf(after == False)

  def testRotateRightOff(self):
    self.ship.rotateRightOn()
    before = self.ship.isRotatingRight()
    self.ship.rotateRightOff()
    after = self.ship.isRotatingRight()    
    self.failIf(before == after)
    self.failIf(before == False)
    self.failIf(after == True)

  def testIsRotatingRight(self):
    isRotatingRight = self.ship.isRotatingRight()
    self.failUnless( isinstance(isRotatingRight, bool) )

  def testUpdate(self):
    # Test thrustOn and visual node position changing
    velBefore = self.ship.getVel()
    posBefore = self.ship.getPos()
    visualNodePosBefore = self.ship.getVisualNode().getPos()
    self.ship.thrustOn()
    self.ship.update(1.0) # 1.0 seconds has passed.
    velAfter = self.ship.getVel()
    posAfter = self.ship.getPos()
    visualNodePosAfter = self.ship.getVisualNode().getPos()
    self.failUnless(velBefore < velAfter)
    self.failUnless(posBefore != posAfter)
    self.failUnless(visualNodePosAfter != visualNodePosBefore)

    # Test rotating left
    headingBefore = self.ship.heading
    visualNodeHeadingBefore = self.ship.getVisualNode().getH()
    self.ship.rotateLeftOn()
    self.ship.update(1.0)
    headingAfter = self.ship.heading
    visualNodeHeadingAfter = self.ship.getVisualNode().getH()
    self.failUnless(headingBefore != headingAfter)
    self.failUnless(visualNodeHeadingBefore != visualNodeHeadingAfter)

  def testLimitVelocity(self):
    vel = (1,1)
    self.ship.setVel(vel)
    self.ship.limitVelocity()
    newVel = self.ship.getVel()
    newVelScalar = tupleLength(newVel)
    self.failIf(newVelScalar > Ship.SPEED_MAX)
    self.failIf(newVelScalar < 0)

    vel = (Ship.SPEED_MAX, Ship.SPEED_MAX)
    self.ship.setVel(vel)
    self.ship.limitVelocity()
    newVel = self.ship.getVel()
    newVelScalar = tupleLength(newVel)
    self.failUnless( abs(newVelScalar - Ship.SPEED_MAX) < 0.01)

    
  def testAddCollision(self):
    self.ship.addCollision( point3ToTuple( Point3(1, 2, 0) ) )
    self.failIfEqual( self.ship.getCollisions(), [] )
    
  def testApplyForce(self):
    self.ship.applyForce( (1, 5) )
    self.failIfEqual( self.ship.forces, [] )

  # ####################################################################
  # Feature tests
  #
  # These tests don't necessarily test any single method, but rather
  # features. They are slightly more complex in that the focus of a
  # feature test is a higher level concept, such as gravity, collisions
  # or forces.
  # ####################################################################
  def testForce(self):
    oldPos = self.ship.getPos()
    self.ship.update(.01)
    newPos = self.ship.getPos()
    self.failUnlessEqual( oldPos, newPos )
    
    self.ship.applyForce( (4, 6) )
    oldPos = self.ship.getPos()
    self.ship.update(.01)
    newPos = self.ship.getPos()
    self.failIfEqual( oldPos, newPos )
