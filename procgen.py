from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap

import tile_types

if TYPE_CHECKING:
  from entity import Entity

class Room:
  def __init__(self, x: int, y: int, width: int, height: int):
    self.x1 = x
    self.y1 = y
    self.x2 = x + width
    self.y2 = y + height

  @property
  def center(self) -> Tuple[int, int]:
    center_x = int((self.x1 + self.x2) / 2)
    center_y = int((self.y1 + self.y2) / 2)

    return center_x, center_y

  @property
  def inner(self) -> Tuple[slice, slice]:
    return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

  def intersect(self, other_room: Room) -> bool:
    return (
      self.x1 <= other_room.x2
      and self.x2 >= other_room.x1
      and self.y1 <= other_room.y2
      and self.y2 >= other_room.y1
    )


def generate_dungeon(
    room_max_number: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity
  ) -> GameMap:
  dungeon = GameMap(map_width, map_height)

  rooms: List[Room] = []

  for r in range(room_max_number):
    room_width = random.randint(room_min_size, room_max_size)
    room_height = random.randint(room_min_size, room_max_size)

    x = random.randint(0, dungeon.width - room_width - 1)
    y = random.randint(0, dungeon.height - room_height - 1)

    new_room = Room(x, y, room_width, room_height)

    if any(new_room.intersect(other_room) for other_room in rooms):
      continue

    dungeon.tiles[new_room.inner] = tile_types.floor

    if len(rooms) == 0:
      player.x, player.y = new_room.center
    else:
      for x, y in tunnel(new_room.center, rooms[-1].center):
        dungeon.tiles[x, y] = tile_types.floor

    rooms.append(new_room)

  return dungeon

def tunnel(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
  x1, y1 = start
  x2, y2 = end

  if random.random() < 0.5:
    corner_x, corner_y = x2, y1
  else:
    corner_x, corner_y = x1, y2

  for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
    yield x, y
  for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
    yield x, y