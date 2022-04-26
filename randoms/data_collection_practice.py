# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 14:18:52 2022

@author: sbaldwin
"""

#%% modules
try:
    # default packages
    import sys
    import random as rand

    # non-default packages
    import matplotlib.pyplot as plt
    from matplotlib import cm, colors
    import numpy as np
    import easygui
    

except ModuleNotFoundError as err:
    input(str(err) +' \n Press enter to exit')
    
#%% functions
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
        # if a series of WD and WS are passsed
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

def CalcCmErr(fit, WD, U, t):
    c_nom = CalcCm(fit['Cmax'],
                    fit['WDc'],
                    fit['Uc'],
                    fit['A'],
                    fit['B'],
                    WD,
                    U )
    
    if t.lower()=='short' or t.lower()=='s':
        nom_err=10 # % probably a bit more noisy than actual WT, no normal dist.
    if t.lower()=='long' or t.lower()=='l':
        nom_err=3 
    
    err=rand.randint(100 - nom_err, 100 + nom_err)/100
    return c_nom * err

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

    while True:
        # loop until acceptable inputs or cancel button
        # should catch any non-number
        try: 
            inputs = easygui.multenterbox(msg='Confirm/Enter fit parameters:',
                                      fields=fields,
                                      values=values
                                      )
            
            d = {'Cmax':float(inputs[0]),
                      'WDc':float(inputs[1]),
                      'Uc':float(inputs[2]),
                      'A':float(inputs[3]),
                      'B':float(inputs[4]), 
                      }
            
            print(d)
            return d
            break
        
        except:
            if inputs is None: 
                # needed to be able to exit script loop
                print('Goodbye')
                plt.close('all')
                sys.exit()
            else: 
                print('Input error, please try again:')
                next

def GetTrl(fit, WD, WS, Cm, trl):

    fields = ['Wind Direction (deg):',
              'Wind Speed (m/s):',
              'Long or short?:',
              ]
    
    values= ['','','short']
    
    while True:
        # loop until acceptable inputs or cancel button
        # should catch any non-number
        try: 
            inputs = easygui.multenterbox(msg='Sample:', fields=fields, values=values)
            WD.append(float(inputs[0]))
            WS.append(float(inputs[1]))
            trl.append(inputs[2])
            Cm.append(CalcCmErr(fit, WD[-1], WS[-1], trl[-1]))
            print(f"WD={WD[-1]} deg, WS={WS[-1]} m/s, Cm={round(Cm[-1])} trl={trl[-1]}")
            return WD, WS, Cm, trl
            break
        except:
            if inputs is None: 
                print('Exiting run...')
                return None
                break
            else: 
                print('Input error, please try again:')
                next

def ScatPlot(WD, WS, Cm, trl):
    plt.close('all')
    
# =============================================================================
#     # plot styles
#     import matplotlib as mpl
#     mpl.rcdefaults()            # reset to defaults
#     styles=plt.style.available  # save all plot styles to  list
# =============================================================================
    
    # set style
    plt.style.use('seaborn-darkgrid')
    
    # set markers
    s_marker="o"
    l_marker="*"
    markers=[]
    
    for t in trl:
        if t.lower()=='short' or t.lower()=='s':
            markers.append(s_marker)
        if t.lower()=='long' or t.lower()=='l':
            markers.append(l_marker)
        
    fig, ax = plt.subplots(2,1)    
    
    ax[0].set_xlim(0, 360)
    ax[0].set_ylim(0, max(Cm)*1.1)
    ax[0].set_xlabel('WD (deg)')
    ax[0].set_ylabel('Cm')
    
    ax[1].set_xlim(0, 25)
    ax[1].set_ylim(0, max(Cm)*1.1)
    ax[1].set_xlabel('WS (m/s)')
    ax[1].set_ylabel('Cm')
    
    # colorbar setup    
    sm_ws = cbScale([0, 25], 'gist_rainbow')
    sm_wd = cbScale([0, 360], 'prism')
        
    # shorts
    s_index = [i for i, x in enumerate(markers) if x == s_marker]
    size = 20
    for i in s_index:
        ax[0].scatter(WD[i], Cm[i], s=size, color=sm_ws.cmap(sm_ws.norm(WS[i])), marker=s_marker)
        ax[1].scatter(WS[i], Cm[i], s=size, color=sm_wd.cmap(sm_wd.norm(WD[i])), marker=s_marker)

    # longs
    l_index = [i for i, x in enumerate(markers) if x == l_marker]
    size = 100
    for i in l_index:
        ax[0].scatter(WD[i], Cm[i], s=size, color=sm_ws.cmap(sm_ws.norm(WS[i])), marker=l_marker)
        ax[1].scatter(WS[i], Cm[i], s=size, color=sm_wd.cmap(sm_wd.norm(WD[i])), marker=l_marker)
    
    plt.tight_layout()
    plt.show(block=False)


# colorbar setup func
def cbScale(bounds, cmap):
    '''
    use:
    sm = cbScale(bounds, cmap)
    ax.scatter(... , color=sm.cmap(sm.norm(series[i]), ...)
    '''
    s=np.arange(bounds[0],bounds[1]+1,1)
    norm = colors.Normalize()
    norm.autoscale(s)
    sm = cm.ScalarMappable(cmap=cmap,norm=norm)
    sm.set_array([])
    return sm

def mainloop():
    # first pass
    # intitialize lists
    fit = GetFit()
    WD = []
    WS = []
    Cm = []
    trl = []
    
    while True:
        try:
            WD, WS, Cm, trl = GetTrl(fit, WD, WS, Cm, trl)
            ScatPlot(WD, WS, Cm, trl)
            next
        except (TypeError, ValueError):
            print('Starting new run...')
            # reset for another run
            # program can be quit by cancelling GetFit() window
            fit = GetFit()
            WD = []
            WS = []
            Cm = []
            trl = []
            next

#%% Run
if __name__ == '__main__': mainloop()
    
    
    
    

