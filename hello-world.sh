#!/bin/bash
echo ciao > t.txt
echo set>>t.txt
python hello-world.py &>> t.txt
echo executed >> t.txt