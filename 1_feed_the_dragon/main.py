import pygame, random

# Initialize pygame
pygame.init()

# Set display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 3
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 5
COIN_ACCERLATION = 0.4
BUFFER_DISTANCE = 100

score = 0
lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (10, 50, 10)

# Set fonts
font = pygame.font.SysFont('AttackGraffiti', 32)

# Set text
score_text = font.render(f"Score: {score}", True, GREEN, DARK_GREEN)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

title_text = font.render("Feed the Dragon", True, GREEN, DARK_GREEN)
title_text_rect = title_text.get_rect()
title_text_rect.centerx = WINDOW_WIDTH // 2
title_text_rect.y = 10

lives_text = font.render(f"Lives: {lives}", True, GREEN, DARK_GREEN)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("Game Over", True, GREEN, DARK_GREEN)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

game_continue_text = font.render("Press any key to play again", True, GREEN, DARK_GREEN)
game_continue_text_rect = game_continue_text.get_rect()
game_continue_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 32)


# Set sounds
coin_sound = pygame.mixer.Sound('./sounds/coin.wav')
miss_sound = pygame.mixer.Sound('./sounds/miss.wav')
pygame.mixer.music.load('./sounds/music.wav')
gameover_music = pygame.mixer.Sound('./sounds/gameover.wav')


# Set images
dragon_image = pygame.image.load('./images/dragon.png')
dragon_rect = dragon_image.get_rect()
dragon_rect.left = 10
dragon_rect.centery = WINDOW_HEIGHT // 2

coin_image = pygame.image.load('./images/coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - coin_rect.height)



# Start the background music
pygame.mixer.music.play(-1, 0.0)

# The main game loop
running = True
while running:
    # check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Check to see if user wants to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and dragon_rect.top > 64:
        dragon_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and dragon_rect.bottom < WINDOW_HEIGHT:
        dragon_rect.y += PLAYER_VELOCITY

    # Move the coin
    if coin_rect.x < 0:
        # player missed the coin
        lives -= 1
        miss_sound.play()
        coin_rect.centerx = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - coin_rect.height)
    else:
        # move the coin
        coin_rect.x -= coin_velocity


    # Check for collision
    if dragon_rect.colliderect(coin_rect):
        # player caught the coin
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCERLATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - coin_rect.height)


    # Update HUD
    score_text = font.render(f"Score: {score}", True, GREEN, DARK_GREEN)
    lives_text = font.render(f"Lives: {lives}", True, GREEN, DARK_GREEN)


    # Check for game over
    if lives <= 0:
        # player lost
        pygame.mixer.music.stop()
        gameover_music.play()
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(game_continue_text, game_continue_text_rect)
        pygame.display.update()

        # Wait for user to press a key
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    score = 0
                    lives = PLAYER_STARTING_LIVES
                    dragon_rect.bottom = WINDOW_HEIGHT // 2
                    coin_velocity = COIN_STARTING_VELOCITY
                    gameover_music.stop()
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False




    # Fill the display surface
    display_surface.fill(BLACK)

    # Blit the HUD to the display surface
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(lives_text, lives_text_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    # Blit assets to the display surface
    display_surface.blit(dragon_image, dragon_rect)
    display_surface.blit(coin_image, coin_rect)

    # Update the display
    pygame.display.update()
    clock.tick(FPS)

    
# End the game
pygame.quit()