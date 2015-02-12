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
        self.builder.add_from_file('glade/CiscoPortConnectionsDiscovery.glade')
        # Connect the signals/events from the glade file
        self.builder.connect_signals(self)

        #Get objects from glade file
        self.cbb_from_switch = self.builder.get_object('cbb_from_switch')
        self.ent_IP_address = self.builder.get_object('ent_IP_address')
        self.ent_password = self.builder.get_object('ent_password')
        self.statusbar_1 = self.builder.get_object('statusbar_1')
        self.statusbar_2 = self.builder.get_object('statusbar_2')

        #Get the window object and show it
        self.window = self.builder.get_object("applicationwindow")
        self.window.show_all()
        #Close main when window gets closed
        self.window.connect("destroy", Gtk.main_quit)

        #Declaration of variables
        self.arp_filename = ''
        self.arp_filename = ''
        self.host_list = []
        self.mac_list = []
        self.port_list = []

        # its context_id - not shown in the UI but needed to uniquely identify
        # the source of a message
        self.context_id = self.statusbar_1.get_context_id("status")
        # we push a message onto the statusbar's stack
        self.statusbar_1.push(self.context_id, "Waiting for you to do something...")

        # its context_id - not shown in the UI but needed to uniquely identify
        # the source of a message
        self.context_id = self.statusbar_2.get_context_id("status")
        # we push a message onto the statusbar's stack
        self.statusbar_2.push(self.context_id, "Press the Start Discovery button")

    def on_btn_quit_clicked(self, *args):
        """
        Close main if button is clicked
        :param args:
        """
        Gtk.main_quit(*args)


    def on_btn_help_clicked(self, button):
        """
        Open help dialog form
        :param button:
        """

    def on_btn_start_clicked(self, button):
        """
        Start discovery process
        :param button:
        :return:
        """
        fd_arp = FileDialog
        fd_arp.open_file(self, 'Select the ARP text file')
        #Check the response of the dialog
        if fd_arp.get_response(self) == Gtk.ResponseType.OK:
            self.arp_filename = fd_arp.get_filename(self)
            self.statusbar_1.push(self.context_id, self.arp_filename)
            self.statusbar_2.push(self.context_id, 'Select mac address file')
        else:
            self.statusbar_1.push(self.context_id, 'No arp file selected')
            self.statusbar_2.push(self.context_id, 'Try again')
            warn = MessageBox.warning
            warn('No file is selected', 'Click Start discovery again and select a ARP file.')
            return
        del fd_arp

        #Open de mac address and arp file generated from the switch
        fd_mac = FileDialog
        fd_mac.open_file(self, 'Select mac address text file')
        #Check the response of the dialog
        if fd_mac.get_response(self) == Gtk.ResponseType.OK:
            self.mac_filename = fd_mac.get_filename(self)
            self.statusbar_2.push(self.context_id, self.mac_filename)
        else:
            self.statusbar_1.push(self.context_id, 'No mac address file selected')
            self.statusbar_2.push(self.context_id, 'Try again')
            warn = MessageBox.warning
            warn('No file is selected', 'Click Start discovery again and select a mac file.')
            return
        del fd_mac

        start = datetime.datetime.now()  #For performance testing

        #Filter the data and store data in host object lists
        arp_file = open(self.arp_filename, 'r')
        for line in arp_file:
            x = line.split()
            for strings in x:
                if strings.find('.') is 3: #a string with 3 dots is the IP address
                    ip = strings
                elif strings.find('.') is 4: #a string with 4 dots is the mac address
                    mac = strings.lower()
                    self.host_list.append(Host(mac, ip))

        #Filter the data and store data in mac object lists
        mac_file = open(self.mac_filename, 'r')
        for line in mac_file:
            x = line.split()
            for strings in x:
                if strings.find('.') is 4: #a string with 4 dots is the mac address
                    mac = strings.lower()
                elif '/' in strings: #If there is a / in the string then this is the port
                    port = strings
                    self.mac_list.append(Mac(mac, port))

        self.mac_list.sort(key=lambda x: x.port) #Sort on port string

        for c in self.mac_list:
            print(c)

        #Clear lists
        self.host_list.clear()
        self.mac_list.clear()

        #Check runtime for performance
        finish = datetime.datetime.now()
        print(finish - start)


class Host():
    """
    :return: string with IP addres, string with mac address
    """
    def __init__(self, ip_address, mac_address):
        self.ip_address = ip_address
        self.mac_address = mac_address
    def __str__(self):
        return "%s%s" % (self.ip_address, self.mac_address)


class Mac():
    """
    :return: string with mac address and port
    """
    def __init__(self, mac_address, port):
        self.mac_address = mac_address
        self.port = port
    def __str__(self):
        return "%s%s" % (self.mac_address, self.port)


class CheckData:
    """
    :param title: Title of message dialog when text is no int
    :param text: The value as a string to be tested if it is an integer
    :return: -1 if test fails, text is not an integer
    """

    def int(title, text):
        try:
            if int(text) >= 0:
                return int(text)
            else:
                MessageBox.error(title, 'Value ' + text + ' is less then 0')
                return -1

        except ValueError:
            MessageBox.error(title, 'Value ' + text + ' is not a number')
            return -1


class MessageBox():
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
        #Get response of open file dialog


class FileDialog:
    def __init__(self):
        self.filename = None
        self.response = None

    def open_file(self, title):
        file_open_dialog = Gtk.FileChooserDialog(title=title, buttons=(
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