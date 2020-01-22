#!/usr/bin/env bash

RATE=$1
DURATION=$2
NAME=$3

vegeta attack -timeout=8s -format="json" -duration="$DURATION"s -rate=$RATE -name=$NAME > "$NAME".bin

vegeta plot --title "$NAME" "$NAME".bin > "$NAME".html
vegeta report -type=text "$NAME".bin > "$NAME".txt
cat ./"$NAME".txt
