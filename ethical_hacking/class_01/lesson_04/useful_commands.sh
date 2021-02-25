# https://github.com/wwong99/pentest-notes/blob/master/oscp_resources/OSCP-Survival-Guide.md
# NMAP
# Other interesting flags
# -S <IP_Address>: Spoof source address (check other firewall/IDS evasion techniques)
# -vv for increasing verbosity
nmap -A -sT -sU -sV -p T:1-1024,U:1-1024