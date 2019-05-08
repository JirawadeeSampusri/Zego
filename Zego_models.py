class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    def update(self, delta):
        pass

class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bg_state = 1

        self.state = World.STATE_FROZEN

        self.player = Player(self, width // 2, height // 2)

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def is_started(self):
        return self.state == World.STATE_STARTED

    def die(self):
        self.state = World.STATE_DEAD

    def update(self, delta):
        if self.state in [World.STATE_STARTED, World.STATE_DEAD]:
            return
