import os
import pygame

pygame.init()


WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

_IMAGES = {}
running = True
current_screen = "main_menu"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "resources", "images")

def get_image(image_name):
    if image_name not in _IMAGES:
        _IMAGES[image_name] = pygame.image.load(load_image(image_name)).convert_alpha()
    return _IMAGES[image_name]

def load_image(image_name):
    path = os.path.join(IMAGES_DIR, image_name + ".png")
    return path

# Функции отрисовки разных экранов
def draw_main_menu():
    menu_img = get_image("mainmenu")
    screen.blit(menu_img, (0, 0))
    start_btn.draw(screen)
    exit_btn.draw(screen)

def draw_level_menu():
    level_menu_img = get_image("levelmenu")
    screen.blit(level_menu_img, (0, 0))

# Функции кнопок
def start_game():
    global current_screen
    current_screen = "level_menu"

def exit_game():
    global running
    running = False

class ImageButton:
    def __init__(self, image_name, x, y, callback, hover_image=None):
        self.image = get_image(image_name)
        self.hover_image = hover_image or self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.callback = callback

    def draw(self, surface):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.hover_image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

start_btn = ImageButton("startgamebtn", WIDTH // 2, 400, start_game)
exit_btn = ImageButton("exitgamebtn", WIDTH // 2, 480, exit_game)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        start_btn.handle_event(event)
        exit_btn.handle_event(event)
    draw_main_menu()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


