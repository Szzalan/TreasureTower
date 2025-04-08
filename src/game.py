import math

import pygame

from assets.button import Button
import random

from assets.dice import Dice
from assets.player import Player
from assets.enemy import Enemy
import combat

pygame.init()
clock = pygame.time.Clock()

FLOOR_WIDTH = 500
FLOOR_HEIGHT = 500
NUM_ROOMS = 5

class GameStates:
    EXPLORATION = "exploration"
    COMBAT = "combat"
def return_to_exploration(screen,main_menu):
    print("Returning to exploration mode!")
    # Set the game state to exploration
    current_state = GameStates.EXPLORATION

    # Launch the appropriate game/exploration logic
    game(screen,main_menu)  # If "game()" is the main loop managing exploration


def entity_spawner(dungeon_map,enemy_types):
    """SPAWNS THE ENTITIES IN THE DUNGEON"""
    enemy_group = pygame.sprite.Group()
    entity_positions = {'trapdoor' : None, 'door' : None, 'enemies': []}
    floor_list, wall_list, _ = sort_tile_types(dungeon_map)

    player_spawn = random.choice(floor_list)
    trapdoor_pos = player_spawn
    dungeon_map[player_spawn[0]][player_spawn[1]] = "TRAPDOOR"
    entity_positions['trapdoor'] = trapdoor_pos

    door_spawn = random.choice(wall_list)
    dungeon_map[door_spawn[0]][door_spawn[1]] = "DOOR"

    entity_positions['door'] = door_spawn
    floor_list.remove(player_spawn)

    for _ in range(NUM_ROOMS):

        spawn_x, spawn_y = random.choice(floor_list)
        enemy_type = random.choice(enemy_types)
        enemy = Enemy(spawn_y,spawn_x,enemy_type)
        enemy_group.add(enemy)
        floor_list.remove((spawn_x,spawn_y))
        entity_positions['enemies'].append((spawn_x,spawn_y))

    return player_spawn, enemy_group, entity_positions

def door_interact(door_spawn,player_pos,event):
    adjacent_positions = [
        (door_spawn[0] + 1, door_spawn[1]),  # Right
        (door_spawn[0] - 1, door_spawn[1]),  # Left
        (door_spawn[0], door_spawn[1] + 1),  # Down
        (door_spawn[0], door_spawn[1] - 1)  # Up
    ]
    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
        if player_pos in adjacent_positions:
            print("Door opened!")
            return True
    else:
        return False


def sort_tile_types(dungeon_map):
    floor_list = []
    wall_list = []
    corner_list = []

    for y,row in enumerate(dungeon_map):
        for x,tile in enumerate(row):
            if tile == "WALL":
                if ((dungeon_map[y][x-1] == "WALL" or dungeon_map[y][x+1] == "WALL")
                    and (dungeon_map[y-1][x] == "WALL" or dungeon_map[y+1][x] == "WALL")):
                    corner_list.append((y,x))
                else:
                    wall_list.append((y,x))
            elif tile == "FLOOR":
                floor_list.append((y,x))

    return floor_list, wall_list, corner_list

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    TILE = None
    WALL = None
    TRAPDOOR = None
    DOOR = None

    @classmethod
    def load_images(cls):
        cls.TILE = pygame.image.load("../assets/map_assets/dongeonWallFloorTransparent1.png").convert_alpha()
        cls.WALL = pygame.image.load("../assets/map_assets/dongeonWallFloorTransparent10.png").convert_alpha()
        cls.TRAPDOOR = pygame.image.load("../assets/trapdoor.png").convert_alpha()
        cls.DOOR = pygame.image.load("../assets/door.png").convert_alpha()

    def center(self):
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return center_x, center_y

    def check_overlap(self,other_room):
        tile_width = Room.TILE.get_width()
        tile_height = Room.TILE.get_height()

        return (
            self.x // tile_width < (other_room.x + other_room.width) // tile_width
            and (self.x + self.width) // tile_width > other_room.x // tile_width
            and self.y // tile_height < (other_room.y + other_room.height) // tile_height
            and (self.y + self.height) // tile_height > other_room.y // tile_height
                    )

def generate_rooms(floor_width, floor_height,num_rooms):
    rooms = []
    tile_width = Room.TILE.get_width()
    min_room_size = tile_width * 3
    max_room_size = tile_width * 5
    buffer = 1 * tile_width

    for i in range(num_rooms):
        room_width = random.randint(min_room_size, max_room_size)
        room_height = random.randint(min_room_size, max_room_size)
        room_x = random.randint(buffer, floor_width - room_width - buffer)
        room_y = random.randint(buffer, floor_height - room_height - buffer)
        new_room = Room(room_x, room_y, room_width, room_height)

        if all(not new_room.check_overlap(other_room) for other_room in rooms):
            rooms.append(new_room)
    return rooms

def carve_rooms(room_list, dungeon_map):
    tile_width = Room.TILE.get_width()
    tile_height = Room.TILE.get_height()

    for room in room_list:
        for y in range(room.y // tile_height,(room.y+room.height) // tile_height):
            for x in range(room.x // tile_width, (room.x + room.width) // tile_width):
                dungeon_map[y][x] = "FLOOR"

def carve_corridors(rooms,dungeon_map):
    for i in range(len(rooms) - 1):
        room_a = rooms[i]
        room_b = rooms[i + 1]
        tile_width = Room.TILE.get_width()
        tile_height = Room.TILE.get_height()
        center_a = (room_a.center()[0] // tile_width, room_a.center()[1] // tile_height)
        center_b = (room_b.center()[0] // tile_width, room_b.center()[1] // tile_height)

        for x in range(min(center_a[0], center_b[0]), max(center_a[0], center_b[0]) + 1):
            if dungeon_map[center_a[1]][x] == "WALL":
                dungeon_map[center_a[1]][x] = "CORRIDOR"

        for y in range(min(center_a[1], center_b[1]), max(center_a[1], center_b[1]) + 1):
            if dungeon_map[y][center_b[0]] == "WALL":
                dungeon_map[y][center_b[0]] = "CORRIDOR"

def create_empty_map(map_width, map_height):
    return [["WALL" for x in range(map_width)] for _ in range(map_height)]

def rotate_walls(dungeon_map,x ,y):
    map_height = len(dungeon_map)
    map_width = len(dungeon_map[0])

    def is_wall(x,y):
        if 0 <= x < map_width and 0 <= y < map_height:
            return dungeon_map[y][x] == "WALL" or dungeon_map[y][x] == "DOOR"
        return False

    def is_floor_or_corridor(x,y):
        if 0 <= x < map_width and 0 <= y < map_height:
            return (dungeon_map[y][x] == "FLOOR" or dungeon_map[y][x] == "CORRIDOR"
                    or dungeon_map[y][x] == "TRAPDOOR")
        return False

    top = is_wall(x, y - 1)
    bottom = is_wall(x, y + 1)
    right = is_floor_or_corridor(x + 1, y)
    left = is_floor_or_corridor(x - 1, y)

    if top and bottom and left:
        return "right_turn"
    elif top and bottom and right:
        return "left_turn"
    else:
        return "wall"

def generate_dungeon_surface(dungeon_map):
    tile_width = Room.TILE.get_width()
    tile_height = Room.TILE.get_height()
    dungeon_width = len(dungeon_map[0])
    dungeon_height = len(dungeon_map)
    dungeon_surf = pygame.Surface((dungeon_width, dungeon_height), pygame.SRCALPHA)

    for y, row in enumerate(dungeon_map):
        for x, tile_type in enumerate(row):
            x_pixel_pos = x * tile_width
            y_pixel_pos = y * tile_height
            if tile_type == "WALL":
                wall_rotation = rotate_walls(dungeon_map,x,y)
                if wall_rotation == "right_turn":
                    rotated_wall = pygame.transform.rotate(Room.WALL, -90)
                    dungeon_surf.blit(rotated_wall, (x_pixel_pos, y_pixel_pos))
                elif wall_rotation == "left_turn":
                    rotated_wall = pygame.transform.rotate(Room.WALL, 90)
                    dungeon_surf.blit(rotated_wall, (x_pixel_pos, y_pixel_pos))
                else:
                    dungeon_surf.blit(Room.WALL, (x_pixel_pos, y_pixel_pos))
            elif tile_type == "DOOR":
                wall_rotation = rotate_walls(dungeon_map,x,y)
                if wall_rotation == "right_turn":
                    rotated_wall = pygame.transform.rotate(Room.DOOR, -90)
                    dungeon_surf.blit(rotated_wall, (x_pixel_pos, y_pixel_pos))
                elif wall_rotation == "left_turn":
                    rotated_wall = pygame.transform.rotate(Room.DOOR, 90)
                    dungeon_surf.blit(rotated_wall, (x_pixel_pos, y_pixel_pos))
                else:
                    dungeon_surf.blit(Room.DOOR, (x_pixel_pos, y_pixel_pos))
            elif tile_type == "FLOOR":
                dungeon_surf.blit(Room.TILE, (x_pixel_pos, y_pixel_pos))
            elif tile_type == "CORRIDOR":
                dungeon_surf.blit(Room.TILE, (x_pixel_pos, y_pixel_pos))
            elif tile_type == "TRAPDOOR":
                dungeon_surf.blit(Room.TRAPDOOR, (x_pixel_pos, y_pixel_pos))
    return dungeon_surf

def draw_dungeon(screen, dungeon_surf):
    dungeon_width = dungeon_surf.get_width()
    dungeon_height = dungeon_surf.get_height()
    global offset_x, offset_y

    screen_width, screen_height = screen.get_size()

    offset_x = (screen_width - dungeon_width) // 2
    offset_y = (screen_height - dungeon_height) // 2

    screen.blit(dungeon_surf, (offset_x, offset_y))

def update_wall_boundaries(dungeon_map):
    map_height = len(dungeon_map)
    map_width = len(dungeon_map[0])
    new_map = [["EMPTY" for _ in range(map_width)] for _ in range(map_height)]

    for y in range(map_height):
        for x in range(map_width):
            if dungeon_map[y][x] in ["FLOOR", "CORRIDOR"]:
                new_map[y][x] = dungeon_map[y][x]
                for dy in [-1, 0,1]:
                    for dx in [-1, 0,1]:
                        neighbor_x = x + dx
                        neighbor_y = y + dy

                        if 0 <= neighbor_x < map_width and 0 <= neighbor_y < map_height:
                            if dungeon_map[neighbor_y][neighbor_x] == "WALL":
                                new_map[neighbor_y][neighbor_x] = "WALL"
    return new_map

def dungeon_generator():
    dungeon_map = create_empty_map(FLOOR_WIDTH, FLOOR_HEIGHT)
    rooms = generate_rooms(FLOOR_WIDTH, FLOOR_HEIGHT, NUM_ROOMS)
    carve_rooms(rooms, dungeon_map)
    carve_corridors(rooms, dungeon_map)
    dungeon_map = update_wall_boundaries(dungeon_map)
    player_spawn,enemy_group,entity_positions = entity_spawner(dungeon_map,["slime","skeleton","zombie"])

    return dungeon_map,rooms,player_spawn,enemy_group,entity_positions

def game(screen, main_menu):
    Room.load_images()
    dungeon_map,rooms,player_spawn,enemy_group,entity_pos = dungeon_generator()
    dungeon_surface = generate_dungeon_surface(dungeon_map)
    state = GameStates.EXPLORATION

    dice = Dice(screen.get_width()/2, 350)
    all_sprites = pygame.sprite.Group(dice)
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    roll_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 60),"Roll")
    player_start = player_spawn
    player = Player(player_start[1] * 16, player_start[0] * 16,16,16)
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    main_menu()
                    running = False

                if roll_button.rect.collidepoint(event.pos):
                    dice.roll_dice_start()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                player.move(16,16,dungeon_map,event)
                door_interact(entity_pos['door'], (player.y // 16, player.x // 16),event)

            if state == GameStates.EXPLORATION:
                for enemy in enemy_group:
                    if enemy.interact(event,player):
                        state = GameStates.COMBAT
                        current_enemy = enemy
                        result = combat.combat(screen,main_menu,current_enemy.enemy_type)
                        if result == "ENEMY_DEFEATED":
                            return_to_exploration(screen, main_menu)
                            current_enemy.kill()
                        break
        player.animation_loop()
        draw_dungeon(screen, dungeon_surface)
        enemy_group.update(current_time)
        for enemy in enemy_group:
            screen.blit(enemy.image, (((enemy.x * 16) + offset_x), (enemy.y * 16) + offset_y))
        all_sprites.update()
        all_sprites.draw(screen)
        roll_button.draw(screen)
        back_button.draw(screen)
        screen.blit(player.current_frame, (player.x + offset_x, player.y + offset_y))
        pygame.display.flip()
        clock.tick(60)