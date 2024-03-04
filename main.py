import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)

# Enumeration for game states
class GameState:
    PLAYING = 1

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load player image
        self.image = pygame.image.load("Redball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.hotbar = []

# Crop class
class Crop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_planted = False
        self.growth_time = random.randint(0, 5)  # Adjusted initial growth time for testing

    def update(self):
        if self.is_planted and self.growth_time > 0:
            self.growth_time -= 1
        elif self.is_planted:
            self.image.fill(BROWN)  # Change color to brown when fully grown

# Initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Farmers")  # Set window caption to "Ball Farmers"
clock = pygame.time.Clock()

# Create player and crop groups
all_sprites = pygame.sprite.Group()
crops_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Initial game state
current_state = GameState.PLAYING

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # Plant a crop when 'E' key is pressed
                x, y = player.rect.center
                new_crop = Crop(x, y)
                crops_group.add(new_crop)
                all_sprites.add(new_crop)
            elif event.key == pygame.K_p:
                # Harvest crops when 'P' key is pressed
                for crop in pygame.sprite.spritecollide(player, crops_group, dokill=True):
                    player.hotbar.append(crop)

    # Player movement
    keys = pygame.key.get_pressed()
    player_speed = 5
    if keys[pygame.K_LEFT]:
        player.rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.rect.x += player_speed
    if keys[pygame.K_UP]:
        player.rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player.rect.y += player_speed

    # Update crop growth
    crops_group.update()

    # Draw background
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
