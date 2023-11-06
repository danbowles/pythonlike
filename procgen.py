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


def generate_dungeon(map_width, map_height) -> GameMap:
  dungeon = GameMap(map_width, map_height)

  room_one = Room(x=20, y=15, width=10, height=15)
  room_two = Room(x=35, y=15, width=10, height=15)

  dungeon.tiles[room_one.inner] = tile_types.floor
  dungeon.tiles[room_two.inner] = tile_types.floor

  for x, y in tunnel(start=room_one.center, end=room_two.center):
    dungeon.tiles[x, y] = tile_types.floor

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