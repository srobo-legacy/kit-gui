#!/usr/bin/env python

import pygtk
pygtk.require ('2.0')
import gtk
import gobject
import dummylib as srobolib

class Check:
    _label = None
    _checkFunc = None
    IN_PROGRESS_COLOR = "#FFFF00"
    SUCCESS_COLOR = "#0CFF00"
    FAILURE_COLOR = "#FF0000"
    _markup = ""
    
    def __init__ (self, string, checkFunction):
        self._label = gtk.Label ("")
        self._markup = string + ": <b><span foreground=\"" + self.IN_PROGRESS_COLOR + "\">In progress</span></b>"
        self._updateLabel ()
        self._label.set_alignment (0,0)
        self._checkFunc = checkFunction
    
    def addToContainer (self, container):
        #don't expand to fill the screen, instead make checks appear one
        #after the other
        container.pack_start (self._label, expand = False)
        self._label.show_all ()
    
    def doCheck (self):
        checkResult = self._checkFunc ()
        markup = self._markup
        
        #if checkResult is True we passed the test, otherwise we failed
        if checkResult:
            markup = markup.replace (self.IN_PROGRESS_COLOR, self.SUCCESS_COLOR)
            markup = markup.replace ("In progress", "Passed")
        else:
            markup = markup.replace (self.IN_PROGRESS_COLOR, self.FAILURE_COLOR)
            markup = markup.replace ("In progress", "Failed")
        
        self._markup = markup
        self._updateLabel ()
    
    def _updateLabel (self):
        self._label.set_markup (self._markup)

    
def setupChecks (primitiveChecks):
    checks = []
    
    for string, function in primitiveChecks:
        checks.append (Check (string, function))
    
    return checks
    
def showChecks (window, checks):
    checkBox = gtk.VBox ()
    
    for check in checks:
        check.addToContainer (checkBox)
    
    sv = gtk.ScrolledWindow ()
    
    #make the hscrollbar never appear, and the vertical one always appear
    sv.set_policy (gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
    sv.add_with_viewport (checkBox)
    window.add (sv)
    checkBox.show_all ()

def doChecks (checks):

    for check in checks:
        check.doCheck ()
    
    #return false because we only want to be called once
    return False
        
def main ():
    window = gtk.Window (gtk.WINDOW_TOPLEVEL)
    checkList = setupChecks (srobolib.checks)
    showChecks (window, checkList)
    window.show_all ()
    #start the checks in 100ms
    gobject.timeout_add (100, doChecks, checkList)
    gtk.main ()
    
if __name__ == "__main__":
    main ()
    
