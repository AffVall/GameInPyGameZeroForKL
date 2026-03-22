import pgzrun
import traceback

# Menu Configurations
WIDTH = 1000
HEIGHT = 600

# Tile size for map blocks
TILE_SIZE = 64

# Game States
MENU = 0
GAME = 1
GAMEOVER = 2
WIN = 3

# Sound States
SOUND_ON = True
SOUND_OFF = False

# Game Variables
current_state = MENU
sound_state = SOUND_ON

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def play_sound(sound, enabled=True):
    # Play sound if enabled
    if not enabled:
        return
    try:
        sound.play()  #type: ignore
    except Exception as e:
        print(f"Aviso: Erro ao tocar som - {e}")

def safe_blit(image, position):
    # Draw image
    try:
        screen.blit(image, position)  #type: ignore
    except Exception as e:
        print(f"Aviso: Erro ao desenhar imagen '{image}' - {e}")

def background():
    # Create a background
    try:
        safe_blit(r"background_color_mushrooms", (0, 0))
        safe_blit(r"background_color_mushrooms", (512, 0))
        safe_blit(r"background_solid_dirt", (0, 512))
        safe_blit(r"background_solid_dirt", (512, 512))
    except Exception as e:
        print(f"Erro ao desenhar background: {e}")
        screen.clear()  #type: ignore

# ============================================================================
# MENU CLASS
# ============================================================================
class Menu:
    def __init__(self):
        try:
            self.menu_player = Actor(r"character_pink_walk_a")  # type: ignore
            self.menu_player.pos = (200, 450)
            self.menu_player_x = self.menu_player.x
            self.menu_player_y = self.menu_player.y
            self.menu_player_angle = 0
            self.sound_text = "ON"
        except Exception as e:
            print(f"Error initializing Menu: {e}")
            traceback.print_exc()

    def _draw_composite_element(self, parts, center_x, center_y, text, fontsize):
        """Draws a composite element (title or button)."""
        try:
            total_width = sum(part.width for part in parts)
            start_x = center_x - total_width // 2
            
            x_pos = start_x
            for part in parts:
                part.pos = (x_pos + part.width // 2, center_y)
                part.draw()
                x_pos += part.width
            
            screen.draw.text(text, center=(center_x, center_y), fontsize=fontsize, color="black")  #type: ignore
            return parts[0].pos, parts[-1].pos, parts[0].height
        except Exception as e:
            print(f"Error drawing element: {e}")
            return (0, 0), (0, 0), 0

    def title(self, Title, title_part1, title_part2, title_part3):
        """Draws the menu title."""
        return self._draw_composite_element([title_part1, title_part2, title_part3], WIDTH // 2, HEIGHT // 4, Title, 60)
    
    def button(self, position_y, part1, part2, part3, text="Button"):
        """Draws a menu button."""
        return self._draw_composite_element([part1, part2, part3], WIDTH // 2, position_y, text, 40)

    def draw(self):
        try:
            screen.clear() #type: ignore
            # Menu elements
            background()
            self.menu_player.draw()

            # Title: "Main Menu"
            try:
                title_part1 = Actor(r"title/terrain_grass_cloud_left")  # type: ignore 
                title_part2 = Actor(r"title/terrain_grass_cloud_middle")  # type: ignore
                title_part3 = Actor(r"title/terrain_grass_cloud_right")  # type: ignore
            except Exception as e:
                print(f"Warning: Error loading title images - {e}")
                title_part1 = title_part2 = title_part3 = None
            if title_part1 and title_part2 and title_part3:
                self.title("Main Menu", title_part1, title_part2, title_part3)

            # Buttons: "Start Game", "Sound: On/Off", "Exit"
            try:
                button_part1 = Actor(r"terrain_stone_cloud_left")  # type: ignore
                button_part2 = Actor(r"terrain_stone_cloud_middle")  # type: ignore
                button_part3 = Actor(r"terrain_stone_cloud_right")  # type: ignore
            except Exception as e:
                print(f"Warning: Error loading button images - {e}")
                button_part1 = button_part2 = button_part3 = None
                
            if button_part1 and button_part2 and button_part3:
                self.button1_position = self.button(HEIGHT//2, button_part1, button_part2, button_part3, "Start Game")
                self.button2_position = self.button(HEIGHT//2 + 75, button_part1, button_part2, button_part3, f"Sound: {self.sound_text}")
                self.button3_position = self.button(HEIGHT//2 + 150, button_part1, button_part2, button_part3, "Exit")
            else:
                screen.draw.text("Error loading images", center=(WIDTH//2, HEIGHT//2), color="red")  #type: ignore
        except Exception as e:
            print(f"Error drawing menu: {e}")
            traceback.print_exc()

    def update(self):
        # menu animation
        try:
            speed = 3
            self.menu_player.x += speed
            if self.menu_player.right > WIDTH + 300:
                self.menu_player.x -= 1300
            self.menu_player.angle += 1
            self.menu_player.angle %= 360
        except Exception as e:
            print(f"Error updating menu: {e}")
        
    def _is_click_in_button(self, button_pos, pos):
        """Checks if the click is within button bounds."""
        try:
            b_ini, b_end, b_height = button_pos
            return (b_ini[0] <= pos[0] <= b_end[0] and b_ini[1] - b_height//2 <= pos[1] <= b_ini[1] + b_height//2)
        except:
            return False

    def on_mouse_down(self, pos):
        """Processes mouse clicks in the menu."""
        global current_state, sound_state
        
        try:
            # Button "Start Game"
            if hasattr(self, 'button1_position') and self._is_click_in_button(self.button1_position, pos):
                play_sound(sounds.sfx_select, sound_state == SOUND_ON)  #type: ignore
                current_state = GAME
                return

            # Button "Sound"
            if hasattr(self, 'button2_position') and self._is_click_in_button(self.button2_position, pos):
                sound_state = SOUND_OFF if sound_state == SOUND_ON else SOUND_ON
                self.sound_text = "Off" if sound_state == SOUND_OFF else "On"
                play_sound(sounds.sfx_select, sound_state == SOUND_ON)  #type: ignore
                return

            # Button "Exit"
            if hasattr(self, 'button3_position') and self._is_click_in_button(self.button3_position, pos):
                play_sound(sounds.sfx_select, sound_state == SOUND_ON)  #type: ignore
                exit()
        except Exception as e:
            print(f"Error processing menu click: {e}")

# ============================================================================
# PLAYER
# ============================================================================
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
            "jump": [r"char/character_pink_jump"],
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
        # Player takes damage
        if not self.invincible:
            self.health -= 1
            self.current_animation = "hit"
            self.invincible = True
            self.invincibility_timer = 60
            self.player_damaged = True

    def update(self):
        # Update player state
        try:
            self.player.pos = (self.player_x, self.player_y)
            self.player_rect = Rect((self.player.left + 30, self.player.top), (self.player.width * 0.5, self.player.height))  #type: ignore

            # Handle input
            if keyboard.left and not self.player_damaged and self.player_x >= -10:  #type: ignore
                self.player_x -= self.velocity_x
                self.facing_direction = 1
                self.current_animation = "walk"
            elif keyboard.right and not self.player_damaged and self.player_x <= 1010:  #type: ignore
                self.player_x += self.velocity_x
                self.facing_direction = -1
                self.current_animation = "walk"
            elif keyboard.up and not self.floating:  #type: ignore
                self.velocity_y += self.jump_strength
                self.floating = True
            else:
                self.current_animation = "idle"

            # Handle damage state
            if self.player_damaged:
                self.current_animation = "hit"
                # Damage knockback
                if self.invincibility_timer == 60:
                    self.velocity_y = 5
                # Damage stun timer 
                elif self.invincibility_timer == 50:
                    self.player_damaged = False
            # Handle jump
            elif self.floating and self.velocity_y > 0:
                if self.velocity_y == self.jump_strength:
                    play_sound(sounds.sfx_jump, sound_state == SOUND_ON)  #type: ignore
                self.current_animation = "jump"
                self.velocity_y -= 1
            elif self.invincibility_timer == 0:
                self.invincible = False

            self.invincibility_timer -= 1
            self.animation()
        except Exception as e:
            print(f"Error updating player: {e}")

# ============================================================================
# CREATE ENEMIES 
# ============================================================================
class Enemy:
    def __init__(self, x, y, min_x, max_x):
        # Enemy Initialization
        try:
            self.enemy = Actor(r"enemy/slime_block_walk_a")  # type: ignore
            self.enemy.pos = (x, y)
            self.direction = 1
            self.speed = 2
            self.min_x = min_x
            self.max_x = max_x
            self.animations = [r"enemy/slime_block_walk_a", r"enemy/slime_block_walk_b"]
            self.animation_index = 0
            self.animation_speed = 0.1
        except Exception as e:
            print(f"Error initializing Enemy: {e}")
            traceback.print_exc()

    def animation(self):
        # Enemy Animation
        try:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.animations):
                self.animation_index = 0
            self.enemy.image = self.animations[int(self.animation_index)]
        except Exception as e:
            print(f"Error in enemy animation: {e}")

    def update(self):
        try:
            self.enemy.x += self.direction * self.speed
            self.animation()
            
            # change direction if enemy reaches movement limits
            if self.enemy.x <= self.min_x or self.enemy.x >= self.max_x:
                self.direction *= -1
            
            # Collision mask (ENEMY)
            self.enemy_rect = Rect((self.enemy.left + 10, self.enemy.top), (self.enemy.width * 0.8, self.enemy.height * 0.2))  #type: ignore
        except Exception as e:
            print(f"Error updating enemy: {e}")

# ============================================================================
# GAME CLASS
# ============================================================================
class Game:
    # Map and Block Definitions
    BLOCK_MAP = {
        ".": "empty",
        "D": "dirt_top_center",
        "L": "dirt_top_left",
        "R": "dirt_top_right",
        "S": "middle_stone",
        "-": "block_center",
        "l": "block_left",
        "r": "block_right",
        "¨": "cloud_left",
        "&": "cloud_center",
        "*": "cloud_right"
    }

    BLOCK_IMAGES = {
        "dirt_top_center": r"terrain_dirt_block_top",
        "dirt_top_left": r"terrain_dirt_block_top_left",
        "dirt_top_right": r"terrain_dirt_block_top_right",
        "middle_stone": r"terrain_stone_cloud_middle",
        "cloud_left": r"terrain_dirt_cloud_left",
        "cloud_center": r"terrain_dirt_cloud_middle",
        "cloud_right": r"terrain_dirt_cloud_right",
        "block_center": r"terrain_dirt_block_center",
        "block_left": r"terrain_dirt_block_left",
        "block_right": r"terrain_dirt_block_right"
    }
    
    COLLISION_BLOCKS = {
        "dirt_top_center", "dirt_top_left", "dirt_top_right",
        "middle_stone", "cloud_left", "cloud_center", "cloud_right"
    }

    def __init__(self):
        # Player and Enemies Definition
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

    def load_map_from_file(self):
        """Loads the map from map.txt file."""
        complete_map = []
        try:
            with open("map.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:  # Ignora linhas vazias
                        continue
                    line_blocks = [self.BLOCK_MAP.get(block, "empty") for block in line]
                    complete_map.append(line_blocks)
            return complete_map
        except FileNotFoundError:
            print("Error: File 'map.txt' not found!")
            return []
        except Exception as e:
            print(f"Error loading map: {e}")
            return []

    def _draw_block(self, block_type, x, y):
        """Draws a single block with collision if necessary."""
        if block_type in self.BLOCK_IMAGES:
            safe_blit(self.BLOCK_IMAGES[block_type], (x, y))
            
            if block_type in self.COLLISION_BLOCKS:
                self.top_collision_blocks.append(Rect((x, y), (TILE_SIZE, TILE_SIZE)))  #type: ignore

    def _draw_game_entities(self):
        """Draws player, enemies and flag."""
        self.player.player.draw()
        for enemy in self.enemies:
            enemy.enemy.draw()
        self.flag.draw()

    def map(self):
        """Draws the entire map and entities."""
        try:
            background()
            self.top_collision_blocks.clear()
            complete_map = self.load_map_from_file()

            # Draw all blocks
            for line, row in enumerate(complete_map):
                for column, block_type in enumerate(row):
                    x = column * TILE_SIZE
                    y = line * TILE_SIZE
                    self._draw_block(block_type, x, y)
            
            # Draw game entities
            self._draw_game_entities()
        except Exception as e:
            print(f"Error drawing map: {e}")

    def check_collision(self, blocks):
        # Prevents gravity if the character is on the ground.
        collided = False
        for block in blocks:
            if self.player.player_rect.colliderect(block):                # if on floor, Set Floating False
                self.player.floating = False

                # Prevents the player falling.
                if self.player.velocity_y <= 0 and self.player.player_rect.bottom <= block.top + 10:
                    self.player.player_y = block.top - self.player.player.height // 2
                    self.player.velocity_y = 0
                    collided = True
                    break        # if in the air, Ser Floating True
        if not collided:
            self.player.floating = True

        self.player.player_y += self.gravity - self.player.velocity_y

    def check_enemy_collision(self):
        try:
            for enemy in self.enemies:
                if self.player.player_rect.colliderect(enemy.enemy_rect) and not self.player.invincible:
                    play_sound(sounds.sfx_hurt, sound_state == SOUND_ON)  #type: ignore
                    self.player.take_damage()
                    break
        except Exception as e:
            print(f"Error checking enemy collision: {e}")

    def draw(self):
        try:
            screen.clear()  #type: ignore
            screen.fill((0, 100, 0))  #type: ignore
            self.map()
        except Exception as e:
            print(f"Error drawing game: {e}")
            traceback.print_exc()
    
    def update(self):
        global current_state
        
        try:
            # Update player and enemies
            self.player.update()
            for enemy in self.enemies:
                enemy.update()
            
            self.check_collision(self.top_collision_blocks)
            self.check_enemy_collision()
            
            # Knockback
            if self.player.player_damaged:
                self.player.player_x += self.player.velocity_x * self.player.facing_direction
            
            # Flag animation
            self.flag_animation_index += self.flag_animation_speed
            if self.flag_animation_index >= len(self.flag_animation):
                self.flag_animation_index = 0
            self.flag.image = self.flag_animation[int(self.flag_animation_index)]

            # Victory condition
            if self.player.player.colliderect(self.flag):
                play_sound(sounds.sfx_gem, sound_state == SOUND_ON)  #type: ignore
                current_state = WIN
            # Game Over condition
            elif self.player.health <= 0:
                current_state = GAMEOVER
                return
        except Exception as e:
            print(f"Error updating game: {e}")
            traceback.print_exc()

# ============================================================================
# WIN AND GAME OVER SCREENS
# ============================================================================
class Win:
    def draw(self):
        try:
            screen.clear()  #type: ignore
            screen.draw.text("YOU WIN!!!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="blue")  #type: ignore
        except Exception as e:
            print(f"Error drawing Win: {e}")

class Gameover:
    def draw(self):
        try:
            screen.clear()  #type: ignore
            screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="red")  #type: ignore
        except Exception as e:
            print(f"Error drawing Game Over: {e}")


# ============================================================================
# GLOBAL INSTANCES AND MAIN LOOP
# ============================================================================
try:
    menu = Menu()
    game = Game()
    gameover = Gameover()
    win = Win()
except Exception as e:
    print(f"Error initializing game instances: {e}")
    traceback.print_exc()

def draw():
    try:
        if current_state == MENU:
            menu.draw()  
        elif current_state == GAME:
            game.draw()
        elif current_state == GAMEOVER:
            gameover.draw()
        elif current_state == WIN:
            win.draw()
    except Exception as e:
        print(f"Error in render loop: {e}")
        traceback.print_exc()

def update():
    try:
        if current_state == GAME:
            game.update() 
        if current_state == MENU:
            menu.update()
    except Exception as e:
        print(f"Error in update loop: {e}")
        traceback.print_exc()

# Click only in menu
def on_mouse_down(pos):
    """Processes mouse clicks with error handling."""
    try:
        if current_state == MENU:
            menu.on_mouse_down(pos)
    except Exception as e:
        print(f"Error processing mouse click: {e}")

pgzrun.go()
