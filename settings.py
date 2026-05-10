import os
import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

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
score_font = pygame.font.Font(None, 32)
leaderboard_font = pygame.font.Font(None, 28)
leaderboard_db = None
player_name = ""
show_name_popup = False
name_input_active = False
selected_item_index = None
binoculars_obj = None
microwave_obj = None
sabotage_glue_done = False
sabotage_microwave_done = False
victory_start_ms = None
victory_anim_start_ms = None
timer_paused = False
score = 0
level_start_ms = None
defeat_active = False
defeat_start_ms = None
sabotage_scores = {"glue": None, "microwave": None}
victory_saved = False
MAX_NAME_LEN = 16
name_font = pygame.font.Font(None, 58)
NAME_TEXT_POS = (295, 408)
DEBUG_ROOMS = False
ROOM_COLORS = {
    "living_room": (255, 0, 0),
    "hall": (0, 255, 0),
    "kitchen": (0, 0, 255),
}
ROOMS = {
    "living_room": pygame.Rect(420, 380, 760, 250),
    "hall": pygame.Rect(120, 100, 700, 260),
    "kitchen": pygame.Rect(880, 100, 420, 260),
}
TRANSITION_TIME_MS = 1500 # столько мс персонажи переходят между комнатами
INTERACT_RANGE_PX = 60 # погрешность от мебели для взаимодействия
INVENTORY_START_X = 180
INVENTORY_START_Y = 536
INVENTORY_ITEM_SPACING = 80
SCORE_LIST_POS = (WIDTH - 145, HEIGHT - 65)
SCORE_LIST_SPACING = 24
SCORE_TOTAL_POS = (WIDTH - 49, HEIGHT - 63)
SCORE_SABOTAGE_POS = (WIDTH - 49, HEIGHT - 30)
LEADERBOARD_TEXT_POS = (200, 180)
LEADERBOARD_LINE_SPACING = 28
LEADERBOARD_BACK_POS = (40, 30)
LEADERBOARD_BG_NAME = "leaderboard"
LEADERBOARD_BTN_NAME = "leaderboardbtn"
ARROW_BACK_NAME = "arrow_back"
ARROW_BACK_HOVER_NAME = "arrow_back_hover"
TOP_DOOR_POS = (1090, 205)
BOTTOM_DOOR_POS = (1099, 485)
PLAYER_START_X = 1000
PLAYER_START_Y = 560
TOP_DOOR_SPAWN_Y = 270
DOOR_IDLE_NAME = "Front_door_idle"
DOOR_LEAVE_PREFIX = "W_leave_"
DOOR_ENTER_PREFIX = "W_enter_"
DOOR_IDLE_HOVER_NAME = "Front_door_idle_hover"
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
FRIDGE_HOVER_NAME = "fridge_hover"
ARK_HOVER_NAME = "ark_hover"
MICROWAVE_HOVER_NAME = "microwawe_hover"
BINOCULARS_HOVER_NAME = "binoculars_ms_hover"
HALL_DOOR_POS = (830, 160)
KITCHEN_DOOR_POS = (846, 160)
HALL_DOOR_IDLE_NAME = "door_left_idle"
KITCHEN_DOOR_IDLE_NAME = "door_right_idle"
HALL_DOOR_EXIT_PREFIX = "N_enter_"
KITCHEN_DOOR_ENTER_PREFIX = "N_enterr_"
ENEMY_SPEED = 12
ENEMY_HALL_POINT_X = 600
ENEMY_KITCHEN_POINT_X = 1180
ENEMY_HALL_Y = 280
ENEMY_KITCHEN_Y = 280
ENEMY_DOOR_RANGE_PX = 10
ENEMY_WALK_RIGHT_PREFIX = "N_mg1_000"
ENEMY_WALK_LEFT_PREFIX = "N_mg3_000"
ENEMY_WALK_FRAMES = 8
ENEMY_WALK_FRAME_MS = 200
ENEMY_IDLE_RIGHT_NAME = "N_ms1_0004"
ENEMY_IDLE_LEFT_NAME = "N_ms3_0008"
ENEMY_PEEP_PREFIX = "N_peep_"
ENEMY_PEEP_FRAMES = 31
ENEMY_PEEP_FRAME_MS = 150
ENEMY_PEEP_GLUED_PREFIX = "N_peep_glued_"
ENEMY_PEEP_GLUED_START = 1
ENEMY_PEEP_GLUED_END = 44
ENEMY_SHOUT_PREFIX = "N_shout2_"
ENEMY_SHOUT_FRAMES = 10
ENEMY_SHOUT_FRAME_MS = 80
ENEMY_SHOUT_PAUSE_MS = 1000
ENEMY_USE_MID_PREFIX = "N_use_mid_"
ENEMY_USE_MID_FRAMES = 14
ENEMY_USE_MID_FRAME_MS = 80
ENEMY_HALL_WAIT_MS = 10000
ENEMY_BINOCULARS_OFFSET_X = 40
ENEMY_MICROWAVE_RANGE_PX = 10
ENEMY_PUNCH_PREFIX = "N_punch_"
ENEMY_PUNCH_FRAMES = 11
ENEMY_PUNCH_FRAME_MS = 80
ENEMY_PUNCH_LOOPS = 3
PLAYER_VICTORY_PREFIX = "W_triumph_"
PLAYER_VICTORY_FRAMES = 31
PLAYER_VICTORY_FRAME_MS = 120
VICTORY_LOCK_MS = 4000
VICTORY_EXIT_MS = 6000
SCORE_BASE = 100
DEFEAT_DISTANCE_PX = 20
DEFEAT_EXIT_MS = 3000
PLAYER_SPEED = 16
PLAYER_WALK_FRAME_MS = 100
PLAYER_WALK_FRAMES = 7
PLAYER_WALK_LEFT_PREFIX = "W_mg3_000"
PLAYER_WALK_RIGHT_PREFIX = "W_mg1_000" # да, спрайты так называются, не я придумывал
PLAYER_IDLE_LEFT_NAME = "W_ms3_0008"
PLAYER_IDLE_RIGHT_NAME = "W_ms1_0004"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "resources", "images")