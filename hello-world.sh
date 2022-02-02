#!/bin/sh
echo ciao > t.txt
python hello-world.py 2>> t.txt
echo executed >> t.txt