import pygame
import random
import sys
from gesture_control import SwipeDetector

pygame.init()

WIDTH, HEIGHT = 500, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Swipe Runner")

BG = pygame.image.load("assets/background.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
PLAYER_IMG = pygame.image.load("assets/player.png")
OBSTACLE_IMG = pygame.image.load("assets/obstacle.png")

FPS = 60
clock = pygame.time.Clock()
lanes = [100, 250, 400]
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)
huge_font = pygame.font.SysFont("Arial", 80)

OBSTACLE_SPEED = 7
SPAWN_RATE = 30
gesture = SwipeDetector()

class Obstacle:
    def __init__(self):
        self.lane = random.randint(0, 2)
        self.y = -100
        self.img = pygame.transform.scale(OBSTACLE_IMG, (60, 60))

    def move(self):
        self.y += OBSTACLE_SPEED

    def draw(self):
        WIN.blit(self.img, (lanes[self.lane] - 30, self.y))

    def collide(self, player_lane, player_y, immune=False):
        if immune:
            return False
        return self.y > player_y - 60 and self.lane == player_lane

def draw_window(bg_y, player_img, player_lane, player_y, obstacles, score, feedback_text):
    WIN.blit(BG, (0, bg_y))
    WIN.blit(BG, (0, bg_y - HEIGHT))
    WIN.blit(player_img, (lanes[player_lane] - 32, player_y))
    for obs in obstacles:
        obs.draw()
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (10, 10))
    if feedback_text:
        feedback_render = font.render(feedback_text, True, (0, 255, 0))
        WIN.blit(feedback_render, (WIDTH // 2 - feedback_render.get_width() // 2, HEIGHT - 60))
    pygame.display.update()

def start_screen():
    blink_timer = 0
    while True:
        WIN.fill((10, 10, 40))
        title = huge_font.render("AIR SWIPE RUNNER", True, (255, 255, 0))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))

        if (blink_timer // 30) % 2 == 0:
            start_text = font.render("Swipe to Move | Press Any Key to Start", True, (200, 200, 255))
            WIN.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 20))

        pygame.display.update()
        blink_timer += 1
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def countdown():
    for i in range(3, 0, -1):
        WIN.fill((10, 10, 40))
        count = big_font.render(str(i), True, (255, 255, 255))
        WIN.blit(count, (WIDTH // 2 - count.get_width() // 2, HEIGHT // 2 - 20))
        pygame.display.update()
        pygame.time.wait(700)

def game_over_screen(score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    blink = 0
    while True:
        WIN.blit(overlay, (0, 0))
        over_text = huge_font.render("GAME OVER", True, (255, 50, 50))
        final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart or ESC to Exit", True, (180, 180, 180))

        WIN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 100))
        WIN.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 - 20))

        if (blink // 30) % 2 == 0:
            WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

        pygame.display.update()
        blink += 1
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    gesture.start()
    player_img = pygame.transform.scale(PLAYER_IMG, (64, 64))
    player_lane = 1
    player_y = 550
    score = 0
    bg_y = 0
    frame_count = 0
    obstacles = []

    last_swipe_time = 0
    swipe_cooldown = 0.3
    immunity_duration = 0.5
    feedback_text = ""

    start_screen()
    countdown()
    run = True

    while run:
        clock.tick(FPS)
        bg_y += 5
        if bg_y >= HEIGHT:
            bg_y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        swipe = gesture.get_gesture()
        current_time = pygame.time.get_ticks() / 1000

        if swipe and (current_time - last_swipe_time > swipe_cooldown):
            feedback_text = swipe.upper()
            if swipe == "left" and player_lane > 0:
                player_lane -= 1
            elif swipe == "right" and player_lane < 2:
                player_lane += 1
            elif swipe == "up":
                feedback_text = "JUMP (Coming Soon)"
            last_swipe_time = current_time

        frame_count += 1
        if frame_count % SPAWN_RATE == 0:
            obstacles.append(Obstacle())

        immune = (current_time - last_swipe_time) < immunity_duration

        for obs in obstacles[:]:
            obs.move()
            if obs.collide(player_lane, player_y, immune=immune):
                run = False
            if obs.y > HEIGHT:
                obstacles.remove(obs)
                score += 1

        draw_window(bg_y, player_img, player_lane, player_y, obstacles, score, feedback_text)

    gesture.stop()
    game_over_screen(score)

if __name__ == "__main__":
    main()

