# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
mod2 = "mod1"
myTerm = "kitty"                             # My terminal of choice

keys = [
         ## My keybinds
         #bindsym Mod1+Tab exec --no-startup-id rofi -modi combi -combi-modi window -show combi
         Key([mod2], "Tab",
             lazy.spawn("rofi -modi combi -combi-modi window -show combi -theme merah"),
             desc='Launches rofi alt-tab solution'
             ),
         Key([mod], "e",
             lazy.spawn("exec ~/Downloads/Github_Clones/dmscripts/dmconf"),
             desc="Launch dmenu config launcher"
             ),
         ### The essentials
         Key([mod], "Return",
             lazy.spawn("kitty"),
             desc='Launches My Terminal'
             ),
         Key([mod], "b",
             lazy.spawn("firefox"),
             desc='Launches browser'
             ),
         Key([mod], "r",
             #lazy.spawn("dmenu_run -p 'Run: '"),
             #lazy.spawn("rofi -show drun -config ~/.config/rofi/themes/dt-dmenu.rasi -display-drun \"Run: \" -drun-display-format \"{name}\""),
             lazy.spawn("rofi -show drun -theme merah"),
             desc='Run Launcher'
             ),
         Key([mod], "d",
             lazy.spawn("dmenu_run -p 'Run: '"),
             desc="dmenu run launcher"
             ),
         Key([mod], "space",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key(["control", "shift"], "e",
             lazy.spawn("emacsclient -c -a emacs"),
             desc='Doom Emacs'
             ),
         ### Switch focus to specific monitor (out of three)
         #Key([mod], "w",
         #    lazy.to_screen(0),
         #    desc='Keyboard focus to monitor 1'
         #    ),
         #Key([mod], "e",
         #    lazy.to_screen(1),
         #    desc='Keyboard focus to monitor 2'
         #    ),
         #Key([mod], "r",
         #    lazy.to_screen(2),
         #    desc='Keyboard focus to monitor 3'
         #    ),
         ### Switch focus of monitors
         Key([mod, "shift"], "z",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod,"shift"], "x",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
             #Switch Workspace Directionally
         Key([mod], "Left",
             lazy.screen.prev_group(),
             desc='Move focus to prev monitor'
             ),
         Key([mod], "Right",
             lazy.screen.next_group(),
             desc='Move focus to prev monitor'
             ),
         ### Treetab controls
         Key([mod, "control"], "k",
             lazy.layout.section_up(),
             desc='Move up a section in treetab'
             ),
         Key([mod, "control"], "j",
             lazy.layout.section_down(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "x",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "z",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "control"], "x",
             lazy.layout.shuffle_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "control"], "z",
             lazy.layout.shuffle_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod2], "z",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod2], "x",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
       #  Key([mod, "shift"], "f",
       #      lazy.window.toggle_floating(),
       #      desc='toggle floating'
       #      ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "space",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
         #Key([mod], "space",
         #    lazy.layout.next(),
         #    desc='Switch window focus to other pane(s) of stack'
         #    ),
         Key([mod, "control"], "Return",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
         # Emacs programs launched using the key chord CTRL+e followed by 'key'
         KeyChord(["control"],"e", [
             Key([], "e", lazy.spawn("emacsclient -c -a 'emacs'")),
             Key([], "b", lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'")),
             Key([], "d", lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'")),
             Key([], "i", lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'")),
             Key([], "m", lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'")),
             Key([], "n", lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'")),
             Key([], "s", lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'")),
             Key([], "v", lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"))
         ]),
         # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
#         KeyChord([mod], "p", [
#             Key([], "e", lazy.spawn("./dmscripts/dmconf")),
#             Key([], "i", lazy.spawn("./dmscripts/dmscrot")),
#             Key([], "k", lazy.spawn("./dmscripts/dmkill")),
#             Key([], "l", lazy.spawn("./dmscripts/dmlogout")),
#             Key([], "m", lazy.spawn("./dmscripts/dman")),
#             Key([], "r", lazy.spawn("./dmscripts/dmred")),
#             Key([], "s", lazy.spawn("./dmscripts/dmsearch")),
#             Key([], "p", lazy.spawn("passmenu"))
#         ])
]

group_names = [("WWW", {'layout': 'monadtall'}), #Workspace list
               ("DOC", {'layout': 'monadtall'}),
               ("GAMES", {'layout': 'floating'}),
               ("COMMS", {'layout': 'monadtall'}),
               ("MP3", {'layout': 'monadtall'}),
               ("MP4", {'layout': 'monadtall'}),
               ("DEV", {'layout': 'monadtall'}),
               ("MISC", {'layout': 'monadtall'}),
               ("SYS", {'layout': 'monadtall'})]

group_indeces = {1:group_names[0][0],
                 2:group_names[1][0],
                 3:group_names[0][0],
                 4:group_names[3][0],
                 5:group_names[4][0],
                 6:group_names[5][0],
                 7:group_names[6][0],
                 8:group_names[7][0],
                 9:group_names[8][0],
                 }

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    #keys.append(Key([mod], "Left", lazy.group[group_indeces[i - 1]].to_screen())) #Scuffed
    #keys.append(Key([mod], "Right", lazy.group[group_indeces[i + 1]].to_screen()))
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

#use arrow keys to change workspaces?
#for i, (name, kwargs) in enumerate(group_names, 1):
#
#keys.append(Key([mod], "Left", lazy.group[group_indeces[i - 1]].to_screen()))
#keys.append(Key([mod], "Right", lazy.group[group_indeces[i + 1]].to_screen()))
layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "f2ca3c",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    #layout.TreeTab(
    #     font = "Ubuntu",
    #     fontsize = 10,
    #     sections = ["FIRST", "SECOND"],
    #     section_fontsize = 11,
    #     bg_color = "141414",
    #     active_bg = "90C435",
    #     active_fg = "000000",
    #     inactive_bg = "384323",
    #     inactive_fg = "a0a0a0",
    #     padding_y = 5,
    #     section_top = 10,
    #     panel_width = 320
    #     ),
    layout.Floating(**layout_theme)
]

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#f2ca3c", "#f2ca3c"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#3973a5", "#3973a5"], # color for the 'even widgets'
          ["#2cbff7", "#2cbff7"]] # window name

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Image(
                       filename = "~/.config/qtile/icons/python.png",
                       scale = "False",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
                       ),
             widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 9,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "Ubuntu Mono",
                       padding = 10,
                       foreground = colors[3],
                       background = colors[1]
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 40,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[4],
                       padding = -7,
                       fontsize = 50
                       ),
              #widget.TextBox(
              #         text = " ₿",
              #         padding = 0,
              #         foreground = colors[2],
              #         background = colors[4],
              #         fontsize = 12
              #         ),
              #widget.BitcoinTicker(
              #         foreground = colors[2],
              #         background = colors[4],
              #         padding = 5
              #         ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -7,
                       fontsize = 50
                       ),
              widget.TextBox(
                       text = " 🌡",
                       padding = 2,
                       foreground = colors[2],
                       background = colors[5],
                       fontsize = 11
                       ),
              widget.ThermalSensor(
                       foreground = colors[2],
                       background = colors[5],
                       threshold = 90,
                       padding = 5
                       ),
              widget.TextBox(
                       text='',
                       background = colors[5],
                       foreground = colors[4],
                       padding = -7,
                       fontsize = 50
                       ),
              widget.TextBox(
                       text = " ⟳",
                       padding = 2,
                       foreground = colors[2],
                       background = colors[4],
                       fontsize = 14
                       ),
              widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "{updates} Updates",
                       foreground = colors[2],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       background = colors[4]
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -7,
                       fontsize = 50
                       ),
              widget.TextBox(
                       text = " 🖬",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0,
                       fontsize = 14
                       ),
              widget.Memory(
                       foreground = colors[2],
                       background = colors[5],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       padding = 5
                       ),
              widget.TextBox(
                       text='',
                       background = colors[5],
                       foreground = colors[4],
                       padding = -7,
                       fontsize = 50
                       ),
              widget.Net(
                       interface = "enp34s0",
                       format = '{down} ↓↑ {up}',
                       foreground = colors[2],
                       background = colors[4],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -7,
                       fontsize = 50
                       ),
              widget.TextBox(
                      text = " Vol:",
                       foreground = colors[2],
                       background = colors[5],
                       padding = 0
                       ),
              widget.Volume(
                       foreground = colors[2],
                       background = colors[5],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[5],
                       foreground = colors[4],
                       padding = -7,
                       fontsize = 50
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[4],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[4],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -7,
                       fontsize = 50
                       ),
              widget.Clock(
                       foreground = colors[2],
                       background = colors[5],
                       format = "%A, %B %d - %l:%M:%S "
                       ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),  # tastyworks exit box
    Match(title='Qalculate!'),  # qalculate-gtk
    Match(wm_class='kdenlive'),  # kdenlive
    Match(wm_class='pinentry-gtk-2'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
