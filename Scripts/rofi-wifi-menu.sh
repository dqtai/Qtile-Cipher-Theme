#!/usr/bin/env bash

# Notify user
notify-send "Getting list of available Wi-Fi networks..."

# Fetch available Wi-Fi networks with SECURITY and SSID
wifi_list=$(nmcli --fields "SECURITY,SSID" device wifi list | sed 1d | sed 's/  */ /g' | \
            sed -E "s/WPA.*|WEP//g" | sed "s/^--//g" | sed "/--/d")

# Check Wi-Fi status to create toggle option
wifi_status=$(nmcli -t -f WIFI g)
if [[ "$wifi_status" == "enabled" ]]; then
    toggle="󰖪  Disable Wi-Fi"
elif [[ "$wifi_status" == "disabled" ]]; then
    toggle="󰖩  Enable Wi-Fi"
fi

# Highlight currently connected network (optional)
current_ssid=$(nmcli -t -f ACTIVE,SSID dev wifi | grep '^yes' | cut -d: -f2)
wifi_list_highlighted=""
while IFS= read -r line; do
    ssid=$(echo "$line" | awk '{$1=""; print substr($0,2)}')
    if [[ "$ssid" == "$current_ssid" ]]; then
        wifi_list_highlighted+=" $ssid\n"
    else
        wifi_list_highlighted+="$line\n"
    fi
done <<< "$wifi_list"

# Show rofi menu
chosen_network=$(echo -e "$toggle\n$wifi_list_highlighted" | rofi -dmenu -i -selected-row 1 -p "Wi-Fi SSID: ")

# Exit if nothing selected
[ -z "$chosen_network" ] && exit

# Handle Wi-Fi toggle
if [[ "$chosen_network" == "󰖩"* ]]; then
    nmcli radio wifi on && notify-send "Wi-Fi Enabled"
    exit
elif [[ "$chosen_network" == "󰖪"* ]]; then
    nmcli radio wifi off && notify-send "Wi-Fi Disabled"
    exit
fi

# Extract SSID from selection (removes first word/icon)
chosen_id=$(echo "$chosen_network" | awk '{$1=""; print substr($0,2)}')

# Success message
success_message="You are now connected to the Wi-Fi network \"$chosen_id\"."

# Check if the connection already exists
if nmcli connection show --active | grep -qw "$chosen_id"; then
    nmcli connection up id "$chosen_id" && notify-send "Connection Established" "$success_message"
else
    # Ask for password if needed
    if echo "$chosen_network" | grep -q ""; then
        wifi_password=$(rofi -dmenu -p "Password: " -password)
        if [ -z "$wifi_password" ]; then
            notify-send "Connection Cancelled" "No password entered"
            exit
        fi
        nmcli device wifi connect "$chosen_id" password "$wifi_password" && notify-send "Connection Established" "$success_message" || \
            notify-send "Connection Failed" "Check SSID or password"
    else
        # Open network
        nmcli device wifi connect "$chosen_id" && notify-send "Connection Established" "$success_message" || \
            notify-send "Connection Failed" "Check SSID"
    fi
fi
