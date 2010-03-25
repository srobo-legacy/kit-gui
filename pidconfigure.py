#!/usr/bin/env python

import pygtk
pygtk.require ('2.0')
import gtk
import dummylib as srobolib

class SwitchableLabel:
    _label = None
    _prefix = ""
    _getter, _setter = None, None
    box = None
    
    def __init__ (self, valueGetter, valueSetter, labelPrefix = ""):
        #setup box, and values for updating
        self.box = gtk.VBox ()
        self._prefix = labelPrefix
        self._getter = valueGetter
        self._setter = valueSetter
        
        #create buttons and connect
        upButton = gtk.Button (label = "+")
        upButton.connect ('activate', self.update, +1)
        
        downButton = gtk.Button (label = "-")
        downButton.connect ('activate', self.update, -1)
        
        #create the label and update it to the current value
        self._label = gtk.Label ("")
        self._updateLabel ()
        
        #add items to the box
        self.box.add (upButton)
        self.box.add (self._label)
        self.box.add (downButton)
        
        
    def addToContainer (self, container):
        container.add (self.box)
        
    def update (self, button, diff):
        currentValue = self._getter ()
        currentValue += diff
        self._setter (currentValue)
        self._updateLabel ()
    
    def _updateLabel (self):
        self._label.set_markup ("<span font=\"sans 24\"><b>" + self._prefix + str (self._getter ()) + "</b></span>")

class PidConfigure:
    _pLabel = None
    
    def __init__ (self, window):
        pSwitcher = SwitchableLabel (srobolib.getPidP, srobolib.setPidP, "P: ")
        iSwitcher = SwitchableLabel (srobolib.getPidI, srobolib.setPidI, "I: ")
        dSwitcher = SwitchableLabel (srobolib.getPidD, srobolib.setPidD, "D: ")
        
        pidBox = gtk.HBox (spacing=10, homogeneous=True)
        pSwitcher.addToContainer (pidBox)
        iSwitcher.addToContainer (pidBox)
        dSwitcher.addToContainer (pidBox)
        
        window.add (pidBox)
        window.show_all()
        
def main ():
    PidConfigure (gtk.Window (gtk.WINDOW_TOPLEVEL))
    gtk.main ()
    
if __name__ == "__main__":
    main ()
