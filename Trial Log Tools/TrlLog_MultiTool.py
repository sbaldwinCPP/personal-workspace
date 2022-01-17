# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 10:20:28 2021

new tool for all things trl.log related
collect existing functions and combine into single "launcher"

@author: sbaldwin
"""

#%% Import
print('Importing modules...')

try:
    #default packages
    import sys
    import os
    import datetime
    #non default packages
    import pandas as pd
    import easygui
    
    print('All modules imported')

except ModuleNotFoundError as err:
    input(str(err) +' \n Press enter to exit')
    sys.exit()

#%% File functions 
def get_TrlLog():
    print('Use GUI to Select trial log...')
    inidir=os.getcwd()
    txt='Select trial log...'
    ftyp= '*trl.log'
    dft=os.path.join(inidir, ftyp)
    filepath = easygui.fileopenbox(default=dft,msg=txt,filetypes=ftyp)
    return filepath

def read_TrlLog(filepath):
    print('Reading trl.log...')
    #read body data
    names= ('RunNum','RunLet','Trial','Long','Operator','StackID','SourceID','Source_Height','Receptor_Number',
            'Wind_Direction','Approach_Config','Anem_Wind_Speed',
            'Bulk_setup_info','Cm','Sd','Date_Time')
    widths=(6,1,7,2,6,5,8,6,10,11,17,4,167,9,9,24)
    df=pd.read_fwf(filepath,skiprows=(13),header=None,names=names,widths=widths)
    df.Cm=df.Cm.replace(',','', regex=True).astype(int)
    df.Sd=df.Sd.replace(',','', regex=True).astype(int)
    df['Date_Time']=pd.to_datetime(df['Date_Time'])
    return df

#%% option functions
def get_option():
    
    options=['WR_QA',
             'Animate_Run',
             'KPI_Report',
             ]
    return easygui.multchoicebox('Select option(s)...','Option Selection',options,preselect=None)

def WR_QA(trl):
    print('do somethin for WR')
    
def Animate_Run(trl):
    print('do somethin animated')
    
def KPI_Report(trl):
    print('do somethin for KPIs') 

### add funtions as options are added


#%% Main
try:
    # get path to file
    filepath='D:\\Repos\\GitHub\\personal-workspace\\Trial Log Tools\\14025trl.log'
    #filepath=get_TrlLog()
    
    # read file
    trl=read_TrlLog(filepath)
    
    # get options
    opt=get_option()
    
    if 'WR_QA' in opt:
        WR_QA(trl)
        
    if 'Animate_Run' in opt:
        Animate_Run(trl)
        
    if 'KPI_Report' in opt:
        KPI_Report(trl)
        
    ### add function calls as options are added 
    
    # test errors
# =============================================================================
#     a=1/0
#     import nothing
#     defined=undefined
# =============================================================================

except BaseException as err:
    input('ERROR: '+ str(err) +' \nPress enter to exit')
    raise

#%% TEST
# =============================================================================
# 
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider
# 
# #fig, ax = plt.subplots()
# fig, ax = plt.subplots(2,1, sharex=True)
# #plt.axis([0, 100, 0, 1000])
# plt.subplots_adjust(bottom=0.25)
# axcolor = 'lightgoldenrodyellow'
# axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
# spos = Slider(axpos, 'Pos', 0.1, df.ID.max())
# 
# df['ID']=df.index
# df.plot(kind='scatter', x='ID', y='Wind_Direction',ax=ax[0], marker='.', c='Cm', cmap='gist_ncar', colorbar=False, label=None)
# df.plot(kind='scatter', x='ID', y='Anem_Wind_Speed',ax=ax[1], marker='.', c='Cm', cmap='cool', colorbar=False, label=None)
# def update(val):
#     pos = spos.val
#     ax[0].axis([pos,pos+300,0,360])
#     ax[1].axis([pos,pos+300,0,df.Anem_Wind_Speed.max()])
#     fig.canvas.draw_idle()
# 
# spos.on_changed(update)
# 
# plt.show()
# 
# #%% og
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider
# 
# fig, ax = plt.subplots()
# 
# plt.subplots_adjust(bottom=0.25)
# 
# t = np.arange(0.0, 100.0, 0.1)
# s = np.sin(2*np.pi*t)
# l, = plt.plot(t,s)
# plt.axis([0, 10, -1, 1])
# 
# axcolor = 'lightgoldenrodyellow'
# axpos = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
# 
# spos = Slider(axpos, 'Pos', 0.1, 90.0)
# 
# def update(val):
#     pos = spos.val
#     ax.axis([pos,pos+10,-1,1])
#     fig.canvas.draw_idle()
# 
# spos.on_changed(update)
# 
# plt.show()
# 
# =============================================================================
