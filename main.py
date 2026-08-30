import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Danh Nhau 2 Nguoi")
clock = pygame.time.Clock()

# Màu sắc
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Lớp Nhân Vật
class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, 50, 80)
        self.color = color
        self.controls = controls  # Phím điều khiển [Trái, Phải, Nhảy, Đánh]
        self.vel_y = 0
        self.is_jumping = False
        self.health = 100
        self.attacking = False
        self.attack_cooldown = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.facing_right = True

    def move(self, keys):
        dx = 0
        gravity = 0.8

        # Di chuyển trái/phải
        if keys[self.controls['left']]:
            dx = -5
            self.facing_right = False
        if keys[self.controls['right']]:
            dx = 5
            self.facing_right = True

        # Nhảy
        if keys[self.controls['jump']] and not self.is_jumping:
            self.vel_y = -15
            self.is_jumping = True

        # Trọng lực
        self.vel_y += gravity
        dy = self.vel_y

        # Va chạm sàn nhà
        if self.rect.bottom + dy >= HEIGHT - 50:
            dy = HEIGHT - 50 - self.rect.bottom
            self.is_jumping = False

        # Giới hạn màn hình
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right

        # Cập nhật vị trí
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            # Tạo vùng đấm phía trước nhân vật
            attack_x = self.rect.right if self.facing_right else self.rect.left - 40
            self.attack_rect = pygame.Rect(attack_x, self.rect.y + 20, 40, 20)

            # Kiểm tra trúng đối phương
            if self.attack_rect.colliderect(target.rect):
                target.health -= 10
                if target.health < 0:
                    target.health = 0

            self.attack_cooldown = 20  # Thời gian hồi đòn

    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown < 15:
                self.attacking = False

    def draw(self, surface):
        # Vẽ nhân vật
        pygame.draw.rect(surface, self.color, self.rect)
        # Vẽ hiệu ứng đấm
        if self.attacking:
            pygame.draw.rect(surface, YELLOW, self.attack_rect)

# Cấu hình phím bấm cho 2 người chơi
p1_controls = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w, 'attack': pygame.K_f}
p2_controls = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP, 'attack': pygame.K_KP_ENTER}

# Khởi tạo 2 người chơi
player1 = Player(150, 300, GREEN, p1_controls)
player2 = Player(600, 300, RED, p2_controls)

# Vẽ thanh máu
def draw_health_bar(surface, health, x, y):
    pygame.draw.rect(surface, WHITE, (x - 2, y - 2, 204, 24))
    pygame.draw.rect(surface, RED, (x, y, 200, 20))
    pygame.draw.rect(surface, GREEN, (x, y, health * 2, 20))

# Vòng lặp chính của Game
running = True
font = pygame.font.Font(None, 60)

while running:
    clock.tick(60)
    screen.fill(GRAY)

    # Vẽ sàn nhà
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))

    # Bắt sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == player1.controls['attack']:
                player1.attack(player2)
            if event.key == player2.controls['attack']:
                player2.attack(player1)

    # Cập nhật trạng thái
    keys = pygame.key.get_pressed()
    if player1.health > 0 and player2.health > 0:
        player1.move(keys)
        player2.move(keys)
        player1.update()
        player2.update()

    # Vẽ nhân vật và thanh máu
    player1.draw(screen)
    player2.draw(screen)
    draw_health_bar(screen, player1.health, 50, 30)
    draw_health_bar(screen, player2.health, 550, 30)

    # Kiểm tra thắng thua
    if player1.health <= 0:
        win_text = font.render("NGUOI CHOI 2 THANG!", True, RED)
        screen.blit(win_text, (WIDTH // 2 - 220, HEIGHT // 2 - 50))
    elif player2.health <= 0:
        win_text = font.render("NGUOI CHOI 1 THANG!", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - 220, HEIGHT // 2 - 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
