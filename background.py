class Ground:
    def __init__(self):
        self.w = 64
        # ширина одного блока земли
        self.list = [i * 64 for i in range(5)]

    # список все блоков земли

    def update(self):
        # обновление положения блоков земли
        for i in range(len(self.list)):
            # сдвигает каждый блок земли на 1 пиксель левее
            self.list[i] -= 1

        if self.list[0] <= -self.w:
            # если блок вышел за левую границу кадра удаляет его и добавляет
            # новый блок в конец списка
            self.list.pop(0)
            self.list.append(self.list[-1] + 64)
