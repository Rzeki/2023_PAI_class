import pygame as pg
from pygame import Vector2 as Vec2
from GameObject import MovingObject
from Vehicle import Vehicle
import util

class Enemy(Vehicle):
    def __init__(self, game_world, player: MovingObject) -> None:
        super().__init__(game_world, player)

