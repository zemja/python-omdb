#!/usr/bin/env python3

# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.3 on Tue Nov  6 13:10:02 2018
#

import json
import os
import sys
import urllib.request
import tempfile
import wx
import math
import webbrowser
import random

import SaveData
import API

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

app = wx.App()

# Name of the script for putting in error messages, probably just python-omdb.py
NAME = os.path.basename(sys.argv[0])

def error(msg, warning = False):
    global NAME
    print(f"{NAME}: {'warning' if warning else 'error'}: {msg}", file=sys.stderr)
    wx.MessageBox(msg, 'Warning' if warning else 'Error', wx.ICON_EXCLAMATION if warning else wx.ICON_ERROR)

# Read their fokin saved data
SAVE_DATA = SaveData.SaveData()

if not SAVE_DATA.from_file:
    error(f"Could not read saved data '{SAVE_DATA.path}.' (Using defaults.)", True)

MOVIE_API = None

if SAVE_DATA.keys['omdb'] is None:
    if SAVE_DATA.keys['tmdb'] is None:
        MOVIE_API = None
    else:
        MOVIE_API = API.TMDB(SAVE_DATA.keys['tmdb'])
else:
    MOVIE_API = API.OMDB(SAVE_DATA.keys['omdb'])

class APIFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: APIFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((630, 180))
        self.radio_btn_omdb = wx.RadioButton(self, wx.ID_ANY, "")
        self.text_ctrl_omdb = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_key_omdb = wx.Button(self, wx.ID_ANY, "Get key")
        self.radio_btn_tmdb = wx.RadioButton(self, wx.ID_ANY, "")
        self.text_ctrl_tmdb = wx.TextCtrl(self, wx.ID_ANY, "")
        self.button_key_tmdb = wx.Button(self, wx.ID_ANY, "Get key")
        self.button_ok = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.get_key_omdb_clicked, self.button_key_omdb)
        self.Bind(wx.EVT_BUTTON, self.get_key_tmdb_clicked, self.button_key_tmdb)
        self.Bind(wx.EVT_BUTTON, self.button_ok_clicked, self.button_ok)
        # end wxGlade

        self.Bind(wx.EVT_CLOSE, self.on_close)

        global SAVE_DATA
        self.text_ctrl_omdb.SetValue(SAVE_DATA.keys['omdb'] or '')
        self.text_ctrl_tmdb.SetValue(SAVE_DATA.keys['tmdb'] or '')

        if type(MOVIE_API) is API.TMDB:
            self.radio_btn_tmdb.SetValue(True)
        else: # Because it might be None
            self.radio_btn_omdb.SetValue(True)

    def __set_properties(self):
        # begin wxGlade: APIFrame.__set_properties
        self.SetTitle("API and keys")
        self.button_ok.SetFocus()
        self.button_ok.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: APIFrame.__do_layout
        sizer_rows = wx.BoxSizer(wx.VERTICAL)
        sizer_tmdb = wx.BoxSizer(wx.HORIZONTAL)
        sizer_omdb = wx.BoxSizer(wx.HORIZONTAL)
        label_heading = wx.StaticText(self, wx.ID_ANY, "Select API and enter keys...")
        sizer_rows.Add(label_heading, 0, wx.ALL, 5)
        sizer_omdb.Add(self.radio_btn_omdb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        label_omdb = wx.StaticText(self, wx.ID_ANY, "OMDb")
        label_omdb.SetMinSize((50, 21))
        sizer_omdb.Add(label_omdb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer_omdb.Add(self.text_ctrl_omdb, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer_omdb.Add(self.button_key_omdb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer_rows.Add(sizer_omdb, 1, wx.EXPAND, 0)
        sizer_tmdb.Add(self.radio_btn_tmdb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        label_tmdb = wx.StaticText(self, wx.ID_ANY, "TMDb")
        label_tmdb.SetMinSize((50, 21))
        sizer_tmdb.Add(label_tmdb, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer_tmdb.Add(self.text_ctrl_tmdb, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer_tmdb.Add(self.button_key_tmdb, 0, wx.ALL, 5)
        sizer_rows.Add(sizer_tmdb, 1, wx.EXPAND, 0)
        sizer_rows.Add(self.button_ok, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.SetSizer(sizer_rows)
        self.Layout()
        # end wxGlade

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler

    def on_close(self, event):
        global MOVIE_API
        global SAVE_DATA
        SAVE_DATA.keys['omdb'] = self.text_ctrl_omdb.GetLineText(0) if self.text_ctrl_omdb.GetLineText(0) else None
        SAVE_DATA.keys['tmdb'] = self.text_ctrl_tmdb.GetLineText(0) if self.text_ctrl_tmdb.GetLineText(0) else None
        if self.radio_btn_omdb.GetValue() and SAVE_DATA.keys['omdb'] is not None:
            MOVIE_API = API.OMDB(SAVE_DATA.keys['omdb'])
        elif self.radio_btn_tmdb.GetValue() and SAVE_DATA.keys['tmdb'] is not None:
            MOVIE_API = API.TMDB(SAVE_DATA.keys['tmdb'])
        else:
            MOVIE_API = None
        self.MakeModal(False)
        event.Skip()

    def get_key_omdb_clicked(self, event):  # wxGlade: APIFrame.<event_handler>
        webbrowser.open('http://www.omdbapi.com/apikey.aspx')
        event.Skip()
    def get_key_tmdb_clicked(self, event):  # wxGlade: APIFrame.<event_handler>
        webbrowser.open('https://www.themoviedb.org/settings/api')
        event.Skip()
    def button_ok_clicked(self, event):  # wxGlade: APIFrame.<event_handler>
        self.Close()
        event.Skip()
# end of class APIFrame
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
        self.list_ctrl_results.InsertColumn(0, "Title", format=wx.LIST_FORMAT_LEFT, width=460)
        self.list_ctrl_results.InsertColumn(1, "Released", format=wx.LIST_FORMAT_LEFT, width=157)
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
        parent = self.GetParent()
        film = self.list_ctrl_results.GetFirstSelected()
        # Make sure a film is really selected.
        if film == -1:
            error('No film selected.')
            event.Skip()
            return
        film = self.results[film]
        if MOVIE_API is None:
            error('No API key for the selected API! Please enter one in Settings -> API and keys.')
            return
        try:
            film[0] = MOVIE_API.imdb_id(film[0])
        except Exception as e:
            error(f'Could not get film info: {str(e)}')
        if parent.add_film(self.results[self.list_ctrl_results.GetFirstSelected()]):
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
        self.SetSize((830, 600))

        # Menu Bar
        self.frame_main_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "API and keys...", "")
        self.Bind(wx.EVT_MENU, self.api_settings_clicked, id=item.GetId())
        self.frame_main_menubar.Append(wxglade_tmp_menu, "Settings")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Get random film", "")
        self.Bind(wx.EVT_MENU, self.random_film_clicked, id=item.GetId())
        self.frame_main_menubar.Append(wxglade_tmp_menu, "Misc")
        self.SetMenuBar(self.frame_main_menubar)
        # Menu Bar end
        self.window_all = wx.SplitterWindow(self, wx.ID_ANY)
        self.window_all_pane_left = wx.Panel(self.window_all, wx.ID_ANY)
        self.list_box_saved = wx.ListBox(self.window_all_pane_left, wx.ID_ANY, choices=[])
        self.search_ctrl_find = wx.SearchCtrl(self.window_all_pane_left, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.button_delete = wx.Button(self.window_all_pane_left, wx.ID_DELETE, "")
        self.window_all_pane_right = wx.ScrolledWindow(self.window_all, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.bitmap_poster = wx.StaticBitmap(self.window_all_pane_right, wx.ID_ANY, wx.EmptyBitmap(135, 205))
        self.label_rating = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, u"\u2605\u2605\u2605\u2605\u2605", style=wx.ALIGN_CENTER)
        self.label_title = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Film Title")
        self.label_genre = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Genre")
        self.label_released = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Released")
        self.label_runtime = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Runtime")
        self.label_director = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Directed by Director")
        self.label_plot = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "A gr8 film.")
        self.label_actors = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Ethan Ansell")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX, self.list_box_saved_clicked, self.list_box_saved)
        self.Bind(wx.EVT_TEXT_ENTER, self.search_ctrl_find_enter_pressed, self.search_ctrl_find)
        self.Bind(wx.EVT_BUTTON, self.button_delete_clicked, self.button_delete)
        # end wxGlade

        # Disable horizontal scrolling
        self.window_all_pane_right.SetScrollRate(0, 10)

        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.do_search, self.search_ctrl_find)

        self.rewrap_labels()

        # Populate the listbox
        self.films = films

        for film in self.films:
            self.list_box_saved.Append(film[1])

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("python-omdb")
        self.search_ctrl_find.SetFocus()
        self.bitmap_poster.SetMinSize((135, 205))
        self.label_rating.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.label_title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.window_all_pane_right.SetScrollRate(10, 10)
        self.window_all.SetMinimumPaneSize(20)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_all = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_right = wx.BoxSizer(wx.VERTICAL)
        self.sizer_plot_actors = wx.BoxSizer(wx.VERTICAL)
        sizer_poster_info = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_title = wx.BoxSizer(wx.VERTICAL)
        sizer_info = wx.BoxSizer(wx.VERTICAL)
        sizer_poster = wx.BoxSizer(wx.VERTICAL)
        sizer_list = wx.BoxSizer(wx.VERTICAL)
        sizer_controls = wx.BoxSizer(wx.HORIZONTAL)
        sizer_list.Add(self.list_box_saved, 1, wx.EXPAND, 0)
        sizer_controls.Add(self.search_ctrl_find, 1, wx.ALL | wx.EXPAND, 3)
        sizer_controls.Add(self.button_delete, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        sizer_list.Add(sizer_controls, 0, wx.EXPAND, 0)
        self.window_all_pane_left.SetSizer(sizer_list)
        sizer_poster.Add(self.bitmap_poster, 0, wx.ALL, 5)
        sizer_poster.Add(self.label_rating, 0, wx.ALL | wx.EXPAND, 5)
        sizer_poster_info.Add(sizer_poster, 0, wx.EXPAND, 0)
        self.sizer_title.Add(self.label_title, 0, wx.ALL, 5)
        static_line_title = wx.StaticLine(self.window_all_pane_right, wx.ID_ANY)
        self.sizer_title.Add(static_line_title, 0, wx.ALL | wx.EXPAND, 5)
        sizer_info.Add(self.label_genre, 0, wx.ALL, 5)
        sizer_info.Add(self.label_released, 0, wx.ALL, 5)
        sizer_info.Add(self.label_runtime, 0, wx.ALL, 5)
        sizer_info.Add(self.label_director, 0, wx.ALL, 5)
        self.sizer_title.Add(sizer_info, 1, wx.EXPAND, 0)
        sizer_poster_info.Add(self.sizer_title, 1, wx.EXPAND, 0)
        self.sizer_right.Add(sizer_poster_info, 0, wx.EXPAND, 0)
        label_plot_heading = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Plot")
        label_plot_heading.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_plot_actors.Add(label_plot_heading, 0, wx.ALL, 5)
        self.sizer_plot_actors.Add(self.label_plot, 0, wx.ALL, 5)
        label_actors_heading = wx.StaticText(self.window_all_pane_right, wx.ID_ANY, "Actors")
        label_actors_heading.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        self.sizer_plot_actors.Add(label_actors_heading, 0, wx.ALL, 5)
        self.sizer_plot_actors.Add(self.label_actors, 0, wx.ALL, 5)
        self.sizer_right.Add(self.sizer_plot_actors, 0, wx.ALL | wx.EXPAND, 0)
        self.window_all_pane_right.SetSizer(self.sizer_right)
        self.window_all.SplitVertically(self.window_all_pane_left, self.window_all_pane_right)
        sizer_all.Add(self.window_all, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_all)
        self.Layout()
        # end wxGlade

    # NOTE: `film` better bloody be a list that looks like ['ID', 'Title'].
    # Returns False if the film is already in the list, and shows an error message. True otherwise.
    def add_film(self, film):
        for list_film in self.films:
            if list_film[0] == film[0]:
                error(f"Film '{film[1]}' is already in the list.")
                return False
        self.films.append(film)
        self.list_box_saved.SetSelection(self.list_box_saved.Append(film[1]))
        self.update_info(film[0])
        self.search_ctrl_find.Clear()
        return True

    def do_search(self, event):  # wxGlade: MainFrame.<event_handler>
        if MOVIE_API is None:
            error('No API key for the selected API! Please enter one in Settings -> API and keys.')
            return
        try:
            frame_find = FindFrame(MOVIE_API.search(event.GetString()), self, wx.ID_ANY, 'Find')
        except Exception as e:
            error(f'Could not search: {str(e)}')
            return
        frame_find.MakeModal()
        frame_find.Show()
        event.Skip()

    def update_info(self, ID):
        if MOVIE_API is None:
            error('No API key for the selected API! Please enter one in Settings -> API and keys.')
            return
        try:
            info = MOVIE_API.get(ID)
        except Exception as e:
            error(f'Could not get movie info: {str(e)}')
            return

        self.label_title.SetLabel(info.title or 'Unknown')
        self.label_genre.SetLabel(info.genre or 'Unknown')
        self.label_released.SetLabel(info.released or 'Unknown')
        self.label_runtime.SetLabel(info.runtime or 'Unknown')
        self.label_director.SetLabel(f"Directed by {info.director or 'Unknown'}")
        self.label_rating.SetLabel(('\u2605' * info.rating) if info.rating is not None else 'Unknown')
        self.label_plot.SetLabel(info.plot or 'Unknown')
        self.label_actors.SetLabel(info.actors or 'Unknown')

        if info.poster is None:
            self.blank_poster()
        else:
            with tempfile.NamedTemporaryFile(suffix = os.path.splitext(info.poster)[1]) as file:
                size = self.bitmap_poster.GetBitmap().GetSize()
                try:
                    # If we can't get the image just show a warning and make the poster blank
                    image = wx.Image(urllib.request.urlretrieve(info.poster, file.name)[0])
                except Exception as e:
                    error(f'Could not get poster: {str(e)}', True)
                    self.blank_poster()
                else:
                    bitmap = wx.Bitmap(image.Scale(size.GetWidth(), size.GetHeight()))
                    self.bitmap_poster.SetBitmap(bitmap)

        # TODO Re-wrap the text when the window resizes/the split changes
        self.rewrap_labels()

        # This is SO STUPID!! for some reason the scroll bars don't appear until you resize the
        # window. And I don't think there's any way to directly send a resize event, so we just make
        # the window a pixel bigger then reset it. (Because SetSize(GetSize()) does nothing.)
        size = self.GetSize()
        self.SetSize((size[0] + 1, size[1] + 1))
        self.SetSize(size)

    def blank_poster(self):
        # Irritatingly we have to create a black poster image ourselves in memory and use that.
        width  = self.bitmap_poster.GetBitmap().GetSize()
        height = width.GetHeight()
        width  = width.GetWidth()
        self.bitmap_poster.SetBitmap(wx.Bitmap.FromBuffer(width, height, bytes([0] * width * height * 3)))

    def rewrap_labels(self):
        # Forgive me, for I have sinned.
        # I have hard-coded these numbers, like a moron, to account for the 5-pixel border around the labels.
        # Because there's no way of getting the border size (that I can find), and I want to enter the borders in wxGlade.
        self.label_title.Wrap(self.window_all_pane_right.GetSize().GetWidth() - self.bitmap_poster.GetSize().GetWidth() - 20)
        self.label_plot.Wrap(self.window_all_pane_right.GetSize().GetWidth() - 10)
        self.label_actors.Wrap(self.window_all_pane_right.GetSize().GetWidth() - 10)

        # Re-do the layout so our big fat labels don't go over each other
        self.window_all_pane_right.Layout()

    def button_delete_clicked(self, event):  # wxGlade: MainFrame.<event_handler>
        selection = self.list_box_saved.GetSelection()
        if selection == -1:
            error('No film selected.')
            return
        self.list_box_saved.Delete(selection)
        del self.films[selection]
        event.Skip()
    def list_box_saved_clicked(self, event):  # wxGlade: MainFrame.<event_handler>
        self.update_info(self.films[self.list_box_saved.GetSelection()][0])
        event.Skip()
    def search_ctrl_find_enter_pressed(self, event):  # wxGlade: MainFrame.<event_handler>
        self.do_search(event)
        event.Skip()
    def api_settings_clicked(self, event):  # wxGlade: MainFrame.<event_handler>
        frame_api = APIFrame(self, wx.ID_ANY, 'API Settings')
        frame_api.MakeModal()
        frame_api.Show()
        event.Skip()
    def random_film_clicked(self, event):  # wxGlade: MainFrame.<event_handler>
        ID = ''
        movie = None
        if MOVIE_API is None:
            error('No API key for the selected API! Please enter one in Settings -> API and keys.')
            return
        for tries in range(1, 5):
            try:
                # TODO Just get a random MOVIE, not random anything
                ID = f'tt{random.randint(1000000, 9999999)}'
                movie = MOVIE_API.get(ID)
            except Exception:
                continue
            break

        if movie is None:
            # Thanks for the helpful error mesage, you dickhead.
            error('Could not get random movie.')
        else:
            self.add_film([ID, movie.title])

        event.Skip()
# end of class MainFrame

frame_main = MainFrame(SAVE_DATA.films, None, wx.ID_ANY, 'python-omdb')
app.SetTopWindow(frame_main)
frame_main.Show()
app.MainLoop()

# TODO Maybe do this before the program has closed, to give the user a chance to try again.
try:
    SAVE_DATA.save()
except Exception as e:
    error(f"Could not write save data: '{str(e)}.'")
