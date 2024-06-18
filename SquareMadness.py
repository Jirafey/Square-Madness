import random

import pygame
import pygame as pg
from sys import exit
from button import Button
from player import *

turrets = pg.sprite.Group()
# ! NOTES:
# ! add this sounds where a player powers up:
# power_up_sound = pg.mixer.Sound('assets/Sounds/powerupes.wav')
# power_up_sound.set_volume(0.05)
# power_up_sound.play()
# ! add this sounds where a player dies:

# ! add this sounds where a player wins:
# victory_sound = pg.mixer.Sound('assets/Sounds/8-bit-retro-success-victory.mp3')
# victory_sound.set_volume(0.05)
# victory_sound.play()

# turrets

fullscreen = False
sound_off = False
music_off = False
width = 1280
height = 720


class turret(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('assets/Sprites/PLAYERSPRITE.png')
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > width:
            self.rect.left = 0


class Collectable:
    def __init__(self):
        w, h = pygame.display.get_window_size()
        self.pos = Vector2(random.randint(-w * 2, w * 2), random.randint(-h * 2, h * 2))

    def update_pos(self, dir):
        self.pos.x += dir[0]
        self.pos.y += dir[1]

    def draw(self, win):
        pygame.draw.circle(win, (0, 255, 0), self.pos, 20)


pg.init()
bg_music = pg.mixer.Sound('assets/music/geoswap-v3.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.3)
screen = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption("SquareMadness")

click_sound = pg.mixer.Sound('assets/Sounds/blipSelect.wav')
click_sound.set_volume(0.05)

Clock = pg.time.Clock()
background = pg.image.load("assets/Backgrounds/Background.png")

player = Player(5, 10, 700, 80)

collectables = [Collectable() for _ in range(150)]

wave_timer = pygame.USEREVENT + 1
pygame.time.set_timer(wave_timer, 5000)

wave_enemy_count = 10
wave_count = 0
current_time = pg.time.get_ticks() // 1000


def get_font(size):  # supportive function
    return pg.font.Font("assets/Fonts/font.ttf", size)


def adding_sprites():  # for loading the sprites
    triangle = pg.image.load('assets/Sprites/triangle-purple.png').convert_alpha()
    triangle_rect = triangle.get_rect()
    circle = pg.image.load('assets/Sprites/circle-green.png').convert_alpha()
    circle_rect = circle.get_rect(center=(400, 50))
    triangle_rect = triangle.get_rect(center=(600, 50))

    screen.blit(circle, circle_rect)
    screen.blit(triangle, triangle_rect)


def upgrade_screen():
    global wave_count, wave_enemy_count
    screen_w, screen_h = pygame.display.get_window_size()
    size = 150
    exit_ = False
    upgrades = [shoot_rate, "damage"]
    selected_upgrade = 0

    def upgrade(index, upgrade_select):
        if upgrade_select == "rate of fire":

            if sides[index][upgrade_select] == 600:
                sides[index][upgrade_select] = 60
            sides[index][upgrade_select] -= 10
        else:
            sides[index][upgrade_select] += 1

    while not exit_:
        screen.fill("black")
        t3 = get_font(18).render(f"Press          on the arrow keys to switch between the upgrades", True,
                                 (180, 180, 180))
        t2_1 = get_font(18).render(f"up/down", True,
                                   'yellow')
        t3_1 = get_font(18).render(f"1/2/3/4", True,
                                   'yellow')
        t2 = get_font(18).render(f"Press          on the keyboard to pick a side you want to upgrade", True,
                                 (180, 180, 180))
        screen.blit(t2, (10, 80))
        screen.blit(t2_1, (120, 60))
        screen.blit(t3_1, (120, 80))
        screen.blit(t3, (10, 60))
        t = get_font(20).render(f"Upgrade ", True, (180, 180, 180))
        t4 = get_font(20).render(f"{upgrades[selected_upgrade]}", True, 'red')
        screen.blit(t, (10, t2.get_height() + 10))
        screen.blit(t4, (180, t2.get_height() + 10))

        pygame.draw.rect(screen, (255, 255, 255), ((screen_w // 2) - size, (screen_h // 2) - size, size * 2, size * 2),
                         5)
        t2 = get_font(20).render(f"(1)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2 - (size + t2.get_width() + 10), screen_h // 2))

        t2 = get_font(20).render(f"(4)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2, screen_h // 2 + (size + t2.get_height() + 10)))

        t2 = get_font(20).render(f"(3)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2 + (size + t2.get_width() + 10), screen_h // 2))

        t2 = get_font(20).render(f"(2)", True, (180, 180, 180))
        blit_center(screen, t2, (screen_w // 2, screen_h // 2 - (size + t2.get_height() + 10)))
        # 1-right 2-down 3 - left 4- top
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected_upgrade -= 1
                if event.key == pygame.K_DOWN: selected_upgrade += 1
                if selected_upgrade > len(upgrades) - 1: selected_upgrade = 0
                if selected_upgrade < 0: selected_upgrade = len(upgrades) - 1

                selected_one = upgrades[selected_upgrade]

                if event.key == pygame.K_3:
                    power_up_sound = pg.mixer.Sound('assets/Sounds/powerupes.wav')
                    power_up_sound.set_volume(0.05)
                    if not sound_off:
                        power_up_sound.play()
                    upgrade(0, selected_one)
                    exit_ = True

                if event.key == pygame.K_4:
                    power_up_sound = pg.mixer.Sound('assets/Sounds/powerupes.wav')
                    power_up_sound.set_volume(0.05)
                    if not sound_off:
                        power_up_sound.play()
                    upgrade(1, selected_one)
                    exit_ = True

                if event.key == pygame.K_1:
                    power_up_sound = pg.mixer.Sound('assets/Sounds/powerupes.wav')
                    power_up_sound.set_volume(0.05)
                    if not sound_off:
                        power_up_sound.play()
                    upgrade(2, selected_one)
                    exit_ = True

                if event.key == pygame.K_2:
                    power_up_sound = pg.mixer.Sound('assets/Sounds/powerupes.wav')
                    power_up_sound.set_volume(0.05)
                    if not sound_off:
                        power_up_sound.play()
                    upgrade(3, selected_one)
                    exit_ = True
                player.update_side_date()
        pg.display.update()

    wave_count += 1
    wave_enemy_count += 2
    spawn_enemy(screen_w, screen_h)
    shield = 50


def game_over_screen():
    screen_w, screen_h = pygame.display.get_window_size()
    screen.fill("black")
    death_sound = pg.mixer.Sound('assets/Sounds/death.wav')
    death_sound.set_volume(0.05)
    if not sound_off:
        death_sound.play()
    while True:
        t2 = get_font(34).render(f"Game Over", True, (255, 255, 255))
        t2__1 = get_font(20).render(f'Please restart the game to play again', True, 'red')
        t3 = get_font(20).render(f"Wave count: {wave_count + 1}", True, 'pink')
        t5 = get_font(20).render(f"Time:{current_time}", True, 'pink')
        t = get_font(20).render(f"Score:{player.score}", True, 'pink')
        blit_center(screen, t, (screen_w // 2, (screen_h // 2 + 150)))
        blit_center(screen, t5, (screen_w // 2, (screen_h // 2 + 100)))
        blit_center(screen, t3, (screen_w // 2, (screen_h // 2 + 50)))
        blit_center(screen, t2, (screen_w // 2, (screen_h // 2) - 50))
        blit_center(screen, t2__1, (screen_w // 2, (screen_h // 2)))
        if wave_count >= 3 and wave_count < 5:
            ts = get_font(20).render(f"HELP #1: How about only upgrading one side?", True, 'pink')
            blit_center(screen, ts, (screen_w // 2, (screen_h // 2 + 150)))
        if wave_count >= 5 and wave_count < 7:
            tss = get_font(20).render(f"HELP #2: How about only upgrading rate of fire?", True, 'pink')
            blit_center(screen, tss, (screen_w // 2, (screen_h // 2 + 200)))
        if wave_count >= 7:
            tsss = get_font(20).render(f"HELP #3: Just upgrade 2nd side's rate of fire?", True, 'pink')
            blit_center(screen, tsss, (screen_w // 2, (screen_h // 2 + 250)))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        pg.display.update()
def game_win_screen():
    screen_w, screen_h = pygame.display.get_window_size()
    screen.fill("black")
    death_sound = pg.mixer.Sound('assets/Sounds/8-bit-retro-success-victory.mp3')
    death_sound.set_volume(0.05)
    if not sound_off:
        death_sound.play()
    while True:
        t2 = get_font(34).render(f"You Won", True, (255, 255, 255))
        t2__1 = get_font(20).render(f'Please restart the game to play again', True, 'red')
        t3 = get_font(20).render(f"Wave count: {wave_count + 1}", True, 'pink')
        t5 = get_font(20).render(f"Time:{current_time}", True, 'pink')
        t = get_font(20).render(f"Score:{player.score}", True, 'pink')
        blit_center(screen, t, (screen_w // 2, (screen_h // 2 + 150)))
        blit_center(screen, t5, (screen_w // 2, (screen_h // 2 + 100)))
        blit_center(screen, t3, (screen_w // 2, (screen_h // 2 + 50)))
        blit_center(screen, t2, (screen_w // 2, (screen_h // 2) - 50))
        blit_center(screen, t2__1, (screen_w // 2, (screen_h // 2)))
        if wave_count >= 3 and wave_count < 5:
            ts = get_font(20).render(f"HELP #1: How about only upgrading one side?", True, 'pink')
            blit_center(screen, ts, (screen_w // 2, (screen_h // 2 + 150)))
        if wave_count >= 5 and wave_count < 7:
            tss = get_font(20).render(f"HELP #2: How about only upgrading rate of fire?", True, 'pink')
            blit_center(screen, tss, (screen_w // 2, (screen_h // 2 + 200)))
        if wave_count >= 7:
            tsss = get_font(20).render(f"HELP #3: Just upgrade 2nd side's rate of fire?", True, 'pink')
            blit_center(screen, tsss, (screen_w // 2, (screen_h // 2 + 250)))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        pg.display.update()


def spawn_enemy(screen_w, screen_h):
    for enemy_i in range(wave_enemy_count):
        i = random.random()
        if i < .25:
            x = random.randint(-screen_w, 0)
            y = random.randint(0, screen_h)
        elif i < .50:
            x = random.randint(screen_w, screen_w * 2)
            y = random.randint(0, screen_h)
        elif i < .75:
            x = random.randint(0, screen_w)
            y = random.randint(-screen_h, 0)

        else:
            x = random.randint(0, screen_w)
            y = random.randint(screen_h, screen_h * 2)

        items.append(Enemy(x, y, 30, 30, (255, 0, 0)))


shoot_event = pygame.USEREVENT + 2
pygame.time.set_timer(shoot_event, 500)


def play():  # what happens after play button gets clicked
    sound_vic_played = 0
    shield = 0
    counter = 1
    counter_win = 0
    global wave_count
    hit_sound_en = pg.mixer.Sound('assets/Sounds/bum.wav')
    hit_sound_en.set_volume(0.1)
    screen_w, screen_h = pygame.display.get_window_size()
    global current_time
    while True:
        current_time = pg.time.get_ticks() // 1000

        if shield > 0:
            shield -= 1

        player.shoot()

        for event in pg.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    options()

            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if len(items) == 0:
                if wave_count % 3 == 0:

                    upgrade_screen()
                    shield = 50
                elif event.type == wave_timer:
                    wave_count += 1
                    spawn_enemy(screen_w, screen_h)
            if wave_count == 10 and wave_count != 0 and sound_vic_played == 0:
                victory_sound = pg.mixer.Sound('assets/Sounds/8-bit-retro-success-victory.mp3')
                victory_sound.play()
                victory_sound.set_volume(0.3)
                sound_vic_played += 1
                wave_count += 20
                Enemy.SPEED += 10
            if wave_count > 10:
                wave_count += 20 * counter_win
                Enemy.SPEED += 10 * counter_win
                counter_win += 1
            if player.score % 10 == 0 and (counter + 9 * counter) == player.score:
                upgrade_screen()
                shield = 50
                counter += 1

            # if event.type == shoot_event:
            #     # print(event.button)
            #     # if event.button == 1:
            #     # player.shoot()

            #     # else:
            #     #     items.append(Enemy(*pygame.mouse.get_pos(), 30, 30, (255, 0, 255)))

        player.move(items + collectables, screen_w, screen_h)
        screen.fill("black")

        player.draw(screen, items, screen_w, screen_h)
        if wave_count%1 == 0 and not wave_count == 0:
            game_win_screen()
        for item in items:
            item.update(player)
            for b in player.bullets:
                if item.rect.collidepoint(b["pos"].x, b["pos"].y) and not sound_off:
                    item.health -= b["damage"]
                    hit_sound = pg.mixer.Sound('assets/Sounds/hitHurt.wav')
                    hit_sound.set_volume(0.05)
                    if not sound_off:
                        hit_sound.play()
                    if item.health <= 0 and item in items:
                        items.remove(item)

            for b in item.bullets:
                if player.rect.collidepoint(b["pos"].x, b["pos"].y) and shield == 0:
                    player.health -= 1
                    if not sound_off:
                        hit_sound_en.play()
                    shield = 50
                    if player.health <= 0:
                        game_over_screen()
                    if b in item.bullets:
                        item.bullets.remove(b)
                    if b in player.bullets:
                        player.bullets.remove(b)

        for collectable in collectables:
            collectable.draw(screen)

        shield_on_off = bool
        shielder = ''
        if shield > 0:
            shield_on_off = True

        else:
            shield_on_off = False
        if not shield_on_off:
            shielder = 'No'
        if shield_on_off:
            shielder = 'Yes'

        t = get_font(20).render(f"FPS: {round(Clock.get_fps(), 2)}", True, (180, 180, 180))
        screen.blit(t, (10, 50))
        t2 = get_font(20).render(f"Wave count: {wave_count + 1}", True, (180, 180, 180))
        screen.blit(t2, (10, 50 + (t.get_height() + 10)))
        t3 = get_font(20).render(f"HP:{player.health}", True, 'green')
        screen.blit(t3, (10, 50 + (t.get_height() + 40)))
        t5 = get_font(20).render(f"Time:{current_time}", True, (180, 180, 180))
        screen.blit(t5, (10, 50 + (t.get_height() + 100)))
        t4 = get_font(20).render(f"Shield: {shielder}", True, (180, 180, 180))

        screen.blit(t4, (10, 50 + (t.get_height() + 70)))

        helping = get_font(14).render(f"Use WASD to move around", True, 'pink')
        screen.blit(helping, (screen_w // 4, 10))
        helping2 = get_font(14).render(f"Collect 10 green circles to get an upgrade (this will send a wave)", True,
                                       'gray')
        screen.blit(helping2, (screen_w // 4, 30))
        helping3 = get_font(14).render(f"Click ESC key to open options", True,
                                       'gray')
        screen.blit(helping3, (screen_w // 4, 50))
        collisions = player.rect.collidelistall([pygame.Rect(c.pos.x, c.pos.y, 20, 20) for c in collectables])
        player.score += len(collisions)

        for collision in collisions:
            collect_sound = pg.mixer.Sound('assets/Sounds/pickupCoin.wav')
            collect_sound.set_volume(0.05)
            if not sound_off:
                collect_sound.play()

            collectables.pop(collision)
        # collectables = collectables_copy.copy()

        t = get_font(34).render(f"Score:{player.score}", True, (255, 255, 255))
        screen.blit(t, (10, 10))
        pg.display.update()
        turrets.update()
        turrets.draw(screen)
        Clock.tick(60)


def options_video():  # what happens after options -> video button gets clicked
    global fullscreen
    while True:
        options_mouse_pos = pg.mouse.get_pos()
        sw, sh = pygame.display.get_window_size()
        screen_ = pygame.transform.scale(background, (sw, sh))
        screen.blit(screen_, (0, 0))
        options_video_mouse_pos = pg.mouse.get_pos()
        options_video_text = get_font(45).render("This is the VIDEO screen.", True, "gray")
        options_video_rect = options_video_text.get_rect(center=(sw / 2, sh / 2 - 120))

        options_video_back = Button(image=None, pos=(sw / 2, sh / 2 + 120),
                                    text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")

        options_video_fullscreen = Button(image=None, pos=(sw / 2, sh / 2 + 0),
                                          text_input="FULLSCREEN", font=get_font(75), base_color="gray",
                                          hovering_color="Green")
        screen.fill("black")
        options_video_fullscreen.changeColor(options_video_mouse_pos)
        options_video_fullscreen.update(screen)
        options_video_back.changeColor(options_video_mouse_pos)
        options_video_back.update(screen)
        screen.blit(options_video_text, options_video_rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if not sound_off:
                    click_sound.play()
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_video_back.checkForInput(options_video_mouse_pos):
                    if not sound_off:
                        click_sound.play()
                    options()
            if event.type == pg.MOUSEBUTTONDOWN:
                if options_video_fullscreen.checkForInput(options_video_mouse_pos):
                    if fullscreen:
                        if not sound_off:
                            click_sound.play()
                            screen_ = pygame.display.set_mode((screen.get_width(), screen.get_height()),
                                                              pygame.RESIZABLE)
                    if not fullscreen:
                        if not sound_off:
                            click_sound.play()
                        screen_ = pg.display.set_mode((width, height), pg.FULLSCREEN)
                        screen_ = pygame.transform.scale(background, (sw, sh))
                        screen.blit(screen_, (0, 0))
                        fullscreen = True
        pg.display.update()


def options_audio():  # what happens after options -> audio button gets clicked

    global sound_off
    global music_off
    while True:
        if sound_off:
            sound_off_human = 'OFF'
        else:
            sound_off_human = 'ON'
        if music_off:
            music_off_human = 'OFF'
        else:
            music_off_human = 'ON'
        options_mouse_pos = pg.mouse.get_pos()
        sw, sh = pygame.display.get_window_size()
        screen_ = pygame.transform.scale(background, (sw, sh))
        screen.blit(screen_, (0, 0))
        options_audio_mouse_pos = pg.mouse.get_pos()
        options_audio_back = Button(image=None, pos=(sw / 2, sh / 2 + 240),
                                    text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")
        options_audio_sound_off = Button(image=None, pos=(sw / 2, sh / 2),
                                         text_input=f"Sound {sound_off_human}", font=get_font(75), base_color="gray",
                                         hovering_color="Green")
        options_audio_music_off = Button(image=None, pos=(sw / 2, sh / 2 + 120),
                                         text_input=f"Music {music_off_human}", font=get_font(75), base_color="gray",
                                         hovering_color="Green")
        screen.fill("black")
        options_audio_music_off.changeColor(options_mouse_pos)
        options_audio_music_off.update(screen)
        options_audio_sound_off.changeColor(options_audio_mouse_pos)
        options_audio_sound_off.update(screen)
        options_audio_back.changeColor(options_audio_mouse_pos)
        options_audio_back.update(screen)
        options_text = get_font(45).render("This is the AUDIO screen.", True, "gray")
        options_rect = options_text.get_rect(center=(sw / 2, sh / 2 - 120))
        screen.blit(options_text, options_rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if not sound_off:
                    click_sound.play()
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_audio_back.checkForInput(options_audio_mouse_pos):
                    if not sound_off:
                        click_sound.play()
                    options()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_audio_sound_off.checkForInput(options_audio_mouse_pos):
                    if sound_off:
                        sound_off = False
                    else:
                        sound_off = True
                        click_sound.play()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if options_audio_music_off.checkForInput(options_audio_mouse_pos):
                    if music_off:
                        music_off = False
                        bg_music.play()
                    else:
                        music_off = True
                        bg_music.stop()
                        if not sound_off:
                            click_sound.play()

        pg.display.update()


def options():  # what happens after options button gets clicked
    while True:
        options_mouse_pos = pg.mouse.get_pos()
        sw, sh = pygame.display.get_window_size()
        screen_ = pygame.transform.scale(background, (sw, sh))
        screen.blit(screen_, (0, 0))

        options_text = get_font(45).render("This is the OPTIONS screen.", True, "gray")
        options_rect = options_text.get_rect(center=(sw / 2, sh / 2 - 120))

        screen.blit(options_text, options_rect)

        options_audio_btn = Button(image=None, pos=(sw / 2, sh / 2),
                                   text_input="AUDIO", font=get_font(75), base_color="gray", hovering_color="Green")
        options_video_btn = Button(image=None, pos=(sw / 2, sh / 2 + 120),
                                   text_input="VIDEO", font=get_font(75), base_color="gray", hovering_color="Green")
        options_back = Button(image=None, pos=(sw / 2, sh / 2 + 240),
                              text_input="BACK", font=get_font(75), base_color="gray", hovering_color="Green")
        options_buttons = [options_audio_btn, options_video_btn, options_back]
        options_back.changeColor(options_mouse_pos)
        options_back.update(screen)
        options_audio_btn.changeColor(options_mouse_pos)
        options_audio_btn.update(screen)
        options_video_btn.changeColor(options_mouse_pos)
        options_video_btn.update(screen)
        for button in options_buttons:
            button.changeColor(options_mouse_pos)
            button.update(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if not sound_off:
                    click_sound.play()
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked

                if options_audio_btn.checkForInput(options_mouse_pos):
                    if not sound_off:
                        click_sound.play()

                    options_audio()
                if options_video_btn.checkForInput(options_mouse_pos):
                    if not sound_off:
                        click_sound.play()
                    options_video()
                if options_back.checkForInput(options_mouse_pos):
                    if not sound_off:
                        click_sound.play()
                    main_menu()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        play()
        pg.display.update()


def main_menu():  # Main screen upon opening the game, showing the main menu
    while True:
        sw, sh = pygame.display.get_window_size()
        background_ = pygame.transform.scale(background, (sw, sh))
        screen.blit(background_, (0, 0))

        menu_mouse_pos = pg.mouse.get_pos()
        s1 = sh / 2
        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(sw // 2, s1 - 120))

        play_button = Button(image=pg.image.load("assets/Buttons/Play Rect.png"), pos=(sw // 2, s1),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")

        options_button = Button(image=pg.image.load("assets/Buttons/Options Rect.png"),
                                pos=(sw // 2, s1 + 120),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")

        quit_button = Button(image=pg.image.load("assets/Buttons/Quit Rect.png"), pos=(sw // 2, s1 + 240),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="gray")

        buttons = [play_button, options_button, quit_button]
        screen.blit(menu_text, menu_rect)

        for button in buttons:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:  # what happens if a certain button gets clicked
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pg.quit()
                    exit()

        pg.display.update()
        Clock.tick(60)


if __name__ == '__main__':
    main_menu()
