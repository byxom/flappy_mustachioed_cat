class Player:
    def __init__(self):
        self.height = 16
        self.width = 26
        # height и width размеры персонажа
        self.jump = 20
        # jump - это количество пикселей, которые
        # добавляются к y координате персонажа каждый кадр
        self.v_acc = 0.2
        # ускорение с которым меняется jump
        self.x = 35
        self.y = 120
        # x и y координаты персонажа
        self.wings = 0
        # если wings = 0 - крылья опущены,
        # если равен 1 - подняты

    def update(self):
        # перемещает персонажа каждый кардр
        self.y += self.jump
        if self.y < 0:
            self.y = 0
        elif self.y > 236 - self.height:
            self.y = 236 - self.height
        self.jump += self.v_acc
