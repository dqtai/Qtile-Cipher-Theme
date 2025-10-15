#!/bin/bash

memory=$(free | grep Mem | awk '{print $3}')
#battery=$(acpi | cut -f 4 -d ' ' | sed 's/%/ /')
temperature=$(sensors | grep "Package id 0:" | awk '{print $4}' | sed 's/+//; s/°C//')

while [[ true ]]; do

	if [[ $memory>=5242880 ]]; then
		dunstify "Warning!" "High memory usage"
	fi

#	if [[ $battery=100 ]]; then
#		dunstify "Warning!" "Battery fully charged. Unplug the charger"
#		elif [[ $battery<=20 ]]; then
#			dunstify "Warning!" "Low battery. Plug the charger"
#	fi

	if [[ $temperature>=40 ]]; then
		dunstify "Warning!" "High temperature recorded"
	fi

	sleep 5s
done
