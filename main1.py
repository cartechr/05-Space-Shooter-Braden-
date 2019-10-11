import sys, logging, os, random, math, arcade, open_color

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
Margin = 20
SCREEN_TITLE = "Space Shooter"

Number_Of_Enemies = 5
Starting_Location = (600,300)
Bullet_Damage = 34
Enemy_Hp = 100
Kill_Score = 100
Initial_Velocity = 10
PLAYER_HP = 300



class Enemy(arcade.Sprite):
    def __init__(self, position, velocity):
        #starts the alien enemy
        '''
        Parameter: position: (x,y) tuple
        '''
        #normal enemies
        super().__init__("assets/Nave_1.png", 1)
        self.hp = Enemy_Hp
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity

class Laser(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        #starts the missile
        '''
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/beams (2).png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        #Moves the missile
        self.center_x += self.dx
        self.center_y += self.dy

class Laser2(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        #starts the missile
        '''
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/beams (2).png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        #Moves the missile
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/Spaceship_tut.png", 0.5)
        (self.center_x, self.center_y) = Starting_Location
        self.hp = PLAYER_HP
        self.moving_left = False
        self.moving_right = False

class Window(arcade.Window):

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)


        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(True)

        self.laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.laser2_list = arcade.SpriteList()
        self.player1 = Player()
        self.player_list = arcade.SpriteList()
        self.score = 0
        self.background = None
        

    def winner(self):

        arcade.draw_text(f"Victory is yours!", 600, 500, arcade.color.WHITE, 60)
        arcade.draw_text(f"Score: {self.score}", 550, 450, arcade.color.WHITE, 30)

    def end(self):
        arcade.draw_text(f"Ya done lost :()",600, 500, arcade.color.WHITE, 60)

    def setup(self):

        self.won = False
        self.died = False

        
        '''
        Set up enemies
        '''
        for i in range(Number_Of_Enemies):
            x = random.randint(Margin, SCREEN_WIDTH - Margin)
            y = 900
            dx = random.uniform(-Initial_Velocity, Initial_Velocity)
            dy = random.uniform(-Initial_Velocity, Initial_Velocity)
            enemy = Enemy((x,y), (dx,dy))
            self.enemy_list.append(enemy)
        self.background = arcade.load_texture('assets/space.jpg')
        

    def update(self, delta_time):
        self.laser_list.update()
        for e in self.enemy_list:
            boolets = arcade.check_for_collision_with_list(e,self.laser_list)
            for b in boolets:
                e.hp = e.hp - b.damage
                b.kill()
                if e.hp <= 0:
                    e.kill()
                    self.score = self.score + Kill_Score
        self.enemy_list.update()
        for e in self.enemy_list:
            e.center_x = e.center_x + e.dx
            e.center_y = e.center_y + e.dy
            if e.center_x <= 0:
                e.dx = abs(e.dx)
            if e.center_x >= SCREEN_WIDTH:
                e.dx = abs(e.dx) * -1
            if e.center_y <= 900:
                e.dy = abs(e.dy)
            if e.center_y >= SCREEN_HEIGHT:
                e.dy = abs(e.dy) * -1

        self.laser2_list.update()
        for e in self.enemy_list:
            if (random.random() < .05):
                self.laser2_list.append(Laser2((e.center_x, e.center_y - 15), (0, -10), 100))

        damage = arcade.check_for_collision_with_list(self.player1,self.laser2_list)
        for d in damage:
            self.player1.hp = self.player1.hp - d.damage
            d.kill()
            if self.player1.hp <= 0:
                self.player1.kill()
                self.died = True
    
#come back
            
    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player1.draw()

        if self.won:
            self.winner()
        elif self.died:
            self.end
        else:
            self.laser_list.draw()
            self.enemy_list.draw()
            self.player_list.draw()
            self.laser2_list.draw()
        
        


    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects. Happens approximately 60 times per second."""
        self.player1.center_x = x
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player1.center_x
            y = self.player1.center_y + 15
            laser = Laser((x,y),(0,10),Bullet_Damage)
            self.laser_list.append(laser)


    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            print("Left")
        elif key == arcade.key.RIGHT:
            print("Right")
        elif key == arcade.key.UP:
            print("Up")
        elif key == arcade.key.DOWN:
            print("Down")

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        pass


def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
