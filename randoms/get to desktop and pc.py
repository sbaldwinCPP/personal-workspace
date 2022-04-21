# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 15:23:51 2021

@author: sbaldwin
"""

import os
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

thispc = os.path.join(os.path.join(os.environ['USERPROFILE']), 'This PC')

testpath=os.path.join(desktop,'test.txt')
if os.path.isfile(testpath):
    print('found')

testpath=os.path.join(thispc,'test.txt')

import easygui
#inidir = os.getcwd() #starts file selection at working directory
txt='Select data file...'
ftyp= '*.txt'
#dflt=thispc
dflt=desktop
filepath = easygui.fileopenbox(default=dflt,msg=txt,filetypes=ftyp,multiple=False)
    
    

# =============================================================================
# if os.path.isfile(testpath):
#     print('found')
# =============================================================================
#%%

# =============================================================================
# import string
# from ctypes import windll
# 
# def get_drives():
#     drives = []
#     bitmask = windll.kernel32.GetLogicalDrives()
#     for letter in string.uppercase:
#         if bitmask & 1:
#             drives.append(letter)
#         bitmask >>= 1
# 
#     return drives
# 
# if __name__ == '__main__':
#     print(get_drives())     # On my PC, this prints ['A', 'C', 'D', 'F', 'H']
#     
#     
#     
# #%%
# import win32api
# 
# drives = win32api.GetLogicalDriveStrings()
# drives = drives.split('\000')[:-1]
# print(drives)
# =============================================================================

#%%

import os, string
available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
