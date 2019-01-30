from __future__ import division

from Tkinter import *
import numpy as np
from mypymods.vector import Vector2
from tqdm import tqdm
from PIL import Image, ImageDraw

wd = 1000
ht = 800

class Branch(Vector2):
    def __init__(self, x, y):
        Vector2.__init__(self, x, y)
        self.open = True
        self.level = -1
        self.anchor = Vector2(0,0)

    def copy(self):
        new = Branch(self.x, self.y)
        new.open = self.open
        new.level = self.level
        new.anchor = self.anchor
        return new

class Tree:
    def __init__(self, iters, seeds):
        self.iters = iters
        self.seeds = seeds
        self.init_width = 20
        self.droop = 0.3
        self.droop_divergence = 0 #Percentage
        self.droop_max = 0.7
        self.seed_divergence = 0 #Percentage
        self.seed_max = 5
        self.branch_length = 70
        self.branch_length_div = 0 #Percentage
        self.branch_length_shrink = 0
        self.branch_length_change = self.branch_length
        self.branches = []
        tree_root = Branch(0, self.branch_length)
        self.branches.append(tree_root)
        self.image = Image.new('RGB', (wd,ht), (255,255,255))
    
    def reset(self):
        self.branches = []
        tree_root = Branch(0, self.branch_length)
        self.branches.append(tree_root)
        self.image = Image.new('RGB', (wd,ht), (255,255,255))

    def grow(self):
        if (np.random.random() < self.droop_divergence):
            rot = self.droop + np.random.uniform(-self.droop_max, self.droop_max)
            self.branches[0].rotate(rot/5)
        for i in tqdm(range(self.iters), desc="Growing...", nested=True):
            for branch in tqdm(self.branches, nested=True):
                if branch.open == True and branch.level == i-1:
                    if (np.random.random() < self.seed_divergence):
                        seeds = np.random.randint(2,self.seed_max+1)
                    else:
                        seeds = self.seeds
                    for j in range(seeds):
                        droop_div = (np.random.random() < self.droop_divergence)
                        droop = self.droop + np.random.uniform(-self.droop_max,self.droop_max)*droop_div
                        new_branch = Branch(0, 0)
                        new_branch.x = branch.x
                        new_branch.y = branch.y
                        new_branch.level = i
                        rot = -droop + j*2*droop/(seeds-1)
                        new_branch.rotate( rot )
                        new_branch.anchor = branch.anchor + branch
                        
                        if self.branch_length_shrink != 0:
                            self.branch_length_change /= self.branch_length_shrink
                            new_branch.rescale(self.branch_length_change)
                        
                        if (np.random.random() < self.branch_length_div):
                            r = (np.random.random()-0.5)*self.branch_length_change
                            new_branch.rescale(self.branch_length_change + r)
                        
                        
                        self.branches.append( new_branch )
                        branch.open = False

    def draw(self):
        draw = ImageDraw.Draw(self.image)
        for branch in tqdm(self.branches, desc="Drawing...", nested=True):
            a = wd/2 + branch.anchor.x
            b = 50 + branch.anchor.y
            c = a + branch.x
            d = b + branch.y
            
            b = ht-b
            d = ht-d
            
            width = self.init_width/((branch.level+2)*3)
            draw.line((a,b,c,d), fill=(0,0,0), width=int(width))

    def show(self):
        self.image.show()

    def save(self, fn='', show=False):
        self.image.save(fn+'.png')

    def quick_draw(self):
        self.reset()
        self.grow()
        self.draw()
        self.show()

tree = Tree(6,3);
#tree.seed_divergence = 0.5;
#tree.droop_divergence = 0.6;
#tree.branch_length_div = 0.7;
tree.branch_length_shrink = 1.1;
tree.quick_draw();

'''
fn = 1
for i in tqdm(range(100)):
    tree = Tree(5,3)
    tree.branch_length = np.random.uniform(40,50)
    tree.iters = np.random.randint(7,9)
    tree.seed = np.random.randint(2,6)
    tree.droop = np.random.uniform(0.1,0.5)
    tree.droop_max = 0.6
    tree.droop_divergence = np.random.uniform(0,1)
    tree.seed_divergence = np.random.uniform(0,1)
    tree.branch_length_div = np.random.uniform(0,1)
    tree.grow()
    tree.draw()
    tree.draw()
    tree.save('Trees/'+str(fn).zfill(3))
    fn += 1
    #tree.show()
    #raw_input()
'''