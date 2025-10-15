#!/bin/bash

if [ "$1" == "prev" ]; then
  TODAY=$(date -d "-1 month" '+%-d')
  MONTH=$(date -d "-1 month" '+%-m')
elif [ "$1" == "next" ]; then
  TODAY=$(date -d "+1 month" '+%-d')
  MONTH=$(date -d "+1 month" '+%-m')
else
  TODAY=$(date '+%-d')
  MONTH=$(date '+%-m')
fi

HEAD=$(cal $MONTH $(date '+%Y') | head -n1)
BODY=$(ncal -bM -h $MONTH $(date '+%Y') | tail -n7 | sed -z "s|$TODAY|<u><b>$TODAY</b></u>|1")
dunstify "$HEAD" "$BODY" -u NORMAL
