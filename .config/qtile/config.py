import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy

import arcobattery
#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)



############################################
#                                          #
#       D E F A U L T     A P P S          #
#                                          #
############################################

myTerm = "konsole" # My terminal of choice
myFileManager = "dolphin"
myBrowser = "brave"




keys = [

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "t", lazy.spawn('xterm')),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod], "d", lazy.spawn('nwggrid -p -o 0.4')),
    Key([mod], "s", lazy.spawn("dmenu_run -i -nb '#2C165C' -nf '#ffffff' -sb '#311F89' -sf '#ffffff' -fn 'Poppins:bold:pixelsize=14'")),
    Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn(myTerm)),
    Key([mod], "KP_Enter", lazy.spawn(myTerm)),
    Key([mod], "w", lazy.spawn(myBrowser)),
    Key([mod], "p", lazy.spawn('pamac-manager')),
    Key([mod], "e", lazy.spawn(myFileManager)),
    Key([mod], "x", lazy.shutdown()),

# SUPER + SHIFT KEYS

    Key([mod, "shift"], "Return", lazy.spawn(myFileManager)),
#    Key([mod, "shift"], "d", lazy.spawn(home + '/.config/qtile/scripts/dmenu.sh')),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "shift"], "x", lazy.shutdown()),

# CONTROL + ALT KEYS

    Key(["mod1", "control"], "o", lazy.spawn(home + '/.config/qtile/scripts/picom-toggle.sh')),
    Key(["mod1", "control"], "t", lazy.spawn(myTerm)),
    Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),

# ALT + ... KEYS


    Key(["mod1"], "f", lazy.spawn(myBrowser)),
    Key(["mod1"], "m", lazy.spawn(myFileManager)),
    Key(["mod1"], "w", lazy.spawn('garuda-welcome')),


# CONTROL + SHIFT KEYS

    Key([mod2, "shift"], "Escape", lazy.spawn('lxtask')),


# SCREENSHOTS

    Key([], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
    Key([mod2], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
#    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),

# MULTIMEDIA KEYS

# INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

# INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

#    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
#    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
#    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
#    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

         ### Treetab controls
    Key([mod, "control"], "k",
        lazy.layout.section_up(),
        desc='Move up a section in treetab'
        ),
    Key([mod, "control"], "j",
        lazy.layout.section_down(),
        desc='Move down a section in treetab'
        ),



# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),]

groups = []

group_names = ["1", "2","3","4",]

#group_labels = ["💻","🌎","🎥","🎮",]
group_labels = ["Dev","View","Media","Others",]

group_layouts = ["monadtall", "monadtall","monadtall","monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":10,
            "border_width":2,
            "border_focus": "#ff00ff",
            "border_normal": "#f4c2c2"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(margin=16, border_width=2, border_focus="#ffffff", border_normal="#411f89"),
    layout.MonadWide(margin=16, border_width=2, border_focus="#ffffff", border_normal="#411f89"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Stack(**layout_theme),
    layout.Tile(**layout_theme),
    layout.TreeTab(
        sections=['FIRST', 'SECOND'],
        bg_color = '#141414',
        active_bg = '#411F89',
        inactive_bg = '#2C165C',
        padding_y =5,
        section_top =10,
        panel_width = 280),
    layout.VerticalTile(**layout_theme),
    layout.Zoomy(**layout_theme)
]

# COLORS FOR THE BAR


# MY COLORS
kPurple = "#411F89"
kDarkPurple = "#2C165C"
white = "#FFFFFF"
black = "#000000"
gray = "#7b8088"

def base(fg='text', bg='dark'):
    return {'foreground': white,'background': kDarkPurple}


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Poppins",
                fontsize = 9,
                padding = 2,
                background=kDarkPurple)

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [

                 widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = kDarkPurple,
                        background = kDarkPurple
                        ),              #
               widget.Image(
                       filename = "~/.config/qtile/icons/menu.png",
                       iconsize = 5,
                       background = kDarkPurple,
                       mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('jgmenu_run')}
                       ),
                widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = kPurple,
                        background = kDarkPurple
                        ),
               widget.GroupBox(

            **base(bg=kPurple),
            font='Poppins',

                    fontsize = 11,
                    margin_y = 3,
                    margin_x = 2,
                    padding_y = 5,
                    padding_x = 4,
                    borderwidth = 3,

            active=white,
            inactive=gray,
            rounded= True,
            highlight_method='line',
            highlight_color=['411F89', '282828'],
            urgent_alert_method='block',
            urgent_border=kPurple,
            this_current_screen_border=white,
            this_screen_border=kPurple,
            other_current_screen_border=kDarkPurple,
            other_screen_border=kDarkPurple,
            disable_drag=False
                        ),
                widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = kPurple,
                        background = kDarkPurple
                        ),
                widget.WindowName(
                       foreground = white,
                       background = kDarkPurple,
                       padding = 0,
                       fontsize = 12,
                       font = "Poppins Bold"

                       ),
                widget.TextBox(
                       text = '',
                       background = kDarkPurple,
                       foreground = kPurple,
                       padding = 0,
                       fontsize = 37
                       ),
                widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = white,
                       background = kPurple,
                       padding = 0,
                       scale = 0.7
                       ),
                widget.CurrentLayout(
                      font = "Poppins Bold",
                      fontsize = 12,
                      foreground = white,
                      background = kPurple 
                        ),
                widget.TextBox(
                       text = '',
                       background = kPurple,
                       foreground = kDarkPurple,
                       padding = 0,
                       fontsize = 37
                       ),
                widget.Net(
                         font="Poppins",
                         fontsize=12,
                        # Here enter your network name
                         interface=["wlo1"],
                         format = '{down} ↓↑ {up}',
                         foreground=white,
                         background=kDarkPurple,
                         padding = 0,
                         ),
                widget.TextBox(
                       text = '',
                       background = kDarkPurple,
                       foreground = kPurple,
                       padding = 0,
                       fontsize = 37
                       ), 
                widget.TextBox(
                       text = "🖬 " ,
                       foreground = white,
                       background = kPurple,
                       padding = 0,
                       fontsize = 14
                       ),

                widget.CPU(
                        font="Poppins",
                        #format = '{MemUsed}M/{MemTotal}M',
                        update_interval = 1,
                        fontsize = 12,
                        foreground = white,
                        background = kPurple,
                        mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e htop')},
                       ),
                widget.TextBox(
                       text = '',
                       background = kPurple,
                       foreground = kDarkPurple,
                       padding = 0,
                       fontsize = 37
                       ),
               widget.Memory(
                        font="Poppins",
                        format = '{MemUsed: .0f}M/{MemTotal: .0f}M',
                        update_interval = 1,
                        fontsize = 12,
                        measure_mem = 'M',
                        foreground = white,
                        background = kDarkPurple,
                        mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e htop')},
                       ),
               widget.TextBox(
                       text = '',
                       background = kDarkPurple,
                       foreground = kPurple,
                       padding = 0,
                       fontsize = 37
                       ),

               widget.Clock(
                        foreground = white,
                        background = kPurple,
                        fontsize = 12,
                        font="Poppins Bold",
                        format="%Y-%m-%d %H:%M"
                        ),
               widget.TextBox(
                       text = '',
                       background = kPurple,
                       foreground = kDarkPurple,
                       padding = 0,
                       fontsize = 37
                       ),
               arcobattery.BatteryIcon(
                       padding=0,
                       scale=0.7,
                       y_poss=2,
                       theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
                       update_interval = 5,
                       background = kDarkPurple
                       ),
                widget.Battery(
                        empty_char='x',
                        low_percentage=0.1,
                        font="Poppins Bold",
                        background=kDarkPurple,
                        foreground=white,
                        update_interval=1,
                        show_short_text=False,
                        format='{percent:2.0%}'
                        ),
                widget.TextBox(
                       text = '',
                       background = kDarkPurple,
                       foreground = kPurple,
                       padding = 0,
                       fontsize = 37
                       ),
               widget.Systray(
                       background=kPurple,
                       icon_size=20,
                       padding = 4
                       ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = kPurple,
                        background = kPurple
                        ),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=20, opacity=0.85, background= "000000")),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=20, opacity=0.85, background= "000000"))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #########################################################
#     ################ assgin apps to groups ##################
#     #########################################################
#     d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d["2"] = [ "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl3", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d["3"] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d["4"] = ["Gimp", "gimp" ]
#     d["5"] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d["8"] = ["pcmanfm", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "pcmanfm", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d["0"] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ##########################################################
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),


],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
