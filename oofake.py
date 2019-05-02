import random
import arcade
import os
from Zego_models import World

SPRITE_SCALING_PLAYER = 0.8
SPRITE_SCALING_COIN = 0.6
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Collect Coins Moving Down Example"

MOVEMENT_SPEED = 5

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()

class ZegoDotWindow(arcade.Window):
    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.background = None

        self.player_list = None
        self.player_sprite = None
        self.coin_sprite_list = None

        self.player_sprite = None
        self.score = 0
        self.score_text = None

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.background = arcade.load_texture("images/background1.jpg")

        self.player_list = arcade.SpriteList()
        self.coin_sprite_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = ModelSprite("images/dot.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = Coin("images/coin_01.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_sprite_list.append(coin)

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.coin_sprite_list.draw()
        self.player_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """

        self.player_list.update()
        self.coin_sprite_list.update()

        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_sprite_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.kill()
            self.score += 1


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = ZegoDotWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()