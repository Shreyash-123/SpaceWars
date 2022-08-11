# Space Wars Game
# Made By -> @Shreyash
import pygame
from pygame import mixer
import os
import random
import sys

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
PLAYER_X = 430
PLAYER_Y = 480
MOVE_PLAYER_X = 10
ENEMY_X = 480
ENEMY_Y = 20
ENEMY_X_CHANGE = 20
ENEMY_Y_CHANGE = 30
BULLET_X = 0  # Not used
BULLET_Y = 480
BULLET_CHANGE_X = 0
BULLET_CHANGE_Y = 15
FPS = 40
WHITE = (255, 255, 255)
"""
 Enemy respawning range
 -> x-axis = randint(0, 870)
 -> y-axis = randint(0, 200)
"""


class Game:
    def __init__(self):
        pygame.init()
        icon = pygame.image.load(r"GameImages\GameIcon.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Space Wars By -> @Shreyash Suyal")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = Player(self.screen)
        self.enemy = Enemy(self.screen)
        self.bullet = Bullet(self.screen)
        self.clock = pygame.time.Clock()
        self.background_image = pygame.image.load(
            r"GameImages\Background.png")
        pygame.mixer.init()
        self.background_music()
        self.score = 0
        # Game Sounds
        self.bullet_sound = mixer.Sound(r"GameSounds\BulletSound.mp3")
        self.collision_sound = mixer.Sound(r"GameSounds\EnemyKilledSound.mp3")

    # Game Over
    def game_over(self):
        pygame.mixer.music.pause()
        game_over_image = pygame.image.load(r"GameImages\GameOver.png")
        game_over_sound = mixer.Sound(r"GameSounds\GameOverSound.mp3")
        game_over_sound.play()
        # Game Over Loop
        while True:
            self.screen.blit(game_over_image, (0, 0))
            font = pygame.font.SysFont('arail', 220)
            line1 = font.render("GAME OVER", True, WHITE)
            self.screen.blit(line1, (30, 100))
            font = pygame.font.SysFont('arail', 130)
            line2 = font.render(f"Your Score is : {self.score}", True, WHITE)
            self.screen.blit(line2, (130, 280))
            font = pygame.font.SysFont('arail', 100)
            line3 = font.render("Press \"Enter\" to play again", True, WHITE)
            self.screen.blit(line3, (50, 410))
            font = pygame.font.SysFont('arail', 80)
            line4 = font.render("Made By -> @Shreyash Suyal", True, (0, 0, 0))
            self.screen.blit(line4, (100, 530))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        start()

    # Background Music
    @staticmethod
    def background_music():
        bg_music = r"GameSounds\BackgroundSound.mp3"
        pygame.mixer.music.load(bg_music)
        pygame.mixer.music.play(-1)

    # Score
    def display_score(self):
        font = pygame.font.SysFont('arail', 50)
        score = font.render(f"Score : {self.score}", True, WHITE)
        self.screen.blit(score, (20, 10))

    # Bullet and Enemy Collision
    def is_collision(self, i):
        enemy_rectangle = self.enemy.image[i].get_rect(topleft=(self.enemy.x[i], self.enemy.y[i]))
        bullet_rectangle = self.bullet.bullet_image.get_rect(topleft=(self.bullet.bullet_x, self.bullet.bullet_y))
        if enemy_rectangle.colliderect(bullet_rectangle):
            return True
        return False

    # Spaceship and Enemy Collision
    def game_over_collision(self, i):
        enemy_rectangle = self.enemy.image[i].get_rect(topleft=(self.enemy.x[i], self.enemy.y[i]))
        spaceship_rectangle = self.player.image.get_rect(topleft=(self.player.x, self.player.y))
        if enemy_rectangle.colliderect(spaceship_rectangle):
            return True
        return False

    def play(self):
        self.player.move()
        self.bullet.move(BULLET_X)
        for i in range(self.enemy.num_of_enemies):
            # Game Over Logic
            if self.enemy.y[i] > 380:
                if self.game_over_collision(i):
                    self.game_over()
            # Collision Logic
            if self.bullet.bullet_state == "fire" and self.is_collision(i):
                self.collision_sound.play()
                self.bullet.bullet_y = 480
                self.bullet.bullet_state = "ready"
                self.score += 1
                # Make Game Challenging Condition
                if self.score % 5 == 0:
                    self.enemy.num_of_enemies += 3
                    for j in range(3):
                        self.enemy.add_enemy()
                self.enemy.x[i] = random.randint(0, 870)
                self.enemy.y[i] = random.randint(0, 200)
                self.enemy.random_enemy_after_collision(i)
        self.display_score()
        self.enemy.move()
        pygame.display.flip()
        self.clock.tick(FPS)

    def run(self):
        while True:
            self.screen.blit(self.background_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_a:
                        self.player.move_left()
                    elif event.key == pygame.K_d:
                        self.player.move_right()
                    elif event.key == pygame.K_SPACE:
                        if self.bullet.bullet_state == "ready":
                            self.bullet_sound.play()
                            global BULLET_X
                            BULLET_X = self.player.x
                            self.bullet.fire_bullet(BULLET_X, BULLET_Y)
            self.play()


class Player:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load(r"GameImages\2D_Space_Craft.png")
        self.x = PLAYER_X
        self.y = PLAYER_Y
        self.direction = random.choice([-MOVE_PLAYER_X, MOVE_PLAYER_X])

    def move_left(self):
        self.direction = -5

    def move_right(self):
        self.direction = 5

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x += self.direction
        if self.x <= 0:
            # Set to screen width bounds
            self.x = 0
            self.direction = MOVE_PLAYER_X
        if self.x >= 902:
            # Set to screen width bounds
            self.x = 902
            self.direction = -MOVE_PLAYER_X

        self.draw()


class Enemy:
    def __init__(self, screen):
        self.screen = screen
        self.num_of_enemies = 6
        self.x = []
        self.y = []
        self.image = []
        self.direction = []
        self.enemy_dir = r"GameImages\Enemies"
        self.enemies_list = os.listdir(self.enemy_dir)
        for i in range(self.num_of_enemies):
            self.add_enemy()

    def add_enemy(self):
        # Range of positioning enemy
        self.x.append(random.randint(0, 870))
        self.y.append(random.randint(0, 200))
        rand_enemy = (random.randint(0, len(self.enemies_list) - 1))
        enemy_image = os.path.join(self.enemy_dir, self.enemies_list[rand_enemy])
        self.image.append(pygame.image.load(enemy_image))
        self.direction.append(random.choice([-ENEMY_X_CHANGE, ENEMY_X_CHANGE]))

    def random_enemy_after_collision(self, i):
        self.image.pop(i)
        self.direction.pop(i)
        rand_enemy = (random.randint(0, len(self.enemies_list) - 1))
        enemy_image = os.path.join(self.enemy_dir, self.enemies_list[rand_enemy])
        self.image.insert(i, pygame.image.load(enemy_image))
        self.direction.insert(i, random.choice([-ENEMY_X_CHANGE, ENEMY_X_CHANGE]))

    def move(self):
        for i in range(self.num_of_enemies):
            self.x[i] += self.direction[i]
            if self.x[i] <= 0:
                # Set to screen width bounds
                self.x[i] = 0
                self.direction[i] = ENEMY_X_CHANGE
                self.y[i] += ENEMY_Y_CHANGE
            if self.x[i] >= 900:
                # Set to screen width bounds
                self.x[i] = 900
                self.direction[i] = -ENEMY_X_CHANGE
                self.y[i] += ENEMY_Y_CHANGE
            self.draw(i)

    def draw(self, i):
        self.screen.blit(self.image[i], (self.x[i], self.y[i]))
        # pygame.display.flip()


class Bullet:
    def __init__(self, screen):
        self.screen = screen
        self.bullet_image = pygame.image.load(r"GameImages\Bullet.png")
        self.bullet_x = 0
        # Same as spaceship
        self.bullet_y = BULLET_Y
        # Ready state : bullet cannot be seen on the screen
        # Fire state : bullet is currently moving
        self.bullet_state = "ready"

    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        self.screen.blit(self.bullet_image, (x + 30, y + 10))

    def move(self, x):
        self.bullet_x = x
        if self.bullet_y <= 0:
            self.bullet_y = 480
            self.bullet_state = "ready"

        if self.bullet_state == "fire":
            self.fire_bullet(self.bullet_x, self.bullet_y)
            self.bullet_y -= BULLET_CHANGE_Y


# Function to Start the Game
def start():
    game = Game()
    game.run()


if __name__ == "__main__":
    start()
