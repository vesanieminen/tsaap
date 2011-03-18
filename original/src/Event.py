class Event:

  PLAYER_MOVE_FORWARD_ON = "Player Move Forward On"
  PLAYER_MOVE_FORWARD_OFF = "Player Move Forward Off"
  PLAYER_ROTATE_LEFT_ON = "Player Rotate Left On"
  PLAYER_ROTATE_LEFT_OFF = "Player Rotate Left Off"
  PLAYER_ROTATE_RIGHT_ON = "Player Rotate Right On"
  PLAYER_ROTATE_RIGHT_OFF = "Player Rotate Right Off"
  PLAYER_SHOOT = "Player Shoot"

def createNamedEvent(name, event):
  return name + " " + event

