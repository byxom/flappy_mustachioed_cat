import pyxel
import player
import piping
import background
import sys
import json
import argparse


class App:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Short sample app')
        parser.add_argument("-f", "--fps", type=int,
                            help="frames per second", default=60)
        parser.add_argument("-p", "--palette", type=int,
                            help="allows you to choose one of three "
                                 "possible color palette schems", default=0)
        # добавил аргпарс аргументы, при помощи которых
        # можно изменять количество кадров в секнуду и цветовую схему игры
        args = parser.parse_args()
        if 10 > args.fps or args.fps > 120:
            # защита от дурака
            # огриничиваю возможный fps
            print('only int fps from 10 to 120 is available\n'
                  'starting with a default value')
            args.fps = 60
        if args.palette not in (0, 1, 2):
            # защита от дурака
            print('only 0, 1 or 2 is available\n'
                  'starting with a default value')
            args.palette = 0
        palettes = [pyxel.DEFAULT_PALETTE,
                    [0x000000, 0xFF6347, 0xFF7F50, 0xFFA500, 0xEFD334,
                     0xD1E231, 0xB2EC5D, 0x30BA8F, 0x6495ED, 0x9370DB,
                     0xCD5C5C, 0x434750, 0xFFF8DC, 0xB0C4DE, 0x08457E,
                     0xE0B0FF],
                    [0x000000, 0x1D2B53, 0x7E2553, 0x008751, 0xAB5236,
                     0x5F574F, 0xC2C3C7, 0xFFF1E8, 0xFF004D, 0xFFA300,
                     0xFFEC27, 0x00E436, 0x29ADFF, 0x83769C, 0xFF77A8,
                     0xFFCCAA], ]
        # список, содержащий три возможные цветовые палитры
        pyxel.init(192, 256, caption="Flappy Mustachioed Cat",
                   scale=3, fps=args.fps, palette=palettes[args.palette])
        # инициирую приложение
        self.x = 0
        self.reset()
        pyxel.load("[pyxel_resource_file].pyxres")
        pyxel.run(self.update, self.draw)

    def reset(self):
        # эта функция восстанавливает аргументы приложения к
        # начальному состоянию
        self.dead = 0
        # аргумент dead равен 1, когда персонаж умирает
        self.score = 0
        # аргумент счета
        self.wait_c = 1
        # аругумент, переключащий игру в режим ожидания, а
        # так же отвечающий за движение персонажа вверх и вниз
        # в режиме ожидания
        self.delay = False
        # аргумент, включающий задержку
        self.frame_count = pyxel.frame_count
        # аргумент, хронящий количетсво кадров, которые
        # сменились с момента запуска до момента иницииации self.reset()
        self.blind = 0

        with open('hys.json', 'r') as h:
            dat = json.load(h)
            self.best_one = dat['best_one']
            # считываю рекордный счет из файла json
        self.player = player.Player()
        # создает объект игрока
        self.piping = piping.Piping()
        # создает объект труб
        self.backgnd = background.Ground()
        # создает объект земли

    def update(self):

        # основная функция обновления игры
        if pyxel.btn(pyxel.KEY_Q):
            sys.exit()
            # в этом месте можно использовать pyxel.quit(),
            # но использование этой функции вызывает на моем ноутбуке
            # ошибку виндоус, устранить котору у меня не получилось

        if pyxel.frame_count % 6 == 0:
            # обновляю состояние крыльев, кажде
            # 6 кадров, для создания анимации "махания"
            self.player.wings = (self.player.wings + 1) % 2

        if self.wait_c:
            # вводит игру в режим ожидания, если wait True
            self.wait()
            return

        if self.dead:
            # включается, когда персонаж умер
            self.save_score()
            self.player.wings = 0
            if pyxel.btn(pyxel.KEY_SPACE) and not self.blind:
                # перезапускает игру, когда игрок нажимает пробел
                self.reset()
                return
            if not self.wait_c:
                self.player.update()
            if self.player.y == (236 - self.player.height) \
                    and self.player.jump:
                # фикрсирует трубы и персонажа
                # если персонаж уже упал на землю
                self.piping.speed = 0
                self.player.jump = 0
            return

        if pyxel.btn(pyxel.KEY_SPACE) and self.player.jump >= 0:
            # реагирует на нажатие пробела, поднимая персонаж
            # запускает звук прыжка
            pyxel.play(0, 1)

            self.player.jump = -3.3
            self.player.wings = 0

        self.player.update()
        self.backgnd.update()

        if pyxel.frame_count - self.frame_count < 120:
            # устанавливает пробел в 120 кадров
            # после начала игры и перед появлением труб
            if self.player.y == (236 - self.player.height):
                # при столкновении персонажа с землей
                # персонаж умирает, включается затемнение экрана
                # запускает звук удара

                pyxel.play(0, 0)
                self.blind += 1
                self.dead = 1
            return
        self.piping.update_level()

        if self.check_collision():
            # если произошло столкновение с трубой
            # или землей персонаж умирает, включается затемнение экрана
            # запускает звук удара

            pyxel.play(0, 0)
            self.blind += 1
            self.dead = 1

        self.score_count()

    def wait(self):
        # работает в режиме ожидания нажатия на пробел

        if not pyxel.btn(pyxel.KEY_SPACE):
            # срабатывает при условии, если пробел не нажат
            # это условие необходимо, так как pyxel считает пробел
            # нажатым в течении какого-то времени, за которое
            # игра успевает отрисовать несколько кадров
            self.delay = True
        if not (not pyxel.btn(pyxel.KEY_SPACE) or not self.delay):
            # при нажатии пробела(с учетом задержки pyxel)
            # выводит игру из режима ожидания
            # реагирует на нажатие пробела, поднимая персонажа
            # запускает звук прыжка
            self.wait_c = 0
            self.player.jump = -3.3
            self.player.wings = 0
            pyxel.play(0, 1)
            return
        if pyxel.frame_count % 16 == 0:
            # каждые 16 кадров меняет направление
            # движения персонажа по оси y
            self.wait_c = self.wait_c * (-1)
        self.player.y += self.wait_c
        self.backgnd.update()

    def save_score(self):
        # сохраняет счет игрока в файл json

        with open('hys.json', 'r') as h:
            dat = json.load(h)
            if self.score > dat['best_one']:
                dat['best_one'] = self.score
                with open('hys.json', 'w') as h1:
                    json.dump(dat, h1)

    def score_count(self):
        # считает счет игрока, регистрируя
        # прохождение через трубы

        for i in range(2):
            # проверяет прохождение для двух левых пар труб в кадре
            pipe_start = self.piping.upper_pipes[i][0]
            pipe_end = self.piping.upper_pipes[i][0] + self.piping.pipe_width
            if (pipe_start <= self.player.x <= pipe_end) \
                    and self.piping.pipe_flag[i]:
                # если пара труб пройдена, и не была засчитана
                # добавляет один бал к счету и ставит 0 флаг для пары трубы
                self.score += 1
                self.piping.pipe_flag[i] = 0

    def check_collision(self):
        # эта функция проверяет столкновения с землей или трубами
        piping_col = False
        for i in range(2):
            pipe_start = self.piping.upper_pipes[i][0] - self.player.width
            pipe_end = self.piping.upper_pipes[i][0] + self.piping.pipe_width
            up_pipe = self.piping.upper_pipes[i][3]
            btm_pipe = self.piping.buttom_pipes[i][1] - self.player.height
            if (pipe_start <= self.player.x <= pipe_end) and not (
                    up_pipe < self.player.y < btm_pipe):
                # срабатывает, если персонаж столкнулся с трубой
                piping_col = True
            return self.player.y == (236 - self.player.height) or piping_col

    def draw(self):
        # эта функция рисует уровень и игрока

        self.draw_lvl()
        self.draw_player()

    def draw_player(self):
        # эта функция рисует игрока
        pyxel.blt(self.player.x, self.player.y, 1, 40, 80
                  if self.player.wings else 104, 26, 20, colkey=8)
        # условие отвечает за переключение текстуры персонажы
        # с поднятыми и опущенными крыльями

    def draw_lvl(self):
        # эта функция рисует все кроме игрока

        if self.blind:
            # включается затемнение экрана в течении 10
            # кадров после столкновения с игроыми объектами
            self.blind += 1
            if self.blind % 10 == 0:
                self.blind = 0
            pyxel.cls(0)
            return
        pyxel.blt(0, 0, 0, 0, 14, 192, 240)
        # рисует фон игры

        for up in self.piping.upper_pipes:
            # рисует верхние трубы
            pyxel.blt(up[0], up[3] - 160, 1, 0, 16, 40, 160, colkey=10)

        for btm in self.piping.buttom_pipes:
            # рисует нижние трубы
            pyxel.blt(btm[0], btm[1], 1, 0, 16, 40, 160, colkey=10)

        for i in range(len(self.backgnd.list)):
            # рисует землю
            pyxel.blt(self.backgnd.list[i], 240, 1, 0, 0, 64, 16)

        if self.dead and not self.wait_c:
            # рисует табличку с счетом игры и рекордом, когда персонаж умер, но
            # еще не перешел в режим ожидания

            pyxel.blt(70, 100, 1, 40, 128, 48, 48, colkey=8)
            pyxel.text(86, 110, str('SCORE'), 9)
            pyxel.text(94, 118, str(self.score), 0)
            pyxel.text(88, 125, str('BEST'), 9)
            pyxel.text(94, 133, str(self.best_one), 0)
            return

        pyxel.text(92, 60, str(self.score), 7)
        # рисует текущий счет игры


if __name__ == "__main__":
    App()
