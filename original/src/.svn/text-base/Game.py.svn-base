################################################################################
#
# Two Ships And A Planet - Tsaap
#
# Authors: Miika Vihersaari and Vesa Nieminen
#
# Version: 0.1
#
################################################################################

import sys, math, random

import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import (
  getModelPath,
  Filename,
  OdeHashSpace,
  OdeWorld,
  OdeUtil,
  OdeSphereGeom,
  AmbientLight,
  DirectionalLight,
  Vec3,
  Vec4,
  Quat,
  AntialiasAttrib,
  TextNode
)

from Ship import Ship
from Player import Player
from Event import Event, createNamedEvent
from Utils import (
  tupleToVec3,
  tripleToVec3,
  vec3ToTriple,
  vec3ToTuple,
  point3ToTuple,
  tupleDistance,
  tupleDistanceSquared,
  tupleNormalize,
  tupleMiddle,
  tupleSegment,
  scaleTuple,
  tupleFurthestDistance
)

class Game:

  STATE_INITIALIZING = "Initializing"
  STATE_RUNNING = "Running"
  SHIPS_MAX_X_DISTANCE = 330.0
  SHIPS_MAX_Y_DISTANCE = 250.0
  NAME_SHIP_ONE = "Ship 1"
  NAME_SHIP_TWO = "Ship 2"
  NAME_PLAYER_ONE = "Player 1"
  NAME_PLAYER_TWO = "Player 2"
  START_POS_SHIP_ONE = (100, 100)
  START_POS_SHIP_TWO = (-100, -100)
  START_HEADING_SHIP_ONE = -135.0
  START_HEADING_SHIP_TWO = 45.0
  PLAYER_ONE_FORWARD_KEY = "arrow_up"
  PLAYER_ONE_ROTATE_LEFT_KEY = "arrow_left"
  PLAYER_ONE_ROTATE_RIGHT_KEY = "arrow_right"
  PLAYER_ONE_SHOOT = "rcontrol"
  PLAYER_TWO_FORWARD_KEY = "w"
  PLAYER_TWO_ROTATE_LEFT_KEY = "a"
  PLAYER_TWO_ROTATE_RIGHT_KEY = "d"
  PLAYER_TWO_SHOOT = "lcontrol"
  HUD_TEXT_SCALE = 0.05
  HUD_PLAYER_ONE_X = -1.25
  HUD_PLAYER_TWO_X = 1.05
  HUD_Y_FIRST_LINE = 0.85
  HUD_Y_SECOND_LINE = 0.75
  HUD_Y_THIRD_LINE = 0.65
  CAMERA_POS_DEFAULT = (0.0, 0.0, 250.0)
  CAMERA_HPR_DEFAULT = (0.0, -90.0, 0.0)
  CAMERA_DISTANCE_COEFFICIENT = 3.0
  CAMERA_DISTANCE_MAX = 450.0
  CAMERA_DISTANCE_MIN = 150.0
  CAMERA_MODE_GAME = "Game"
  CAMERA_MODE_FPS_ONE = "Fps 1"
  CAMERA_MODE_FPS_TWO = "Fps 2"
  CAMERA_MODE_STILL = "Still"
  CAMERA_FPS_OFFSET_HEIGHT = 2.0
  CAMERA_FPS_OFFSET_BACK = 15.0
  WINNER_TEXT = "has won the round"
  PLANET_POSITION = (0, 0)
  PLANET_CAMERA_DISTANCE_MAX = 400.0
  MATCH_MAX_POINTS = 5
  GRAVITY_DISTANCE = 100.0
  GRAVITY = 2000.0

  def __init__(self):
    # Disable Panda's base camera mover
    base.disableMouse()
    base.setBackgroundColor(0,0,0,0)
    self.state = Game.STATE_INITIALIZING
    # contains a list of the ships in game
    self.ships = None
    self.players = None
    self.bullets = None
    self.stars = None
    self.planet = None
    self.time = 0.0
    self.isListening = False
    getModelPath().prependDirectory( Filename('./media/') )
    
    self.physWorld = OdeWorld()
    self.physWorld.setGravity(0, 0, 0)
    self.physWorld.initSurfaceTable(1)
    self.physWorld.setSurfaceEntry(
      0,
      0,
      1.0, # u
      .35, # elasticity
      .01, # minimum threshold for physical movement
      .01, #
      .00000001, # softening
      .01, #
      .01) # dampening
    
    self.physSpace = OdeHashSpace()
    self.winnerText = None
    self.gameFrames = 0
    self.lastWarp = 0
    self.cameraMode = Game.CAMERA_MODE_GAME
    self.lastCameraPos = None
    self.pause = False

  def start(self):
    self.resetCamera()
    self.loadPlanet()
    self.loadShips()
    self.loadPlayers()
    self.loadStars()
    self.loadHUD()
    
    light = DirectionalLight('light')
    light.setDirection( Vec3(-1, .1, -.5) )
    light.setColor( Vec4(.7, .6, .6, 0) )
    light.setSpecularColor( Vec4(.3, .5, .7, 0) )
    lightnode = render.attachNewNode(light)
    render.setLight(lightnode)

    render.setShaderAuto()
    render.setShaderInput('light', lightnode)

    render.setAntialias(AntialiasAttrib.MAuto)

    # TODO: it might be necessary here to check that the task
    # does not already exist in the task manager because the
    # unit tests at the moment call the start method
    # continuously.
    taskMgr.add(self.tick, "gameloop")
    self.time = self.getTime()
    self.registerListeners()
    self.state = Game.STATE_RUNNING
    
    # Load music
    self.music = loader.loadSfx('MVi - Ilwrath Are Watching.mp3')
    self.music.setLoop(True)
    self.music.setVolume(0.5)
    self.music.play()    

  def loadHUD(self):
    self.winnerText = OnscreenText(
      text= "Insert Winner Text Here",
      style=1,
      fg=(1,1,1,1),
      pos=(-0.25, 0),
      align=TextNode.ALeft,
      scale = .07
    )
    self.winnerText.hide()
    self.scoreTextPlayerOne = OnscreenText(
      text= "Player 1:",
      style=1,
      fg=(1,1,1,1),
      pos=(Game.HUD_PLAYER_ONE_X, Game.HUD_Y_FIRST_LINE),
      align=TextNode.ALeft,
      scale = Game.HUD_TEXT_SCALE
    )
    self.scorePlayerOne = OnscreenText(
      text= "Score: 0",
      style=1,
      fg=(1,1,1,1),
      pos=(Game.HUD_PLAYER_ONE_X, Game.HUD_Y_SECOND_LINE),
      align=TextNode.ALeft,
      scale = Game.HUD_TEXT_SCALE
    )
    self.healthPlayerOne = OnscreenText(
      text= "Health: " + str(Ship.HEALTH),
      style=1,
      fg=(1,1,1,1),
      pos=(Game.HUD_PLAYER_ONE_X, Game.HUD_Y_THIRD_LINE),
      align=TextNode.ALeft,
      scale = Game.HUD_TEXT_SCALE
    )

    self.scoreTextPlayerTwo = OnscreenText(
      text= "Player 2:",
      style=1,
      fg=(1,1,1,1),
      pos=(Game.HUD_PLAYER_TWO_X, Game.HUD_Y_FIRST_LINE),
      align=TextNode.ALeft,
      scale = Game.HUD_TEXT_SCALE
    )
    self.scorePlayerTwo = OnscreenText(
      text= "Score: 0",
      style=1,
      fg=(1,1,1,1),
      pos=(Game.HUD_PLAYER_TWO_X, Game.HUD_Y_SECOND_LINE),
      align=TextNode.ALeft,
      scale = Game.HUD_TEXT_SCALE
    )
    self.healthPlayerTwo = OnscreenText(
      text= "Health: " + str(Ship.HEALTH),
      style=1,
      fg=(1,1,1,1),
      pos=(Game.HUD_PLAYER_TWO_X, Game.HUD_Y_THIRD_LINE),
      align=TextNode.ALeft,
      scale = Game.HUD_TEXT_SCALE
    )  
  
  def generateRandomPos( self ):
    return (
      random.random() * Game.SHIPS_MAX_X_DISTANCE - Game.SHIPS_MAX_X_DISTANCE / 2.,
      random.random() * Game.SHIPS_MAX_Y_DISTANCE - Game.SHIPS_MAX_Y_DISTANCE / 2.
    )
    
  def generateRandomStartPos( self, offlimits = [] ):
    pos = self.generateRandomPos()
    while not self.checkIfStartPosValid( pos, offlimits ):
      pos = self.generateRandomPos()
    return pos
    
  def checkIfStartPosValid( self, pos, offlimits ):
    for o in offlimits:
      if tupleDistanceSquared( pos, o[0] ) < o[1]**2:
        return False
    return True

  def getBullets(self):
    ships = self.getShips()
    shipOne = ships[0]
    shipTwo = ships[1]
    bullets = [shipOne.bullets, shipTwo.bullets]
    return bullets

  def resetCamera(self):
    self.setCameraPos(Game.CAMERA_POS_DEFAULT)
    self.setCameraHpr(Game.CAMERA_HPR_DEFAULT)
    pos = Game.CAMERA_POS_DEFAULT
    self.lastCameraPos = ( pos[0], pos[1] )

  def setCameraPos(self, pos):
    base.camera.setPos( tripleToVec3(pos) )

  def getCameraPos(self):
    return vec3ToTriple( base.camera.getPos() )

  def setCameraHpr(self, hpr):
    base.camera.setHpr( tripleToVec3(hpr) )

  def getCameraHpr(self):
    return vec3ToTriple( base.camera.getHpr() )

  def getTime(self):
    return globalClock.getFrameTime()

  def getDeltaTime(self):
    return globalClock.getDt()

  def run(self):
    """Call this to run the game. Untested because this method won't return."""
    taskMgr.run()

  def loadShips(self):
    shipOne = Ship(
      Game.NAME_SHIP_ONE,
      Game.START_POS_SHIP_ONE,
      Game.START_HEADING_SHIP_ONE
    )
    shipTwo = Ship(
      Game.NAME_SHIP_TWO,
      Game.START_POS_SHIP_TWO,
      Game.START_HEADING_SHIP_TWO
    )
    offlimits = [ ( vec3ToTuple( self.planet.getPos() ), Game.GRAVITY_DISTANCE ) ]
    shipOne.setPos( self.generateRandomStartPos( offlimits ) )
    shipOne.heading = random.random()*360
    shipTwo.heading = random.random()*360
    offlimits.append( ( shipOne.getPos(), 150 ) )
    shipTwo.setPos( self.generateRandomStartPos( offlimits ) )
    self.ships = []
    self.ships.append(shipOne)
    self.ships.append(shipTwo)

  def loadPlayers(self):
    playerOne = Player(Game.NAME_PLAYER_ONE)
    playerTwo = Player(Game.NAME_PLAYER_TWO)
    self.players = []
    self.players.append(playerOne)
    self.players.append(playerTwo)

  def loadStars(self):
    ambientlight = AmbientLight('alight')
    ambientlight.setColor( Vec4(1, 1, 1, 0) )
    lightnode = render.attachNewNode(ambientlight)
    self.stars = loader.loadModel("stars.bam")
    self.stars.setLight(lightnode)
    self.stars.setScale(1000)
    self.stars.setPos(0,0,0)
    self.stars.reparentTo(render)
    self.starsRotation = self.stars.getQuat()

  def loadPlanet(self):
    self.planet = loader.loadModel('planet.bam')
    self.planet.setPos( tupleToVec3(Game.PLANET_POSITION) )
    self.planet.setScale(20)
    self.planet.reparentTo(render)

    self.planetCollGeom = OdeSphereGeom(20)
    #self.planetCollGeom.setCategoryBits( BitMask32(0xffffffff) )
    #self.planetCollGeom.setCollideBits( BitMask32(0xffffffff) )

  def updateCamera(self):
    ships = self.getShips()
    shipOne = ships[0]
    shipOnePos = shipOne.getPos()
    shipTwo = ships[1]
    shipTwoPos = shipTwo.getPos()

    # Calculate the distance between the ships
    distance = tupleDistance(shipOnePos, shipTwoPos)
    cameraDistance = distance * Game.CAMERA_DISTANCE_COEFFICIENT
    if cameraDistance > Game.CAMERA_DISTANCE_MAX:
      cameraDistance = Game.CAMERA_DISTANCE_MAX
    if cameraDistance < Game.CAMERA_DISTANCE_MIN:
      cameraDistance = Game.CAMERA_DISTANCE_MIN
    # Calculate the middle point in space between the ship's positions
    middle = tupleMiddle(shipOnePos, shipTwoPos)
    cameraPos = self.getCameraPos()
    self.lastCameraPos = cameraPos
    newCameraPos = (middle[0], middle[1], cameraDistance)
    self.setCameraPos(newCameraPos)
    self.updateStars(newCameraPos)

  def updateStars(self, newCameraPos):
    # TODO: Add unit tests!
    self.stars.setPos(newCameraPos)
    cameraDeltaPos = tupleSegment(
      self.lastCameraPos,
      vec3ToTuple( newCameraPos )
    )
    xRotation = Quat()
    xRotation.setFromAxisAngle(
      cameraDeltaPos[0] * .1,
      Vec3( 0, 1, 0 )
    )
    yRotation = Quat()
    yRotation.setFromAxisAngle(
      -cameraDeltaPos[1] * .1,
      Vec3( 1, 0, 0 )
    )
    newRotation = xRotation.multiply( yRotation )
    self.starsRotation *= newRotation
    self.stars.setQuat( self.starsRotation )
    # With Euler angles:
    #self.stars.setHpr(0, -newCameraPos[1] * 0.1, newCameraPos[0] * 0.1 )

  def applyGravity(self, ship, deltaTime):
    distance = tupleDistance(
      ship.getPos(),
      vec3ToTuple( self.planet.getPos() )
    )
    if distance > Game.GRAVITY_DISTANCE: return
    gravity = Game.GRAVITY/distance
    gravityVector = tupleNormalize(
      tupleSegment(
        ship.getPos(),
        vec3ToTuple( self.planet.getPos() )
      )
    )
    gravityVector = scaleTuple( gravityVector, gravity * deltaTime)
    ship.applyForce( gravityVector )

  def tick(self, task):
    if not self.pause:
      ships = self.getShips()

      # Check if the ships' positions need to be warped
      xDistance = abs(ships[0].getPos()[0] - ships[1].getPos()[0] )
      if xDistance >= Game.SHIPS_MAX_X_DISTANCE:
        #and self.gameFrames - self.lastWarp > 10:
        self.warpShips('x')
        #self.lastWarp = self.gameFrames
      yDistance = abs(ships[0].getPos()[1] - ships[1].getPos()[1] )
      if yDistance >= Game.SHIPS_MAX_Y_DISTANCE:
        self.warpShips('y')

      # Check if the planet's position needs to be warped
      planetXDistance = abs( self.getCameraPos()[0] - self.planet.getPos()[0] )
      if planetXDistance >= Game.PLANET_CAMERA_DISTANCE_MAX:
        self.warpPlanet('x')
      planetYDistance = abs( self.getCameraPos()[1] - self.planet.getPos()[1] )
      if planetYDistance >= Game.PLANET_CAMERA_DISTANCE_MAX:
        self.warpPlanet('y')

      # Check collisions
      col = OdeUtil.collide(ships[0].collisionSphere, ships[1].collisionSphere, 1)
      if not col.isEmpty():
        ships[0].addCollision( point3ToTuple( col.getContactPoint(0) ) )
        ships[1].addCollision( point3ToTuple( col.getContactPoint(0) ) )
      colPlanet1 = OdeUtil.collide(ships[0].collisionSphere, self.planetCollGeom, 1)
      colPlanet2 = OdeUtil.collide(ships[1].collisionSphere, self.planetCollGeom, 1)
      if not colPlanet1.isEmpty():
        ships[0].addCollision( point3ToTuple( colPlanet1.getContactPoint(0) ) )
        ships[0].planetHit()
      if not colPlanet2.isEmpty():
        ships[1].addCollision( point3ToTuple( colPlanet2.getContactPoint(0) ) )
        ships[1].planetHit()

      # Bullet collisions ship one
      for bullet in ships[0].bullets:
        colBulletShip1 = OdeUtil.collide( bullet['physical'], ships[1].collisionSphere, 1 )
        if not colBulletShip1.isEmpty():
          ships[0].destroyBullet(bullet)
          ships[1].bulletHit()
        colBulletPlanet = OdeUtil.collide( bullet['physical'], self.planetCollGeom, 1 )
        if not colBulletPlanet.isEmpty():
          ships[0].destroyBullet(bullet)
      # Bullet collisions ship two
      for bullet in ships[1].bullets:
        colBulletShip2 = OdeUtil.collide( bullet['physical'], ships[0].collisionSphere, 1 )
        if not colBulletShip2.isEmpty():
          ships[1].destroyBullet(bullet)
          ships[0].bulletHit()
        colBulletPlanet = OdeUtil.collide( bullet['physical'], self.planetCollGeom, 1 )
        if not colBulletPlanet.isEmpty():
          ships[1].destroyBullet(bullet)
      for ship in ships:
        self.applyGravity( ship, self.getDeltaTime() )
        ship.update( self.getDeltaTime() )

      if not ships[0].isAlive:
        self.showWinnerText(self.players[1])
        self.players[1].score += 1
        self.restartGame()
      if not ships[1].isAlive:
        self.showWinnerText(self.players[0])
        self.players[0].score += 1
        self.restartGame()
      if self.cameraMode == Game.CAMERA_MODE_GAME:
        self.updateCamera()
      if self.gameFrames >= 125:
        self.winnerText.hide()
      self.gameFrames += 1

      # Update health points in the HUD
      # TODO: These should be optimized so that they get updated only when they
      # change.
      self.healthPlayerOne.setText( "Health: " + str(self.ships[0].health) )
      self.healthPlayerTwo.setText( "Health: " + str(self.ships[1].health) )

    return task.cont

  def distanceToPlanetSquared(self, pos):
    return tupleDistanceSquared(
      pos,
      vec3ToTuple( self.planet.getPos() )
    )

  def warpShips(self, warpAxis):
    shipOne = self.ships[0]
    shipTwo = self.ships[1]

    shipOnePos = shipOne.getPos()
    shipTwoPos = shipTwo.getPos()

    furtherShip = None
    closerShip = None

    if shipOnePos == tupleFurthestDistance(
      vec3ToTuple( self.planet.getPos() ),
      [shipOnePos, shipTwoPos]
    ):
      furtherShip = shipOne
      closerShip = shipTwo
    else:
      closerShip = shipOne
      furtherShip = shipTwo

    furtherToCloser = tupleSegment(
      furtherShip.getPos(), closerShip.getPos()
    )

    if warpAxis == 'x':
      furtherShip.setPos(
        (
          furtherShip.getPos()[0] + furtherToCloser[0]*2,
          furtherShip.getPos()[1]
        )
      )
    elif warpAxis == 'y':
      furtherShip.setPos(
        (
          furtherShip.getPos()[0],
          furtherShip.getPos()[1] + furtherToCloser[1]*2
        )
      )

  def warpPlanet(self, warpAxis):
    planetPos = vec3ToTuple( self.planet.getPos() )
    planetToCamera = tupleSegment( planetPos, self.getCameraPos() )

    if warpAxis == 'x':
      self.planet.setPos(
        planetPos[0] + planetToCamera[0]*2,
        planetPos[1],
        0
      )
      self.planetCollGeom.setPosition(
        planetPos[0] + planetToCamera[0]*2,
        planetPos[1],
        0
      )
    elif warpAxis == 'y':
      self.planet.setPos(
        planetPos[0],
        planetPos[1] + planetToCamera[1]*2,
        0
      )
      self.planetCollGeom.setPosition(
        planetPos[0],
        planetPos[1] + planetToCamera[1]*2,
        0
      )

  def restartGame(self):
    self.planet.setPos( Vec3() )
    self.planetCollGeom.setPosition( Vec3() )

    offlimits = [ ( vec3ToTuple( self.planet.getPos() ), 102 ) ]
    
    # Reset ship one
    self.ships[0].setPos( self.generateRandomStartPos( offlimits ) )
    self.ships[0].heading = random.random()*360
    self.ships[0].setVel( Ship.VEL_DEFAULT )
    self.ships[0].isAlive = True
    self.ships[0].health = Ship.HEALTH
    self.ships[0].visualNode.show()
    for bullet in self.ships[0].bullets:
      bullet['isAlive'] = False

    offlimits.append( ( self.ships[0].getPos(), 128 ) )
    
    # Reset ship two
    self.ships[1].setPos( self.generateRandomStartPos( offlimits ) )
    self.ships[1].heading = random.random()*360
    self.ships[1].setVel( Ship.VEL_DEFAULT )
    self.ships[1].isAlive = True
    self.ships[1].health = Ship.HEALTH
    self.ships[1].visualNode.show()
    for bullet in self.ships[1].bullets:
      bullet['isAlive'] = False

    for s in self.ships:
      s.update( 1/60. )

    self.gameFrames = 0

    playerOneScore = self.players[0].score 
    playerTwoScore = self.players[1].score 
    if playerOneScore >= Game.MATCH_MAX_POINTS:
      self.showGameWinnerText(self.players[0])
      self.players[0].score = 0
      self.players[1].score = 0
    if playerTwoScore >= Game.MATCH_MAX_POINTS:
      self.showGameWinnerText(self.players[1])
      self.players[0].score = 0
      self.players[1].score = 0
    playerOneScore = self.players[0].score 
    playerTwoScore = self.players[1].score 
    self.scorePlayerOne.setText( 'Score: ' + str(playerOneScore) )
    self.scorePlayerTwo.setText( 'Score: ' + str(playerTwoScore) )

  def showWinnerText(self, player):
    self.winnerText.setText( player.name + " " + Game.WINNER_TEXT )
    self.winnerText.show()
  
  def showGameWinnerText(self, player):
    self.winnerText.setText( player.name + " wins the match!" )
    self.winnerText.show()

  def registerListeners(self):
    playerOne = self.getPlayers()[0]
    playerTwo = self.getPlayers()[1]
    shipOne = self.getShips()[0]
    shipTwo = self.getShips()[1]
    # Player one events
    playerOneMoveForwardOn = createNamedEvent(
      playerOne.name, Event.PLAYER_MOVE_FORWARD_ON
    )
    playerOneMoveForwardOff = createNamedEvent(
      playerOne.name, Event.PLAYER_MOVE_FORWARD_OFF
    )
    playerOneRotateLeftOn = createNamedEvent(
      playerOne.name, Event.PLAYER_ROTATE_LEFT_ON
    )
    playerOneRotateLeftOff = createNamedEvent(
      playerOne.name, Event.PLAYER_ROTATE_LEFT_OFF
    )
    playerOneRotateRightOn = createNamedEvent(
      playerOne.name, Event.PLAYER_ROTATE_RIGHT_ON
    )
    playerOneRotateRightOff = createNamedEvent(
      playerOne.name, Event.PLAYER_ROTATE_RIGHT_OFF
    )
    playerOneShoot = createNamedEvent(
      playerOne.name, Event.PLAYER_SHOOT
    )
    base.accept(playerOneMoveForwardOn, shipOne.thrustOn)
    base.accept(playerOneMoveForwardOff, shipOne.thrustOff)
    base.accept(playerOneRotateLeftOn, shipOne.rotateLeftOn)
    base.accept(playerOneRotateLeftOff, shipOne.rotateLeftOff)
    base.accept(playerOneRotateRightOn, shipOne.rotateRightOn)
    base.accept(playerOneRotateRightOff, shipOne.rotateRightOff)
    base.accept(playerOneShoot, shipOne.shoot)

    # Player two events
    playerTwoMoveForwardOn = createNamedEvent(
      playerTwo.name, Event.PLAYER_MOVE_FORWARD_ON
    )
    playerTwoMoveForwardOff = createNamedEvent(
      playerTwo.name, Event.PLAYER_MOVE_FORWARD_OFF
    )
    playerTwoRotateLeftOn = createNamedEvent(
      playerTwo.name, Event.PLAYER_ROTATE_LEFT_ON
    )
    playerTwoRotateLeftOff = createNamedEvent(
      playerTwo.name, Event.PLAYER_ROTATE_LEFT_OFF
    )
    playerTwoRotateRightOn = createNamedEvent(
      playerTwo.name, Event.PLAYER_ROTATE_RIGHT_ON
    )
    playerTwoRotateRightOff = createNamedEvent(
      playerTwo.name, Event.PLAYER_ROTATE_RIGHT_OFF
    )
    playerTwoShoot = createNamedEvent(
      playerTwo.name, Event.PLAYER_SHOOT
    )
    base.accept(playerTwoMoveForwardOn, shipTwo.thrustOn)
    base.accept(playerTwoMoveForwardOff, shipTwo.thrustOff)
    base.accept(playerTwoRotateLeftOn, shipTwo.rotateLeftOn)
    base.accept(playerTwoRotateLeftOff, shipTwo.rotateLeftOff)
    base.accept(playerTwoRotateRightOn, shipTwo.rotateRightOn)
    base.accept(playerTwoRotateRightOff, shipTwo.rotateRightOff)
    base.accept(playerTwoShoot, shipTwo.shoot)

    # Player one key mapping
    base.accept(Game.PLAYER_ONE_FORWARD_KEY, playerOne.moveForwardOn)
    base.accept("control-" + Game.PLAYER_ONE_FORWARD_KEY, playerOne.moveForwardOn)
    base.accept(Game.PLAYER_ONE_FORWARD_KEY + "-up", playerOne.moveForwardOff)
    base.accept(Game.PLAYER_ONE_ROTATE_LEFT_KEY, playerOne.rotateLeftOn)
    base.accept("control-" + Game.PLAYER_ONE_ROTATE_LEFT_KEY, playerOne.rotateLeftOn)
    base.accept(Game.PLAYER_ONE_ROTATE_LEFT_KEY + "-up", playerOne.rotateLeftOff)
    base.accept(Game.PLAYER_ONE_ROTATE_RIGHT_KEY, playerOne.rotateRightOn)
    base.accept("control-" + Game.PLAYER_ONE_ROTATE_RIGHT_KEY, playerOne.rotateRightOn)
    base.accept(Game.PLAYER_ONE_ROTATE_RIGHT_KEY + "-up", playerOne.rotateRightOff)
    base.accept(Game.PLAYER_ONE_SHOOT, playerOne.shoot)

    # Player two key mapping
    base.accept(Game.PLAYER_TWO_FORWARD_KEY, playerTwo.moveForwardOn)
    base.accept("control-" + Game.PLAYER_TWO_FORWARD_KEY, playerTwo.moveForwardOn)
    base.accept(Game.PLAYER_TWO_FORWARD_KEY + "-up", playerTwo.moveForwardOff)
    base.accept(Game.PLAYER_TWO_ROTATE_LEFT_KEY, playerTwo.rotateLeftOn)
    base.accept("control-" + Game.PLAYER_TWO_ROTATE_LEFT_KEY, playerTwo.rotateLeftOn)
    base.accept(Game.PLAYER_TWO_ROTATE_LEFT_KEY + "-up", playerTwo.rotateLeftOff)
    base.accept(Game.PLAYER_TWO_ROTATE_RIGHT_KEY, playerTwo.rotateRightOn)
    base.accept("control-" + Game.PLAYER_TWO_ROTATE_RIGHT_KEY, playerTwo.rotateRightOn)
    base.accept(Game.PLAYER_TWO_ROTATE_RIGHT_KEY + "-up", playerTwo.rotateRightOff)
    base.accept(Game.PLAYER_TWO_SHOOT, playerTwo.shoot)

    # Game specific key mapping
    base.accept("escape", sys.exit)
    base.accept( "f1", self.switchCameraMode, [Game.CAMERA_MODE_FPS_ONE] )
    base.accept( "f2", self.switchCameraMode, [Game.CAMERA_MODE_FPS_TWO] )
    base.accept( "f3", self.switchCameraMode, [Game.CAMERA_MODE_GAME] )
    base.accept( "f4", self.switchCameraMode, [Game.CAMERA_MODE_STILL] )
    base.accept( "p", self.togglePause )

    # The game is now listening to all the necessary events
    self.isListening = True

  def togglePause(self):
    self.pause = not self.pause
    
  def windowExists(self):
    return base.isMainWindowOpen()

  def getShips(self):
    return self.ships

  def getPlayers(self):
    return self.players

  def switchCameraMode(self, cameraMode):
    self.cameraMode = cameraMode
    if cameraMode == Game.CAMERA_MODE_FPS_ONE:
      angle = self.ships[0].heading * math.pi / 180.0
      headingX = math.cos(angle)
      headingY = math.sin(angle)
      offset = Vec3( headingX, headingY, 0 )

      pos = self.ships[0].visualNode.getChildren()[0].getPos()
      base.camera.setPos( pos[0] + offset[0],
        pos[1] + offset[1] - Game.CAMERA_FPS_OFFSET_HEIGHT,
        pos[2] - Game.CAMERA_FPS_OFFSET_BACK
      )
      hpr = self.ships[0].visualNode.getChildren()[0].getHpr()
      base.camera.setHpr( hpr[0], hpr[1] + 90, hpr[2] )
      base.camera.reparentTo(self.ships[0].visualNode)
    if cameraMode == Game.CAMERA_MODE_FPS_TWO:
      angle = self.ships[1].heading * math.pi / 180.0
      headingX = math.cos(angle)
      headingY = math.sin(angle)
      offset = Vec3( headingX, headingY, 0 )

      pos = self.ships[1].visualNode.getChildren()[0].getPos()
      base.camera.setPos( pos[0] + offset[0],
        pos[1] + offset[1] - Game.CAMERA_FPS_OFFSET_HEIGHT,
        pos[2] - Game.CAMERA_FPS_OFFSET_BACK
      )
      hpr = self.ships[1].visualNode.getChildren()[0].getHpr()
      base.camera.setHpr( hpr[0], hpr[1] + 90, hpr[2] )
      base.camera.reparentTo(self.ships[1].visualNode)
    if cameraMode == Game.CAMERA_MODE_GAME:
      base.camera.setHpr(Game.CAMERA_HPR_DEFAULT)
      base.camera.reparentTo(render)
    if cameraMode == Game.CAMERA_MODE_STILL:
      base.camera.reparentTo(render)


