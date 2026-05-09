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
door_transition_active = False
door_from = None
door_to = None
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
selected_item_index = None
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
INVENTORY_START_X = 180
INVENTORY_START_Y = 536
INVENTORY_ITEM_SPACING = 80
TOP_DOOR_POS = (1090, 205)
BOTTOM_DOOR_POS = (1099, 485)
PLAYER_START_X = 1000
PLAYER_START_Y = 560
TOP_DOOR_SPAWN_Y = 270
DOOR_IDLE_NAME = "Front_door_idle"
DOOR_LEAVE_PREFIX = "W_leave_"
DOOR_ENTER_PREFIX = "W_enter_"
FRIDGE_IDLE_NAME = "fridge"
FRIDGE_OPEN_NAME = "fridge_opened"
FRIDGE_FRAME_MS = 500
EGG_ICON_NORM = "I_egg_norm"
EGG_ICON_SELECTED = "I_egg_pres"
GLUE_ICON_NORM = "I_superglue_norm"
GLUE_ICON_SELECTED = "I_superglue_pres"
ARK_IDLE_NAME = "ark"
ARK_OPEN_NAME = "ark_opened"
ARK_FRAME_MS = 500
MICROWAVE_IDLE_NAME = "microwawe"
MICROWAVE_DIRTY_NAME = "microwawe_dirty"
BINOCULARS_IDLE_NAME = "binoculars_ms"
BINOCULARS_GLUED_NAME = "binoculars_glue_ms"
ARK_IDLE_NAME = "ark"
ARK_OPEN_NAME = "ark_opened"
ARK_FRAME_MS = 500
GLUE_ICON_NORM = "I_superglue_norm"
GLUE_ICON_SELECTED = "I_superglue_pres"
PLAYER_SPEED = 2
PLAYER_WALK_FRAME_MS = 160
PLAYER_WALK_FRAMES = 7
PLAYER_WALK_LEFT_PREFIX = "W_mg3_000"
PLAYER_WALK_RIGHT_PREFIX = "W_mg1_000" # да, спрайты так называются, не я придумывал
PLAYER_IDLE_LEFT_NAME = "W_ms3_0008"
PLAYER_IDLE_RIGHT_NAME = "W_ms1_0004"

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

#Загрузка кадров для анимации мебели с дверями
def load_frames(prefix, count):
    frames = []
    for i in range(count):
        frame = get_image(f"{prefix}{i}")
        if frame:
            frames.append(frame)
    return frames

def load_frames_range(prefix, start, end, pad=4):
    frames = []
    step = 1 if end >= start else -1
    for i in range(start, end + step, step):
        frame = get_image(f"{prefix}{i:0{pad}d}")
        if frame:
            frames.append(frame)
    return frames

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
    if "door_list" in globals():
        for door in door_list:
            door.draw(screen, camera_x, camera_y)
    if "furniture_list" in globals():
        for furniture in furniture_list:
            furniture.draw(screen, camera_x, camera_y)
    if "enemy" in globals():
        enemy.draw(screen, camera_x, camera_y)
    if "player" in globals() and not player.ghost:
        player.draw(screen, camera_x, camera_y)
    if gameplay_overlay_img:
        screen.blit(gameplay_overlay_img, (0, 0))
        ingame_exit_btn.draw(screen)
    minutes = timer_elapsed_ms // 60000
    seconds = (timer_elapsed_ms // 1000) % 60
    timer_text = timer_font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH-150, HEIGHT-106))
    draw_inventory()

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
    camera_y = 200
    show_name_popup = False
    name_input_active = False
    reset_buttons()

# Функции для всех экранов
def reset_buttons():
    buttons = [start_btn, exit_btn, levelmenu_btn_exit, level1_btn, start_level_btn, start_level_btn, ]
    for btn in buttons:
        btn.is_pressed = False
    level1_btn.is_selected = False

def try_start_door_transition(from_door, to_door):
    global door_transition_active, door_from, door_to
    if door_transition_active or not from_door or not to_door:
        return
    if "player" not in globals():
        return
    if player.room != from_door.from_room:
        return
    if not from_door.is_near(player.x, player.y):
        return
    door_transition_active = True
    door_from = from_door
    door_to = to_door
    player.ghost = True
    door_from.play_leave()
    door_to.play_enter()

def draw_inventory():
    if "player" not in globals():
        return
    x = INVENTORY_START_X
    y = INVENTORY_START_Y
    for i, item in enumerate(player.inventory):
        icon = item.get_icon(i == selected_item_index)
        if icon:
            screen.blit(icon, (x, y))
        x += INVENTORY_ITEM_SPACING

def handle_inventory_click(pos):
    global selected_item_index, held_item
    if "player" not in globals():
        return False
    x = INVENTORY_START_X
    y = INVENTORY_START_Y
    for i, item in enumerate(player.inventory):
        icon = item.get_icon(i == selected_item_index)
        if not icon:
            icon = item.get_icon(False)
        if icon:
            rect = icon.get_rect(topleft=(x, y))
            if rect.collidepoint(pos):
                selected_item_index = i
                held_item = item
                return True
        x += INVENTORY_ITEM_SPACING
    return False


# Создание уровня
def init_level():
    global player, enemy, furniture_list, door_list, held_item, door_top, door_bottom
    global selected_item_index
    global door_transition_active, door_from, door_to

    door_transition_active = False
    door_from = None
    door_to = None

    player_walk_left = load_frames(PLAYER_WALK_LEFT_PREFIX, PLAYER_WALK_FRAMES)
    player_walk_right = load_frames(PLAYER_WALK_RIGHT_PREFIX, PLAYER_WALK_FRAMES)
    player_idle_left = get_image(PLAYER_IDLE_LEFT_NAME)
    player_idle_right = get_image(PLAYER_IDLE_RIGHT_NAME)
    player = Player(
        x=PLAYER_START_X,
        y=PLAYER_START_Y,
        room="living_room",
        frames_left=player_walk_left,
        frames_right=player_walk_right,
        idle_left=player_idle_left,
        idle_right=player_idle_right,
        walk_frame_ms=PLAYER_WALK_FRAME_MS,
        speed=PLAYER_SPEED,
    )
    enemy_patrol = [(100, 120), (620, 120)]
    enemy = Enemy(x=100, y=120, room="hall", patrol_points=enemy_patrol)

    door_idle = get_image(DOOR_IDLE_NAME)
    door_leave_frames = load_frames_range(DOOR_LEAVE_PREFIX, 0, 8)
    door_enter_frames = load_frames_range(DOOR_ENTER_PREFIX, 14, 0)

    egg_icon_norm = get_image(EGG_ICON_NORM)
    egg_icon_selected = get_image(EGG_ICON_SELECTED)
    egg_item = Item("egg", icon_norm=egg_icon_norm, icon_selected=egg_icon_selected)

    glue_icon_norm = get_image(GLUE_ICON_NORM)
    glue_icon_selected = get_image(GLUE_ICON_SELECTED)
    glue_item = Item("glue", icon_norm=glue_icon_norm, icon_selected=glue_icon_selected)

    fridge_idle = get_image(FRIDGE_IDLE_NAME)
    fridge_open = get_image(FRIDGE_OPEN_NAME)
    fridge_use_frames = [frame for frame in [fridge_open, fridge_idle] if frame]

    ark_idle = get_image(ARK_IDLE_NAME)
    ark_open = get_image(ARK_OPEN_NAME)
    ark_use_frames = [frame for frame in [ark_open, ark_idle] if frame]

    microwave_idle = get_image(MICROWAVE_IDLE_NAME)
    microwave_dirty = get_image(MICROWAVE_DIRTY_NAME)
    binoculars_idle = get_image(BINOCULARS_IDLE_NAME)
    binoculars_glued = get_image(BINOCULARS_GLUED_NAME)

    furniture_list = [
        Furniture(
            "ark",
            x=949,
            y=490,
            room="living_room",
            items_inside=[glue_item],
            frames_idle=[ark_idle] if ark_idle else [],
            frames_use=ark_use_frames,
            anim_ms=ARK_FRAME_MS * 2,
            anchor="topleft",
        ),
        Furniture(
            "fridge",
            x=1238,
            y=175,
            room="kitchen",
            items_inside=[egg_item],
            frames_idle=[fridge_idle] if fridge_idle else [],
            frames_use=fridge_use_frames,
            anim_ms=FRIDGE_FRAME_MS * 2,
            anchor="topleft",
        ),
        Furniture(
            "microwave",
            x=880,
            y=195,
            room="kitchen",
            items_inside=[],
            frames_idle=[microwave_idle] if microwave_idle else [],
            alt_frame=microwave_dirty,
            accept_item="egg",
            anchor="topleft",
        ),
        Furniture(
            "binoculars",
            x=1324,
            y=245,
            room="kitchen",
            items_inside=[],
            frames_idle=[binoculars_idle] if binoculars_idle else [],
            alt_frame=binoculars_glued,
            accept_item="glue",
            anchor="topleft",
        ),
    ]

    door_top = Door(
        x=TOP_DOOR_POS[0],
        y=TOP_DOOR_POS[1],
        room_from="kitchen",
        to_room="living_room",
        frames_idle=[door_idle] if door_idle else [],
        frames_leave=door_leave_frames,
        frames_enter=door_enter_frames,
        anim_ms=TRANSITION_TIME_MS,
        spawn_y=TOP_DOOR_SPAWN_Y,
    )
    door_bottom = Door(
        x=BOTTOM_DOOR_POS[0],
        y=BOTTOM_DOOR_POS[1],
        room_from="living_room",
        to_room="kitchen",
        frames_idle=[door_idle] if door_idle else [],
        frames_leave=door_leave_frames,
        frames_enter=door_enter_frames,
        anim_ms=TRANSITION_TIME_MS,
        spawn_y=PLAYER_START_Y,
    )
    door_list = [door_top, door_bottom]

    held_item = None
    selected_item_index = None

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
    def __init__(self, type_name, icon_norm=None, icon_selected=None):
        self.name = type_name
        self.icon_norm = icon_norm
        self.icon_selected = icon_selected

    def get_icon(self, selected):
        if selected and self.icon_selected:
            return self.icon_selected
        return self.icon_norm

class Furniture:
    def __init__(self, name, x, y, room, items_inside=None, frames_idle=None, frames_use=None, anim_ms=800, anchor="center", alt_frame=None, accept_item=None):
        self.name = name
        self.x = x
        self.y = y
        self.room = room
        self.items_inside = items_inside or []
        self.rect = pygame.Rect(x, y, 50, 50)
        self.anim_idle = Anim(frames_idle or [], anim_ms, loop=True)
        self.anim_use = Anim(frames_use or [], anim_ms, loop=False)
        self.state = "idle"
        self.anchor = anchor
        self.pending_item = None
        self.alt_frame = alt_frame
        self.accept_item = accept_item

    def can_interact(self, player_x, player_room):
        if player_room != self.room:
            return False
        frame = self.get_frame()
        ref_x = self.x
        if frame:
            if self.anchor == "topleft":
                ref_x = self.x + frame.get_width() // 2
            elif self.anchor == "topright":
                ref_x = self.x - frame.get_width() // 2
        return abs(player_x - ref_x) <= INTERACT_RANGE_PX
    
    def take_item(self):
        if self.items_inside:
            return self.items_inside.pop()
        else:
            return None
    def apply_item(self, item):
        return False

    def update_anim(self, dt_ms):
        if self.state == "alt":
            return
        if self.state == "use":
            self.anim_use.update(dt_ms)
            if self.anim_use.is_finished():
                self.state = "idle"
                if self.pending_item and "player" in globals():
                    player.inventory.append(self.pending_item)
                    self.pending_item = None
        else:
            self.anim_idle.update(dt_ms)

    def get_frame(self):
        if self.state == "alt" and self.alt_frame:
            return self.alt_frame
        if self.state == "use":
            return self.anim_use.get_frame()
        return self.anim_idle.get_frame()

    def draw(self, surface, cam_x, cam_y):
        frame = self.get_frame()
        if not frame:
            return
        draw_x = self.x - cam_x
        draw_y = self.y - cam_y
        if self.anchor == "topleft":
            rect = frame.get_rect(topleft=(draw_x, draw_y))
        elif self.anchor == "topright":
            rect = frame.get_rect(topright=(draw_x, draw_y))
        else:
            rect = frame.get_rect(center=(draw_x, draw_y))
        surface.blit(frame, rect.topleft)

    def get_screen_rect(self, cam_x, cam_y):
        frame = self.get_frame()
        if frame:
            draw_x = self.x - cam_x
            draw_y = self.y - cam_y
            if self.anchor == "topleft":
                return frame.get_rect(topleft=(draw_x, draw_y))
            if self.anchor == "topright":
                return frame.get_rect(topright=(draw_x, draw_y))
            return frame.get_rect(center=(draw_x, draw_y))
        rect = self.rect.copy()
        rect.x -= cam_x
        rect.y -= cam_y
        return rect

    def hit_test(self, pos, cam_x, cam_y):
        return self.get_screen_rect(cam_x, cam_y).collidepoint(pos)

    def start_use(self):
        if self.state != "idle":
            return False
        if not self.items_inside:
            return False
        self.pending_item = self.items_inside.pop()
        self.state = "use"
        self.anim_use.reset()
        return True

    def apply_item(self, item):
        if not item or not self.accept_item:
            return False
        if item.name != self.accept_item:
            return False
        if not self.alt_frame:
            return False
        if self.state == "alt":
            return False
        self.state = "alt"
        return True

class Anim:
    def __init__(self, frames, duration_ms, loop=True):
        self.frames = frames or []
        self.duration_ms = max(1, duration_ms)
        self.loop = loop
        self.time_ms = 0

    def update(self, dt_ms):
        self.time_ms += dt_ms
        if self.loop:
            self.time_ms %= self.duration_ms
        else:
            if self.time_ms > self.duration_ms:
                self.time_ms = self.duration_ms

    def get_frame(self):
        if not self.frames:
            return None
        idx = int(self.time_ms / self.duration_ms * len(self.frames))
        if idx >= len(self.frames):
            idx = len(self.frames) - 1
        return self.frames[idx]

    def reset(self):
        self.time_ms = 0

    def is_finished(self):
        return (not self.loop) and self.time_ms >= self.duration_ms

class Door:
    def __init__(self, x, y, room_from, to_room, frames_idle=None, frames_leave=None, frames_enter=None, anim_ms=1200, anchor="center", spawn_y=None):
        self.x = x
        self.y = y
        self.from_room = room_from
        self.to_room = to_room
        self.rect = pygame.Rect(x-16, y-32, 32, 64)
        self.anim_idle = Anim(frames_idle or [], anim_ms, loop=True)
        self.anim_leave = Anim(frames_leave or [], anim_ms, loop=False)
        self.anim_enter = Anim(frames_enter or [], anim_ms, loop=False)
        self.state = "idle"
        self.anchor = anchor
        self.spawn_y = spawn_y
    
    def update_anim(self, dt_ms):
        if self.state == "leave":
            self.anim_leave.update(dt_ms)
        elif self.state == "enter":
            self.anim_enter.update(dt_ms)
        else:
            self.anim_idle.update(dt_ms)
    def get_frame(self):
        if self.state == "leave":
            return self.anim_leave.get_frame()
        if self.state == "enter":
            return self.anim_enter.get_frame()
        return self.anim_idle.get_frame()
    def can_enter(self, player_x, player_room):
        return player_room == self.from_room and abs(player_x - self.x) <= INTERACT_RANGE_PX

    def is_near(self, player_x, player_y):
        return abs(player_x - self.x) <= INTERACT_RANGE_PX

    def get_screen_rect(self, cam_x, cam_y):
        frame = self.get_frame()
        if frame:
            draw_x = self.x - cam_x
            draw_y = self.y - cam_y
            if self.anchor == "topleft":
                return frame.get_rect(topleft=(draw_x, draw_y))
            if self.anchor == "topright":
                return frame.get_rect(topright=(draw_x, draw_y))
            return frame.get_rect(center=(draw_x, draw_y))
        rect = self.rect.copy()
        rect.x -= cam_x
        rect.y -= cam_y
        return rect

    def hit_test(self, pos, cam_x, cam_y):
        return self.get_screen_rect(cam_x, cam_y).collidepoint(pos)

    def play_leave(self):
        self.state = "leave"
        self.anim_leave.reset()

    def play_enter(self):
        self.state = "enter"
        self.anim_enter.reset()

    def is_done(self):
        if self.state == "leave":
            return self.anim_leave.is_finished()
        if self.state == "enter":
            return self.anim_enter.is_finished()
        return False

    def set_idle(self):
        self.state = "idle"
    def draw(self, surface, cam_x, cam_y):
        frame = self.get_frame()
        if not frame:
            return
        draw_x = self.x - cam_x
        draw_y = self.y - cam_y
        if self.anchor == "topleft":
            rect = frame.get_rect(topleft=(draw_x, draw_y))
        elif self.anchor == "topright":
            rect = frame.get_rect(topright=(draw_x, draw_y))
        else:
            rect = frame.get_rect(center=(draw_x, draw_y))
        surface.blit(frame, rect.topleft)

class Player:
    def __init__(self, x, y, room, frames_left=None, frames_right=None, idle_left=None, idle_right=None, walk_frame_ms=80, speed=4, anchor="center"):
        self.x = x
        self.y = y
        self.room = room
        self.state = "idle"
        self.inventory = []
        self.sabotage_count = 0
        self.frames_left = frames_left or []
        self.frames_right = frames_right or []
        self.idle_left = idle_left
        self.idle_right = idle_right
        self.walk_frame_ms = max(1, walk_frame_ms)
        self.walk_timer = 0
        self.walk_index = 0
        self.facing = "right"
        self.moving = False
        self.speed = speed
        self.anchor = anchor
        self.ghost = False

    def screen_pos(self, cam_x, cam_y):
        return int(self.x - cam_x), int(self.y - cam_y)

    def update_walk(self, keys, dt_ms):
        if self.ghost:
            self.moving = False
            return
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]

        dx = 0
        direction = None
        if left and not right:
            dx = -self.speed
            direction = "left"
        elif right and not left:
            dx = self.speed
            direction = "right"

        if direction and direction != self.facing:
            self.facing = direction
            self.walk_index = 0
            self.walk_timer = 0

        self.moving = direction is not None
        if self.moving:
            self.walk_timer += dt_ms
            if self.walk_timer >= self.walk_frame_ms:
                self.walk_timer %= self.walk_frame_ms
                frames = self.frames_left if self.facing == "left" else self.frames_right
                if frames:
                    self.walk_index = (self.walk_index + 1) % len(frames)
        else:
            self.walk_index = 0
            self.walk_timer = 0

        self.x += dx

    def get_frame(self):
        if not self.moving:
            if self.facing == "left" and self.idle_left:
                return self.idle_left
            if self.facing == "right" and self.idle_right:
                return self.idle_right
        frames = self.frames_left if self.facing == "left" else self.frames_right
        if not frames:
            frames = self.frames_right if self.frames_left else self.frames_left
        if not frames:
            return None
        if self.walk_index >= len(frames):
            self.walk_index = 0
        return frames[self.walk_index]

    def draw(self, surface, cam_x, cam_y):
        frame = self.get_frame()
        if not frame:
            return
        sx, sy = self.screen_pos(cam_x, cam_y)
        if self.anchor == "topleft":
            rect = frame.get_rect(topleft=(sx, sy))
        elif self.anchor == "topright":
            rect = frame.get_rect(topright=(sx, sy))
        else:
            rect = frame.get_rect(center=(sx, sy))
        surface.blit(frame, rect.topleft)

class Enemy:
    def __init__(self, x, y, room, patrol_points, frames_idle=None, anim_ms=800, anchor="center"):
        self.x = x
        self.y = y
        self.room = room
        self.patrol = patrol_points[:]  # список (x,y) точек
        self.patrol_i = 0
        self.state = "patrol"  # patrol, transition, ghost, inspecting
        self.ghost = False
        self.anim_idle = Anim(frames_idle or [], anim_ms, loop=True)
        self.anchor = anchor

    def update_anim(self, dt_ms):
        self.anim_idle.update(dt_ms)

    def get_frame(self):
        return self.anim_idle.get_frame()

    def draw(self, surface, cam_x, cam_y):
        frame = self.get_frame()
        if not frame:
            return
        draw_x = int(self.x - cam_x)
        draw_y = int(self.y - cam_y)
        if self.anchor == "topleft":
            rect = frame.get_rect(topleft=(draw_x, draw_y))
        elif self.anchor == "topright":
            rect = frame.get_rect(topright=(draw_x, draw_y))
        else:
            rect = frame.get_rect(center=(draw_x, draw_y))
        surface.blit(frame, rect.topleft)

start_btn = ImageButton("startgamebtn", WIDTH // 2, 400, start_game)
exit_btn = ImageButton("exitgamebtn", WIDTH // 2, 480, exit_game)

# Levelmenu элементы
levelmenu_btn_exit = ImageButton("levelmenuexitbtn", WIDTH - 748, HEIGHT - 43, level_menu_exit)
level1_btn = ImageButton("level1btn", WIDTH // 2 - 325, 118, lambda: select_level("Level 1"))
start_level_btn = ImageButton("levelmenustartbtn", WIDTH - 53, HEIGHT - 43, open_name_popup, is_active=False)

#Ingame элементы
ingame_exit_btn = ImageButton("ingameexitbtn", WIDTH - 34, HEIGHT - 91, level_menu_exit)

while running:
    dt_ms = clock.get_time()
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if handle_inventory_click(event.pos):
                    pass
                elif "door_top" in globals() and "door_bottom" in globals():
                    if door_top.hit_test(event.pos, camera_x, camera_y):
                        try_start_door_transition(door_top, door_bottom)
                    elif door_bottom.hit_test(event.pos, camera_x, camera_y):
                        try_start_door_transition(door_bottom, door_top)
                if "furniture_list" in globals() and "player" in globals() and not door_transition_active:
                    for furniture in furniture_list:
                        if not furniture.hit_test(event.pos, camera_x, camera_y):
                            continue
                        if not furniture.can_interact(player.x, player.room):
                            continue
                        if held_item and furniture.apply_item(held_item):
                            if selected_item_index is not None and 0 <= selected_item_index < len(player.inventory):
                                player.inventory.pop(selected_item_index)
                            selected_item_index = None
                            held_item = None
                            break
                        if furniture.name in ("fridge", "ark"):
                            if furniture.start_use():
                                break
            if event.type == pygame.KEYDOWN:
                if "door_top" in globals() and "door_bottom" in globals():
                    if event.key == pygame.K_UP:
                        try_start_door_transition(door_top, door_bottom)
                    elif event.key == pygame.K_DOWN:
                        try_start_door_transition(door_bottom, door_top)

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
        if "door_list" in globals():
            for door in door_list:
                door.update_anim(dt_ms)
        if "furniture_list" in globals():
            for furniture in furniture_list:
                furniture.update_anim(dt_ms)
        if "player" in globals() and not door_transition_active:
            keys = pygame.key.get_pressed()
            player.update_walk(keys, dt_ms)
        if "enemy" in globals():
            enemy.update_anim(dt_ms)
        if door_transition_active and door_from and door_to:
            if door_from.is_done() and door_to.is_done():
                player.x = door_to.x
                player.y = door_to.spawn_y if door_to.spawn_y is not None else door_to.y
                player.room = door_to.from_room
                player.ghost = False
                door_from.set_idle()
                door_to.set_idle()
                door_transition_active = False
                door_from = None
                door_to = None
    
    if current_screen == "main_menu":
        draw_main_menu()
    elif current_screen == "level_menu":
        draw_level_menu()
    elif current_screen == "gameplay":
        draw_gameplay()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


