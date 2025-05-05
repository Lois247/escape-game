import pygame
import random
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Esquive les flèches !")
clock = pygame.time.Clock()
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

# Joueur
lane_positions = [100, 200, 300]
current_lane = 1
target_lane = 1
player_y = HEIGHT - 80
player_x = lane_positions[current_lane]
player_speed = 10

# Flèches
arrow_width = 20
arrow_height = 40
arrow_speed = 5
arrow_spawn_delay = 40
arrow_timer = 0
arrows = []

# Bonus
bonuses = []
bonus_timer = 0
bonus_spawn_delay = 60

# Font
font_large = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 32)

# État du jeu
game_state = "difficulty"
move_cooldown = 0
game_over = False

# Temps et score
start_ticks = 0
elapsed_seconds = 0
score = 0


def draw_player():
    x = int(player_x)
    y = player_y
    head_radius = 12
    pygame.draw.circle(screen, BLACK, (x, y), head_radius)
    pygame.draw.line(screen, BLACK, (x, y + head_radius), (x, y + head_radius + 5), 2)
    shoulder_y = y + head_radius + 5
    pygame.draw.line(screen, BLACK, (x - 12, shoulder_y), (x + 12, shoulder_y), 2)
    body_top = shoulder_y
    body_bottom = body_top + 15
    pygame.draw.line(screen, BLACK, (x, body_top), (x, body_bottom), 3)
    pygame.draw.line(screen, BLACK, (x - 12, shoulder_y), (x - 20, body_top + 15), 2)
    pygame.draw.line(screen, BLACK, (x + 12, shoulder_y), (x + 20, body_top + 15), 2)
    leg_y = body_bottom
    pygame.draw.line(screen, BLACK, (x, leg_y), (x - 10, leg_y + 20), 2)
    pygame.draw.line(screen, BLACK, (x, leg_y), (x + 10, leg_y + 20), 2)
    pygame.draw.line(screen, BLACK, (x - 10, leg_y + 20), (x - 15, leg_y + 20), 2)
    pygame.draw.line(screen, BLACK, (x + 10, leg_y + 20), (x + 15, leg_y + 20), 2)


def draw_arrow(x, y):
    pygame.draw.polygon(screen, RED, [
        (x, y + arrow_height),
        (x - 10, y),
        (x + 10, y)
    ])


def draw_bonus(x, y):
    pygame.draw.rect(screen, GOLD, (x - 10, y, 20, 20))
    pygame.draw.rect(screen, BLACK, (x - 10, y, 20, 20), 2)


def check_collision(arrow):
    player_rect = pygame.Rect(player_x - 10, player_y - 20, 20, 40)
    arrow_rect = pygame.Rect(arrow[0] - 10, arrow[1], 20, arrow_height)
    return player_rect.colliderect(arrow_rect)


def check_bonus_collision(bonus):
    player_rect = pygame.Rect(player_x - 10, player_y - 20, 20, 40)
    bonus_rect = pygame.Rect(bonus[0] - 10, bonus[1], 20, 20)
    return player_rect.colliderect(bonus_rect)


def show_game_over():
    text = font_large.render("Game Over", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    final_time = font_small.render(f"Temps : {elapsed_seconds:.1f}s", True, BLACK)
    final_score = font_small.render(f"Score : {score}", True, BLACK)
    screen.blit(final_time, (WIDTH // 2 - final_time.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 70))
    restart_text = font_small.render("Appuie sur ESPACE pour rejouer", True, RED)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))


def show_victory_screen():
    screen.fill(WHITE)
    text = font_large.render("🎉 Vous avez gagné !", True, (0, 150, 0))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
    win_msg = font_small.render("Félicitations, vous avez survécu !", True, BLACK)
    screen.blit(win_msg, (WIDTH // 2 - win_msg.get_width() // 2, HEIGHT // 2 - 20))
    time_text = font_small.render(f"Temps : {elapsed_seconds:.1f}s", True, BLACK)
    score_text = font_small.render(f"Score : {score}", True, BLACK)
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT // 2 + 20))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
    restart_text = font_small.render("Appuie sur ESPACE pour rejouer", True, (0, 150, 0))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 90))
    pygame.display.flip()


# Boucle principale
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state in ["game_over", "victory", "start"]:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_state = "start"
                current_lane = 1
                target_lane = 1
                player_x = lane_positions[current_lane]
        if game_state == "difficulty" and event.type == pygame.MOUSEBUTTONDOWN:
            if easy_btn.collidepoint(event.pos):
                arrow_speed = 5
                game_state = "start"
            elif medium_btn.collidepoint(event.pos):
                arrow_speed = 8
                game_state = "start"
            elif hard_btn.collidepoint(event.pos):
                arrow_speed = 11
                game_state = "start"

    if game_state == "difficulty":
        screen.fill(WHITE)
        title = font_large.render("Choisissez la difficulté", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        easy_btn = pygame.Rect(100, 200, 200, 50)
        medium_btn = pygame.Rect(100, 280, 200, 50)
        hard_btn = pygame.Rect(100, 360, 200, 50)
        pygame.draw.rect(screen, (0, 150, 0), easy_btn)
        pygame.draw.rect(screen, (180, 180, 180), medium_btn)
        pygame.draw.rect(screen, (255, 0, 0), hard_btn)
        screen.blit(font_small.render("Facile", True, BLACK), (easy_btn.centerx - 30, easy_btn.centery - 10))
        screen.blit(font_small.render("Moyen", True, BLACK), (medium_btn.centerx - 35, medium_btn.centery - 10))
        screen.blit(font_small.render("Difficile", True, BLACK), (hard_btn.centerx - 40, hard_btn.centery - 10))
        pygame.display.flip()

    elif game_state == "start":
        screen.fill(WHITE)
        title = font_large.render("Esquive les flèches !", True, BLACK)
        start_msg = font_small.render("Appuie sur ESPACE pour commencer", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_msg, (WIDTH // 2 - start_msg.get_width() // 2, HEIGHT // 2))
        draw_player()
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "playing"
            arrows = []
            bonuses = []
            arrow_timer = 0
            bonus_timer = 0
            game_over = False
            score = 0
            start_ticks = pygame.time.get_ticks()

    elif game_state == "playing":
        screen.fill(WHITE)
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_seconds >= 45:
            game_state = "victory"

        keys = pygame.key.get_pressed()
        if move_cooldown == 0:
            if keys[pygame.K_LEFT] and target_lane > 0:
                target_lane -= 1
                move_cooldown = 10
            elif keys[pygame.K_RIGHT] and target_lane < 2:
                target_lane += 1
                move_cooldown = 10
        if move_cooldown > 0:
            move_cooldown -= 1

        target_x = lane_positions[target_lane]
        if abs(player_x - target_x) > player_speed:
            player_x += player_speed if player_x < target_x else -player_speed
        else:
            player_x = target_x

        arrow_timer += 1
        if arrow_timer >= arrow_spawn_delay:
            arrow_lane = random.randint(0, 2)
            arrow_x = lane_positions[arrow_lane]
            arrows.append([arrow_x, -40])
            arrow_timer = 0

        for arrow in arrows:
            arrow[1] += arrow_speed
            draw_arrow(arrow[0], arrow[1])
            if check_collision(arrow):
                game_over = True
                game_state = "game_over"

        arrows = [arrow for arrow in arrows if arrow[1] < HEIGHT]

        if elapsed_seconds >= 30:
            bonus_timer += 1
            if bonus_timer >= bonus_spawn_delay:
                bonus_lane = random.randint(0, 2)
                bonus_x = lane_positions[bonus_lane]
                bonuses.append([bonus_x, -20])
                bonus_timer = 0

        for bonus in bonuses[:]:
            bonus[1] += arrow_speed
            draw_bonus(bonus[0], bonus[1])
            if check_bonus_collision(bonus):
                score += 1000
                bonuses.remove(bonus)

        bonuses = [bonus for bonus in bonuses if bonus[1] < HEIGHT]

        score = int(elapsed_seconds * 124.743)

        draw_player()
        time_text = font_small.render(f"Temps : {elapsed_seconds:.1f}s", True, BLACK)
        score_text = font_small.render(f"Score : {score}", True, BLACK)
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (10, 40))
        pygame.display.flip()

    elif game_state == "game_over":
        show_game_over()
        pygame.display.flip()

    elif game_state == "victory":
        show_victory_screen()

pygame.quit()
sys.exit()
