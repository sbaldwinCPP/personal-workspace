# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 14:18:52 2022

@author: sbaldwin
"""

# modules
try:
    # default packages
    import sys
    import random as rand

    # non-default packages
    import matplotlib.pyplot as plt
    import numpy as np
    import easygui
    

except ModuleNotFoundError as err:
    input(str(err) +' \n Press enter to exit')
    
# functions
def CalcCm(Cmax,WDc,Uc,A,B,WD,U):
    '''
    Calculate normalized concentration given fit parameters and 
    any Wind Speed and Wind Direction (single pair or series)
    '''
    try:
        # if a single WD and WS are passsed (tests)
        WD_Bias = WD-WDc
        if WD_Bias > 180: WD_Bias = 360 - WD_Bias
        elif WD_Bias < -180: WD_Bias = WD_Bias + 360
        if U==0: Cm=0
        else: Cm = Cmax * np.exp((-A)*((1/U)-(1/Uc))**2) * np.exp(-(((WD_Bias)/B)**2))
        return Cm
    except ValueError:
        #if a series of WD and WS are passsed
        Cm=np.zeros(len(WD))   
        for i in range(len(WD)):
            if U[i] == 0: 
                Cm[i] = 0
            else:
                WD_Bias = WD[i]-WDc
                if WD_Bias > 180: WD_Bias = 360 - WD_Bias
                elif WD_Bias < -180: WD_Bias = WD_Bias + 360
                Cm[i] = Cmax * np.exp((-A)*((1/U[i])-(1/Uc))**2) * np.exp(-(((WD_Bias)/B)**2))      
        return Cm


def GetFit():
    print('Use GUI to enter fit parameters...')
    fields = ['Peak Cm:',
            'Peak Wind Direction (deg):',
            'Peak Wind Speed (m/s):', 
            'A Coefficient (ws):',
            'B Coeficient (wd):',
            ]

    ucrit= rand.randint(1, 25)
     
    values = [rand.randint(25, 1500),               
              rand.randint(0, 359),                
              ucrit,              
              rand.randint(1, (ucrit+1)**2),              
              rand.randint(10, 80),          
              ]
    
    inputs = easygui.multenterbox(msg='Enter criteria settings:',
                              fields=fields,
                              values=values
                              )
    if inputs is None: sys.exit()
    
    d = {'Cmax':float(inputs[0]),
              'WDc':float(inputs[1]),
              'Uc':float(inputs[2]),
              'A':float(inputs[3]),
              'B':float(inputs[4]),
              }
    print(d)
    return d

def CalcCmErr(fit, WD, U):
    c_nom = CalcCm(fit['Cmax'],
                    fit['WDc'],
                    fit['Uc'],
                    fit['A'],
                    fit['B'],
                    WD,
                    U )
    nom_err=10 # % probably a bit more noisy than actual WT, no normal dist.
    err=rand.randint(100 - nom_err, 100 + nom_err)/100
    return c_nom * err

def GetTrl(WD, WS, Cm):

    fields = ['Sample Wind Direction (deg):',
              'Sample Wind Speed (m/s):', ]

    inputs = easygui.multenterbox(msg='Trial:', fields=fields)
    
    if inputs is None: return None, None, None
    else:
        try:
            WD.append(float(inputs[0]))
            WS.append(float(inputs[1]))
            Cm.append(CalcCmErr(fit, WD[-1], WS[-1]))
            print(f"WD={inputs[0]} deg, WS={inputs[1]} m/s, Cm={round(Cm[-1])}")
            return WD, WS, Cm
        except ValueError:
            # should catch any non-number
            return None, None, None

def ScatPlot(WD, WS, Cm):
    # plot settings
    #mpl.rcdefaults()            # reset to defaults
    styles=plt.style.available  # save all plot styles to  list
    plt.style.use(styles[14])   # set style
        
    fig, ax = plt.subplots(2,1)
    ax[0].set_xlim(0, 360)
    ax[0].set_ylim(0, max(Cm)*1.1)
    ax[0].set_xlabel('WD (deg)')
    ax[0].set_ylabel('Cm')
    
    
    ax[1].set_xlim(0, 25)
    ax[1].set_ylim(0, max(Cm)*1.1)
    ax[1].set_xlabel('WS (m/s)')
    ax[1].set_ylabel('Cm')
    
    #cmap='nipy_spectral'
    cmap='prism'
    ax[0].scatter(WD, Cm, c=WS, cmap=cmap)
    ax[1].scatter(WS, Cm, c=WD, cmap=cmap)
    
    plt.tight_layout()
    plt.show()


#%% Run
fit = GetFit()

# first pass
# intitialize lists for data set
WD = []
WS = []
Cm = []

while True:
    WD, WS, Cm = GetTrl(WD, WS, Cm)
    if WD is None or WS is None or Cm is None: 
        fit = GetFit()
        WD = []
        WS = []
        Cm = []
        WD, WS, Cm = GetTrl(WD, WS, Cm)
    ScatPlot(WD, WS, Cm)
    
    

