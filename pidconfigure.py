#!/usr/bin/env python

import pygtk
pygtk.require ('2.0')
import gtk
import dummylib as srobolib

class SwitchableLabel:
    _label = None
    _prefix = ""
    _getter, _setter = None, None
    #used so that values can be changed quickly
    _changeValues = [1,5,10]
    box = None
    
    def __init__ (self, valueGetter, valueSetter, labelPrefix = ""):
        #setup box, and values for updating
        self.box = gtk.VBox ()
        self._prefix = labelPrefix
        self._getter = valueGetter
        self._setter = valueSetter
        
        #create up buttons and add
        upBox = self._makeButtonBox (True)
        self.box.add (upBox)
        
        #create the label and update it to the current value and add to
        #box
        self._label = gtk.Label ("")
        self._updateLabel ()
        self.box.add (self._label)
        
        #create down buttons and add
        downBox = self._makeButtonBox (False)
        self.box.add (downBox)
        
    def _makeButtonBox (self, up):
        bBox = gtk.VBox (spacing = 5)
        
        if len (self._changeValues) % 2 == 1:
            bBox.add (self._createButton (self._changeValues[0], up))
        
        for i in range (len (self._changeValues) % 2, len (self._changeValues) - 1, 2):
            tBox = gtk.HBox (spacing = 5)
            tBox.add (self._createButton (self._changeValues[i], up))
            tBox.add (self._createButton (self._changeValues[i + 1], up))
            bBox.add (tBox)
        
        return bBox
    
    def _createButton (self, value, up):
        button = None
        if not up:
            value = -value
            button = gtk.Button (label = str (value))
        else:
            button = gtk.Button (label = "+" + str (value))
        button.connect ("activate", self.update, value)
        return button
    
    def addToContainer (self, container):
        container.add (self.box)
        
    def update (self, button, diff):
        currentValue = self._getter ()
        currentValue += diff
        self._setter (currentValue)
        self._updateLabel ()
    
    def _updateLabel (self):
        self._label.set_markup ("<span font=\"sans 32\"><b>" + self._prefix + str (self._getter ()) + "</b></span>")

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
