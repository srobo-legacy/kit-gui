#!/usr/bin/env python

import pygtk
pygtk.require ('2.0')
import gtk
import gobject
import os

reader = None
PIPE_NAME = "logpipe"

def pump (source, cb_condition):
    reader.readNext ()
    return True

class LogReader:
    _pipe = None
    
    def __init__ (self, pipe):
        self._box = gtk.VBox ()
        self._pipe = pipe
    
    def _addTag (self, text):
        l = gtk.Label (text[0 : len (text) - 1])
        l.set_alignment (0,0)
        self._box.pack_start (l, expand=False)
        l.show ()
    
    def readNext (self):
        line = self._pipe.readline ()
        self._addTag (line)
        print "cows"
    
    def addToWindow (self, window):
        #set the background color to white
        eb = gtk.EventBox ()
        eb.add (self._box)
        sv = gtk.ScrolledWindow ()
        sv.add_with_viewport (eb)
        color = gtk.gdk.color_parse ('#ffffff')
        eb.modify_bg (gtk.STATE_NORMAL, color)
        
        #add and show
        window.add (sv)
    
if __name__ == "__main__":
    global reader
    
    window = gtk.Window (gtk.WINDOW_TOPLEVEL)
    
    #try to make the pipe, if it fails it already exists
    try:
        os.mkfifo (PIPE_NAME)
    except:
        pass
    
    #open the pipe and set up the reader
    pipe = open (PIPE_NAME, "r+", 0)
    reader = LogReader (pipe)
    reader.addToWindow (window)
    
    #change the window background
    color = gtk.gdk.color_parse ('#ffffff')
    window.modify_bg (gtk.STATE_NORMAL, color)
    window.show_all ()
    
    #watch the pipe, and pull data when it's available
    gobject.io_add_watch (pipe, gobject.IO_IN, pump)
    gtk.main ()
