from UI import *
import pyautogui


class Application:
    def __init__(self):
        pg.init()
        screen_width, screen_height = pyautogui.size()
        self.display = Display(screen_width * 3 // 4, screen_height * 3 // 4)
        self.runGame = True

    def run_Application(self):
        while self.runGame:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.runGame = False

                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.display.r_screen.rect.collidepoint(event.pos):
                            pass
                        else:
                            self.display.l_screen.lbutton_up(event.pos)

                if event.type == pg.MOUSEMOTION:
                    if self.display.l_screen.moveobj:
                        self.display.l_screen.move_obj(event.pos)

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.display.r_screen.rect.collidepoint(event.pos):
                            self.display.r_screen.click_lmouse(event.pos)
                            self.display.interaction_space.create_object_in_lscreen()
                        else:
                            self.display.l_screen.click_lmouse(event.pos)
                    if event.button == 3:
                        if self.display.r_screen.rect.collidepoint(event.pos):
                            pass
                        else:
                            self.display.l_screen.click_rmouse(event.pos)

                if event.type == pg.KEYDOWN and event.key == pg.K_MINUS or \
                        event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
                    self.display.l_screen.scale_const(-1)
                # в jupyter колёсико работает в первом запуске после рестарта ядра
                if event.type == pg.KEYDOWN and event.key == pg.K_EQUALS or \
                        event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
                    self.display.l_screen.scale_const(1)

            self.display.redraw()
            pg.display.update()
        pg.quit()
