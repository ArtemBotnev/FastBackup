## fast backup script
### backup.sh
 Requires python version 3.5 or higher.
 
 Copies all new and updated source directory files to destination directory
 (checks if each file already exist in destination directory and copy only if
 it doesn't or has been updated).
 
 Copies full directories tree.
 
 Exclude empty folders.
 
#### *How does it work?*
 Specify your source and destination directories in directories.xml file (read explanation in this file).
 Specify additional settings for script in settings.xml file (read explanation in this file).
 On Linux or Mac OS just run ``` ./backup.sh ```
 On Windows double click on ``` backup.bat ```
