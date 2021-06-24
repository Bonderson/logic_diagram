import pygame as pg
import time


class Biba(pg.sprite.Sprite):  # оболочка для вентилей, с помощью которой можно взаимодействовать с ними
    def __init__(self, coord, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(coord[0],
                                                coord[1]))
        self.offsets = [0, 0]

    def update_offsets(self, n_x, n_y): #отступ мыши от центра спрайта при захвате
        self.offsets = [n_x, n_y]

    def update(self, coord):
        self.rect = self.image.get_rect(center=(coord[0] + self.offsets[0],
                                                coord[1] + self.offsets[1]))

def redraw():  # <<переделать, добавить как метод класса box>>
    gameScreen.fill((255,255,255))
    for element in pool:
        gameScreen.blit(element.image, element.rect)
    #pg.display.update()


pg.init() # запускаем pygame
path_rect = "rect.png" # пока одиночная картинка, <<заменить на список путей каритнок>>
# Окно игры: размер, позиция
gameScreen = pg.display.set_mode((500, 400)) # <<замутить как отдельный класс box!!!>>

pg.display.set_caption("Let's try")
gameScreen.fill((255, 255, 255))
pg.display.flip()
runGame = True

pool = list()  # хранятся все объекты, <<будущее поле дочернего класса box>>
moveobj = None  # перемещение
sec_name = [0, -1]  # хранит время последнего клика правой кнопки мыши и имя объекта
while runGame:
    # try:
    for event in pg.event.get():
        if event.type == pg.QUIT: runGame = False
        if event.type == pg.MOUSEBUTTONUP:
            moveobj = None
        if event.type == pg.MOUSEMOTION:
            if moveobj:
                moveobj.update(event.pos)
                redraw()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for element in pool[::-1]:
                    if element.rect.collidepoint(event.pos):
                        moveobj = element
                        moveobj.update_offsets(moveobj.rect.center[0] - event.pos[0],
                                               moveobj.rect.center[1] - event.pos[1])
                        pool.remove(element)
                        pool.append(element)
                        redraw()
                        break

                if moveobj == None:
                    myRect = list(event.pos)  # позиция мыши изначально в кортеже(
                    pool.append(Biba(myRect, path_rect))
                    gameScreen.blit(pool[-1].image, pool[-1].rect)

            if event.button == 3:
                for element in pool[::-1]:
                    if element.rect.collidepoint(event.pos):
                        if abs(sec_name[0] - time.time()) < 0.5 and sec_name[1] == pool.index(element):
                            pool.remove(element)
                            del element
                            sec_name[0] = 0
                            redraw()
                            break
                        else:
                            sec_name[0] = time.time()
                            sec_name[1] = pool.index(element)
                            break

    # print("---")
    pg.display.update()
pg.quit()