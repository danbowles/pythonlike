class Action:
  pass

class EscapeAction:
  pass
  # def __init__(self, player):
  #   self.player = player

  # def execute(self):
  #   self.player.escape()

class MovementAction(Action):
  def __init__(self, dx: int, dy: int):
    super().__init__()

    self.dx = dx
    self.dy = dy
