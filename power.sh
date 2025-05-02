#!/bin/bash

cd powering-raspberrypi

source power-env/bin/activate

python power.py -w "((9,11),(14,16))"
