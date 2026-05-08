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
BG_W = 1428
BG_H = 736
camera_x = 500
camera_y = 100
CAMERA_SPEED = 15
CAMERA_MOVE_AREA = 20
timer_start_ms = None
timer_elapsed_ms = 0
timer_font = pygame.font.Font(None, 42)
player_name = ""
show_name_popup = False
name_input_active = False
MAX_NAME_LEN = 16
name_font = pygame.font.Font(None, 58)
NAME_TEXT_POS = (295, 408)
ROOMS = {
    "living_room": pygame.Rect(0, 400, 1428, 336),
    "hall": pygame.Rect(0, 0, 714, 400),
    "kitchen": pygame.Rect(714, 0, 714, 400),
}
TRANSITION_TIME_MS = 1500 # столько мс персонажи переходят между комнатами
INTERACT_RANGE_PX = 10 # погрешность от мебели для взаимодействия

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
    screen.fill((0, 0, 0))
    menu_img = get_image("mainmenu")
    screen.blit(menu_img, (0, 0))
    start_btn.draw(screen)
    exit_btn.draw(screen)

def draw_level_menu():
    screen.fill((0, 0, 0))
    level_menu_img = get_image("levelmenu")
    screen.blit(level_menu_img, (0, 0))
    levelmenu_btn_exit.draw(screen)
    level1_btn.draw(screen)
    start_level_btn.draw(screen)

    if show_name_popup:
        popup_img = get_image("whatsyourname")
        if popup_img:
            popup_rect = popup_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(popup_img, popup_rect.topleft)

            # Вводимое имя поверх картинки;
            name_text = name_font.render(player_name, True, (255, 255, 255))
            screen.blit(name_text, NAME_TEXT_POS)

            # Небольшой курсор, чтобы было видно активность ввода
            if name_input_active and (pygame.time.get_ticks() // 400) % 2 == 0:
                cursor_x = NAME_TEXT_POS[0] + name_text.get_width() + 2
                cursor_y = NAME_TEXT_POS[1]
                pygame.draw.line(screen, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + name_text.get_height()), 2)
def draw_gameplay():
    screen.fill((0, 0, 0))
    gameplay_img = get_image("house")
    gameplay_overlay_img = get_image("ingameoverlay")
    if gameplay_img:
        global camera_x, camera_y
        # Предполагаем известные размеры фонового изображения BG_W, BG_H
        max_x = BG_W - WIDTH
        max_y = BG_H - HEIGHT
        camera_x = max(0, min(camera_x, max_x))
        camera_y = max(0, min(camera_y, max_y))
        # Быстрое и простое отображение нужной области фона
        screen.blit(gameplay_img, (0, 0), (camera_x, camera_y, WIDTH, HEIGHT))
    if gameplay_overlay_img:
        screen.blit(gameplay_overlay_img, (0, 0))
        ingame_exit_btn.draw(screen)
    minutes = timer_elapsed_ms // 60000
    seconds = (timer_elapsed_ms // 1000) % 60
    timer_text = timer_font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH-150, HEIGHT-106))

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

def open_name_popup():
    global show_name_popup, name_input_active, player_name
    show_name_popup = True
    name_input_active = False
    player_name = ""

def confirm_name_and_start_level():
    global current_screen, camera_x, camera_y, show_name_popup, name_input_active
    current_screen = "gameplay"
    init_level()
    camera_x = 500
    camera_y = 100
    show_name_popup = False
    name_input_active = False
    reset_buttons()

# Функции для всех экранов
def reset_buttons():
    buttons = [start_btn, exit_btn, levelmenu_btn_exit, level1_btn, start_level_btn, start_level_btn, ]
    for btn in buttons:
        btn.is_pressed = False
    level1_btn.is_selected = False


# Создание уровня
def init_level():
    global player, enemy, furniture_list, door_list, held_item

    player = Player(x=200, y=520, room="living_room")
    enemy_patrol = [(100, 120), (620, 120)]
    enemy = Enemy(x=100, y=120, room="hall", patrol_points=enemy_patrol)

    furniture_list = [
        Furniture("cabinet", x=150, y=520, room="living_room", items_inside=[Item("glue")]),
        Furniture("fridge", x=850, y=120, room="kitchen", items_inside=[Item("egg")]),
        Furniture("microwave", x=950, y=120, room="kitchen", items_inside=[]),
        Furniture("binoculars", x=620, y=120, room="hall", items_inside=[]),
    ]

    door_list = [
        Door(x=700, y=380, room_from="hall", to_room="living_room"),
        Door(x=720, y=380, room_from="kitchen", to_room="living_room"),
        Door(x=700, y=380, room_from="living_room", to_room="hall"),
        Door(x=720, y=380, room_from="living_room", to_room="kitchen"),
    ]

    held_item = None

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

class Item:
    def __init__(self, type_name, image=None):
        self.name = type_name
        self.image = image

class Furniture:
    def __init__(self, name, x, y, room, items_inside=None):
        self.name = name
        self.x = x
        self.y = y
        self.room = room
        self.items_inside = items_inside or []
        self.rect = pygame.Rect(x, y, 50, 50)

    def can_interact(self, player_x, player_room):
        return player_room == self.room and abs(player_x - self.x) <= INTERACT_RANGE_PX
    
    def take_item(self):
        if self.items_inside:
            return self.items_inside.pop()
        else:
            return None
    def apply_item(self, item):
        return False
    
class Door:
    def __init__(self, x, y, room_from, to_room):
        self.x = x
        self.y = y
        self.from_room = room_from
        self.to_room = to_room
        self.rect = pygame.Rect(x-16, y-32, 32, 64)
    def can_enter(self, player_x, player_room):
        return player_room == self.from_room and abs(player_x - self.x) <= INTERACT_RANGE_PX

class Player:
    def __init__(self, x, y, room):
        self.x = x
        self.y = y
        self.room = room
        self.state = "idle"
        self.inventory = []
        self.sabotage_count = 0
    def screen_pos(self, cam_x, cam_y):
        return int(self.x - cam_x), int(self.y - cam_y)

class Enemy:
    def __init__(self, x, y, room, patrol_points):
        self.x = x
        self.y = y
        self.room = room
        self.patrol = patrol_points[:]  # список (x,y) точек
        self.patrol_i = 0
        self.state = "patrol"  # patrol, transition, ghost, inspecting
        self.ghost = False

start_btn = ImageButton("startgamebtn", WIDTH // 2, 400, start_game)
exit_btn = ImageButton("exitgamebtn", WIDTH // 2, 480, exit_game)

# Levelmenu элементы
levelmenu_btn_exit = ImageButton("levelmenuexitbtn", WIDTH - 748, HEIGHT - 43, level_menu_exit)
level1_btn = ImageButton("level1btn", WIDTH // 2 - 325, 118, lambda: select_level("Level 1"))
start_level_btn = ImageButton("levelmenustartbtn", WIDTH - 53, HEIGHT - 43, open_name_popup, is_active=False)

#Ingame элементы
ingame_exit_btn = ImageButton("ingameexitbtn", WIDTH - 34, HEIGHT - 91, level_menu_exit)

while running:
    if current_screen == "gameplay" and timer_start_ms is None:
        timer_start_ms = pygame.time.get_ticks()
        timer_elapsed_ms = 0
    elif current_screen != "gameplay" and timer_start_ms is not None:
        timer_start_ms = None
        timer_elapsed_ms = 0

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

            if show_name_popup:
                popup_img = get_image("whatsyourname")
                if popup_img:
                    popup_rect = popup_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                    # Клик по картинке включает ввод имени
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if popup_rect.collidepoint(event.pos):
                            name_input_active = True
                        else:
                            name_input_active = False

                if name_input_active and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Запускаем уровень, имя уже сохранено в player_name
                        confirm_name_and_start_level()
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        show_name_popup = False
                        name_input_active = False
                    else:
                        # Лимит 10 символов
                        if len(player_name) < MAX_NAME_LEN and event.unicode.isprintable() and not event.unicode.isspace():
                            player_name += event.unicode
        elif current_screen == "gameplay":
            ingame_exit_btn.handle_event(event)

    # Движение камеры при наведении мыши к краям экрана (каждый кадр)
    if current_screen == "gameplay":
        mx, my = pygame.mouse.get_pos()
        if mx < CAMERA_MOVE_AREA:
            camera_x -= CAMERA_SPEED//2
        elif mx > WIDTH - CAMERA_MOVE_AREA:
            camera_x += CAMERA_SPEED//2
        if my < CAMERA_MOVE_AREA:
            camera_y -= CAMERA_SPEED//2
        elif my > HEIGHT - CAMERA_MOVE_AREA:
            camera_y += CAMERA_SPEED//2
        # Ограничиваем камеру в пределах фонового изображения
        camera_x = max(0, min(camera_x, BG_W - WIDTH))
        camera_y = max(0, min(camera_y, BG_H - HEIGHT))
        if timer_start_ms is not None:
            timer_elapsed_ms = pygame.time.get_ticks() - timer_start_ms
    
    if current_screen == "main_menu":
        draw_main_menu()
    elif current_screen == "level_menu":
        draw_level_menu()
    elif current_screen == "gameplay":
        draw_gameplay()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


