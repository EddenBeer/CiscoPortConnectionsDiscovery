__author__ = 'Ed den Beer'
'''
Created on 19 november 2014
Version 0.0

@author: Ed den Beer - Rockwell Automation
'''

#import sys
import datetime

from gi.repository import Gtk


class Main():
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('glade/CiscoPortConnectionsDiscovery.glade')
        # Connect the signals/events from the glade file
        self.builder.connect_signals(self)

        #Get objects from glade file
        self.chb_from_switch = self.builder.get_object('chb_from_switch')
        self.chb_netscan = self.builder.get_object('chb_netscan')
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
        self.mac_filename = ''
        self.host_list = []
        self.mac_list = []
        self.vendor_list = []
        self.file_list = []
        self.found = False
        self.chb_from_switch_active = False
        self.chb_netscan_active = False

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

    def on_btn_info_clicked(self, button):
        """
        Open info dialog form
        :param button:
        """
        MessageBox.info('Information:','Information text.')

    def on_btn_start_clicked(self, button):
        self.get_data_from_form()  # Get the data from checkbboxes etc. from form
        self.discover()

    def get_data_from_form(self):
        self.chb_from_switch_active = self.chb_from_switch.get_active()
        self.chb_netscan_active = self.chb_netscan.get_active()

    def discover(self):
        """
        Start discovery process
        :param:
        :return:
        """
        if self.select_files() == 1:
            start = datetime.datetime.now()  # For performance testing
            if self.open_arp_file() == 1:
                if self.open_mac_file() == 1:
                    if self.open_vendor_file() == 1:
                        self.add_vendor_to_maclist()
                        self.find_ip_address()
                        #Check runtime for performance
                        finish = datetime.datetime.now()
                        print(finish - start)
                        self.save_result()
        self.clear_lists()

    def select_files(self):
        """
        Select the arp and mac files and store the names
        :param:
        :return:
        """
        #TODO on statusbar display filename only, subtract path
        fd_arp = FileDialog
        fd_arp.open_file(self, 'Select the ARP text file or netscan csv file')
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
            del fd_arp
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
            del fd_mac
            return
        del fd_mac
        return 1

    def connect_to_switch(self):
        """
        Get the data from the switch
        :param:
        :return:
        """
        #TODO write logic to connect to switch

    def get_data_from_switch(self):
         """
        Get the data from the switch
        :param:
        :return:
        """
        #TODO write logic get the data from the switch

    def open_arp_file(self):
        #Open the ARP file
        try:
            arp_file = open(self.arp_filename, 'r')
        except FileNotFoundError:
            error = MessageBox.error
            error('File not found')
            return
        except:
            error = MessageBox.error
            error('Can not open ARP file')
            return

        #Filter the data and store data from file in host object lists
        _append = self.host_list.append  # Make program more readable

        if self.chb_netscan_active:  # Select netscan file or mac file from switch
            try:
                for line in arp_file:  # Netscan file
                    x = line.split(',')
                    for strings in x:
                        if strings.count('.') == 3:  # a string with 3 dots is the IP address
                            ip = strings
                        elif strings.count('-') == 5:  # a string with 5 - is the mac address
                            y = strings.split('-')  # Split string and remove -
                            mac_str = ''.join([y[0], y[1], '.', y[2], y[3], '.', y[4], y[5]]) # Assemble string as Cisco mac address
                            mac = mac_str.lower()
                            _append(Host(ip, mac))
            except:
                error = MessageBox.error
                error('Netscan file error', 'Decode error.')
                return

        else:
            try:
                for line in arp_file:
                    x = line.split()
                    for strings in x:
                        if strings.count('.') == 3:  # a string with3 dots is the IP address
                            ip = strings
                        elif strings.count('.') == 2:  # a string with 2 dots is the mac address
                            mac = strings.lower()
                            _append(Host(ip, mac))
            except:
                error = MessageBox.error
                error('ARP file error', 'Decode error.')
                return
        return 1

    def open_mac_file(self):
        #Open the MAC file
        try:
            mac_file = open(self.mac_filename, 'r')
        except FileNotFoundError:
            error = MessageBox.error
            error('File not found')
            return
        except:
            error = MessageBox.error
            error('Can not open mac file')
            return

        #Filter the data and store data in mac object lists
        _append = self.mac_list.append  #Make program more readable

        try:
            for line in mac_file:
                x = line.split()
                for strings in x:
                    if strings.count('.') == 2:  # a string with 2 : is the mac address
                        mac = strings.lower()
                    elif '/' in strings:  # If there is a / in the string then this is the port
                        port = strings
                        _append(Mac(mac, port, ''))
        except:
            error = MessageBox.error
            error('mac address file error', 'Decode error.')
            return

        self.mac_list.sort(key=lambda x: x.port) #Sort on port string
        return 1

    def open_vendor_file(self):
        #Open the vendor file from Wireshark
        try:
            vendor_file = open('vendor list.txt', 'r')
        except FileNotFoundError:
            error = MessageBox.error
            error('File not found')
            return
        except:
            error = MessageBox.error
            error('Can not open vendor file')
            return

        #For each mac address in the object list, look for the vendor
        _append = self.vendor_list.append  #Make program more readable
        try:
            for line in vendor_file:
                if line.count(':') >= 2:
                    x = line.split()
                    if not '#' in x[0]:
                        if '/' in x[0]:
                            # Remove the / and anything after the /
                            y = x[0].split('/')
                            string = y[0].lower()
                        else:
                            string = x[0].lower()

                        mac = string.replace(':','')  # Remove the : from the mac address
                        vendor = x[1]
                        _append(Vendor(mac, vendor))
        except:
            error = MessageBox.error
            error('vendor file error', 'Decode error.')
            return
        return 1

    def add_vendor_to_maclist(self):
        # Add the vendor to the mac list
        for mac in self.mac_list:
            for vendor in self.vendor_list:
                mac_address = str(mac.mac_address).replace('.','')
                if vendor.mac_address in mac_address:
                    mac.vendor = vendor.vendor
                    break

    def find_ip_address(self):
        #For each mac address in the object list, look trough the host object list to find the IP address
        _append = self.file_list.append  # Make program more readable

        for sw_port in self.mac_list:
            self.found = False
            for host in self.host_list:
                if sw_port.mac_address == host.mac_address:
                    _append(Text(','.join([sw_port.port, host.ip_address, host.mac_address, sw_port.vendor, "\n"])))
                    self.found = True
                    print(sw_port.vendor)
                    break
            if self.found is False:  # If the mac address is not found append with IP unknown
                _append(Text(','.join([sw_port.port, 'Unknown', sw_port.mac_address, sw_port.vendor, "\n"])))

    def save_result(self):
        #Get the filename
        fd = FileDialog
        fd.save_file(self, 'Select a filename:')
        #Check the response of the dialog
        if fd.get_response(self) == Gtk.ResponseType.OK:
            file = open(fd.get_filename(self), "w")
        else:
            MessageBox.warning('No file is selected', 'Start discovery again and select a filename.')
            return
        del fd  # Delete filedialog object

        try:
            for line in self.file_list:  # Write the text to a file
                file.write(str(line))
        except IOError:
            error = MessageBox.error
            error('Not able to write to file, IO error')
            return
        except:
            error = MessageBox.error
            error('Not able to write to file')
            return

        file.close()

    def clear_lists(self):
        #Clear lists
        self.host_list.clear()
        self.mac_list.clear()
        self.file_list.clear()


class Host():
    """
    :return: string with IP address, string with mac address
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
    def __init__(self, mac_address, port, vendor):
        self.mac_address = mac_address
        self.port = port
        self.vendor = vendor

    def __str__(self):
        return "%s%s%s" % (self.mac_address, self.port, self.vendor)


class Vendor():
    """
    :return: string with mac address and vendor
    """
    def __init__(self, mac_address, vendor):
        self.mac_address = mac_address
        self.vendor = vendor

    def __str__(self):
        return "%s%s" % (self.mac_address, self.vendor)


class Text():
    """
    :return: string with the row text for the CSV file
    """
    def __init__(self, row):
        self.row = row

    def __str__(self):
        return "%s" % (self.row)


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

        FileDialog.add_filters_open(file_open_dialog)

        self.response = file_open_dialog.run()

        if self.response == Gtk.ResponseType.OK:
            self.filename = file_open_dialog.get_filename()

        file_open_dialog.destroy()

    def save_file(self, title):
        save_file_dialog = Gtk.FileChooserDialog(title=title, action=Gtk.FileChooserAction.SAVE, buttons=(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        save_file_dialog.set_do_overwrite_confirmation(True) # Ask for conformation if file already exists
        FileDialog.add_filters_save(save_file_dialog)

        self.response = save_file_dialog.run()

        if self.response == Gtk.ResponseType.OK:
            self.filename = save_file_dialog.get_filename()

        save_file_dialog.destroy()

    #Get filename of open file dialog
    def get_filename(self):
        return self.filename

    #Get response of open file dialog
    def get_response(self):
        return self.response

    def add_filters_open(dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        filter_text.add_pattern("*.txt")
        dialog.add_filter(filter_text)

        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("comma separated files")
        filter_csv.add_mime_type("csv")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def add_filters_save(dialog):
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("comma separated files")
        filter_csv.add_mime_type("csv")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        filter_text.add_pattern("*.txt")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

if __name__ == '__main__':
    main = Main()
    Gtk.main()