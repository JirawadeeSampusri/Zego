import random
import arcade
import math
import os
from Zego_models import World

SPRITE_SCALING_PLAYER = 0.8
SPRITE_SCALING_COIN = 0.5
SPRITE_SCALING_LASER = 0.8
COIN_COUNT = 30

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprites and Bullets Aimed Example"

BULLET_SPEED = 5
# MOVEMENT_SPEED = 5
window = None

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
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
 
        
        self.text_angle = 0
        self.time_elapsed = 0.0

        self.background = None

        self.player_list = None
        self.coin_list = None
        self.bullet_list = None
    
        self.player_sprite = None
        self.score = 0
        self.score_text = None

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.background = arcade.load_texture("images/background1.jpg")
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = ModelSprite("images/dot.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        for i in range(COIN_COUNT):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite("images/coin_01.png", SPRITE_SCALING_COIN)

            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120,SCREEN_HEIGHT)

            # Add the coin to the lists
            self.coin_list.append(coin)
        
        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)
        

    def on_draw(self):
        """
        Render the screen.
        """

        arcade.start_render()

        start_y = 200
        start_x = 20
        arcade.draw_point(start_x, start_y, arcade.color.BLUE, 5)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        arcade.draw_text("Welcome to Zego", start_x, start_y,
                         arcade.color.BLACK, 14, width=200, align="center",
                         anchor_x="center", anchor_y="center", rotation=90.0)
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        self.player_list.update()
        self.coin_list.update()
        self.bullet_list.update()

        self.text_angle += 1
        self.time_elapsed += delta_time

        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.coin_list)

        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.kill()

            # For every coin we hit, add to the score and remove the coin
            for coin in hit_list:
                coin.kill()
                self.score += 1

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.kill()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse moves.
        """
        # Create a bullet
        bullet = arcade.Sprite("images/laser3.png", SPRITE_SCALING_LASER)

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        dest_x = x
        dest_y = y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

       
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

       
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

def main():
    """ Main method """
    window = ZegoDotWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()