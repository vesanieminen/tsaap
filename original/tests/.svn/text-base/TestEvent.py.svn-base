from unittest import TestCase

from Player import Player
from Ship import Ship
from Event import Event, createNamedEvent

class TestEvent(TestCase):

  def testCreateNamedEvent(self):
    playerOne = Player()
    playerOneMoveEvent = createNamedEvent(
      playerOne.name, Event.PLAYER_MOVE_FORWARD_ON
    )
    self.failUnless(playerOneMoveEvent)

