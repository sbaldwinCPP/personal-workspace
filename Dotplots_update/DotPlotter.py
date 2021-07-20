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
#import numpy as np
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
    

t = time.time() #start timer

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
    XYdat=pd.read_excel(XY_path, header=0, usecols=(0,1,2))
    XYdat.columns=('Stack_Rec',
                    'Xpos',
                    'Ypos')
    XYdat.Stack_Rec=XYdat.Stack_Rec.astype('str')       #force to string
    
    #Read 1st 2 rows, used to set cloorbar scale & label, filename
    header=pd.read_excel(XY_path, header=None, nrows=2)
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
    x=float(XYdat[XYdat.Stack_Rec==ID].Xpos)
    y=float(XYdat[XYdat.Stack_Rec==ID].Ypos)
    return x,y

def FS_to_im(x_in,y_in):
    ''' 
    Convert full-scale XY coords into image-scale XY coords

    '''
    xout=x_in*Xscale+Dx
    yout=y_in*Yscale+Dy
    return xout,yout
    
def Get_im_XY(ID):
    ''' 
    Get image-scale XY coordinartes from stack/receptor ID

    '''
    x,y=GetFS_XY(ID)
    X,Y=FS_to_im(x,y)
    return X,Y

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
    
    R1=input('Enter location #1:')
  
    R2=input('Enter location #2:')
  
    
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
    
    # Store data (serialize) as pkl file
    with open(SavePath, 'wb') as handle: pk.dump(ImOut, 
                                                 handle, 
                                                 protocol=pk.HIGHEST_PROTOCOL)    


def DotPlot(series,bounds,*title):
    #make plot function here
    print('do some stuff')
    

    
# =============================================================================
# def Fit_map(df,name,SR):
#     '''
#     Generate the plots this whole script is built for
#     
#     Parameters
#     ----------
#     df : DataFrame
#         Fit File from Read_files()
#     name : String
#         Name of plot.
#     SR : String
#         Type of plot.
# 
#     Returns
#     -------
#     None,
#     Plots saved to target directory
#     '''
#     
#     fig, ax = plt.subplots(figsize=FigSize)
#     ax.imshow(im, 
#               interpolation='spline16'
#               )
#     
#     for i in df.index:
#         
#         #Stack xy pos
#         x,y=Get_im_XY(df.Stack[i])
#         
#         #receptor xy pos (relative to stack)
#         sx,sy=Get_im_XY(df.Rec[i])
#         rx=sx-x
#         ry=sy-y
#         
#         #get wdc in uv coordinates
#         deg=df.WDc[i]-180              # deg points upwind, -180 to point downwind
#         ax,ay=Deg_to_uv(deg)
#         
#         df.loc[i,'x']=x
#         df.loc[i,'y']=y
#         df.loc[i,'rx']=rx
#         df.loc[i,'ry']=ry
#         df.loc[i,'ax']=ax
#         df.loc[i,'ay']=ay
#         df.loc[i,'sx']=sx
#         df.loc[i,'sy']=sy
#         
#         #midpoint locations
#         df.loc[i,'tx']=(x+sx)/2
#         df.loc[i,'ty']=(y+sy)/2
#         
#     #plot green arrow from stack to receptor
#     plt.quiver(df.x,df.y,df.rx,df.ry,
#                     color='lime',
#                     angles='xy',
#                     scale_units='xy',
#                     scale=1,
#                    )
#     
#     #plot color arrow on stack     
#     if SR=='stack':
#         #centered on receptor
#         plt.quiver(df.sx,df.sy,df.ax,df.ay,
#                    df.Cm, cmap=sm.cmap
#                    )
#         
#         #annotations
#         #centered on rec
#         for i in df.index:
#             plt.annotate(df.RunNum[i], (df.sx[i], df.sy[i]+Run_offset), color=Run_color) 
#             #plt.annotate(round(df.Cm[i]), (df.sx[i], df.sy[i]-Cm_offset), color=Cm_color)
#         
#     elif SR=='rec':
#         #centered on stack
#         plt.quiver(df.x,df.y,df.ax,df.ay,
#                    df.Cm, cmap=sm.cmap
#                    )
# 
#         #annotations
#         #centered on stack
#         for i in df.index:
#             plt.annotate(df.RunNum[i], (df.x[i], df.y[i]+Run_offset), color=Run_color) 
#             #plt.annotate(round(df.Cm[i]), (df.x[i], df.y[i]-Cm_offset), color=Cm_color)
#             
#     elif SR=='all':
#         #centered on stack
#         plt.quiver(df.x,df.y,df.ax,df.ay,
#                    df.Cm, cmap=cmap
#                    )
#         
#         #all fits too crowded for annotations, replace with tooltips later
# # =============================================================================
# #         #run num annotations
# #         #centered on stack
# #         for i in df.index:
# #             plt.annotate(df.RunNum[i], (df.x[i], df.y[i]), color='red')
# # =============================================================================
# 
#     #colorbar
#     cb=plt.colorbar(sm)
#     cb.ax.set_title('Cm')
#     
#     plt.axis('off') #remove tick marks on axis
#     
#     SavePath=os.path.join(PlotPath,'Fit_map_'+name+'.png')
#     
#     plt.savefig(SavePath)
#     print('File saved: '+SavePath)
#     
#     plt.close()
# =============================================================================


#%% Begin Real Script

#setup_gui()        #make guis a function later

# read files
XYdat, header,data=Read_files(XY_path)

#%% Plot settings # make this a GUI later

#window size in inches (x,y)
FigSize=(6,8)

cmap=cm.get_cmap('cool')
#cmap=cm.get_cmap('coolwarm')

# =============================================================================
# #annotation text 
# Run_color='k'
# Run_offset=0
# Cm_color='r'
# Cm_offset=0
# =============================================================================

# run image scale function
if not YN_LoadSave: Image_Scale(im_path)

# make plots folder if it doesnt exist
PlotPath=Targdir+'/zFitMaps'
if not os.path.exists(PlotPath):
    os.makedirs(PlotPath)
        
#%% Generate plots

# pull usefull loops out later
# =============================================================================
# if YN_rec:
#     receptors= list(Fits.Rec.drop_duplicates())
#     for rec in receptors:
#         df_in=Fits[Fits.Rec==rec].copy()
#         cbScale(df_in.Cm)
#         Fit_map(df_in, rec, 'rec')
#     
# if YN_stack:
#     stacks= list(Fits.Stack.drop_duplicates())
#     for stack in stacks:
#         df_in=Fits[Fits.Stack==stack].copy()
#         cbScale(df_in.Cm)
#         Fit_map(df_in, stack, 'stack')
# 
# if YN_all:
#     df_in=Fits.copy()
#     cbScale(df_in.Cm)
#     Fit_map(Fits,'All','all')
# =============================================================================
   
#%% done
elapsed = round(time.time()-t,1)
print("Process took: {} seconds".format(elapsed))

input('Press enter to exit')    
    




