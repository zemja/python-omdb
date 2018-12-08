#!/usr/bin/env python3

# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.3 on Tue Nov  6 13:10:02 2018
#

import json
import os
import sys
import urllib.request
import wx

from SaveData import SaveData

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

# Name of the script for putting in error messages, probably just python-omdb.py
NAME = os.path.basename(sys.argv[0])

# Read their fokin saved data
# Obviously this will actually be from a file later
try:
    SAVE_DATA = SaveData()
except Exception as e:
    print(f'{NAME}: warning: {str(e)}', file=sys.stderr)
    wx.MessageBox(f'Warning: Could not read saved data: {str(e)}, using defaults', wx.ICON_ERROR)

# Gets info for a movie by IMDb ID
# Just as a string for now for testing
# Returns an empty string if something went wrong
# TODO Implement this properly
def get_info(ID):
    # Error handling is for pussies!
    # (error handling is not actually for pussies, fix this)

    # TODO do all the actual error handling outside of here (set the label to a description of the
    # error when there's an error, for example)

    try:
        response = json.loads(urllib.request.urlopen(f'http://www.omdbapi.com/?apikey={SAVE_DATA.key}&i={ID}').read().decode('utf-8'))
    except Exception as e:
        print(f'{NAME}: error: {str(e)}', file=sys.stderr)
        wx.MessageBox(f'Error: {str(e)}', 'Error', wx.ICON_ERROR)
        return None

    if response["Response"] == "False":
        print(f'{NAME}: error: {response["Error"]}', file=sys.stderr)
        wx.MessageBox(f'Error: {response["Error"]}', 'Error', wx.ICON_ERROR)
        return None

    return f'Title: {response["Title"]}\nID: {response["imdbID"]}\nYear: {response["Year"]}\nActors: {response["Actors"]}\nPlot: {response["Plot"]}'

# TODO Handle errors
def get_search(title):
    return json.loads(urllib.request.urlopen(f'http://www.omdbapi.com/?apikey={SAVE_DATA.key}&s={urllib.parse.quote_plus(title)}').read().decode('utf-8'))

class FindFrame(wx.Frame):
    # NOTE: `results` should be a list of lists, the inner of which comprising 'ID,' 'Title'
    # and 'Year.' So basically it should look like this:
    # [['ABC123', 'The Greatest Film', '2018'], ['XYZ789', 'The Worst Film', '4321'], ...etc...]
    def __init__(self, results, *args, **kwds):
        # begin wxGlade: FindFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((640, 480))
        self.list_ctrl_results = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_AUTOARRANGE | wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, "")
        self.button_add = wx.Button(self, wx.ID_ADD, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.button_cancel_clicked, self.button_cancel)
        self.Bind(wx.EVT_BUTTON, self.button_add_clicked, self.button_add)
        # end wxGlade

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.results = results

        for result in self.results:
            self.list_ctrl_results.Append(result[1:])

    def __set_properties(self):
        # begin wxGlade: FindFrame.__set_properties
        self.SetTitle("Find")
        self.list_ctrl_results.InsertColumn(0, "Title", format=wx.LIST_FORMAT_LEFT, width=470)
        self.list_ctrl_results.InsertColumn(1, "Year", format=wx.LIST_FORMAT_LEFT, width=157)
        self.button_add.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FindFrame.__do_layout
        sizer_all = wx.BoxSizer(wx.VERTICAL)
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
        sizer_all.Add(self.list_ctrl_results, 1, wx.ALL | wx.EXPAND, 0)
        sizer_buttons.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_buttons.Add(self.button_cancel, 0, wx.ALL, 5)
        sizer_buttons.Add(self.button_add, 0, wx.ALL, 5)
        sizer_all.Add(sizer_buttons, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_all)
        self.Layout()
        # end wxGlade

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def on_close(self, event):
        self.MakeModal(False)
        event.Skip()

    def button_cancel_clicked(self, event):  # wxGlade: FindFrame.<event_handler>
        self.Close()
        event.Skip()

    def button_add_clicked(self, event):  # wxGlade: FindFrame.<event_handler>
        # TODO Do something if the film's already there.
        # TODO Do something if there's no film selected.
        parent = self.GetParent()
        parent.add_film(self.results[self.list_ctrl_results.GetFirstSelected()])
        self.Close()
        event.Skip()

# end of class FindFrame

class MainFrame(wx.Frame):
    # NOTE: `films` should be a list of lists, the inner of which having comprising the ID and
    # Title.
    # [['ABC123', 'The Greatest Film'], ['XYZ789', 'The Worst Film'], ...etc...]
    def __init__(self, films, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((640, 480))
        self.window_all = wx.SplitterWindow(self, wx.ID_ANY)
        self.window_all_pane_left = wx.Panel(self.window_all, wx.ID_ANY)
        self.list_box_saved = wx.ListBox(self.window_all_pane_left, wx.ID_ANY, choices=[])
        self.search_ctrl_find = wx.SearchCtrl(self.window_all_pane_left, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.button_delete = wx.Button(self.window_all_pane_left, wx.ID_DELETE, "")
        self.window_all_pane_right = wx.Panel(self.window_all, wx.ID_ANY)
        self.label_info = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "No film selected")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX, self.list_box_saved_clicked, self.list_box_saved)
        self.Bind(wx.EVT_TEXT_ENTER, self.search_ctrl_find_enter_pressed, self.search_ctrl_find)
        self.Bind(wx.EVT_BUTTON, self.button_delete_clicked, self.button_delete)
        # end wxGlade

        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.do_search, self.search_ctrl_find)

        self.films = films

        for film in self.films:
            self.list_box_saved.Append(film[1])

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("python-omdb")
        self.search_ctrl_find.SetFocus()
        self.window_all.SetMinimumPaneSize(20)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_all = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_info = wx.BoxSizer(wx.VERTICAL)
        sizer_list = wx.BoxSizer(wx.VERTICAL)
        sizer_controls = wx.BoxSizer(wx.HORIZONTAL)
        sizer_list.Add(self.list_box_saved, 1, wx.EXPAND, 0)
        sizer_controls.Add(self.search_ctrl_find, 1, wx.ALL | wx.EXPAND, 3)
        sizer_controls.Add(self.button_delete, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_list.Add(sizer_controls, 0, wx.EXPAND, 0)
        self.window_all_pane_left.SetSizer(sizer_list)
        self.sizer_info.Add(self.label_info, 0, wx.ALL | wx.EXPAND, 3)
        self.window_all_pane_right.SetSizer(self.sizer_info)
        self.window_all.SplitVertically(self.window_all_pane_left, self.window_all_pane_right)
        sizer_all.Add(self.window_all, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_all)
        self.Layout()
        # end wxGlade

    # NOTE: `film` better bloody be a list that looks like ['ID', 'Title'].
    def add_film(self, film):
        self.films.append(film)
        self.list_box_saved.SetSelection(self.list_box_saved.Append(film[1]))
        self.update_info(film[0])
        self.search_ctrl_find.Clear()

    def do_search(self, event):  # wxGlade: MainFrame.<event_handler>
        results = []

        response = get_search(event.GetString())

        if response['Response'] == 'False':
            wx.MessageBox(f'Error: {response["Error"]}', 'Error', wx.ICON_ERROR)
            event.Skip()
            return

        for result in response['Search']:
            results.append([result['imdbID'], result['Title'], result['Year']])

        frame_find = FindFrame(results, self, wx.ID_ANY, 'Find')
        frame_find.MakeModal()
        frame_find.Show()
        event.Skip()

    def update_info(self, ID):
        result = get_info(ID)

        if result is None:
            self.label_info.SetLabel('<ERROR>')
        else:
            self.label_info.SetLabel(result)

        self.sizer_info.Layout() # reloads everything to show the new label text

    def button_delete_clicked(self, event):  # wxGlade: MainFrame.<event_handler>
        # TODO do something if there's no film selected
        selection = self.list_box_saved.GetSelection()
        self.list_box_saved.Delete(selection)
        del self.films[selection]
        event.Skip()
    def list_box_saved_clicked(self, event):  # wxGlade: MainFrame.<event_handler>
        self.update_info(self.films[self.list_box_saved.GetSelection()][0])
        event.Skip()
    def search_ctrl_find_enter_pressed(self, event):  # wxGlade: MainFrame.<event_handler>
        self.do_search(event)
        event.Skip()
# end of class MainFrame

# app = wx.PySimpleApp()
app = wx.App()
frame_main = MainFrame(SAVE_DATA.films, None, wx.ID_ANY, "python-omdb")
app.SetTopWindow(frame_main)
frame_main.Show()
app.MainLoop()

# TODO Maybe do this before the program has closed, to give the user a chance to try again.
try:
    SAVE_DATA.save()
except Exception as e:
    print(f'{NAME}: error: {str(e)}', file=sys.stderr)
    wx.MessageBox(f'Error: Could not write save data: {str(e)}', 'Error', wx.ICON_ERROR)
