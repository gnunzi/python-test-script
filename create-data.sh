#!/bin/bash
echo hello > t.txt
date >>t.txt
#set>>t.txt
python3 create-data.py &>> t.txt
echo executed >> t.txt