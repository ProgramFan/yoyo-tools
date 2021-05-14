#!/bin/bash

NUM_CN=(
  [1]="一" [2]="二" [3]="三" [4]="四" [5]="五"
  [6]="六" [7]="七" [8]="八" [9]="九" [10]="十"
  [11]="十一" [12]="十二" [13]="十三" [14]="十四" [15]="十五"
  [16]="十六" [17]="十七" [18]="十八" [19]="十九" [20]="二十"
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

make-integer-exercise-paper "100以内加减法-A1" 10 -e add100 sub100 -c 60
make-integer-exercise-paper "100以内加减法-A2" 10 -e add100 sub100 -c 60
make-integer-exercise-paper "100以内加减法-B1" 10 -e add100 sub100 -c 80
make-integer-exercise-paper "100以内加减法-B2" 10 -e add100 sub100 -c 80
make-integer-exercise-paper "100以内加减法-C1" 10 -e add100 sub100 -c 96
make-integer-exercise-paper "100以内加减法-C2" 10 -e add100 sub100 -c 96
