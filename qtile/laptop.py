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

# --------------------------
# Key bindings
# --------------------------
keys = [
    # Switch window's focus
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key(["mod1"], "tab", lazy.layout.next()),

    # Move windows between left/right columns or move up/down in current stack.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    
    # Grow windows
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "p", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggle bar"),

    # Suspend, reboot, poweroff
    Key([mod], "F9", lazy.spawn("systemctl suspend -i")),
    Key([mod], "F10", lazy.spawn("systemctl reboot")),
    Key([mod], "F11", lazy.spawn("systemctl poweroff")),
    
    # Volume
    Key([mod], "KP_Multiply", lazy.spawn(f"{VOLUME_SCRIPT} up")),
    Key([mod], "KP_Divide", lazy.spawn(f"{VOLUME_SCRIPT} down")),
    Key([mod], "m", lazy.spawn(f"{VOLUME_SCRIPT} toggle")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(f"{VOLUME_SCRIPT} up")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(f"{VOLUME_SCRIPT} down")),
    Key([], "XF86AudioMute", lazy.spawn(f"{VOLUME_SCRIPT} toggle")),

    # Rofi Wi-Fi menu
    Key([mod], "F12", lazy.spawn(os.path.expanduser("bash /home/user/Documents/rofi-wifi-menu.sh"))),

    # Screenshots
    Key([], "Print", lazy.spawn("flameshot full --path /home/user")),
    Key(["Shift"], "Print", lazy.spawn("flameshot gui")),

    # Open apps
    Key([mod], "r", lazy.spawn("rofi -show drun")),
    Key([mod], "e", lazy.spawn("thunar")),
    Key([mod], "v", lazy.spawn("/home/user/Documents/Helium.AppImage")),
]

# --------------------------
# Groups
# --------------------------
groups = [Group(str(i), label='●') for i in range(1, 10)]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Switch to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc=f"Switch & move to {i.name}"),
    ])

# --------------------------
# Layouts
# --------------------------
layouts = [
    layout.Columns(
        border_width=0,
        border_focus='#97979e',
        border_focus_stack='#97979e',
        border_normal='#000000',
        change_size=10,
        margin=16
    ),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# --------------------------
# Screens and bar
# --------------------------
screens = [
    Screen(
        wallpaper='~/.config/qtile/background.jpg',
        wallpaper_mode='stretch',
        top=bar.Bar(
            [
                widget.Spacer(length=18, background='#000000'),
                widget.Image(
                    filename='~/.config/qtile/icon.png',
                    margin=0,
                    background='#000000',
                ),
                widget.Image(filename='~/.config/qtile/1.png'),
                widget.GroupBox(
                    font='Noto Sans',
                    background='#202020',
                    active='#97979e',
                    inactive='#5f5f5e',
                    this_current_screen_border='#ffffff',
                    this_screen_border='#5d5f4f',
                    highlight_method='text',
                    highlight_color='#000000',
                    borderwidth=2,
                    margin=2,
                    rounded=False,
                    center_aligned=True,
                ),
                widget.Prompt(),
                widget.WindowName(
                    font='JetBrains',
                    format='{none}',
                    max_chars=70,
                ),
                widget.Image(filename='~/.config/qtile/2.png'),
                widget.Spacer(length=4, background='#000000'),
                widget.Systray(background='#000000'),
                
                # Battery icon
                widget.Spacer(length=12, background='#000000'),
                widget.Memory(
                    background='#000000',
                    format='{MemUsed: .0f}{mm}',
                    foreground='#97979e',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    update_interval=5,
                ),
                widget.Spacer(length=7, background='#000000'),

                # Battery icon
                widget.Battery(
                    name="my_battery",
                    font="Font Awesome 6 Free Solid",
                    fontsize=16,
                    background='#000000',
                    foreground='#97979e',
                    update_interval=5,
                    format='{char}',
                    charge_char='',
                    full_char='',
                    three_quarters_char='',
                    half_char='',
                    quarter_char='',
                    empty_char='',
                    discharge_char='',
                    notify_below=30,
                    low_foreground='#ff5555',
                ),
                
                # Battery percentage (hidden by default)
                widget.Battery(
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background='#000000',
                    foreground='#97979e',
                    format="{percent:2.0%}",
                    update_interval=5
                ),

                widget.Spacer(length=14, background='#000000'),    
                widget.Clock(
                    background='#000000',
                    foreground='97979e',
                    font='ProductSans Bold',
                    fontsize=13,
                    format='%H:%M',
                    mouse_callbacks={
                        'Button1': lazy.spawn(os.path.expanduser("bash /home/user/Documents/calendar.sh")),
                        'Button2': lazy.spawn(os.path.expanduser("bash /home/user/Documents/calendar.sh prev")),
                        'Button3': lazy.spawn(os.path.expanduser("bash /home/user/Documents/calendar.sh next")),
                    }
                ),
                widget.Spacer(length=8, background='#000000'),
            ],
            25,
            margin=[6, 8, -4, 8],
            background="#202020"
        ),
    ),
]

# --------------------------
# Mouse and floating layouts
# --------------------------
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

floating_layout = layout.Floating(
    border_width=1,
    border_focus='#000000',
    border_normal='#000000',
    float_rules=[
        Match(wm_class='confirmreset'),
        Match(wm_class='makebranch'),
        Match(wm_class='maketag'),
        Match(wm_class='ssh-askpass'),
        Match(title='branchdialog'),
        Match(title='pinentry'),
        Match(title='KeePassXC'),
        Match(title='LibreOffice'),
        Match(title='thunar'),
        Match(title='Rename'),
    ]
)

# --------------------------
# Other configuration
# --------------------------
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

for c in list_commands:
    os.system(c)
