import pgzrun

WIDTH = 1000
HEIGHT = 600

# Game States
MENU = 0
GAME = 1
GAMEOVER = 2
WIN = 3
current_state = MENU 

SOUND_ON = True
SOUND_OFF = False
sound_state = SOUND_ON

def background():
    # Background assembly
    screen.blit(r"background_color_mushrooms", (0, 0))  #type: ignore
    screen.blit(r"background_color_mushrooms", (512, 0))  #type: ignore
    screen.blit(r"background_solid_dirt", (0, 512))  #type: ignore
    screen.blit(r"background_solid_dirt", (512, 512))  #type: ignore

class Menu:
    def __init__(self):
        self.menu_player = Actor(r"character_pink_walk_a")  # type: ignore
        self.menu_player.pos = (200, 450)
        self.menu_player_x = self.menu_player.x
        self.menu_player_y = self.menu_player.y
        self.menu_player_angle = 0
        self.sound_text = "ON"

    def title(self,Title, title_part1, title_part2, title_part3):
        # Building Grass Title
        title_width = title_part1.width + title_part2.width + title_part3.width
        title_x = (WIDTH - title_width) // 2
        title_y = HEIGHT // 4 

        title_part1.pos = (title_x + title_part1.width // 2, title_y)
        title_part2.pos = (title_part1.pos[0] + title_part1.width // 2 + title_part2.width // 2, title_y)
        title_part3.pos = (title_part2.pos[0] + title_part2.width // 2 + title_part3.width // 2, title_y)
        title_part1.draw()
        title_part2.draw()
        title_part3.draw()

        screen.draw.text(Title, center=(WIDTH//2, HEIGHT//4), fontsize=60, color="black")  #type: ignore
    
    def button(self, position_y, part1, part2, part3, text="Button"):
        # Building Stone Buttons
        button_x = WIDTH // 2
        button_y = position_y - 5

        part1.pos = (button_x - part1.width, button_y)
        part2.pos = (part1.pos[0] + part1.width // 2 + part2.width // 2, button_y)
        part3.pos = (part2.pos[0] + part2.width // 2 + part3.width // 2, button_y)
        part1.draw()
        part2.draw()
        part3.draw()

        screen.draw.text(text, center=(button_x, position_y), fontsize=40, color="black")  #type: ignore
        return part1.pos, part3.pos, part1.height

    def draw(self):
        screen.clear() #type: ignore
        background()
        # Create Player in Menu
        self.menu_player.draw()

        # Title
        title_part1 = Actor(r"title/terrain_grass_cloud_left")  # type: ignore 
        title_part2 = Actor(r"title/terrain_grass_cloud_middle")  # type: ignore
        stitle_part3 = Actor(r"title/terrain_grass_cloud_right")  # type: ignore
        self.title("Main Menu", title_part1, title_part2, stitle_part3)

        # Building Buttons: Start Game, Sound Button, Exist
        button_part1 = Actor(r"terrain_stone_cloud_left")  # type: ignore
        button_part2 = Actor(r"terrain_stone_cloud_middle")  # type: ignore
        button_part3 = Actor(r"terrain_stone_cloud_right")  # type: ignore
        self.button1_position = self.button(HEIGHT//2, button_part1, button_part2, button_part3, "Start Game")
        self.button2_position = self.button(HEIGHT//2 + 75, button_part1, button_part2, button_part3, f"Sound: {self.sound_text}")
        self.button3_position = self.button(HEIGHT//2 + 150, button_part1, button_part2, button_part3, "Exit")

    def update(self):
        global sound_state

        # Player rotation in the menu
        velocidade = 3
        self.menu_player.x += velocidade
        if self.menu_player.right > WIDTH + 300:
            self.menu_player.x -= 1300
        self.menu_player.angle += 1
        self.menu_player.angle %= 360
        
    def on_mouse_down(self, pos):
        global current_state, sound_state

        # Placing click range buttons
        b1_ini, b1_end, b1_height = self.button1_position
        b2_ini, b2_end, b2_height = self.button2_position
        b3_ini, b3_end, b3_height = self.button3_position
        
        # Click in "Start Game Button" Range
        if b1_ini[0] <= pos[0] <= b1_end[0] and b1_ini[1] - b1_height//2 <= pos[1] <= b1_ini[1] + b1_height//2:
            print("Start Game selected")
            if sound_state == SOUND_ON:
                sounds.sfx_select.play() #type: ignore
            current_state = GAME  
        
        #Click in "Sound Button" Range
        elif b2_ini[0] <= pos[0] <= b2_end[0] and b2_ini[1] - b2_height//2 <= pos[1] <= b2_ini[1] + b2_height//2:
            if sound_state == SOUND_ON:
                sound_state = SOUND_OFF
                self.sound_text = "Off"
            else:
                sound_state = SOUND_ON
                self.sound_text = "On"
            
            if sound_state == SOUND_ON:
                sounds.sfx_select.play() #type: ignore
            print("Options selected")

        #Click in "Exit Button" Range
        elif b3_ini[0] <= pos[0] <= b3_end[0] and b3_ini[1] - b3_height//2 <= pos[1] <= b3_ini[1] + b3_height//2:
            if sound_state == SOUND_ON:
                sounds.sfx_select.play() #type: ignore
            print("Exit selected")
            exit() 

class Player:
    def __init__(self):
        # Health and damage
        self.health = 3
        self.invincible = False
        self.invincibility_timer = 0

        # Player
        self.player = Actor(r"char/character_pink_idle")  # type: ignore
        self.current_animation = "idle"
        self.facing_right = True
        self.player_x = 100
        self.player_y = 440
        self.player_damaged = False
        self.velocity_x = 5.2

        # Jumping
        self.velocity_y = 0
        self.floating = False
        self.jump_strength = 21
        self.facing_direction = 1  # 1 for right, -1 for left

        # Animation
        self.animations = {
            "idle": [r"char/character_pink_idle"],
            "walk": [r"char/character_pink_walk_a", r"char/character_pink_walk_b"],
            "jump": [r"char/character_pink_jump",],
            "hit": [r"char/character_pink_hit"]
        }
        self.animation_index = 0
        self.animation_speed = 0.1

    def animation(self):
        #Player Animation
        frames = self.animations.get(self.current_animation, self.animations["idle"])
        self.animation_index += self.animation_speed
        if self.animation_index >= len(frames):
            self.animation_index = 0
        self.player.image = frames[int(self.animation_index)]

    
    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.current_animation = "hit"
            self.invincible = True
            self.invincibility_timer = 60
            self.player_damaged = True


    def update(self):
        global sound_state
        self.player.pos = (self.player_x, self.player_y)
        # Collision mask (PLAYER)
        self.player_rect = Rect((self.player.left +30, self.player.top), (self.player.width *0.5, self.player.height)) #type: ignore 

        # Walk to the left
        if keyboard.left and self.player_damaged == False and self.player_x >= -10: #type: ignore
            self.player_x -= self.velocity_x
            self.facing_direction = 1
            self.current_animation = "walk"
        # Walk to the right
        elif keyboard.right and self.player_damaged == False and self.player_x <= 1010: #type: ignore
            self.player_x += self.velocity_x
            self.facing_direction = -1
            self.current_animation = "walk"
        # Jump
        elif keyboard.up and self.floating == False: #type: ignore
            self.velocity_y += self.jump_strength
            self.floating = True

        # S.T.A.Y
        else:
            self.current_animation = "idle"

        # Jumping physics
        if self.floating and self.velocity_y > 0 and self.player_damaged == False:
            if self.velocity_y == self.jump_strength:
                if sound_state == SOUND_ON:
                    sounds.sfx_jump.play() #type: ignore
            self.current_animation = "jump"
            self.velocity_y -= 1

        # Player took damage
        if self.player_damaged:
            self.current_animation = "hit"
            # Damage knockback
            if self.invincibility_timer == 60:
                self.velocity_y = 5
            # Damage stun timer 
            elif self.invincibility_timer == 50:
                self.player_damaged = False
        
        # Damage invincibility has ended
        elif self.invincibility_timer == 0:
            self.invincible = False

        self.invincibility_timer -= 1
        self.animation()

class Enemy:
    def __init__(self, x, y, min_x, max_x):
        # Enemy Caracteristics
        self.enemy = Actor(r"enemy/slime_block_walk_a")  # type: ignore
        self.enemy.pos = (x, y)
        self.direction = 1
        self.speed = 2
        self.min_x = min_x
        self.max_x = max_x
        self.animations = [r"enemy/slime_block_walk_a", r"enemy/slime_block_walk_b"]
        self.animation_index = 0
        self.animation_speed = 0.1

    def animation(self):
        # Enemy animation
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.animations):
            self.animation_index = 0
        self.enemy.image = self.animations[int(self.animation_index)]

    def update(self):
        self.enemy.x += self.direction * self.speed
        self.animation()
        # Reverses direction upon reaching boundaries
        if self.enemy.x <= self.min_x or self.enemy.x >= self.max_x:
            self.direction *= -1
        #Collision mask (ENEMY) 
        self.enemy_rect = Rect((self.enemy.left +10, self.enemy.top), (self.enemy.width *0.8, self.enemy.height *0.2)) #type: ignore

class Game:
    def __init__(self):
        #Player and Enemys Definition
        self.player = Player()
        self.enemies = [
            Enemy(800, 480, min_x=700, max_x=900),
            Enemy(500, 545, min_x=375, max_x=600),
            Enemy(100, 290, min_x=25, max_x=200),
            Enemy(275, 290, min_x=225, max_x=400)]
        
        # Gravity configs
        self.top_collision_blocks = []
        self.gravity = 4
        
        #Flag
        self.flag = Actor("flag_blue_a") #type: ignore
        self.flag_animation = ["flag_blue_a", "flag_blue_b"]
        self.flag_animation_index = 0
        self.flag_animation_speed = 0.1
        self.flag.pos = 940, 40

    def draw_map(self):
        # Size of each block
        TILE_SIZE = 64
        background()
        
        complete_map = []
        # For block in map.txt (.DLlRrS¨&*) put one block and colision if nescesserie
        with open("map.txt", "r") as file:
            for line in file:
                line = line.strip()
                line_blocks = []
                for block in line:
                    if block == ".":
                        line_blocks.append("empty")
                    elif block == "D":
                        line_blocks.append("dirt_top_center")
                    elif block == "L":
                        line_blocks.append("dirt_top_left")
                    elif block == "R":
                        line_blocks.append("dirt_top_right")
                    elif block == "S":
                        line_blocks.append("middle_stone")
                    elif block == "-":
                        line_blocks.append("block_center")
                    elif block == "l":
                        line_blocks.append("block_left")
                    elif block == "r":
                        line_blocks.append("block_right")
                    elif block == "¨":
                        line_blocks.append("cloud_left")
                    elif block == "&":
                        line_blocks.append("cloud_center")
                    elif block == "*":
                        line_blocks.append("cloud_right")
                complete_map.append(line_blocks)
        # Takes a map line
        for line in range(len(complete_map)):
            # Takes a map column
            for column in range(len(complete_map[line])):
                block_type = complete_map[line][column]
                x = column * TILE_SIZE
                y = line * TILE_SIZE
                if block_type == "dirt_top_center":
                    screen.blit(r"terrain_dirt_block_top", (x, y))  #type: ignore
                    self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE))) #type: ignore
                elif block_type == "dirt_top_left":
                    screen.blit(r"terrain_dirt_block_top_left", (x, y))  #type: ignore
                    self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE))) #type: ignore
                elif block_type == "dirt_top_right":
                    screen.blit(r"terrain_dirt_block_top_right", (x, y))  #type: ignore
                    self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE))) #type: ignore
                elif block_type == "middle_stone":
                    screen.blit(r"terrain_stone_cloud_middle", (x, y))  #type: ignore
                    self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE))) #type: ignore
                elif block_type == "cloud_left":
                    screen.blit(r"terrain_dirt_cloud_left", (x, y))  #type: ignore
                    self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE))) #type: ignore
                elif block_type == "cloud_center":
                    screen.blit(r"terrain_dirt_cloud_middle", (x, y))  #type: ignore
                    self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE))) #type: ignore
                elif block_type == "cloud_right":
                    screen.blit(r"terrain_dirt_cloud_right", (x, y))  #type: ignore
                    self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE))) #type: ignore
                elif block_type == "block_center":
                    screen.blit(r"terrain_dirt_block_center", (x, y))  #type: ignore
                elif block_type == "block_left":
                    screen.blit(r"terrain_dirt_block_left", (x, y))  #type: ignore
                elif block_type == "block_right":
                    screen.blit(r"terrain_dirt_block_right", (x, y))  #type: ignore
        # Draw player and enemies
        self.player.player.draw()
        for enemy in self.enemies:
            enemy.enemy.draw()
        self.flag.draw()

    def check_collision(self, blocks):
        # Prevents gravity if the character is on the ground.
        collided = False
        for block in blocks:
            if self.player.player_rect.colliderect(block):
                # if on floor, Set Floating False
                self.player.floating = False

                # Prevents the player falling.
                if self.player.velocity_y <= 0 and self.player.player_rect.bottom <= block.top + 10:
                    self.player.player_y = block.top - self.player.player.height // 2
                    self.player.velocity_y = 0
                    collided = True
                    break
        # if in the air, Ser Floating True
        if not collided:
            self.player.floating = True

        self.player.player_y += self.gravity - self.player.velocity_y

    def check_enemy_collision(self):
        global sound_state

        #Enemies is a List with 4 enemies
        enemies = self.enemies
        for enemy in enemies: 
            if self.player.player_rect.colliderect(enemy.enemy_rect) and not self.player.invincible:
                if sound_state == SOUND_ON:
                    sounds.sfx_hurt.play() #type: ignore
                self.player.take_damage()
                break

    def draw(self):
        # Draw Game Scene
        screen.clear()  #type: ignore
        screen.fill((0, 100, 0))  #type: ignore
        self.draw_map()
    
    def update(self):
        global current_state
        # Player and Mobs update
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        
        self.check_collision(self.top_collision_blocks)
        self.check_enemy_collision()
        if self.player.health <= 0:
            current_state = GAMEOVER  
            return
        elif self.player.player_damaged:
            self.player.player_x += self.player.velocity_x * self.player.facing_direction
        
        # Flag Animation
        self.flag_animation_index += self.flag_animation_speed
        if self.flag_animation_index >= len(self.flag_animation):
            self.flag_animation_index = 0
        self.flag.image = self.flag_animation[int(self.flag_animation_index)]
        if self.player.player.colliderect(self.flag):
            if sound_state == SOUND_ON:
                sounds.sfx_gem.play() #type: ignore
            current_state = WIN

class Gameover():
    #Print Gameover Screen
    def __init__(self):
        pass
    def draw(self):
        screen.clear() #type: ignore
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red") #type: ignore

class Win():
    # Print Win Screen
    def __init__(self):
        pass
    def draw(self):
        screen.clear() #type:ignore
        screen.draw.text("YOU WIN!!!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="blue") #type: ignore


# Create instances of the Menu and Game classes
menu = Menu()
game = Game()
gameover = Gameover()
win = Win()

# global scope
def draw():
    if current_state == MENU:
        menu.draw()  
    elif current_state == GAME:
        game.draw()
    elif current_state == GAMEOVER:
        gameover.draw()
    elif current_state == WIN:
        win.draw()

def update():
    if current_state == GAME:
        game.update() 
    if current_state == MENU:
        menu.update()

def on_mouse_down(pos):
    if current_state == MENU:
        menu.on_mouse_down(pos)

# Start Game
pgzrun.go()


