from unittest import TestCase

from direct.showbase.ShowBase import ShowBase 

from Game import Game
from Ship import Ship
from Event import Event, createNamedEvent

class TestGame(TestCase):

  def setUp(self):
    self.game = Game()

  def tearDown(self):
    ships = self.game.getShips()
    if ships != None:
      for ship in ships:
        # TODO: Find out why removeNode does not work here 
        #ship.visualNode.removeNode()
        ship.visualNode.detachNode()
        ship = None

  def testInit(self):
    self.failUnless(self.game)
    self.failUnlessEqual(self.game.state, Game.STATE_INITIALIZING)
    self.failUnless( self.game.windowExists() )
    self.failIf( self.game.getShips() )
    self.failUnless(self.game.physWorld)
    self.failUnless(self.game.physSpace)

  def testStart(self):
    self.game.start()
    self.failUnlessEqual(self.game.state, Game.STATE_RUNNING)
    ships = self.game.getShips()
    shipOne = ships[0]
    shipTwo = ships[1]
    self.failUnless( isinstance(ships, list) )
    self.failUnlessEqual( shipOne.name, Game.NAME_SHIP_ONE )
    self.failUnlessEqual( shipTwo.name, Game.NAME_SHIP_TWO )
    self.failUnless(shipOne.getVisualNode)
    self.failUnless(shipTwo.getVisualNode)
    self.failUnless( shipOne.isVisible() )
    self.failUnless( shipTwo.isVisible() )
    players = self.game.getPlayers()
    self.failUnless( isinstance(players, list) )
    playerOne = players[0]
    playerTwo = players[1]
    self.failUnlessEqual( playerOne.name, Game.NAME_PLAYER_ONE )
    self.failUnlessEqual( playerTwo.name, Game.NAME_PLAYER_TWO )

    # Test that the player can move the ship forward
    pos1 = shipOne.getPos()
    vel1 = shipOne.getVel()
    acc1 = shipOne.getAcc()
    playerOne.moveForwardOn()
    # Step Panda3D's task manager one tick forward
    taskMgr.step()
    pos2 = shipOne.getPos()
    vel2 = shipOne.getVel()
    acc2 = shipOne.getAcc()
    self.failIf(pos1 == pos2)
    self.failIf(vel1 == vel2)
    self.failIf(acc1 == acc2)

    # Make sure the game is listening to events
    self.failUnless(self.game.isListening)

  def testResetCamera(self):
    self.game.resetCamera()
    # Check that the camera has been moved to the correct position
    cameraPos = self.game.getCameraPos()
    defaultCameraPos = Game.CAMERA_POS_DEFAULT
    self.failUnless(cameraPos == defaultCameraPos)

  def testSetCameraPos(self):
    pos = (0, 0, 50)
    self.game.setCameraPos( pos )
    self.failUnless( self.game.getCameraPos() == pos )

  def testGetCameraPos(self):
    pos = self.game.getCameraPos()
    self.failUnless(pos)
    self.failUnless( isinstance(pos, tuple) )

  def testSetCameraHpr(self):
    self.game.setCameraHpr(Game.CAMERA_HPR_DEFAULT)
    hpr = self.game.getCameraHpr()
    self.failUnless(hpr == Game.CAMERA_HPR_DEFAULT)

  def testGetCameraHpr(self):
    hpr = self.game.getCameraHpr()
    self.failUnless(hpr)
    self.failUnless( isinstance(hpr, tuple) )

  def testRegisterListeners(self):
    self.game.start()
    players = self.game.getPlayers()
    playerOne = players[0]
    self.game.registerListeners()
    playerOneMoveForwardOnEvent = createNamedEvent(
      playerOne.name, Event.PLAYER_MOVE_FORWARD_ON
    )
    ships = self.game.getShips()
    shipOne = ships[0]
    shipTwo = ships[1]

    # Test that the player can move the ship forward
    pos1 = shipOne.getPos()
    vel1 = shipOne.getVel()
    acc1 = shipOne.getAcc()
    messenger.send(playerOneMoveForwardOnEvent)
    taskMgr.step()
    pos2 = shipOne.getPos()
    vel2 = shipOne.getVel()
    acc2 = shipOne.getAcc()
    self.failIf(pos1 == pos2)
    self.failIf(vel1 == vel2)
    self.failIf(acc1 == acc2)

    # Test that the move forward off event is handled properly
    playerOneMoveForwardOffEvent = createNamedEvent(
      playerOne.name, Event.PLAYER_MOVE_FORWARD_OFF
    )
    acc1 = shipOne.getAcc()
    messenger.send(playerOneMoveForwardOffEvent)
    taskMgr.step()
    acc2 = shipOne.getAcc()
    self.failIf(acc1 == acc2)
    
    # Test that the players' keys are set
    # Player one forward key on:
    pos1 = shipOne.getPos()
    vel1 = shipOne.getVel()
    acc1 = shipOne.getAcc()
    messenger.send(Game.PLAYER_ONE_FORWARD_KEY)
    taskMgr.step()
    pos2 = shipOne.getPos()
    vel2 = shipOne.getVel()
    acc2 = shipOne.getAcc()
    self.failIf(pos1 == pos2)
    self.failIf(vel1 == vel2)
    self.failIf(acc1 == acc2)
    # Player one forward key off:
    acc1 = shipOne.getAcc()
    vel1 = shipOne.getVel()
    messenger.send(Game.PLAYER_ONE_FORWARD_KEY + "-up")
    taskMgr.step()
    acc2 = shipOne.getAcc()
    vel2 = shipOne.getVel()
    self.failIf(acc1 == acc2)
    self.failUnless(vel1 == vel2)
    # Player one rotate left key on:
    headingBefore = shipOne.heading
    messenger.send(Game.PLAYER_ONE_ROTATE_LEFT_KEY)
    taskMgr.step()
    headingAfter = shipOne.heading
    self.failIf(headingBefore == headingAfter)
    # Player one rotate left key off:
    headingBefore = shipOne.heading
    messenger.send(Game.PLAYER_ONE_ROTATE_LEFT_KEY + "-up")
    taskMgr.step()
    headingAfter = shipOne.heading
    self.failUnless(headingBefore == headingAfter)
    # Player one rotate right key on:
    headingBefore = shipOne.heading
    messenger.send(Game.PLAYER_ONE_ROTATE_RIGHT_KEY)
    taskMgr.step()
    headingAfter = shipOne.heading
    self.failIf(headingBefore == headingAfter)
    # Player one rotate right key off:
    headingBefore = shipOne.heading
    messenger.send(Game.PLAYER_ONE_ROTATE_RIGHT_KEY + "-up")
    taskMgr.step()
    headingAfter = shipOne.heading
    self.failUnless(headingBefore == headingAfter)
    # Player one shoot:
    bullets = self.game.getBullets()
    bulletsBefore = len(bullets[0])
    messenger.send(Game.PLAYER_ONE_SHOOT)
    taskMgr.step()
    bulletsAfter = len(bullets[0])
    self.failUnless(bulletsBefore < bulletsAfter)
    # Player two forward key on:
    pos1 = shipTwo.getPos()
    vel1 = shipTwo.getVel()
    acc1 = shipTwo.getAcc()
    messenger.send(Game.PLAYER_TWO_FORWARD_KEY)
    taskMgr.step()
    pos2 = shipTwo.getPos()
    vel2 = shipTwo.getVel()
    acc2 = shipTwo.getAcc()
    self.failIf(pos1 == pos2)
    self.failIf(vel1 == vel2)
    self.failIf(acc1 == acc2)
    # Player two forward key off:
    acc1 = shipTwo.getAcc()
    messenger.send(Game.PLAYER_TWO_FORWARD_KEY + "-up")
    taskMgr.step()
    acc2 = shipTwo.getAcc()
    self.failIf(acc1 == acc2)
    # Player two rotate left key on:
    headingBefore = shipTwo.heading
    messenger.send(Game.PLAYER_TWO_ROTATE_LEFT_KEY)
    taskMgr.step()
    headingAfter = shipTwo.heading
    self.failIf(headingBefore == headingAfter)
    # Player two rotate left key off:
    headingBefore = shipTwo.heading
    messenger.send(Game.PLAYER_TWO_ROTATE_LEFT_KEY + "-up")
    taskMgr.step()
    headingAfter = shipTwo.heading
    self.failUnless(headingBefore == headingAfter)
    # Player two rotate right key on:
    headingBefore = shipTwo.heading
    messenger.send(Game.PLAYER_TWO_ROTATE_RIGHT_KEY)
    taskMgr.step()
    headingAfter = shipTwo.heading
    self.failIf(headingBefore == headingAfter)
    # Player two rotate right key off:
    headingBefore = shipTwo.heading
    messenger.send(Game.PLAYER_TWO_ROTATE_RIGHT_KEY + "-up")
    taskMgr.step()
    headingAfter = shipTwo.heading
    self.failUnless(headingBefore == headingAfter)
    # Player two shoot:
    bullets = self.game.getBullets()
    bulletsBefore = len(bullets[1])
    messenger.send(Game.PLAYER_TWO_SHOOT)
    taskMgr.step()
    bulletsAfter = len(bullets[1])
    self.failUnless(bulletsBefore < bulletsAfter)
    
    # Check that the game is actually listening to events
    self.failUnless(self.game.isListening)

  def testGetBullets(self):
    self.game.start()
    bullets = self.game.getBullets()
    self.failUnless( isinstance(bullets, list) )

  def testLoadShips(self):
    self.game.loadPlanet()
    self.game.loadShips()
    ships = self.game.getShips()
    self.failUnless( len(ships) == 2 )
    shipOne = ships[0]
    shipTwo = ships[1]
    self.failUnless( shipOne.getPos() != shipTwo.getPos() ) 
    self.failUnless( shipOne.getHeading() != shipTwo.getHeading() )

  def testLoadPlayers(self):
    self.game.loadPlayers()
    players = self.game.getPlayers()
    self.failUnless( len(players) == 2 )

  def testUpdateCamera(self):
    self.game.start()
    ships = self.game.getShips()
    shipOne = ships[0]
    shipTwo = ships[1]
    pos1 = (10, 10)
    pos2 = (20, 20)
    pos3 = (30, 30)
    pos4 = (40, 40)
    shipOne.setPos(pos3)
    shipTwo.setPos( (-pos3[0], -pos3[1]) )
    before = self.game.getCameraPos()
    self.game.updateCamera()
    after = self.game.getCameraPos()
    self.failUnless(before != after)
    # Check that the camera's x-y position is the same as the average of the
    # two ship's x-y positions
    averagePosX = ( shipOne.getPos()[0] + shipTwo.getPos()[0] ) / 2.0
    averagePosY = ( shipOne.getPos()[1] + shipTwo.getPos()[1] ) / 2.0
    average = (averagePosX, averagePosY)
    self.failUnless( after[0] == average[0] )
    self.failUnless( after[1] == average[1] )

  def testTick(self):
    self.game.start()
    timeBefore = self.game.getTime()
    # Step Panda3D's task manager one tick forward
    taskMgr.step()
    timeAfter = self.game.getTime()
    self.failIfEqual(timeBefore, timeAfter)
    self.failUnless(timeBefore < timeAfter)
    
    # Test camera updating
    ships = self.game.getShips()
    shipOne = ships[0]
    shipTwo = ships[1]
    pos = (20, 20)
    pos2 = (10, 10)
    shipOne.setPos(pos2)
    shipTwo.setPos( (-pos[0], -pos[1]) )
    before = self.game.getCameraPos()
    taskMgr.step()
    after = self.game.getCameraPos()
    self.failUnless(before != after)
    # Check that the camera's x-y position is the same as the average of the
    # two ship's x-y positions
    averagePosX = ( shipOne.getPos()[0] + shipTwo.getPos()[0] ) / 2.0
    averagePosY = ( shipOne.getPos()[1] + shipTwo.getPos()[1] ) / 2.0
    average = (averagePosX, averagePosY)
    self.failUnless( abs(after[0] - average[0]) < 0.001 )
    self.failUnless( abs(after[1] - average[1]) < 0.001)

  def testWarpShips(self):
    pass
    # Add more tests here!
    #self.game.start()
    #
    #shipOnePosBefore = self.game.ships[0].getPos()
    #shipTwoPosBefore = self.game.ships[1].getPos()
    #self.game.warpShips('x')
    #shipOnePosAfter = self.game.ships[0].getPos()
    #shipTwoPosAfter = self.game.ships[1].getPos()
    #self.failUnless(shipOnePosBefore != shipOnePosAfter)
    #self.failUnless(shipTwoPosBefore != shipTwoPosAfter)
    
  def testWarpPlanet(self):
    pass
    #self.game.start()
    #planetPosBefore = self.game.planet.getPos()
    #self.game.warpPlanet('x')
    #planetPosAfter = self.game.planet.getPos()
    #self.failUnless(planetPosBefore[0] == -planetPosAfter[0] )
    #self.failUnless(planetPosBefore[1] == planetPosAfter[1] )
    #self.failUnless(planetPosBefore[2] == planetPosAfter[2] )

    ## y-axis
    #planetPosBefore = self.game.planet.getPos()
    #self.game.warpPlanet('y')
    #planetPosAfter = self.game.planet.getPos()
    #self.failUnless(planetPosBefore[0] == planetPosAfter[0] )
    #self.failUnless(planetPosBefore[1] == -planetPosAfter[1] )
    #self.failUnless(planetPosBefore[2] == planetPosAfter[2] )


  def testRestartGame(self):
    self.game.start()
    self.game.ships[0].destroy()
    self.failIf( self.game.ships[0].isAlive )
    self.game.restartGame()
    self.failUnless( self.game.ships[0].isAlive )

  def testShowWinnerText(self):
    self.game.start()
    player = self.game.players[0]
    self.game.showWinnerText(player)
    self.failIf( self.game.winnerText.isHidden() )
    self.failUnless( self.game.winnerText.getText() == player.name + " " + Game.WINNER_TEXT )

  def testGetTime(self):
    self.game.start()
    time = self.game.getTime()
    self.failUnless(time)
    self.failUnless(time >= 0.0)
    self.failUnless( isinstance(time, float) )

  def testGetDeltaTime(self):
    self.game.start()
    dt = self.game.getDeltaTime()
    self.failUnless(dt)
    self.failUnless(dt >= 0.0)
    self.failUnless( isinstance(dt, float) )

  def testRun(self):
    # this method won't be tested because it does not return
    pass


  def testSetCameraPos(self):
    pos = (0, 0, 50)
    self.game.setCameraPos( pos )
    self.failUnless( self.game.getCameraPos() == pos )

  def testGetCameraPos(self):
    pos = self.game.getCameraPos()
    self.failUnless(pos)
    self.failUnless( isinstance(pos, tuple) )

  # ####################################################################
  # Feature tests
  #
  # These tests don't necessarily test any single method, but rather
  # features. They are slightly more complex in that the focus of a
  # feature test is a higher level concept, such as gravity, collisions
  # or forces.
  # ####################################################################
  def testCollisionDetection(self):
    self.game.start()
    ships = self.game.getShips()
    ships[0].setPos( (.5, .5) )
    ships[1].setPos( (.5, .5) )
    ships[0].setCollisionHandler(lambda x, y: 0)
    ships[1].setCollisionHandler(lambda x, y: 0)
    for i in range(2):
      taskMgr.step()
    self.failIfEqual(ships[0].getCollisions(), [])
    self.failIfEqual(ships[1].getCollisions(), [])
    
  def testCollisionResponse(self):
    self.game.start()
    ships = self.game.getShips()
    ships[0].setPos( (0, .5) )
    ships[1].setPos( (.5, 0) )
    ships[0].setVel( (.5, .5) )
    ships[1].setVel( (.5, .5) )
    oldPos1 = ships[0].getPos()
    oldPos2 = ships[1].getPos()
    for i in range(2):
      taskMgr.step()
    newPos1 = ships[0].getPos()
    newPos2 = ships[1].getPos()
    self.failIfEqual( oldPos1, newPos1 )
    self.failIfEqual( oldPos2, newPos2 )

