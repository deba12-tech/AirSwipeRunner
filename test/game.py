import pygame
import sys

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Swipe Runner")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game setup
FPS = 60
clock = pygame.time.Clock()

# Lanes: x positions for 3 lanes
lanes = [100, 250, 400]
player_lane = 1  # Start at center
player_y = 600
player_size = 40
jumping = False
jump_height = 0
jump_max = 150
jump_speed = 10

def draw_player():
    pygame.draw.rect(WIN, RED, (lanes[player_lane] - player_size // 2, player_y - jump_height, player_size, player_size))

def main():
    global player_lane, jumping, jump_height

    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Left / Right Movement
        if keys[pygame.K_LEFT] and player_lane > 0:
            player_lane -= 1
            pygame.time.delay(150)
        if keys[pygame.K_RIGHT] and player_lane < 2:
            player_lane += 1
            pygame.time.delay(150)

        # Jump
        if keys[pygame.K_UP] and not jumping:
            jumping = True

        # Jump logic
        if jumping:
            if jump_height < jump_max:
                jump_height += jump_speed
            else:
                jumping = False
        elif jump_height > 0:
            jump_height -= jump_speed

        draw_player()
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
