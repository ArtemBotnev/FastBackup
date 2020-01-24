#!/bin/bash

# Created by Artem Botnev on 09/09/2019

# Requires python version 3.5 or higher
# Copies all new and updated source directory files to destination directory
# (checks if each file already exist in destination directory and copy only if
# it doesn't or has been updated)
# Copies full directories tree
# Exclude empty folders

# example of usage:

# ./backup.sh
# will copy -> subdirectories with files from ~/source to ~/dis, defined in directories.xml file,
# excluded empty directories

cd src
python3 $(dirname "$0")/backup.py