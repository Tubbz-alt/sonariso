#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Install/remove a libreoffice module'''

# Release : 1.0
# Date    : 30 Août 2013
# Author  : Esclapion

import os
from gi.repository import Gtk
from subprocess import *

listModules = [['libreoffice-writer', False, False],
               ['libreoffice-calc', False, False],
               ['libreoffice-impress', False, False],
               ['libreoffice-draw', False, False],
               ['libreoffice-math', False, False],
               ['libreoffice-base', False, False]]

def notification(message) :
    try :
        s = os.environ["USER"]
        m = "su " +  s + " -c 'DISPLAY=:0 notify-send \"" + message + "\"'"
        os.system(m)
    except :
        print("Warning : notification doesnt work")

def install(name) :
    notification("Installation of " + name)
    res = getstatusoutput("pacman -S " + name + " --noconfirm --needed")
    if res[0] != 0 :
        dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK_CANCEL, "Error during installation of " + name)
        dialog.format_secondary_text(res[1])
        response = dialog.run()
        if response == Gtk.ResponseType.CANCEL :
            exit(1)
    else :
        notification(name + " installed")

def namePackLang () :
    try :
        lang = os.environ["LANG"]
    except :
        print("Warning : variable LANG not set !")
        return ""
    i = lang.find('_')
    ext = lang[0:i]
    if ext == "en" or ext == "zh" :
        ext = ext + '-' + lang[i+1:i+3]
    return "libreoffice-" + ext

def module() :
    res = getstatusoutput("pacman -Qq")
    s = res[1]
    for elem in listModules :
        '''Search for the installed modules'''
        i = s.find(elem[0])
        if i >= 0 :
            elem[1] = True

    class ToggleButtonWindow(Gtk.Window):
        def __init__(self):
            Gtk.Window.__init__(self, title="Modules list")
            self.set_border_width(10)

            mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
            self.add(mainbox)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            header = Gtk.Label(label="Click to install or remove a module")
            vbox.add(header)
    
            for elem in listModules :
                name = str(elem[0])
                button = Gtk.ToggleButton(name)
                button.connect("toggled", self.on_button_toggled, name)
                button.set_active(elem[1])
                vbox.pack_start(button, True, True, 0)
            mainbox.add(vbox)

            hbox = Gtk.Box(True, spacing = 150)
            button1 = Gtk.Button(label=" Cancel ")
            button1.connect("clicked", self.on_button_cancel)
            hbox.add(button1)
            button2 = Gtk.Button(label="Continue")
            button2.connect("clicked", self.on_button_continue)
            hbox.add(button2)
            mainbox.add(hbox)

    
        def on_button_toggled(self, button, name):
            if button.get_active():
                state = True
            else:
                state = False
            for elem in listModules :
                if elem[0] == name :
                    elem[2] = state
                    break
        def on_button_cancel(self, widget) :
            exit(1)
        def on_button_continue(self, widget) :
            self.destroy()
            Gtk.main_quit()


# ------------ #
# Main program #
# ------------ #
    if os.geteuid() != 0 :
        print("Error : root privileges are required for running libreoffice installer.")
        print("Use gksu ...")
        exit(1)
    win = ToggleButtonWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

    indNewInstall = True
    indEmpty = True
    try :
        testenv = os.environ["XDG_CURRENT_DESKTOP"]
    except :
        testenv = ""
    for elem in listModules :
        '''Test if nothing installed'''
        if elem[1] == True :
            indNewInstall = False
        if elem[2] == True :
            indEmpty = False
    if indNewInstall == True  and indEmpty == False :
        name = namePackLang ()
        if name == "" :
            print("Warning : problem with language pack installation")
        else :
            install(name)
        if testenv != "KDE" :
            install("libreoffice-gnome")
        
    indChange = False
    for elem in listModules :
        '''Main loop'''
        if elem[1] == False and elem[2] == True :
            '''Installation'''
            indChange = True
            name = elem[0]
            install(elem[0])
        elif elem[1] == True and elem[2] == False :
            '''Removing'''
            indChange = True
            name = elem[0]
            res = getstatusoutput("pacman -Rcs " + name +
                                  " --noconfirm")
            if res[0] != 0 :
                dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                            Gtk.ButtonsType.OK_CANCEL, "Error during removing of " + name)
                dialog.format_secondary_text(res[1])
                response = dialog.run()
                if response == Gtk.ResponseType.CANCEL :
                    exit(1)
            else :
                notification(name + " removed")

    if indEmpty == True and indChange == True :
        name = namePackLang ()
        res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
        notification(name + " removed")
        if testenv != "KDE" :
            res = getstatusoutput("pacman -Rcs libreoffice-gnome --noconfirm")
            notification("libreoffice-gnome removed")


if __name__=="__main__" :

    module()
