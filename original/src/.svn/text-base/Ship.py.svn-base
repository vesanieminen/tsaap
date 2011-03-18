import math

from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import (
  Vec3,
  Vec4,
  NodePath,
  OdeSphereGeom,
  BitMask32,
  AmbientLight
)

from Utils import (
  tupleToVec3,
  tripleToVec3,
  addTuples,
  scaleTuple,
  tupleLength,
  tupleSegment,
  tupleNormalize,
  dotProduct,
  normalizedDotProduct
)

def colHandler(ship, contact):
  pos = ship.getPos()
  
  elasticity = 2.5
  #mass1 = ship.getMass()
  #mass2 = collider.getMass()
  vel1 = ship.getVel()
  normal = tupleNormalize( tupleSegment( pos, contact ) )
  force = (
    scaleTuple(
      normal,
      -elasticity *
      ( 1/2. ) *
      dotProduct( vel1, normal )
    )
  )
  
  ship.applyForce(force)
  ship.setPos( addTuples( ship.getPos(), scaleTuple( normal, -.1 ) ) )
  ship.getCollisions().remove(contact)

class Ship:

  NAME_DEFAULT = "unnamed"
  POS_DEFAULT = (0, 30)
  VEL_DEFAULT = (0, 0)
  ACC_DEFAULT = 0.0 # 0.0 - 1.0
  HEADING_DEFAULT = -90.0
  ACC_COEFFICIENT = 35.0 # This is how much acceleration affects speed
  ROTATION_SPEED = 200
  MODEL_ROTATION_OFFSET = (0.0, 0.0, -5.0)
  HEALTH = 10.0
  BULLET_OFFSET = 5.0 # This is how far ahead the bullet spawns at
  BULLET_SPEED = 200
  BULLET_SHIP_SPEED_CORRELATION = 40.0
  BULLET_MAX_LIFE_TIME = 100
  BULLET_DAMAGE = 1.0
  PLANET_DAMAGE = 0.5
  SPEED_MAX = 50.0

  def __init__(
    self,
    name = NAME_DEFAULT,
    pos = POS_DEFAULT,
    heading = HEADING_DEFAULT,
    vel = VEL_DEFAULT,
    acc = ACC_DEFAULT # player controlled acceleration. Can be 0.0 - 1.0
  ):
    """@param name string"""
    self.name = name
    self.pos = pos
    self.vel = vel
    self.acc = acc
    self.heading = heading
    self.rotateLeft = False
    self.rotateRight = False
    self.visualNode = self.createVisualNode(self.pos)
    self.bullets = []
    self.collisionHandler = colHandler
    self.collisions = []
    self.collisionSphere = OdeSphereGeom(4)
    self.collisionSphere.setCategoryBits( BitMask32(0xffffffff) )
    self.collisionSphere.setCollideBits( BitMask32(0xffffffff) )
    self.collisionSphere.setPosition(pos[0], pos[1], 0)
    self.forces = []
    self.mass = 1.0
    self.health = Ship.HEALTH
    self.isAlive = True
    self.shootingSound = loader.loadSfx('anti_tank_gun_single_shot.mp3')
    self.destroySound = loader.loadSfx('large_explosion.mp3')
    self.bulletHitSound = loader.loadSfx('explosion_loud_internal_explosion_very_reverberant.mp3')
    self.collisionSound = loader.loadSfx('car_door_close.mp3')
    self.bulletParent = NodePath("Bullet Parent")
    self.bulletParent.reparentTo(render)
    self.bulletAmbientLight = AmbientLight('Bullet Light')
    self.bulletAmbientLight.setColor( Vec4(.0, .1, .2, .0) )
    lightnode = render.attachNewNode(self.bulletAmbientLight)
    self.bulletParent.setLight(lightnode)
        
  def createVisualNode( self, pos = (0, 0) ):
    # modelNode is the actualy ship model
    modelNode = loader.loadModel("indicator.bam")
    # visualNode is the node we operate on to move and rotate the ship
    visualNode = NodePath('Ship: ' + self.name)
    visualNode.setPos( tupleToVec3(pos) )
    visualNode.setHpr( Vec3(0,-90,90) )
    # TODO: add scale parameter to this or some other aggregator class
    visualNode.setScale(1)
    # Reparent the actual modelNode to the visualNode
    modelNode.reparentTo(visualNode)
    # Offset the model node relative to the parent
    modelNode.setPos( tripleToVec3(Ship.MODEL_ROTATION_OFFSET) )
    visualNode.reparentTo(render)
    return visualNode

  def applyForce(self, force):
    self.forces.append(force)
    
  def setCollisionHandler(self, handler):
    self.collisionHandler = handler
    
  def addCollision(self, col):
    self.collisions.append(col)
    self.collisionSound.play()
    
  def getCollisions(self):
    return self.collisions
    
  def getVisualNode(self):
    return self.visualNode
  
  def getMass(self):
    return self.mass
    
  def isVisible(self):
    result = False
    visualNode = self.getVisualNode()
    # To be visible the ship has to be not hidden and has to have render as
    # the master parent (aka getTop).
    result = ( not visualNode.isHidden() ) and (
      visualNode.getTop() == render
    )
    return result

  def setPos(self, pos):
    self.pos = pos
    
  def getPos(self):
    return self.pos

  def setVel(self, vel):
    self.vel = vel
    self.momentum = vel
    
  def getVel(self):
    return self.vel
     
  def getAcc(self):
    return self.acc

  def getHeading(self):
    return self.heading

  def shoot(self):
    # TODO: add proper unit tests!
    angle = self.heading * math.pi / 180.0
    headingX = math.cos(angle)
    headingY = math.sin(angle)
    offset = Vec3( headingX, headingY, 0 ) * Ship.BULLET_OFFSET
    shipPos = self.getPos()
    bulletPos = ( offset[0] + shipPos[0], offset[1] + shipPos[1], offset[2] )

    bulletVisual = loader.loadModel("bullet.bam")
    bulletVisual.setPos( tupleToVec3(bulletPos) )
    bulletVisual.setHpr( tupleToVec3( (self.heading + 90, 180) ) )
    bulletVisual.setScale(1.5)
    bulletVisual.reparentTo(self.bulletParent)

    # Create physics for bullet
    collisionSphere = OdeSphereGeom(1.5)
    collisionSphere.setCategoryBits( BitMask32(0xffffffff) )
    collisionSphere.setCollideBits( BitMask32(0xffffffff) )
    collisionSphere.setPosition(bulletPos[0], bulletPos[1], bulletPos[2])

    shipVel = self.getVel()

    bullet = {
      'vel' : (
        headingX * Ship.BULLET_SPEED + shipVel[0]/ Ship.BULLET_SHIP_SPEED_CORRELATION,
        headingY * Ship.BULLET_SPEED + shipVel[1]/ Ship.BULLET_SHIP_SPEED_CORRELATION
      ),
      'visual' : bulletVisual,
      'physical' : collisionSphere,
      'isAlive' : True,
      'timeToLive' : Ship.BULLET_MAX_LIFE_TIME
    }
    self.bullets.append(bullet)
    self.shootingSound.play()

  def bulletHit(self):
    self.health -= Ship.BULLET_DAMAGE
    if self.health <= 0:
      self.destroy()
    self.bulletHitSound.play()

  def planetHit(self):
    self.health -= Ship.PLANET_DAMAGE
    if self.health <= 0.0:
      self.destroy()
    self.bulletHitSound.play()

  def destroyBullet(self, bullet):
    bullet['visual'].removeNode()
    #bullet['physical'].destroy()
    bullet['physical'].disable()
    # If the "bullet['physical'].destroy()" line is giving errors use the
    # following one instead:
    #bullet['physical'].disable()
    self.bullets.remove(bullet)
    bullet = None

  def destroy(self):
    self.isAlive = False
    self.visualNode.hide()
    self.destroySound.play()

  def thrustOn(self):
    self.acc = 1.0

  def thrustOff(self):
    self.acc = 0.0

  def rotateLeftOn(self):
    self.rotateLeft = True

  def rotateLeftOff(self):
    self.rotateLeft = False

  def isRotatingLeft(self):
    return self.rotateLeft

  def rotateRightOn(self):
    self.rotateRight = True

  def rotateRightOff(self):
    self.rotateRight = False

  def isRotatingRight(self):
    return self.rotateRight

  def update(self, deltaTime):
    """@param deltaTime float, how many seconds have passed since last tick"""
    # TODO: refactor the updating code into different methods

    # Update the bullets
    # TODO: Add test for this in testUpdate!
    for bullet in self.bullets:
      bullet['timeToLive'] -= 1
      if bullet['timeToLive'] <= 0:
        bullet['isAlive'] = False
      if not bullet['isAlive']:
        self.destroyBullet(bullet)
        continue

      pos = bullet['visual'].getPos()
      bulletPos = Vec3( bullet['vel'][0] * deltaTime + pos[0], bullet['vel'][1] * deltaTime + pos[1], 0 )
      bullet['visual'].setPos( bulletPos )
      bullet['physical'].setPosition( bulletPos )

    # If the ship is not alive anymore, we don't move it
    if not self.isAlive:
      return

    # update the heading. Must be done before position updating!
    if self.rotateLeft:
      self.heading = self.heading + Ship.ROTATION_SPEED * deltaTime
    elif self.rotateRight:
      self.heading = self.heading - Ship.ROTATION_SPEED * deltaTime

    for c in self.collisions:
      self.collisionHandler( self, c )
    # update position
    gainedSpeedScalar = self.acc * deltaTime * Ship.ACC_COEFFICIENT
    # convert degrees to radians
    angle = self.heading * math.pi / 180.0
    #correction = math.pi / 2
    deltaVelX = gainedSpeedScalar * math.cos(angle)
    deltaVelY = gainedSpeedScalar * math.sin(angle)

    for f in self.forces:
      deltaVelX += f[0]
      deltaVelY += f[1]
    self.forces = []

    self.vel = ( self.vel[0] + deltaVelX, self.vel[1] + deltaVelY )

    # Limit the ship's speed to Ship.SPEED_MAX
    self.limitVelocity()

    deltaPosX = deltaTime * self.vel[0]
    deltaPosY = deltaTime * self.vel[1]
    newPosX = self.pos[0] + deltaPosX
    newPosY = self.pos[1] + deltaPosY
    self.pos = (newPosX, newPosY)

    # Rotate the visual representation of the ship
    self.visualNode.setH(self.heading)
    # Move the actual visual representation
    self.visualNode.setPos( tupleToVec3(self.pos) )
    self.collisionSphere.setPosition( self.pos[0], self.pos[1], 0 )

  def limitVelocity(self):
    shipVel = self.getVel()
    newVelScalar = tupleLength(shipVel)
    if newVelScalar > Ship.SPEED_MAX:
      newVelScale = Ship.SPEED_MAX / newVelScalar
      newVel = scaleTuple(shipVel, newVelScale)
      self.setVel(newVel)
      

