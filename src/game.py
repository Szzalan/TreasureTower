import copy
import math

import pygame

from assets.button import Button
import random

from assets.player import Player
from assets.enemy import Enemy
from assets.items import Item
from assets.healthbar import HealthBar
from assets.playerstate import PlayerState
import combat

pygame.init()
clock = pygame.time.Clock()

floor_number = 1
FLOOR_WIDTH = 500
FLOOR_HEIGHT = 500
NUM_ROOMS = 5
player_state = PlayerState(150,0,potion_amount=3)

class GameStates:
    EXPLORATION = "exploration"
    COMBAT = "combat"

def return_to_exploration(screen,main_menu, saved_dungeon_map=None, enemy_metadata=None):
    print("Returning to exploration mode!")
    if saved_dungeon_map and enemy_metadata:
        game(screen,main_menu,saved_dungeon_map,enemy_metadata)

    else:# Launch the appropriate game/exploration logic
        print("Error: No saved dungeon map or enemy metadata!")

def load_dungeon(saved_dungeon_map, enemy_metadata):
    if saved_dungeon_map is None:
        raise ValueError("No saved dungeon map found.")
    enemy_group = pygame.sprite.Group()
    player_spawn = None
    for enemy_data in enemy_metadata['enemies']:
        spawn_x = enemy_data['x']
        spawn_y = enemy_data['y']
        enemy_type = enemy_data['type']
        killed = enemy_data['killed']
        spawned = enemy_data['spawned']
        if not killed:
            enemy = Enemy(spawn_y, spawn_x, enemy_type)
            enemy_group.add(enemy)
        elif killed and not spawned:
            player_spawn = (spawn_x,spawn_y)
            enemy_data['spawned'] = True
    floor_list, wall_list, _ = sort_tile_types(saved_dungeon_map)
    entity_pos = copy.deepcopy(enemy_metadata)
    return player_spawn,enemy_group,entity_pos

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
        entity_positions['enemies'].append({'x': spawn_x, 'y': spawn_y, 'type': enemy_type, 'killed': False, 'spawned': False})

    return player_spawn, enemy_group, entity_positions

def door_message(screen,message):
    if message:
        font = pygame.font.Font("../assets/Pixeltype.ttf",36)
        text_surf = font.render(message,False,(255,255,255))
        text_rect = text_surf.get_rect(center=(screen.get_width()/2,650))
        screen.blit(text_surf,text_rect)

def door_interact(door_spawn,player_pos,event,enemy_group):
    adjacent_positions = [
        (door_spawn[0] + 1, door_spawn[1]),  # Right
        (door_spawn[0] - 1, door_spawn[1]),  # Left
        (door_spawn[0], door_spawn[1] + 1),  # Down
        (door_spawn[0], door_spawn[1] - 1)  # Up
    ]
    if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
        if player_pos in adjacent_positions:
            if len(enemy_group) > 0:
                return "Kill all enemies to progress to the next floor"
            else:
                return True
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
    if dungeon_map is None or len(dungeon_map) == 0:
        print("Error: dungeon_map is empty or None in generate_dungeon_surface.")
        return None
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

def game(screen, main_menu,dungeon_map = None,enemy_metadata = None):
    gold = Item(410,5,"Gold")
    potion = Item(410,25,"Potion")
    global player_state, floor_number
    health_bar_player = HealthBar(50, 50, 200, 15,150,player_state.current_health)
    font = pygame.font.Font("../assets/Pixeltype.ttf", 20)
    number_of_floors = pygame.font.Font("../assets/Pixeltype.ttf", 50).render(f"Floor: {floor_number}", False, (255, 255, 255))
    message = ""
    message_duration = 0
    Room.load_images()
    if dungeon_map is None:
        dungeon_map,rooms,player_spawn,enemy_group,entity_pos = dungeon_generator()
    else:
        player_spawn, enemy_group, entity_pos = load_dungeon(dungeon_map,enemy_metadata)
    player_start = player_spawn
    player = Player(player_start[1] * 16, player_start[0] * 16, 16, 16)
    dungeon_surface = generate_dungeon_surface(dungeon_map)
    saved_dungeon_map = copy.deepcopy(dungeon_map)
    state = GameStates.EXPLORATION
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    running = True
    while running:
        potions_amount = pygame.font.Font("../assets/Pixeltype.ttf", 50).render(f"{player_state.potion_amount}", False, (255, 255, 255))
        potions_text_x = potion.rect.left - 50
        potions_text_y = potion.rect.centery - 10
        gold_amount = pygame.font.Font("../assets/Pixeltype.ttf", 50).render(f"{player_state.gold}", False, (255, 255, 255))
        gold_text_x = gold.rect.left - 50
        gold_text_y = gold.rect.centery - 10
        health_bar_player.hp = player_state.current_health
        current_time = pygame.time.get_ticks()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(event.pos):
                    main_menu()
                    running = False
                if potion.rect.collidepoint(event.pos):
                    if player_state.potion_amount > 0:
                        player_state.potion_amount -= 1
                        potion.use(player_state)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                player.move(16,16,dungeon_map,event)
                door_result = door_interact(entity_pos['door'], (player.y // 16, player.x // 16),event,enemy_group)
                if isinstance(door_result, str):
                    message = door_result
                    message_duration = current_time + 2000
                elif door_result:
                    floor_number += 1
                    message = ""
                    print("Proceeding to the next floor...")
                    dungeon_map = None  # Clear the current dungeon map
                    saved_dungeon_map = None
                    enemy_metadata = None
                    dungeon_surface = None
                    game(screen, main_menu)  # Restart the game function to regenerate the dungeon
                    return  # Exit the current loop to avoid conflicting with the new game call

            if state == GameStates.EXPLORATION:
                for enemy in enemy_group:
                    if enemy.interact(event,player):
                        state = GameStates.COMBAT
                        current_enemy = enemy
                        result = combat.combat(screen,main_menu,current_enemy.enemy_type,player_state)
                        if result == "ENEMY_DEFEATED":
                            for enemy_data in entity_pos['enemies']:
                                if enemy_data['x'] == current_enemy.y and enemy_data['y'] == current_enemy.x:
                                    enemy_data['killed'] = True
                            return_to_exploration(screen, main_menu,saved_dungeon_map,entity_pos)
                            current_enemy.kill()
                        break
        player.animation_loop()
        draw_dungeon(screen, dungeon_surface)
        enemy_group.update(current_time)
        for enemy in enemy_group:
            screen.blit(enemy.image, (((enemy.x * 16) + offset_x), (enemy.y * 16) + offset_y))
        back_button.draw(screen)
        screen.blit(player.current_frame, (player.x + offset_x, player.y + offset_y))
        if message and current_time <= message_duration:
            door_message(screen, message)
        health_bar_player.draw(screen)
        health_bar_player.health_value_display(screen, font)
        screen.blit(number_of_floors, (screen.get_width()/2-number_of_floors.get_width()/2, screen.get_height()/2-300))
        screen.blit(gold.image,gold.rect.topleft)
        screen.blit(potions_amount, (potions_text_x, potions_text_y))
        screen.blit(gold_amount, (gold_text_x, gold_text_y))
        screen.blit(potion.image,potion.rect.topleft)
        pygame.display.flip()
        clock.tick(60)