#!/bin/bash

# Incremento de volumen en %
STEP=3

# Comprobar argumento
if [[ $# -ne 1 ]]; then
    echo "Uso: $0 {up|down|toggle}"
    exit 1
fi

case $1 in
    up)
        pactl set-sink-volume @DEFAULT_SINK@ +${STEP}% ;;
    down)
        pactl set-sink-volume @DEFAULT_SINK@ -${STEP}% ;;
    toggle)
        pactl set-sink-mute @DEFAULT_SINK@ toggle ;;
    *)
        echo "Opción inválida: $1"
        exit 1 ;;
esac

# Obtener volumen y estado de mute
VOL=$(pactl get-sink-volume @DEFAULT_SINK@ | awk '{print $5}' | head -n1)
MUTED=$(pactl get-sink-mute @DEFAULT_SINK@ | awk '{print $2}')

# Mostrar notificación
if [[ $MUTED == "yes" ]]; then
    notify-send "Muted" \
        -h string:hlcolor:#ffffff \
        --hint=string:x-dunst-stack-tag:volume \
        -t 1800 \
        -i notification-audio-volume-muted \
        -h int:value:$VOL
else
    notify-send "Volume: $VOL" \
        -h string:hlcolor:#ffffff \
        --hint=string:x-dunst-stack-tag:volume \
        -t 1800 \
        -i notification-audio-volume-medium \
        -h int:value:$VOL
fi
