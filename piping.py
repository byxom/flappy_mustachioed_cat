import random


class Piping:
    def __init__(self):
        self.speed = 1
        # количество пискселей, на котрые смещаеются трубы каждый кадр
        self.gap = 70
        # расстояние между верхней и нижней трубой
        self.max_gap_pos_diff = 70
        # максимальное расстояние между разрывами соседних труб
        self.pipe_width = 40
        # ширина трубы
        self.pipe_distance = 70
        # расстояние между соседними трубами
        self.pipe_xmap = [256]
        # список x координат всех труб
        self.pipe_ymap = [100]
        # список y координат всех труб
        self.upper_pipes = []
        # список всех верхних труб
        self.buttom_pipes = []
        # список всех нижник труб
        self.pipe_flag = [1]
        # список флагов всех пар труб, которые равны 0, когда
        # игрок уже получил очки счета за прохождение трубы

    def update_level(self):
        # обновляет позицию труб каждый кадр

        if len(self.pipe_xmap) < 3:
            # добавляет трубы при сразу после
            # создания объекта класса
            self.gen_pipe_pos()
            self.gen_piping()
        for x in range(len(self.pipe_xmap)):
            self.pipe_xmap[x] -= self.speed
        self.check_extra_pipe()
        self.gen_piping()

    def check_extra_pipe(self):
        # убирыет трубу, которая вышла за границы экрана и генерирует новую
        if self.pipe_xmap[0] < -self.pipe_width:
            self.pipe_xmap.pop(0)
            self.pipe_ymap.pop(0)
            self.pipe_flag.pop(0)
            self.gen_pipe_pos()

    def gen_pipe_pos(self):
        # генерирует позицию новой трубы
        pipe_xpos = self.pipe_xmap[-1] + self.pipe_width + self.pipe_distance
        self.pipe_xmap.append(pipe_xpos)
        min_y = max(30, (self.pipe_ymap[-1] - self.max_gap_pos_diff))
        max_y = min(140, (self.pipe_ymap[-1] + self.max_gap_pos_diff))
        self.pipe_ymap.append(random.randint(min_y, max_y))

        self.pipe_flag.append(1)

    def gen_piping(self):
        # собирает координаты трех труб
        for x in range(len(self.pipe_xmap)):
            x1 = self.pipe_xmap[x]
            x2 = self.pipe_width
            uy1 = 0
            uy2 = self.pipe_ymap[x] - 1
            btmy1 = self.pipe_ymap[x] + self.gap - 1
            btmy2 = 256 - btmy1 - 16
            if len(self.upper_pipes) > x:
                # обновляет значения в списках труб
                self.upper_pipes[x] = [x1, uy1, x2, uy2]
                self.buttom_pipes[x] = [x1, btmy1, x2, btmy2]
            else:
                # если труб меньше трех - добавляет трубы к
                self.upper_pipes.append([x1, uy1, x2, uy2])
                self.buttom_pipes.append([x1, btmy1, x2, btmy2])
