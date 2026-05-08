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
selected_level = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "resources", "images")

def get_image(image_name):
    try:
        if image_name not in _IMAGES:
            _IMAGES[image_name] = pygame.image.load(load_image(image_name)).convert_alpha()
        return _IMAGES[image_name]
    except:
        print(f"Изображения нет в папке: {image_name}")
        return None

def load_image(image_name):
    try:
        path = os.path.join(IMAGES_DIR, image_name + ".png")
        return path
    except:
        print(f"Изображения нет в папке: {image_name}")
        return None

# Функции отрисовки разных экранов
def draw_main_menu():
    menu_img = get_image("mainmenu")
    screen.blit(menu_img, (0, 0))
    start_btn.draw(screen)
    exit_btn.draw(screen)

def draw_level_menu():
    level_menu_img = get_image("levelmenu")
    screen.blit(level_menu_img, (0, 0))
    levelmenu_btn_exit.draw(screen)
    level1_btn.draw(screen)
    start_level_btn.draw(screen)
def draw_gameplay():
    gameplay_img = get_image("house")
    screen.blit(gameplay_img,(0, 0))

# Функции кнопок

#mainmenu кнопки
def start_game():
    global current_screen
    current_screen = "level_menu"
    reset_buttons()
def exit_game():
    global running
    running = False
#Levelmenu кнопки
def level_menu_exit():
    global current_screen, selected_level
    current_screen = "main_menu"
    selected_level = None
    reset_buttons()

def select_level(level):
    global selected_level
    selected_level = level
    start_level_btn.is_active = True
    level1_btn.is_selected = True
def start_level():
    global current_screen
    current_screen = "gameplay"
    reset_buttons()

# Функции для всех экранов
def reset_buttons():
    buttons = [start_btn, exit_btn, levelmenu_btn_exit, level1_btn, start_level_btn, start_level_btn, ]
    for btn in buttons:
        btn.is_pressed = False
    level1_btn.is_selected = False

# Класс кнопок

class ImageButton:
    def __init__(self, image_name, x, y, callback, hover_image=None, pressed_image=None, passed_image=None, nonactive_image=None, is_active=True):
        self.image = get_image(image_name)
        self.hover_image = get_image(image_name + "hover") or self.image
        self.pressed_image = get_image(image_name + "pressed") or self.image
        self.passed_image = get_image(image_name + "passed") or self.image
        self.nonactive_image = get_image(image_name + "nonactive") or self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.callback = callback
        self.is_pressed = False
        self.is_active = is_active
        self.is_selected = False

    def draw(self, surface):
        if not self.is_active:
            surface.blit(self.nonactive_image, self.rect.topleft)
        elif self.is_selected or self.is_pressed:
            surface.blit(self.pressed_image, self.rect.topleft)
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.hover_image, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)
    def handle_event(self, event):
        if not self.is_active:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                try:
                    self.callback()
                except Exception as e:
                    print(f"Ошибка при выполнении действия кнопки: {e}")
            self.is_pressed = False

start_btn = ImageButton("startgamebtn", WIDTH // 2, 400, start_game)
exit_btn = ImageButton("exitgamebtn", WIDTH // 2, 480, exit_game)

# Levelmenu элементы
levelmenu_btn_exit = ImageButton("levelmenuexitbtn", WIDTH - 748, HEIGHT - 43, level_menu_exit)
level1_btn = ImageButton("level1btn", WIDTH // 2 - 325, 118, lambda: select_level("Level 1"))
start_level_btn = ImageButton("levelmenustartbtn", WIDTH - 53, HEIGHT - 43, start_level, is_active=False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_screen == "main_menu":
            start_btn.handle_event(event)
            exit_btn.handle_event(event)
        elif current_screen == "level_menu":
            levelmenu_btn_exit.handle_event(event)
            level1_btn.handle_event(event)
            start_level_btn.handle_event(event)
    if current_screen == "main_menu":
        draw_main_menu()
    elif current_screen == "level_menu":
        draw_level_menu()
    elif current_screen == "gameplay":
        draw_gameplay()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


