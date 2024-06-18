import math

import pygame
from pygame.math import Vector2


class Enemy:
    SPEED = 7

    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.dir = Vector2()
        self.color = color
        self.max_range = 250

        self.tmp_bullet = {
            'pos': Vector2(0, 0),
            "vel": Vector2(0, 0)

        }
        self.bullets = []
        self.bullet_speed = 7

        self.shoot_timer_max = 40
        self.shoot_timer = self.shoot_timer_max

        self.health = 5

    def draw(self, win, w, h):
        pygame.draw.ellipse(win, self.color, self.rect,2)
        for b in self.bullets:
            pygame.draw.circle(win, 'yellow', b["pos"], 2)
            b["pos"] += b["vel"] * self.bullet_speed
            if not 0 < b["pos"].x < w or not 0 < b["pos"].y < h:
                if b in self.bullets:
                    self.bullets.remove(b)

    def update_pos(self, dir):
        self.rect.x += dir[0]
        self.rect.y += dir[1]

    def update(self, player):
        self.move(player)

    def get_direction_to_player(self, player):
        angle = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
        return math.cos(angle), math.sin(angle)

    def dist_to_player(self, player):
        return math.sqrt(
            abs(player.rect.centerx - self.rect.centerx) ** 2 + abs(player.rect.centery - self.rect.centery) ** 2)

    def move(self, player):
        dx, dy = self.get_direction_to_player(player)
        if self.dist_to_player(player) > self.max_range:
            self.rect.x += dx * self.SPEED
            self.rect.y += dy * self.SPEED
        else:
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.shoot_timer = self.shoot_timer_max
                tmp = self.tmp_bullet.copy()
                tmp["pos"] = Vector2(*self.rect.center)
                tmp["vel"].x = dx
                tmp["vel"].y = dy
                self.bullets.append(tmp.copy())

        # print(dx, dy, self.rect.center)


test_obstacle = Enemy(50, 50, 30, 30, (255, 0, 0))
items = [test_obstacle]

stats = {
    "triangle": {
        "img": pygame.image.load("assets/Sprites/triangle-purple.png"),
        "bullet_speed": 10

    }
}


def blit_center(screen, surface: pygame.Surface, position):
    w, h = surface.get_width(), surface.get_height()
    screen.blit(surface, (position[0] - w // 2, position[1] - h // 2))


shoot_rate = "rate of fire"
sides = [
    {"damage": 1, shoot_rate: 600 * 1, "c": 0},# right
    {"damage": 1, shoot_rate: 600 * 1, "c": 0}, # down
    {"damage": 1, shoot_rate: 600 * 1, "c": 0}, # left
    {"damage": 1, shoot_rate: 60 * 1, "c": 0}
]


class Player:
    def __init__(self, speed, health, x, y):
        self.speed = speed
        self.health = health
        self.score = 0
        self.side = 4
        self.rect = pygame.rect.Rect(x, y, 50, 50)
        self.health = 10

        self.state = "triangle"
        self.tmp_bullet = {
            'pos': Vector2(0, 0),
            "vel": Vector2(0, 0),
            "damage": 0

        }
        self.bullets = []
        self.img = stats[self.state]["img"].convert_alpha()
        self.img = pygame.transform.scale(self.img, self.rect.size)

    def draw(self, screen, items, w, h):
        placing = 360 / self.side
        prev = None
        ang_ = math.atan2(self.rect.y - pygame.mouse.get_pos()[1], self.rect.x - pygame.mouse.get_pos()[0])
        ang_ = math.degrees(ang_)
        for i in range(self.side + 1):
            ang = i * placing + 45 + ang_
            ang = math.radians(ang)
            rad = self.rect.w
            x = math.cos(ang) * rad
            y = math.sin(ang) * rad
            # print(x+500, y+500)
            if prev is not None:
                # pygame.draw.line(screen, (255, 255, 255), (x + self.rect.centerx, y + self.rect.centery),                                 (prev[0] + self.rect.centerx, prev[1] + self.rect.centery), 2)

                pygame.draw.line(screen, (255, 255, 255), (x + self.rect.centerx, y + self.rect.centery),
                                 (prev[0] + self.rect.centerx, prev[1] + self.rect.centery), 2)
            prev = x, y

        # pygame.draw.rect(screen, (255, 255, 255), self.rect)
        angle = math.atan2(self.rect.y - pygame.mouse.get_pos()[1], self.rect.x - pygame.mouse.get_pos()[0])
        rotated_img = pygame.transform.rotozoom(self.img, math.degrees(-angle) + 90, 1)

        blit_center(screen, rotated_img, self.rect.center)

        for item in items:
            item.draw(screen, w, h)

        for bullet in self.bullets:
            if not 0 < bullet["pos"].x < w or not 0 < bullet["pos"].y < h:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
            pygame.draw.circle(screen, (255, 255, 255), bullet["pos"], bullet["damage"])
            bullet["pos"] += bullet["vel"] * stats[self.state]["bullet_speed"]

    def move(self, items, w, h):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.rect.top > 75:
                self.rect.y -= self.speed
            else:
                for item in items:
                    item.update_pos((0, self.speed))

        elif keys[pygame.K_s]:
            if self.rect.bottom < h - 75:
                self.rect.y += self.speed
            else:
                for item in items:
                    item.update_pos((0, -self.speed))

        if keys[pygame.K_a]:
            if self.rect.left > 75:
                self.rect.x -= self.speed
            else:
                for item in items:
                    item.update_pos((+self.speed, 0))

        elif keys[pygame.K_d]:
            if self.rect.right < w - 75:
                self.rect.x += self.speed
            else:
                for item in items:
                    item.update_pos((-self.speed, 0))

    def shoot(self):
        placing = 360 / self.side
        ang_ = math.atan2(self.rect.y - pygame.mouse.get_pos()[1], self.rect.x - pygame.mouse.get_pos()[0])
        ang_ = math.degrees(ang_)

        for i in range(self.side + 1):
            ang = i * placing - 90 + ang_
            ang = math.radians(ang)
            rad = self.rect.w
            x = math.cos(ang) * rad
            y = math.sin(ang) * rad

            if i >= self.side:
                break
            sides[i]["c"] += 1
            if sides[i]["c"] >= sides[i][shoot_rate]:
                tmp = self.tmp_bullet.copy()
                tmp["pos"] = Vector2(self.rect.centerx + x, self.rect.centery + y)
                tmp["damage"] = sides[i]["damage"]

                angle = math.atan2(y, x)

                tmp["vel"] = tmp["vel"].copy()
                tmp["vel"].x = math.cos(angle)
                tmp["vel"].y = math.sin(angle)

                self.bullets.append(tmp.copy())
                sides[i]["c"] = 0

    def update_side_date(self):
        pass
