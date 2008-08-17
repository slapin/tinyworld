# 
# File: leveleditor.py
# Author: Martin Yrjola
# Desc: A level editor for the platformer, now using objdict.db
#       to make a list of available objects.
#

import os
import sys
import pickle

import pygame

from gooeypy import sdl as gui
from gooeypy.const import *

if os.path.exists('leveleditor.py'):
    # to get to the project root if run from projectroot/leveleditor/
    os.chdir(os.path.join(os.getcwd(), '..')) 
 
sys.path.insert(0, os.path.join("lib")) 
import gamefunc

def dbload(filename):
    '''loads the object database from external file'''
    db = open(filename, 'r')
    objdict = pickle.load(db)
    return objdict

def alignToGrid((x,y)):
    xout = x/32*32
    yout = y/32*32
    return (xout,yout)

class mouseSprite(pygame.sprite.Sprite):
    def __init__(self, (image,rect)):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
        self.image.fill((0,0,0,0))
    def update(self, image=None):
        mousepos = pygame.mouse.get_pos()
        self.rect.topleft = alignToGrid((mousepos[0] - 195, mousepos[1]))
        if image:
            if image == 'noimage':
                self.image.fill((0,0,0,0))
            self.image = image
        

class placedObject(pygame.sprite.Sprite):
    def __init__(self, (image, rect), pos, background):
        pygame.sprite.Sprite.__init__(self)
        self.image,self.rect = image,rect
        background.blit(image, pos)
        self.rect.topleft = pos

class objSelectBox:
    '''The SelectBox where you can choose the objects you
       want to the level, also includes buttons to save,
       clear and change the level'''
    def __init__(self, app, objdict):
        self.app = app
        self.objdict = objdict
        self.vbox = gui.VBox(x=0, y=0, bgcolor=(5,5,255), spacing=5)
        self.selectbox = gui.SelectBox(x=0, y=0, width=195, height=645, scrollable=True, disabled=True)
        self.b1 = gui.Button('Save', width=195, disabled=True)
        self.b2 = gui.Button('Clear', width=195, disabled=True)
        self.b3 = gui.Button('Change Level', width=195, disabled=True)
        self.vbox.add(self.selectbox, self.b1, self.b2, self.b3)
        self.app.add(self.vbox)
        self.populate()
        self.selectbox.connect(CLICK, self.getValue)

    def populate(self):
        '''populates the selectbox with objects'''
        for objname, imgname in self.objdict.iteritems():
            self.selectbox.add(objname, imgname)

    def getValue(self):
        return str(self.selectbox.values)[6:-3]

class levelEditingArea:
    '''
    Includes the level editing logic and the visual 
    representation of the objects placed on the level
    
    '''
    def __init__(self, app, selbox):
        self.app = app
        self.selbox = selbox
        self.levelmap = gamefunc.imgLoad('levelmap.png')[0]
        self.image = self.levelmap.copy()
        self.bgimage = self.levelmap.copy()
        self.imagewidget = gui.Image(self.image, x=200, y=0)
        self.imagewidget.connect(CLICK, self.clickedOn)
        self.app.add(self.imagewidget)
        self.state = 'chooselevel'
        self.selbox.b3.connect(CLICK, self.toChooseLevel)

    def clickedOn(self):
        if self.state == 'chooselevel':
            self.state = 'editlevel'
            self.selbox.selectbox.disabled = False
            self.selbox.b1.disabled = False
            self.selbox.b2.disabled = False
            self.selbox.b3.disabled = False
            self.objlist = []
            mousepos = pygame.mouse.get_pos()
            self.chosenlevel = str( (mousepos[0] - 195) / 64) + str(mousepos[1] / 64)
            self.openLevel(self.chosenlevel)
        else:
            self.editLevel()

    def toChooseLevel(self):
        self.image.blit(self.levelmap,(0,0))
        self.bgimage = self.levelmap.copy()
        self.state = 'chooselevel'
        self.selbox.selectbox.disabled = True
        self.selbox.b1.disabled = True
        self.selbox.b2.disabled = True
        self.selbox.b3.disabled = True
             
    def openLevel(self, levelname):
        self.bgimage.fill((255,255,255))
        self.image.fill((255,255,255))

    def editLevel(self):
        mousepos = pygame.mouse.get_pos()
        mousepos = alignToGrid((mousepos[0] - 195, mousepos[1]))
        self.objlist.append(placedObject(gamefunc.imgLoad(self.selbox.getValue()), \
                mousepos, self.bgimage))

        
    
def main():
    objdict = dbload('objdict.db')
    window = pygame.display.set_mode((1224, 768))
    gui.init(myscreen = window)
    app = gui.App(width=1224, height=768)
    spritegroup = pygame.sprite.Group()
    cursor = mouseSprite(gamefunc.imgLoad('ball1.png'))
    spritegroup.add(cursor)
    objselbox = objSelectBox(app, objdict)
    leveleditor = levelEditingArea(app, objselbox)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                running = False
        objimg = objselbox.getValue()
        if len(objimg) > 1:
            cursor.update(gamefunc.imgLoad(objimg)[0])
        else: cursor.update()
        app.run(events)
        app.dirty = True
        app.draw()
        spritegroup.clear(leveleditor.image, leveleditor.bgimage)
        spritegroup.draw(leveleditor.image)
        gui.update_display()

if __name__ == '__main__':
    main()
