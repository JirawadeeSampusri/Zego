import random
import arcade
import math
import os
from Zego_models import World

SPRITE_SCALING_PLAYER = 0.8
SPRITE_SCALING_COIN = 0.5
SPRITE_SCALING_LASER = 0.8
SPRITE_SCALING_GIFT = 0.5
COIN_COUNT = 30
GIFT_COUNT = 3

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Zego"

BULLET_SPEED = 10
MOVEMENT_SPEED = 7
window = None

state = {'game':0,
         'dead':1,
         'start':2
         }

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

        if self.top < 0:
            self.reset_pos()

class Gift(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 30,
                                         SCREEN_HEIGHT + 140)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the gift
        self.center_y -= 1

        if self.top < 0:
            self.reset_pos()
      
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

class ZegoDotWindow(arcade.Window):
    def __init__(self):
        # STATE_FROZEN = 1
        # STATE_STARTED = 2
        # STATE_DEAD = 3

        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.state = 0
        # self.frame_count = 0 
        self.text_angle = 0
        self.time_elapsed = 0.0
        self.total_time = 0.0

        self.background = None

        self.player_list = None
        self.coin_sprite_list = None
        self.gift_sprite_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.player = None
        self.box_list = None
        
        
        
        self.player_sprite = None
        self.score = 0
        self.score_text = None
        self.blood = 220

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)
    

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.background = arcade.load_texture("images/background1.jpg")
        self.player_list = arcade.SpriteList()
        self.coin_sprite_list = arcade.SpriteList()
        self.gift_sprite_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.blue_bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.box_list = arcade.SpriteList()

        self.score = 0
        self.total_time = 0.0
        self.blood = 220

        self.player_sprite = ModelSprite("images/dot.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)


        #add 1st ships
        enemy = arcade.Sprite("images/enermy.png", 0.5)
        enemy.center_x = 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 165
        self.enemy_list.append(enemy)

        #add sec ships
        enemy = arcade.Sprite("images/enermy.png", 0.5)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 165
        self.enemy_list.append(enemy)

        #add thd ships
        enemy = arcade.Sprite("images/enermy.png", 0.5)
        enemy.center_x = SCREEN_WIDTH - 360
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 140
        self.enemy_list.append(enemy)


        for i in range(COIN_COUNT):

            
            coin = Coin("images/coin_01.png", SPRITE_SCALING_COIN)

     
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120,SCREEN_HEIGHT)

    
            self.coin_sprite_list.append(coin)

        for i in range(GIFT_COUNT):

  
            gift = Gift("images/gift.png", SPRITE_SCALING_GIFT)

      
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(120,SCREEN_HEIGHT)


            self.gift_sprite_list.append(gift)
        
        
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

        self.enemy_list.draw()
        self.coin_sprite_list.draw()
        self.gift_sprite_list.draw()
        self.bullet_list.draw()
        self.blue_bullet_list.draw()
        self.player_list.draw()
        arcade.draw_text("Welcome to Zego", start_x, start_y,
                         arcade.color.BLACK, 14, width=200, align="center",
                         anchor_x="center", anchor_y="center", rotation=90.0)
        if self.state == 0:
            arcade.draw_text("Press SPACE to start",250,SCREEN_HEIGHT//2,arcade.color.BLACK,30)
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 12)

        # Blood 
        self.blood_sprite = ModelSprite(f"blood/b{self.blood//10}.png", 0.5)
        self.blood_sprite.center_x = 400
        self.blood_sprite.center_y = 545

        self.blood_sprite.draw()

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(output, 350, 560, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        if self.state == 0 or self.state == 2:
            return

        self.player_list.update()
        self.coin_sprite_list.update()
        self.gift_sprite_list.update()
        self.bullet_list.update()
        self.blue_bullet_list.update()

        self.text_angle += 1
        self.time_elapsed += delta_time
        self.total_time += delta_time

        for coin in self.coin_sprite_list:
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                            self.coin_sprite_list)

        
            for coin in hit_list:
                coin.reset_pos()
                self.score +=1

        for gift in self.gift_sprite_list:

            hit_gift = arcade.check_for_collision_with_list(self.player_sprite,self.gift_sprite_list)

            for gift in hit_gift:
                gift.reset_pos()
                self.score += 5

        for enemy in self.enemy_list:
            if enemy.center_x >= -80:
                enemy.center_x-=1
            else:
                enemy.center_x = 800

        for bullet in self.blue_bullet_list:

  
            hit_enemy_list = arcade.check_for_collision_with_list(bullet,self.enemy_list)
          
            if len(hit_enemy_list) > 0:
                bullet.kill()
            
            for enemy in hit_enemy_list:
                # enemy.kill()
                enemy.center_x = random.randint(880,1300)

            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.kill()

        
        for enemy in self.enemy_list:

            if random.randrange(100) == 0:
                bullet = arcade.Sprite("images/laser4.png")
                bullet.center_x = enemy.center_x
                bullet.angle = -90
                bullet.top = enemy.bottom
                bullet.change_y = -2
                self.bullet_list.append(bullet)
            
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.kill()

        self.bullet_list.update()

        bullet_hit_player = arcade.check_for_collision_with_list(self.player_sprite, self.bullet_list)
        for b in bullet_hit_player:
            if bullet_hit_player:
                b.kill()
                self.blood -= 10
                if self.blood >1 :
                    if self.blood <= 0:
                        self.player_sprite.kill()
                        self.blue_bullet_list.remove
                else:
                    self.state = 2        
                

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.R and self.state == 2:
            self.setup()
            self.state = 0
        if key == arcade.key.SPACE:
            if self.state != 2 and self.state == 0:
                self.state =1    
       
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """

        if self.state == 1:
            self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse moves.
        """
        # Create a bullet
        if button == arcade.key.SPACE:
            if self.state != 2 and self.state == 0:
                self.state =1

        bullet = arcade.Sprite("images/bluelaser2.png", SPRITE_SCALING_LASER)

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        dest_x = x
        dest_y = y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

       
        bullet.angle = 90
       
        
        bullet.change_y = BULLET_SPEED

        self.blue_bullet_list.append(bullet)

def main():
    """ Main method """
    window = ZegoDotWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()