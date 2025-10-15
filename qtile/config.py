# Dqtai's configuration.

import os
from typing import List  # noqa: F401
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

VOLUME_SCRIPT = os.path.expanduser("~/Documents/volume.sh")

mod = "mod4"
terminal = "kitty"

keys = [
    # Switch window's focus
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key(["mod1"], "tab", lazy.layout.next()),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize(),
        desc="Reset all window sizes"),

    Key([mod], "return", lazy.spawn(terminal),
        desc="Launch terminal"),

    Key([mod], "w", lazy.window.kill(),
        desc="Kill focused window"),
        
    Key([mod, "control"], "r", lazy.reload_config(),
        desc="Reload the config"),
        
    Key([mod, "control"], "q", lazy.shutdown(),
        desc="Shutdown Qtile"),
        
    Key([mod], "p", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    Key([mod], "f", lazy.window.toggle_fullscreen(),
		desc="Toggle fullscreen"),

    Key([mod], "b", lazy.hide_show_bar(position='all'),
		desc="Toggle bar"),

    # To suspend computer
    Key([mod], "F9", lazy.spawn("systemctl suspend -i")),

    # To reboot computer
    Key([mod], "F10", lazy.spawn("systemctl reboot")),

    # To shutdown computer
    Key([mod], "F11", lazy.spawn("systemctl poweroff")),
    

    # My custom keybinds
    # Volume
    Key([mod], "KP_Multiply", lazy.spawn(f"{VOLUME_SCRIPT} up")),
    Key([mod], "KP_Divide", lazy.spawn(f"{VOLUME_SCRIPT} down")),
    Key([mod], "m", lazy.spawn(f"{VOLUME_SCRIPT} toggle")),
    
    Key([], "XF86AudioRaiseVolume", lazy.spawn(f"{VOLUME_SCRIPT} up")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(f"{VOLUME_SCRIPT} down")),
    Key([], "XF86AudioMute", lazy.spawn(f"{VOLUME_SCRIPT} toggle")),

    # To run rofi-wifi-menu.sh
    Key([mod], "F12", lazy.spawn(os.path.expanduser ("bash /home/user/Documents/rofi-wifi-menu.sh"))),
    
    # To take screenshots, fullscreen
    Key([], "Print", lazy.spawn("flameshot full --path /home/user")),
    
    # To take screenshots, GUI
    Key(["Shift"], "Print", lazy.spawn("flameshot gui")),

    # To open Rofi
    Key([mod], "r", lazy.spawn("rofi -show drun")),

    # To open Thunar
    Key([mod], "e", lazy.spawn("thunar")),

    # To open Browser
    Key([mod], "v", lazy.spawn("~/Documents/Helium.AppImage")),


]
groups = [
    Group('1', label='●'),
    Group('2', label='●'),
    Group('3', label='●'),
    Group('4', label='●'),
    Group('5', label='●'),
    Group('6', label='●'),
    Group('7', label='●'),
    Group('8', label='●'),
    Group('9', label='●'),
]

# Allows to switch groups
for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),
        # mod + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])



layouts = [
    layout.Columns(
        border_width = 0,
        border_focus = '#97979e',
        border_focus_stack = '#97979e',
        border_normal = '#000000',
        change_size = 10,
        margin = 16
        ),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

screens = [
    # Primary screen
    Screen(
        wallpaper='~/.config/qtile/background.jpg',
        wallpaper_mode='stretch',
        top=bar.Bar(
            [
                widget.Spacer(length=8),
                widget.GroupBox(
                    font='Noto Sans',
                    background='#000000',
                    active='#97979e',
                    inactive='#5f5f5e',
                    this_current_screen_border='#ffffff',
                    this_screen_border='#5d5f4f',
                    highlight_method='text',
                    highlight_color='#000000',
                    borderwidth=2,
                    foreground='#000000',
                    margin=2,
                    rounded=False,
                    center_aligned=True,
                ),
                widget.Prompt(),
                widget.WindowName(
                    font='JetBrains',
                    #format='{class}',
                    format='{none}',
                    max_chars = 70,
                    ),
                widget.Systray(),
                widget.Spacer(length=6),
                #widget.Volume(),
                #widget.Clock(format='%Y-%m-%d %a %H:%M'),   # 2022-12-30 18:30
                widget.Clock(
                    font='ProductSans Bold',
                    fontsize=13,
                    format='  %a, %b %d %H:%M', # Sun, Dec 30 18:30
                    mouse_callbacks={
                    'Button1': lazy.spawn(os.path.expanduser ("bash /home/user/Documents/calendar.sh")),
                    'Button2': lazy.spawn(os.path.expanduser ("bash /home/user/Documents/calendar.sh prev")),
                    'Button3': lazy.spawn(os.path.expanduser ("bash /home/user/Documents/calendar.sh next")),
                    }
                    ),
                widget.Spacer(length=8),
            ],
            25,
            # Nort, East, South, West
            margin = [6, 8, -4, 8],
            background = "#000000"
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

# Floating windows layout
floating_layout = layout.Floating(
        border_width=1,
        border_focus = '#000000',
        border_normal = '#000000',
# Define what windows should always be floating
# Run the utility of `xprop` to see the wm class and name of an X client.
        float_rules=[
    #*layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(title='KeePassXC'), # KeePassXC
    Match(title='LibreOffice'), # LibreOffice
    Match(title='Thunar'), # Thunar
])

# Configuration variables
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = False
wmname = "qtile"

list_commands = [
        "setxkbmap -layout es",
        "picom --config ~/.config/picom/picom.conf &",
    ]

# Here I execute each command
for c in list_commands:
    os.system(c)
