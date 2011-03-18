from direct.showbase.ShowBase import ShowBase

from Event import Event, createNamedEvent

class Player:

  NAME_DEFAULT = "unnamed" 
  FORWARD_DEFAULT = False
  ROTATE_LEFT_DEFAULT = False
  ROTATE_RIGHT_DEFAULT = False

  def __init__(self, name = NAME_DEFAULT):
    self.name = name
    self.forward = Player.FORWARD_DEFAULT
    self.rotateLeft = Player.ROTATE_LEFT_DEFAULT
    self.rotateRight = Player.ROTATE_RIGHT_DEFAULT
    self.score = 0

  def shoot(self):
    shootEvent = createNamedEvent(self.name, Event.PLAYER_SHOOT)
    messenger.send(shootEvent)

  def moveForwardOn(self):
    self.forward = True
    moveEvent = createNamedEvent(self.name, Event.PLAYER_MOVE_FORWARD_ON)
    messenger.send(moveEvent)

  def moveForwardOff(self):
    self.forward = False
    moveEvent = createNamedEvent(self.name, Event.PLAYER_MOVE_FORWARD_OFF)
    messenger.send(moveEvent)

  def isForwardOn(self):
    return self.forward

  def rotateLeftOn(self):
    self.rotateLeft = True
    rotateEvent = createNamedEvent(
      self.name,
      Event.PLAYER_ROTATE_LEFT_ON
    )
    messenger.send(rotateEvent)

  def rotateLeftOff(self):
    self.rotateLeft = False
    rotateEvent = createNamedEvent(
      self.name,
      Event.PLAYER_ROTATE_LEFT_OFF
    )
    messenger.send(rotateEvent)

  def isRotateLeftOn(self):
    return self.rotateLeft

  def rotateRightOn(self):
    self.rotateRight = True
    rotateEvent = createNamedEvent(
      self.name,
      Event.PLAYER_ROTATE_RIGHT_ON
    )
    messenger.send(rotateEvent)

  def rotateRightOff(self):
    self.rotateRight = False
    rotateEvent = createNamedEvent(
      self.name,
      Event.PLAYER_ROTATE_RIGHT_OFF
    )
    messenger.send(rotateEvent)

  def isRotateRightOn(self):
    return self.rotateRight
