# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 16:15:24 2022
from: https://stackoverflow.com/questions/7908636/how-to-add-hovering-annotations-in-matplotlib
@author: sbaldwin
"""
#%% imports
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)

#%% generate plot
x = np.random.rand(15)
y = np.random.rand(15)
names = np.array(list("ABCDEFGHIJKLMNO"))
c = np.random.randint(1,5,size=15)

norm = plt.Normalize(min(c),max(c))
cmap = plt.cm.coolwarm

fig,ax = plt.subplots()
sc = plt.scatter(x,y,c=c, s=100, cmap=cmap, norm=norm)

#%% add hover notes
annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}, {}".format(
                            " ".join(list(map(str,ind["ind"]))), 
                            " ".join([names[n] for n in ind["ind"]]),
                            c[ind["ind"][0]]
                            )
    
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()

#%% extra
def show_figure(fig):
# from: https://stackoverflow.com/questions/31729948/matplotlib-how-to-show-a-figure-that-has-been-closed
    
# create a dummy figure and use its
    # manager to display "fig"

    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)