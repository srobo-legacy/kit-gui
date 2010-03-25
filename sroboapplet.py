#!/usr/bin/python
import pygtk
pygtk.require ('2.0')
import gtk
import subprocess
from time import sleep

RIGHT_CLICK = 3

class SroboTray:
    _currentIndex = 0
    
    _apps = [
             ("Log Checker", ["./logreader.py"]), 
             ("PID configure", ["./pidconfigure.py"])
            ]
            
    _currentLabel = None
    _sleepTime = 0.10
    
    def __init__ (self):
        self.statusIcon = gtk.StatusIcon ()
        self.statusIcon.set_from_stock (gtk.STOCK_ABOUT)
        self.statusIcon.set_visible (True)
        self.statusIcon.set_tooltip ("srobo menu")
        
        i = 0
        self.menu = gtk.Menu ()
        
        for title, command in self._apps:
            subprocess.Popen (command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            sleep (self._sleepTime)
            self.menuItem = gtk.MenuItem (title)
            self.menuItem.connect ('activate', self.flip, self.statusIcon, i)
            self.menu.append (self.menuItem)
            
            if (i == len (self._apps) -1 ):
                label = self.menuItem.get_children ()[0]
                title = label.get_text ()
                label.set_markup ("<b>" + title + "</b>")
                self._currentIndex = i
                self._currentLabel = label
                
            i += 1

        self.statusIcon.connect ('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible (1)

        gtk.main()
    
    def _selectPrevWindow (self):
        subprocess.Popen (["matchbox-remote", "-prev"])
    
    def _selectNextWindow (self):
        subprocess.Popen (["matchbox-remote", "-next"])
    
    def flip (self, widget, event, data = None):
        indexdiff = data - self._currentIndex
        
        if (indexdiff < 0):
            for i in range (0, indexdiff, -1):
                self._selectPrevWindow ()
                
        elif (indexdiff > 0):
            for i in range (0, indexdiff, 1):
                self._selectNextWindow ()
        
        label = widget.get_children ()[0]
        oldtitle = self._currentLabel.get_text ()
        self._currentLabel.set_markup (oldtitle)
        title = label.get_text ()
        label.set_markup ("<b>" + title + "</b>")
        self._currentIndex = data
        self._currentLabel = label

    def popup_menu_cb (self, widget, button, time, data = None):
        if button == RIGHT_CLICK:
            if data:
                data.show_all ()
                data.grab_focus () 
                data.popup (None, None, gtk.status_icon_position_menu, 3, time, self.statusIcon)

if __name__ == "__main__":
  
  helloWord = SroboTray ()
