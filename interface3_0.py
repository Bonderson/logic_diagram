#!/usr/bin/env python
# coding: utf-8
!pip install pygame
# # Programm

# In[1]:


import pygame as pg
import time
from win32api import GetSystemMetrics


# In[2]:


class display:
    def __init__(self, width, height):
        self.m_screen = pg.display.set_mode((width, height))
        pg.display.set_caption("Logic_scheme")
        self.l_screen = field(width - width//4, height)
        self.r_screen = gates_list(width//4, height)
        self.mini_rect = pg.Rect(width - width//4 - 2, 0, 4, height)
        self.redraw()
    def redraw(self):
        self.m_screen.fill((0,0,0))
        self.m_screen.blit(*self.l_screen.scale())
        self.m_screen.blit(self.r_screen.surface, self.r_screen.rect)
        pg.draw.rect(self.m_screen, [0,0,0], self.mini_rect)


# In[3]:


class Gateway():
    def __init__(self, name, rect, wave = None):
        self.name = name
        self.wave = wave
        self.rect = rect
    
    def change_wave(self, wave = None):
        self.wave = wave


# In[4]:


class Wave():
    def __init__(self, name, inp, outp):
        self.name = name
        self.input = inp
        self.output = outp
        self.state = 0
        self.color = [0,0,0]
    def __str__(self):
        return "wave"
    
    def change_input(self, inp = None):
        self.input = inp
        
    def change_output(self, outp = None):
        self.output = outp
    
    def change_state(self):
        self.state = abs(self.state - 1)
        self.color[0] = 255*self.state
        self.color[1] = 255*self.state
    
    def del_self(self):
        try:
            self.input.change_wave()
        except:
            pass
        try:
            self.output.change_wave()
        except:
            pass


# In[5]:


class Biba(pg.sprite.Sprite): #оболочка для вентилей, с помощью которой можно взаимодействовать с ними
    def __init__(self, coord, filename, name, inum, onum, selnum = 0):
        self.name = name
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha() # содержит отмасштабированную картинку
        self.rect = self.image.get_rect(center = (coord[0],
                                                  coord[1]))
        self.offsets = [0,0]
        self.left_rect = pg.Rect(self.rect.left, self.rect.top, 20, self.rect.height)
        
        self.right_rect = pg.Rect(self.rect.right-20, self.rect.top, 20, self.rect.height)
        self.bottom_rect = pg.Rect(self.rect.left, self.rect.bottom - 20, self.rect.width, 20)
        self.old_coord = self.rect.center
        
        self.input_pool = list()
        for i in range(inum):
            rect = pg.Rect(self.left_rect.left, self.left_rect.top, self.left_rect.width, self.left_rect.height//inum)
            rect.move_ip(0, i*self.left_rect.height//inum)
            self.input_pool.append(Gateway(self.name[4:], rect))
            
        self.output_pool = list()
        for i in range(onum):
            rect = pg.Rect(self.right_rect.left, self.right_rect.top, self.right_rect.width, self.right_rect.height//onum)
            rect.move_ip(0, i*self.right_rect.height//onum)
            self.output_pool.append(Gateway(self.name[4:], rect))
            
        self.selector_pool = list()
        for i in range(selnum):
            rect = pg.Rect(self.bottom_rect.left, self.bottom_rect.top,
                           self.bottom_rect.width//selnum, self.bottom_rect.height)
            rect.move_ip(i*self.bottom_rect.width//selnum, 0)
            self.selector_pool.append(self.name[4:], Gateway(rect))
            
    def update_offsets(self, coord):
        self.offsets = [self.rect.center[0] - coord[0], self.rect.center[1] - coord[1]]
        
    def move(self, coord):
        self.rect.move_ip(coord[0] + self.offsets[0] - self.rect.center[0],
                          coord[1] + self.offsets[1] - self.rect.center[1])
        
        self.left_rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])
        self.right_rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])
        self.bottom_rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])
        for element in [*self.input_pool, *self.output_pool, *self.selector_pool]:
            element.rect.move_ip(self.rect.center[0] - self.old_coord[0], self.rect.center[1] - self.old_coord[1])
        
        self.old_coord = self.rect.center
        
    def where_to_click(self, coord):
        if self.left_rect.collidepoint((coord[0], coord[1])):
            for gateway in self.input_pool:
                if gateway.rect.collidepoint((coord[0], coord[1])):
                    return "input", gateway
        elif self.right_rect.collidepoint((coord[0], coord[1])):
            for gateway in self.output_pool:
                if gateway.rect.collidepoint((coord[0], coord[1])):
                    return "output", gateway
        elif self.bottom_rect.collidepoint((coord[0], coord[1])):
            for gateway in self.selector_pool:
                if gateway.rect.collidepoint((coord[0], coord[1])):
                    return "input", gateway
        return self.name, None
    
    def return_all_gateways(self):
        return [*self.input_pool, *self.output_pool, *self.selector_pool]
    
    def del_self(self):
        for gateway in [*self.input_pool, *self.output_pool, *self.selector_pool]:
            try:
                gateway.wave.del_self()
            except:
                pass


# In[6]:


class gates_list:
    def __init__(self, width, height):
        self.time_name = [0, -1]
        self.surface = pg.surface.Surface((width, height))
        self.rect = self.surface.get_rect(center = (width*3 + width//2, height//2))
        self.surface.fill((255,255,255))
        self.gates_pool = list([Biba((0,0), "./gates/and.png", "./gates/and.png",2,1),
                              Biba((0,0), "./gates/or.png", "./gates/or.png",2,1),
                              Biba((0,0), "./gates/button.png", "./gates/button.png",0,1),
                              Biba((0,0), "./gates/output.png", "./gates/output.png",1,0)])
        self.font = pg.font.SysFont(None, 20)
        self.gates_names = [self.font.render(element.name[8:-4], True, (0,0,0)) for element in self.gates_pool]
        #self.gates_names = [element.name[8:-4] for element in self.gates_pool] нужна для отладки
        sum_heights = 5
        for element in self.gates_pool:
            element.rect.inflate_ip(0, 15)
            element.rect.move_ip(width//2, element.rect.height*0.5 + sum_heights + 5)
            sum_heights += element.rect.height + 10
        self.redraw()
        
    def redraw(self):
        self.surface.fill((255,255,255))
        for element, name in zip(self.gates_pool, self.gates_names):
            self.surface.blit(element.image, element.rect)
            self.surface.blit(name, name.get_rect(center=(element.rect.center[0],
                                                          element.rect.center[1] + element.rect.height*0.5-5)))
            
#     def scroll(self): # при нынешнем кол-ве вентилей скорее всего будет не нужен
#         self.speed = 10
#         pass
    def click_lmouse(self, coord):
        self.redraw()
        coord = [self.rect.width//2, coord[1]]
        for element in self.gates_pool:
            if element.rect.collidepoint((coord[0], coord[1])):
                if abs(self.time_name[0] - time.time()) < 0.5 and self.time_name[1] == element.name:
                    Display.l_screen.create_object(element)
                    
                    break
                else:
                    self.time_name[0] = time.time()
                    self.time_name[1] = element.name
                    color_rect = pg.Rect(0, element.rect.top, self.rect.width, element.rect.height)
                    color_surface = pg.surface.Surface((color_rect.width, color_rect.height))
                    color_surface.fill((200,200,200))
                    color_surface.set_alpha(128)
                    self.surface.blit(color_surface, color_rect)
                    break


# In[7]:


class field:
    def __init__(self, width, height):
        self.scale_val = 100
        self.scale_speed = 10
        self.scale_edges = [50, 150] # speed должен быть кратен разности val и edges[0]
        k = (self.scale_val-self.scale_edges[0])/self.scale_speed
        self.surface = pg.surface.Surface((width//k*k*2, height//k*k*2))
        self.surface.fill((255,255,255))
        self.pool_objects = [list(), list()] # 0 - вентили, 1 - провода
        self.rect = self.surface.get_rect(center = (width//k*k//2, height//k*k//2))
        self.time_name = [0, -1] # хранит время последнего клика правой кнопки мыши и имя объекта
        self.moveobj = None
        self.old_coord = [0,0]
        
    def redraw(self):
        self.surface.fill((255,255,255))
        for element in self.pool_objects[0]:
            self.surface.blit(element.image, element.rect)
            
        for element in self.pool_objects[1]:
            try:
                self.draw_wave(element.input.rect.center, element.output.rect.center, element.color)
                #pg.draw.line(self.surface, element.color, element.input.rect.center, 
                             #element.output.rect.center, 2)
            except:
                pass
    
    def draw_wave(self, inp, outp, color):
        pg.draw.line(self.surface, color, inp, [outp[0]//2 + inp[0]//2,inp[1]], 1)
        pg.draw.line(self.surface, color, [outp[0]//2 + inp[0]//2, inp[1]], [outp[0]//2 + inp[0]//2, outp[1]], 1)
        pg.draw.line(self.surface, color, [outp[0]//2 + inp[0]//2, outp[1]], outp, 1)
    
    def scale_const(self, k):
        new_scale = self.scale_val + self.scale_speed*k
        if self.scale_edges[0] <= new_scale <= self.scale_edges[1] and self.moveobj == None:
            self.scale_val = new_scale
            self.moveobj = self.rect
            self.old_coord = list(self.rect.center)
            self.move_obj(self.rect.center)
            self.moveobj = None
            
    def scale(self):
        sc_surf = pg.transform.smoothscale(self.surface,
                                     (self.rect.width*self.scale_val//100, self.rect.height*self.scale_val//100))
        sc_rect = sc_surf.get_rect(center = self.rect.center)
        return sc_surf, sc_rect
    
    def transform_c(self, x, y):    #преобразование координат из системы дисплея в систему поверхности класса field
        n_x = self.rect.left + (x - self.rect.center[0])*100//self.scale_val + self.rect.width//2
        n_y = self.rect.top + (y - self.rect.center[1])*100//self.scale_val + self.rect.height//2
        return n_x, n_y
    
    def move_obj(self, coord):
        coord = self.transform_c(*coord)
        if self.moveobj.__str__() == "wave":
            self.redraw()
            if self.moveobj.output == None:
                #pg.draw.line(self.surface, [0,0,0], self.moveobj.input.rect.center,
                             #(coord[0] - self.rect.left, coord[1] - self.rect.top), 2)
                self.draw_wave(self.moveobj.input.rect.center,
                               (coord[0] - self.rect.left, coord[1] - self.rect.top), [0,0,0])
            else:
                #pg.draw.line(self.surface, [0,0,0], self.moveobj.output.rect.center,
                             #(coord[0] - self.rect.left, coord[1] - self.rect.top), 2)
                self.draw_wave(self.moveobj.output.rect.center,
                               (coord[0] - self.rect.left, coord[1] - self.rect.top), [0,0,0])
                            
        elif self.moveobj == self.rect:
            self.rect.move_ip(coord[0] - self.old_coord[0], 
                              coord[1] - self.old_coord[1])
            if self.rect.center[0] - self.rect.width*self.scale_val//100//2 > 0:
                self.rect.move_ip(-(self.rect.center[0] - self.rect.width*self.scale_val//100//2), 0)
            elif self.rect.center[0] + self.rect.width*self.scale_val//100//2 < self.rect.width//2:
                self.rect.move_ip(self.rect.width//2 - (self.rect.center[0] + self.rect.width*self.scale_val//100//2), 0)
            if self.rect.center[1] + self.rect.height*self.scale_val//100//2 < self.rect.height//2:
                self.rect.move_ip(0, self.rect.height//2 - (self.rect.center[1] + self.rect.height*self.scale_val//100//2))
            elif self.rect.center[1] - self.rect.height*self.scale_val//100//2 > 0:
                self.rect.move_ip(0, -(self.rect.center[1] - self.rect.height*self.scale_val//100//2))
            self.old_coord = coord
            self.redraw()
        else:    
            if coord[0] - self.rect.left <= self.rect.width:
                self.moveobj.move((coord[0] - self.rect.left, coord[1] - self.rect.top))
            else:
                self.moveobj.move((self.rect.width - 10, coord[1] - self.rect.top))
            self.redraw()
    
    
    def click_lmouse(self, coord):
        coord = self.transform_c(*coord)
        for element in self.pool_objects[0][::-1]:
            if element.rect.collidepoint((coord[0] - self.rect.left, coord[1] - self.rect.top)):
                #print(element.left_rect)
                
                part, gateway = element.where_to_click((coord[0] - self.rect.left, coord[1] - self.rect.top))
                if part == "input" or part == "output":
                    if gateway.wave == None:
                        global count_of_waves
                        if part == "input":
                            gateway.change_wave(Wave(f"wave{count_of_waves}", None, gateway))
                        else:
                            gateway.change_wave(Wave(f"wave{count_of_waves}", gateway, None))
                            count_of_waves += 1
                        self.moveobj = gateway.wave
                        #pg.draw.line(self.surface, [0,0,0], gateway.rect.center,
                                     #(coord[0] - self.rect.left, coord[1] - self.rect.top), 2)
                        self.draw_wave(gateway.rect.center,
                               (coord[0] - self.rect.left, coord[1] - self.rect.top), [0,0,0])
                    else:
                        self.moveobj = gateway.wave
                        if part == "input":
                            self.moveobj.change_output()
                            self.redraw()
                            #pg.draw.line(self.surface, [0,0,0], self.moveobj.input.rect.center,
                                         #(coord[0] - self.rect.left, coord[1] - self.rect.top), 2)
                            self.draw_wave(self.moveobj.input.rect.center,
                                          (coord[0] - self.rect.left, coord[1] - self.rect.top), [0,0,0])
                        else:
                            self.moveobj.change_input()
                            self.redraw()
                            #pg.draw.line(self.surface, [0,0,0], self.moveobj.output.rect.center,
                                         #(coord[0] - self.rect.left, coord[1] - self.rect.top), 2)
                            self.draw_wave((coord[0] - self.rect.left, coord[1] - self.rect.top),
                                          self.moveobj.output.rect.center, [0,0,0])
                        gateway.change_wave()
                        self.pool_objects[1].remove(self.moveobj)
                    break
                    
                else:
                    #print("in", [x.wave for x in element.input_pool])
                    #print("out", [x.wave for x in element.output_pool])
                    #print("...")
                    self.moveobj = element
                    self.moveobj.update_offsets((coord[0] - self.rect.left, coord[1] - self.rect.top))
                    self.pool_objects[0].remove(element)
                    self.pool_objects[0].append(element)
                    self.redraw()
                    break
        if self.moveobj == None:
            self.moveobj = self.rect
            self.old_coord = [coord[0], coord[1]]
        
    def lbutton_up(self, coord):
        coord = self.transform_c(*coord)
        if self.moveobj.__str__() == "wave":
            for element in self.pool_objects[0][::-1]:
                if element.rect.collidepoint((coord[0] - self.rect.left, coord[1] - self.rect.top)):
                    part, gateway = element.where_to_click((coord[0] - self.rect.left, coord[1] - self.rect.top))
                    if (part == "input" or part == "output") and gateway.wave == None:
                        if part == "input" and self.moveobj.output == None and gateway.name != self.moveobj.input.name:
                            self.moveobj.change_output(gateway)
                            gateway.change_wave(self.moveobj)
                            self.pool_objects[1].append(gateway.wave)
                        elif part == "output" and self.moveobj.input == None and gateway.name != self.moveobj.output.name:
                            self.moveobj.change_input(gateway)
                            gateway.change_wave(self.moveobj)
                            self.pool_objects[1].append(gateway.wave)
                        break
            if self.moveobj.output == None or self.moveobj.input == None:
                self.moveobj.del_self()
            self.redraw()
        self.moveobj = None
    
    def click_rmouse(self, coord):
        self.del_object(coord)
    
    def create_object(self, obj):
        global count_of_gates
        
        coord = self.transform_c(self.rect.width//4, self.rect.height//4)
        self.pool_objects[0].append(obj.__class__((coord[0] - self.rect.left, coord[1] - self.rect.top),
                                         obj.name, f"gate{count_of_gates}", len(obj.input_pool),
                                                  len(obj.output_pool), len(obj.selector_pool)))
        self.surface.blit(self.pool_objects[0][-1].image, self.pool_objects[0][-1].rect)
        count_of_gates += 1
        
    def del_object(self, coord):
        coord = self.transform_c(*coord)
        for element in self.pool_objects[0][::-1]:
            if element.rect.collidepoint((coord[0] - self.rect.left, coord[1] - self.rect.top)):
                part, gateway = element.where_to_click((coord[0] - self.rect.left, coord[1] - self.rect.top))
                if part == "input" or part == "output":
                    if gateway.wave != None:
                        element = gateway.wave
                if abs(self.time_name[0] - time.time()) < 0.5 and self.time_name[1] == element.name:
                    if element.__str__() == "wave":
                        element.del_self()
                        print(len(self.pool_objects[1]))
                        self.pool_objects[1].remove(element)
                        
                    else:
                        for gateway in element.return_all_gateways():
                            try:
                                self.pool_objects[1].remove(gateway.wave)
                            except:
                                pass
                        element.del_self()
                        self.pool_objects[0].remove(element)
                    self.time_name[0] = 0
                    self.redraw()
                    break
                else:
                    self.time_name[0] = time.time()
                    self.time_name[1] = element.name
                    break


# In[8]:


count_of_gates = 0
count_of_waves = 0
pg.init()
Display = display(GetSystemMetrics(0)*3//4, GetSystemMetrics(1)*3//4)
runGame = True
while runGame:
    for event in pg.event.get():
        if event.type == pg.QUIT: runGame = False
            
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                Display.l_screen.lbutton_up(event.pos)
            
        if event.type == pg.MOUSEMOTION:
            if Display.l_screen.moveobj:
                Display.l_screen.move_obj(event.pos)
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if Display.r_screen.rect.collidepoint(event.pos):
                    Display.r_screen.click_lmouse(event.pos)
                else:
                    Display.l_screen.click_lmouse(event.pos)
            if event.button == 3:
                if Display.r_screen.rect.collidepoint(event.pos):
                    pass
                else:
                    Display.l_screen.click_rmouse(event.pos)
        
        if event.type == pg.KEYDOWN and event.key == pg.K_MINUS or event.type == pg.MOUSEBUTTONDOWN and event.button == 5:
            Display.l_screen.scale_const(-1)

        if event.type == pg.KEYDOWN and event.key == pg.K_EQUALS or event.type == pg.MOUSEBUTTONDOWN and event.button == 4:
            Display.l_screen.scale_const(1)

    Display.redraw()
    pg.display.update()
pg.quit()
