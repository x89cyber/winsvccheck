# winsvccheck
Windows service check is a windows utility written in python to check for windows service vulnerabilities.  

This utility currently looks for the following vulns:
1) Unquoted service path
2) Service paths that are writable by the current user

The script was developed and tested with Windows 10 Pro
