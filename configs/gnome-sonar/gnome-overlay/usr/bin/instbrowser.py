#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Install/remove a browser'''

# Release : 1.0
# Date    : 18 Août 2013
# Author  : Esclapion

from os import environ,system
from gi.repository import Gtk
from subprocess import *

listBrowser = [['chromium', False, False], ['firefox', False, False],
               ['rekonq', False, False], ['konqueror', False, False],
               ['midori', False, False], ['opera', False, False],
               ['qupzilla', False, False], ['arora', False, False]]

def notification(message) :
    try :
        s = environ["USER"]
        m = "su " +  s + " -c 'DISPLAY=:0 notify-send \"" + message + "\"'"
        system(m)
    except :
        print("Warning : notification doesnt work")

def browser() :
    res = getstatusoutput("pacman -Qq")
    s = res[1]
    for elem in listBrowser :
        '''Search for the installed browsers'''
        i = s.find(elem[0])
        if i >= 0 :
            elem[1] = True

    class ToggleButtonWindow(Gtk.Window):
        def __init__(self):
            Gtk.Window.__init__(self, title="Browsers list")
            self.set_border_width(10)

            mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=30)
            self.add(mainbox)
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            header = Gtk.Label(label="Click to install or remove a browser")
            vbox.add(header)
    
            for elem in listBrowser :
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
            for elem in listBrowser :
                if elem[0] == name :
                    elem[2] = state
                    break
        def on_button_cancel(self, widget) :
            exit(1)
        def on_button_continue(self, widget) :
            self.destroy()
            Gtk.main_quit()

    win = ToggleButtonWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

    indChange = False
    for elem in listBrowser :
        '''Main loop'''
        if elem[1] == False and elem[2] == True :
            '''Installation'''
            indChange = True
            name = elem[0]
            notification("Installation of " + name)
            if name == "chromium" :
                res = getstatusoutput("pacman -S " + name + " --noconfirm")
            elif name == "firefox" :
                res = getstatusoutput("pacman -S firefox firefox-i18n-fr --noconfirm")
            elif name == "rekonq" :
                res = getstatusoutput("pacman -S " + name + " --noconfirm")
            elif name == "konqueror" :
                res = getstatusoutput("pacman -S kdebase-konqueror --noconfirm")
            elif name == "midori" :
                res = getstatusoutput("pacman -S " + name + " --noconfirm")
            elif name == "opera" :
                res = getstatusoutput("pacman -S " + name + " --noconfirm")
            elif name == "qupzilla" :
                res = getstatusoutput("pacman -S " + name + " --noconfirm")
            elif name == "arora" :
                res = getstatusoutput("pacman -S " + name + " --noconfirm")
            if res[0] != 0 :
                dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                            Gtk.ButtonsType.OK_CANCEL, "Error during installation of " + name)
                dialog.format_secondary_text(res[1])
                response = dialog.run()
                if response == Gtk.ResponseType.CANCEL :
                    exit(1)
            else :
                notification(name + " installed")
        elif elem[1] == True and elem[2] == False :
            '''Removing'''
            # indChange = True
            name = elem[0]
            if name == "chromium" :
                res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
            elif name == "firefox" :
                res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
            elif name == "rekonq" :
                res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
            elif name == "konqueror" :
                res = getstatusoutput("pacman -Rcs kdebase-konqueror --noconfirm")
            elif name == "midori" :
                res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
            elif name == "opera" :
                res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
            elif name == "qupzilla" :
                res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
            elif name == "arora" :
                res = getstatusoutput("pacman -Rcs " + name + " --noconfirm")
            if res[0] != 0 :
                dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                            Gtk.ButtonsType.OK_CANCEL, "Error during removing of " + name)
                dialog.format_secondary_text(res[1])
                response = dialog.run()
                if response == Gtk.ResponseType.CANCEL :
                    exit(1)
            else :
                notification(name + " removed")

    if indChange == True :
        try :
            session = environ["XDG_MENU_PREFIX"][0:-1]
        except :
            print("Unknown session type")
            session = "unknown"
        if session == "gnome" :
            system("killall gnome-shell")

if __name__=="__main__" :

    browser()
