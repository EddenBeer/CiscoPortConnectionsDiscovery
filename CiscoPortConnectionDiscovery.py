__author__ = 'Ed den Beer'
'''
Created on 19 november 2014
Version 0.0

@author: Ed den Beer - Rockwell Automation
'''

import sys
import datetime

from gi.repository import Gtk

class Main():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('CopyDataToArray.glade')
        # Connect the signals/events from the glade file
        self.builder.connect_signals(self)

        #Get objects from glade file

         #Get the window object and show it
        self.window = self.builder.get_object("applicationwindow1")
        self.window.show_all()
        #Close main when window gets closed
        self.window.connect("destroy", Gtk.main_quit)

        #Declaration of variables

        # its context_id - not shown in the UI but needed to uniquely identify
        # the source of a message
        self.context_id = self.statusbar.get_context_id("status")
        # we push a message onto the statusbar's stack
        self.statusbar.push(self.context_id, "Waiting for you to do something...")



        self.file = None
        FileDialog.open_file(self)
        #Check the response of the dialog
        if FileDialog.get_response(self) == Gtk.ResponseType.OK:
            self.file = FileDialog.get_filename(self)
            self.statusbar.push(self.context_id, self.file)
        else:
            MessageBox.warning('No file is selected', 'Click Generate code again and select a CSV file.')
            self.statusbar.push(self.context_id, 'No file selected')
            return
        #Open the file in a csv reader
        #f = open(self.file)
        #self.reader = csv.reader(f, delimiter=',')

        start = datetime.datetime.now()  #For performance testing
    '''
    Open cisco file

    Open mac adress - ip adres file IP scanner

    For each port find ip adress
    '''


        #Check runtime for performance
        finish = datetime.datetime.now()
        print(finish - start)

##############################################################################################################


class CheckData:
    def int(title, text):
        """
        :param title: Title of message dialog when text is no int
        :param text: The value as a string to be tested if it is an integer
        :return: -1 if test fails, text is not an integer
        """
        try:
            if int(text) >= 0:
                return int(text)
            else:
                MessageBox.error(title, 'Value ' + text + ' is less then 0')
                return -1

        except ValueError:
            MessageBox.error(title, 'Value ' + text + ' is not a number')
            return -1

 ###############################################################################################################

class MessageBox:
    def info(text, text2=None):
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   text)
        if text2 is not None:
            dialog.format_secondary_text(text2)
        dialog.run()
        dialog.destroy()

    def warning(text, text2=None):
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK,
                                   text)
        if text2 is not None:
            dialog.format_secondary_text(text2)
        dialog.run()
        dialog.destroy()

    def error(text, text2=None):
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK,
                                   text)
        if text2 is not None:
            dialog.format_secondary_text(text2)
        dialog.run()
        dialog.destroy()

    def question(text, text2=None):
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO,
                                   text)
        if text2 is not None:
            dialog.format_secondary_text(text2)
        response = dialog.run()
        dialog.destroy()
        return response

# #############################################################################################################


class FileDialog:
    def __init__(self):
        self.filename = None
        self.response = None

    def open_file(self):
        file_open_dialog = Gtk.FileChooserDialog(title="Open CSV file", buttons=(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        FileDialog.add_filters(file_open_dialog)

        self.response = file_open_dialog.run()

        if self.response == Gtk.ResponseType.OK:
            self.filename = file_open_dialog.get_filename()

        file_open_dialog.destroy()

    #Get filename of open file dialog
    def get_filename(self):
        return self.filename

    #Get response of open file dialog
    def get_response(self):
        return self.response

    def add_filters(dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


if __name__ == '__main__':
    main = Main()
    Gtk.main()