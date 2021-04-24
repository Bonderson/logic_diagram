#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pygame')


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


class Biba(pg.sprite.Sprite): #оболочка для вентилей, с помощью которой можно взаимодействовать с ними
    def __init__(self, coord, filename, name):
        self.name = name
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(filename).convert_alpha() # содержит отмасштабированную картинку
        self.rect = self.image.get_rect(center = (coord[0],
                                                  coord[1]))
        self.offsets = [0,0]
        
    def update_offsets(self, coord):
        self.offsets = [self.rect.center[0] - coord[0], self.rect.center[1] - coord[1]]
        
    def move(self, coord):
        self.rect.move_ip(coord[0] + self.offsets[0] - self.rect.center[0],
                          coord[1] + self.offsets[1] - self.rect.center[1])


# In[4]:


class gates_list:
    def __init__(self, width, height):
        self.time_name = [0, -1]
        self.surface = pg.surface.Surface((width, height))
        self.rect = self.surface.get_rect(center = (width*3 + width//2, height//2))
        self.surface.fill((255,255,255))
        self.gates_pool = list([Biba((0,0), "./gates/and.png", "./gates/and.png"),
                              Biba((0,0), "./gates/or.png", "./gates/or.png"),
                              Biba((0,0), "./gates/button.png", "./gates/button.png"),
                              Biba((0,0), "./gates/output.png", "./gates/output.png")])
        self.font = pg.font.SysFont(None, 20)
        self.gates_names = [self.font.render(element.name[8:-4], True, (0,0,0)) for element in self.gates_pool]
        sum_heights = 5
        for element in self.gates_pool:
            element.rect.inflate_ip(0, 10)
            element.rect.move_ip(width//2, element.rect.height*0.5 + sum_heights + 5)
            sum_heights += element.rect.height + 10
        self.redraw()
        
    def redraw(self):
        self.surface.fill((255,255,255))
        for element, name in zip(self.gates_pool, self.gates_names):
            self.surface.blit(element.image, element.rect)
            self.surface.blit(name,
                              name.get_rect(center=(element.rect.center[0],element.rect.center[1] + element.rect.height*0.5-5)))
            
#     def scroll(self): # при нынешнем кол-ве вентилей скорее всего будет не нужен
#         speed = 10
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


# In[5]:


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
        for x in range(2):
            for element in self.pool_objects[x]:
                self.surface.blit(element.image, element.rect)
    
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
        if self.moveobj == self.rect:
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
                self.moveobj = element
                self.moveobj.update_offsets((coord[0] - self.rect.left, coord[1] - self.rect.top))
                self.pool_objects[0].remove(element)
                self.pool_objects[0].append(element)
                self.redraw()
                break
        if self.moveobj == None:
            self.moveobj = self.rect
            self.old_coord = [coord[0], coord[1]]
        
    def click_rmouse(self, coord):
        self.del_object(self.pool_objects[0], coord)
    
    def create_object(self, obj):
        coord = self.transform_c(self.rect.width//4, self.rect.height//4)
        self.pool_objects[0].append(obj.__class__((coord[0] - self.rect.left, coord[1] - self.rect.top),
                                         obj.name, f"gate{len(self.pool_objects[0])}"))
        self.surface.blit(self.pool_objects[0][-1].image, self.pool_objects[0][-1].rect)
        
    def del_object(self, objs, coord):
        coord = self.transform_c(*coord)
        for element in objs[::-1]:
            if element.rect.collidepoint((coord[0] - self.rect.left, coord[1] - self.rect.top)):
                if abs(self.time_name[0] - time.time()) < 0.5 and self.time_name[1] == element.name:
                    objs.remove(element)
                    del element
                    self.time_name[0] = 0
                    self.redraw()
                    break
                else:
                    self.time_name[0] = time.time()
                    self.time_name[1] = element.name
                    break


# In[6]:


pg.init()
Display = display(GetSystemMetrics(0)*3//4, GetSystemMetrics(1)*3//4)
runGame = True
while runGame:
    for event in pg.event.get():
        if event.type == pg.QUIT: runGame = False
            
        if event.type == pg.MOUSEBUTTONUP:
            Display.l_screen.moveobj = None
            
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


# In[7]:


d = pg.Rect(0,0,10,10)
d.inflate_ip(0,10)
d

