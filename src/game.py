import math

import pygame
from assets.button import Button
import random

from assets.dice import Dice
import assets.spritesheet as spritesheet

pygame.init()
clock = pygame.time.Clock()

FLOOR_WIDTH = 500
FLOOR_HEIGHT = 500
NUM_ROOMS = 5

def entity_spawner(dungeon_map):
    wall_list = []
    floor_list = []
    for y,row in enumerate(dungeon_map):
        if "WALL" in row:
            wall_list.append((y,row.index("WALL")))
        if "FLOOR" in row:
            floor_list.append((y,row.index("FLOOR")))
    player_spawn = random.choice(floor_list)
    dungeon_map[player_spawn[0]][player_spawn[1]] = "TRAPDOOR"

def move_player(player, dx, dy, event):
    if event.key == pygame.K_w:
        player.x += dx
    elif event.key == pygame.K_a:
        player.y -= dy
    elif event.key == pygame.K_s:
        player.x -= dx
    elif event.key == pygame.K_d:
        player.y += dy

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    TILE = None
    WALL = None

    @classmethod
    def load_images(cls):
        cls.TILE = pygame.image.load("../assets/map_assets/dongeonWallFloorTransparent1.png").convert_alpha()
        cls.WALL = pygame.image.load("../assets/map_assets/dongeonWallFloorTransparent10.png").convert_alpha()

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

    for i in range(num_rooms):
        room_width = random.randint(min_room_size, max_room_size)
        room_height = random.randint(min_room_size, max_room_size)
        room_x = random.randint(0, floor_width - room_width)
        room_y = random.randint(0, floor_height - room_height)
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
            return dungeon_map[y][x] == "WALL"
        return False

    def is_floor_or_corridor(x,y):
        if 0 <= x < map_width and 0 <= y < map_height:
            return dungeon_map[y][x] == "FLOOR" or dungeon_map[y][x] == "CORRIDOR"
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
            elif tile_type == "FLOOR":
                dungeon_surf.blit(Room.TILE, (x_pixel_pos, y_pixel_pos))
            elif tile_type == "CORRIDOR":
                dungeon_surf.blit(Room.TILE, (x_pixel_pos, y_pixel_pos))
            elif tile_type == "TRAPDOOR":
                dungeon_surf.blit(Room.TILE, (x_pixel_pos, y_pixel_pos))
    return dungeon_surf

def draw_dungeon(screen, dungeon_surf):
    dungeon_width = dungeon_surf.get_width()
    dungeon_height = dungeon_surf.get_height()

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
    entity_spawner(dungeon_map)

    return dungeon_map,rooms

def game(screen, main_menu):
    Room.load_images()
    dungeon_map,rooms = dungeon_generator()
    dungeon_surface = generate_dungeon_surface(dungeon_map)
    sprite_sheet_image = pygame.image.load("../assets/player_sheet.png").convert_alpha()
    sprite_sheet = spritesheet.HandleSpriteSheet(sprite_sheet_image)
    right_frame_idle = sprite_sheet.get_image(0,0,16,16,offset_v=8)
    left_frame_idle = sprite_sheet.get_image(1,0,16,16,offset_v=8)
    back_frame_idle = sprite_sheet.get_image(2,0,16,16,offset_v=8)
    front_frame_idle = sprite_sheet.get_image(3,0,16,16,offset_v=8)
    right_frame_run_1 = sprite_sheet.get_image(0,1,16,16,offset_v=8)
    right_frame_run_2 = sprite_sheet.get_image(1,1,16,16,offset_v=8)
    left_frame_run_1 = sprite_sheet.get_image(2,1,16,16,offset_v=8)
    left_frame_run_2 = sprite_sheet.get_image(3,1,16,16,offset_v=8)
    back_frame_run_1 = sprite_sheet.get_image(0,2,16,16,offset_v=8)
    back_frame_run_2 = sprite_sheet.get_image(1,2,16,16,offset_v=8)
    front_frame_run_1 = sprite_sheet.get_image(2,2,16,16,offset_v=8)
    front_frame_run_2 = sprite_sheet.get_image(3,2,16,16,offset_v=8)
    trapdoor = pygame.image.load("../assets/trapdoor.png").convert_alpha()

    dice = Dice(screen.get_width()/2, 350)
    all_sprites = pygame.sprite.Group(dice)
    back_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 120),"Back")
    roll_button = Button((screen.get_width() / 2, screen.get_height() / 2 + 60),"Roll")
    running = True
    while running:
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
                if event.key == pygame.K_w:
                    pass
                if event.key == pygame.K_a:
                    pass
                if event.key == pygame.K_s:
                    pass
                if event.key == pygame.K_d:
                    pass

        draw_dungeon(screen, dungeon_surface)
        all_sprites.update()
        all_sprites.draw(screen)
        roll_button.draw(screen)
        back_button.draw(screen)
        screen.blit(trapdoor,(100,100))
        screen.blit(back_frame_idle,(0,0))
        pygame.display.flip()
        clock.tick(60)