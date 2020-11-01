#!/bin/bash

NUM_CN=(
  [1]="一" [2]="二" [3]="三" [4]="四" [5]="五" [6]="六"
  [7]="七" [8]="八" [9]="九" [0]="零"
)

# Usage: make-integer-exercise-paper NAME COUNT ...
function make-integer-exercise-paper() {
  local name=$1
  shift
  local count=$1
  shift
  local n
  for n in $(seq 1 $count); do
    ./integer-exercise.py -l "$name (${NUM_CN[$n]})" "$@" >tmp.tex &&
      xelatex tmp.tex && mv tmp.pdf "$name-$n.pdf" &&
      rm -f tmp.* || exit 255
  done
}

make-integer-exercise-paper "10以内加减法" 2 -e add10 sub10 -c 100
make-integer-exercise-paper "20以内加法" 3 -e add20-l -c 100
make-integer-exercise-paper "20以内减法" 2 -e sub20 -c 100
make-integer-exercise-paper "20以内加减法" 5 -e add20-l sub20 -c 100
