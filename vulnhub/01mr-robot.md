**Getting Started**
If you want to try out the Mr. Robot VM or follow along, you can download it [here](https://www.vulnhub.com/entry/mr-robot-1,151/)

**Prerequisites**
Before starting, ensure you have:
- A virtualization software (VirtualBox)
- Kali Linux
- Basic understanding of Linux commands
- Network scanning tools (Nmap, Nikto)
- Web exploitation tools

**Objective**
Our goal is to find **3 keys** hidden in different locations. Each key is progressively more challenging to locate. This VM is designed for beginner to intermediate users, with no advanced exploitation or reverse engineering required

**The Hack**
1. **Intelligence Gathering**: The first step in any penetration test is gathering information. This includes footprinting and fingerprinting hosts and servers. For more details, refer to the [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/Main_Page)

2. **Network Scanning**: Since the Mr. Robot VM is hosted on my PC using a Bridged Adapter in VirtualBox, we will scan our network to identify the IP address. Use the following command:
   ```bash
   2series@kali:~# netdiscover
   This command will scan your network and display the IP address of the Mr. Robot VM
   **Note**: The output of this command will provide information about the network and help identify the IP address of the Mr. Robot VM

3. **Nmap Scan**: Once we have the target IP, run an Nmap scan to check for open ports and services:
   ```bash
   2series@kali:~# nmap -sS -O -A -n 192.168.1.9
   ```

   This command will scan the target IP and display open ports and services and OS information

4. **Nikto Scan**: Use Nikto to scan for vulnerabilities:
   ```bash
   2series@kali:~# nikto -h 192.168.1.9

   This command will scan the target IP and display vulnerabilities like SQL injection, cross-site scripting, and other web application security issues

5. **Access the Website**: Navigate to `http://192.168.1.9` in your browser. Explore the site and execute the available commands

6. **Check robots.txt**: The `/robots.txt` file reveals two locations:
   ```
   User-agent: *
   fsocity.dic
   key-1-of-3.txt
   ```

   This indicates the presence of two files: `fsocity.dic` and `key-1-of-3.txt`
49~
50~
7. **Retrieve Key 1**: Access `http://192.168.1.9/key-1-of-3.txt` to find:
51~   **Key 1**: `073403c8a58a1f80d943455fb30724b9`
52~   This is the first key
53~
54~
8. **Explore fsocity.dic**: Check `http://192.168.1.9/fsocity.dic` for a potential word list.
55~   The word list is used to brute-force the login page
56~
9.  **Check Other Files**: Explore `index.html`, `index.php`, and `/readme.html` for additional information
    - `index.html`: Contains a link to `index.php`
    - `index.php`: Contains the WordPress login page
    - `/readme.html`: Contains a link to `http://192.168.1.9/wp-login.php`

10. **Decode Password**: Access `/license.txt` to find a base64 encoded password. Decode it:
```
    ```bash
    2series@kali:~# echo ZWxsaW90OkVSMjgtMDY1Mgo= | base64 --decode
    ```
    This command will decode the base64 encoded password
    **Username**: `elliot`
    **Note**: The password is stored as a base64 encoded string and is not displayed in plain text in the terminal
```
11. **Log into WordPress**: Use the credentials to log into the WordPress admin page
    ```bash
    2series@kali:~# curl -X POST -d "log=admin&pwd=admin" http://192.168.1.9/wp-login.php
    ```
    This command will log into the WordPress admin page

12. **Scan for Vulnerabilities**: Check plugin versions and run WPScan to identify vulnerabilities
```
    ```bash
    2series@kali:~# wpscan --url http://192.168.1.9 --enumerate vp
    ```
```
13. **Upload Shell**: Use Metasploit to upload an admin shell
    
14. **Retrieve Key 2**: After gaining access, find:
    **Key 2**: `822c73956184f694993bede3eb39f959`

15. **Post-Exploitation**: Run an Nmap scan on localhost to identify open ports and potential privilege escalation opportunities.

    ```bash
    # Check for SUID binaries
    find / -perm -u=s -type f 2>/dev/null
    # Check running services
    ps aux
    ```
    **Note**: The output of these commands will provide information about SUID binaries and running services

16. **Retrieve Key 3**: Access the root directory to find:
    **Key 3**: `04787ddef27c3dee1ee161b21670b4e4`

**Conclusion**
Successfully captured all 3 keys and gained root access to the system! This exercise provided valuable insights into the hacking process and various exploitations.

**Tools Used**
- Nmap: Network scanning
- Nikto: Web vulnerability scanner
- WPScan: WordPress vulnerability scanner
- Metasploit Framework: Exploitation
- Burp Suite: Web proxy
- Various Linux command-line tools
