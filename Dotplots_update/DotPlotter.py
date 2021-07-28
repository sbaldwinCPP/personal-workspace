# -*- coding: utf-8 -*-
"""
Created to replace matlab code AQColoredDotsPlots.m

@author: sbaldwin
"""
'''
required packages:
    openpyxl
    pandas
    easygui

 Inputs:
       XY coordinates
       .PNG of site
'''

#%% modules
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import os
import easygui
import sys
import time
import pickle as pk

#%% initialize
inidir = os.path.dirname(os.path.abspath(__file__)) 
SavePath=inidir+'/DotPlotSave.pkl'

#%% dialogs & setup

#make this  a function later to keep msg, title, etc. out of memory
if os.path.exists(SavePath):
    msg='Re-use these saved image settings? \n'+SavePath
    title='Previous settings found...'
    YN_LoadSave=easygui.ynbox(msg,title)    
else:
    YN_LoadSave=False


if YN_LoadSave:
    with open(SavePath, 'rb') as handle: ImIn = pk.load(handle)
    im_path=ImIn['im_path']
    XY_path=ImIn['XY_path']
    Xscale=ImIn['Xscale']
    Yscale=ImIn['Yscale']
    Dx=ImIn['Dx']
    Dy=ImIn['Dy']
    im = plt.imread(im_path)
    Targdir=os.path.dirname(XY_path)
else:
    txt='Select input file...'
    ftyp= '*.xlsx'
    dft=inidir + "\\" + ftyp
    XY_path = easygui.fileopenbox(default=dft,msg=txt,filetypes=ftyp)
    if XY_path==None:sys.exit()
    #target the location of fit file for addtl file selections & plots
    Targdir=os.path.dirname(XY_path)
    imtxt='Please select a site plan...'
    imftyp= '*.png'
    imdft=Targdir + "\\" + imftyp
    im_path=easygui.fileopenbox(default=imdft,msg=imtxt,filetypes=imftyp)
    if im_path==None:sys.exit()
    


#%% functions
def Read_files(XY_path):
    '''
    Read input file and parse data

    Returns
    -------
    XYdat, header, data 
    Input data parsed into dataframes

    '''
        
    #read XY coordinates
    XYdat=pd.read_excel(XY_path, skiprows=2, usecols=(0,1,2), header=None)
    XYdat.columns=('ID',
                    'X_FS',
                    'Y_FS')
    XYdat.ID=XYdat.ID.astype('str')       #force to string
    
    
    #Read 1st 2 rows, used to set colorbar scale & label, filename
    header=pd.read_excel(XY_path, nrows=2, header=None)
    header.drop(columns=[0,1,2], inplace=True)
    
    #Read data to be plotted, column indexes match those in header
    data=pd.read_excel(XY_path, skiprows=2, header=None)
    data.drop(columns=[0,1,2], inplace=True)
    
    return XYdat, header, data

def GetFS_XY(ID):
    ''' 
    Get full-scale XY coordinartes from XYdat

    '''
    ID=str(ID)                                        # force to string
    x=float(XYdat[XYdat.ID==ID].X_FS)
    y=float(XYdat[XYdat.ID==ID].Y_FS)
    return x,y

def Image_Scale(im_file):
    '''
    GUI tool to set and save image scale variables 

    Parameters
    ----------
    im_file : String
        Path to Site .PNG.

    Returns
    -------
    None.
    Sets and saves Xscale, Yscale, Dx, Dy.
    Also saves Im_path, XY_path.
    Saved values are checked/loaded in dialogs cell

    '''
    
    global Xscale,Yscale,Dx,Dy,im
    
    im = plt.imread(im_file)
    
    print('Click on 2 numbered locations')
    fig, ax = plt.subplots(figsize=FigSize)
    ax.imshow(im, 
              interpolation='spline16'
              )
    plt.suptitle('Click on 2 numbered locations')
    
    pos1,pos2= plt.ginput(n=2)
    
    plt.close()
    
    x1,y1=pos1[0],pos1[1]
    x2,y2=pos2[0],pos2[1]
    
    #R1=input('Enter location #1:') 
    #R2=input('Enter location #2:')
    R1,R2=easygui.multenterbox(msg='Enter Locations',
                                title='Enter Locations',
                               fields=['Location 1:','Location 2:'],
                               values=[1,2])
  
    
    X1,Y1=GetFS_XY(R1)
    X2,Y2=GetFS_XY(R2)
    
    Xscale=abs((x1-x2)/(X1-X2))
    Yscale=(y1-y2)/(Y1-Y2)
    
    Dx=x1-X1*Xscale
    Dy=y1-Y1*Yscale
    
    ImOut={'im_path':im_path,
           'XY_path':XY_path,
           'Xscale':Xscale,
           'Yscale':Yscale,
           'Dx':Dx,
           'Dy':Dy,
           }
    #Save data (serialize) as pkl file
    with open(SavePath, 'wb') as handle: pk.dump(ImOut, 
                                                 handle, 
                                                 protocol=pk.HIGHEST_PROTOCOL)    

#colorbar setup func
def cbScale(bounds):
    series=np.arange(bounds[0],bounds[1]+1,1)
    #cmap=cm.get_cmap('jet')    #set color scheme here
    norm = colors.Normalize()
    norm.autoscale(series)
    sm = cm.ScalarMappable(cmap=cmap,norm=norm)
    sm.set_array([])
    return sm


def DotPlot(series,bounds,title):
    #make plot function here
    print('Plotting {}'.format(title))
    x=XYdat.X_im
    y=XYdat.Y_im
    
    if bounds[0]=='%':
        bounds=[0,100]
        series=series*100
    else: 
        bounds=[int(x) for x in bounds]
        
    sm=cbScale(bounds)
    
    fig, ax = plt.subplots(figsize=FigSize)
    ax.imshow(im, interpolation='spline16')
    
    ax.scatter(x, y, c=series, cmap=sm.cmap, s=DotSize)
    
    cb=plt.colorbar(sm)
    cb.ax.set_title(title[0])
    
    for i in series.index:
        if not np.isnan(series[i]):
            plt.annotate(round(series[i]), (x[i]+X0,y[i]-Y0), color=FontColor, fontsize=FontSize)
    
    plt.axis('off') #remove tick marks on axis
    
    config=title[len(title)-1]      #in case only 1 title 
    
    SavePath=os.path.join(PlotPath,'DotPlot_{}_{}.png'.format(FigSet,config))
    
    plt.savefig(SavePath)
    print('File saved: '+SavePath)
    
    plt.close()
    

def FigSettings():
    fields=['Figure width (in):','Figure height (in):', 'Dot Size (pixels^2):',
            'Font size:','Font color (r,g,b,k,w,etc.):','Font x offset (pixels):', 'Font y offset (pixels):',
            'Colormap (jet,cool,turbo,etc.)']
    values=[9,7,200,
            7,'k',-15,-10,
            'jet'] #defaults
    FigSet= easygui.multenterbox(msg='Select figure settings:',fields=fields,values=values)
    return FigSet


#%% Begin Real Script

# read files
XYdat, header, data = Read_files(XY_path)

#run figure settings gui
FigSet=FigSettings()

t0 = time.time() #start timer

#unpack fig settings
FigSize=(float(FigSet[0]),float(FigSet[1])) #fig size
DotSize=float(FigSet[2])        #colored dots size/area (pixels)
FontSize=float(FigSet[3])       #txt size
FontColor=FigSet[4]             #txt color
X0=float(FigSet[5])             #x offset
Y0=float(FigSet[6])             #y offset
cmap=FigSet[7]                  #colormap

# run image scale function
if not YN_LoadSave: Image_Scale(im_path)

#create image scale coordinates
XYdat['X_im']=XYdat.X_FS*Xscale+Dx
XYdat['Y_im']=XYdat.Y_FS*Yscale+Dy

# make plots folder if it doesnt exist
PlotPath=Targdir+'/zDotPlots'
if not os.path.exists(PlotPath):
    os.makedirs(PlotPath)
        
#%% Generate plots

for i in data.columns:
    bounds= header[i][0].split(',')
    title=  header[i][1].split(',')
    DotPlot(data[i], bounds, title)
   
#%% done
elapsed = round(time.time()-t0,1)
easygui.msgbox(msg="Done!\nFiles saved here:\n{}\nProcess took: {} seconds".format(PlotPath,elapsed))


