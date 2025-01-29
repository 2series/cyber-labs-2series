# VulnHub VM Write-ups: Mr. Robot

> "When a bug finally makes itself known, it can be exhilarating, like you just unlocked something. A grand opportunity waiting to be taken advantage of." - Mr. Robot, 2016

 
Download [Mr. Robot VM](https://www.vulnhub.com/entry/mr-robot-1,151/)

## Description

This VM is inspired by the show Mr. Robot and contains three keys hidden in different locations. Our goal is to find all three keys, each progressively more challenging to locate. The difficulty level is considered beginner to intermediate, with no advanced exploitation or reverse engineering required.

## The Hack

The first step in any penetration test, whether network or web-based, is intelligence gathering, which includes footprinting and fingerprinting hosts and servers. For more detailed procedures, I recommend reading the [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/Main_Page).

Since the Mr. Robot VM is hosted on my PC using a `Bridged Adapter` over VirtualBox, we'll scan our network to identify the target IP address:

```bash
2series@kali:~# netdiscover
```

### Network Scan Results

```
Currently scanning: 192.168.98.0/16   |   Screen View: Unique Hosts           
3 Captured ARP Req/Rep packets, from 3 hosts.   Total size: 180               
_____________________________________________________________________________
IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
-----------------------------------------------------------------------------
192.168.1.1     [----Redacted---]      1      60  NETGEAR                     
192.168.1.3     [----Redacted---]      1      60  Micro-Star INTL CO., LTD.   
192.168.1.9     [----Redacted---]      1      60  Cadmus Computer Systems 
```

The target IP is **192.168.1.9**. 

Next, run an Nmap scan to check for open ports and probe for running services and operating systems:

```bash
2series@kali:~# nmap -sS -O -A -n 192.168.1.9
```

### Nmap Scan Results

```
Starting Nmap 7.25BETA2 ( https://nmap.org ) at 2025-01-28 10:21 CDT
Nmap scan report for 192.168.1.9
Host is up (0.00040s latency).
Not shown: 997 filtered ports

PORT    STATE  SERVICE  VERSION
------- ------  -------  -------
22/tcp  closed ssh
80/tcp  open   http     Apache httpd
443/tcp open   ssl/http Apache httpd
```

From our initial scans, we see that ports 80 and 443 are open, both running [Apache HTTPD](https://httpd.apache.org/), indicating this is a `web server`.

### Vulnerability Scanning with Nikto

Next, run [Nikto](https://sectools.org/tool/nikto/) to scan for potential vulnerabilities or misconfigurations:

```bash
2series@kali:~# nikto -h 192.168.1.9
```

### Nikto Scan Results

Nikto reveals several interesting findings, including:

- The X-XSS-Protection header is not defined.
- The X-Content-Type-Options header is not set.
- A WordPress installation was found.

With this information, we can access the website by navigating to **http://192.168.1.9** in our browser and explore the site.

## Exploring the Website

Upon accessing the site, we discover a UI that allows us to run six commands. While exploring, we also check the **/robots.txt** file, `http://192.168.1.9/robots.txt`which reveals two locations:

> /robots.txt - is a text file that is used to prevent crawlers from indexing certain parts of a website. 

```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

### Finding the First Key

Let's navigate to **http://192.168.1.9/key-1-of-3.txt** to retrieve the first key:

```
Key 1: 073403c8a58a1f80d943455fb30724b9
```

### Exploring the Word List

Next, we check **http://192.168.1.9/fsocity.dic**, which appears to be a C source code file, likely a word list for brute-forcing.

### Further Exploration

We then explore the **/readme.html** and **/license.txt** files to gather more information about the WordPress version and potential vulnerabilities.

## Gaining Access

With the credentials obtained from **/license.txt**, we attempt to log in to the WordPress admin page at **/wp-login/**. After successfully logging in as Elliot, we explore the plugins and their versions.

### Running WPScan

To identify vulnerabilities:

```bash
root@kali:~# wpscan -u 192.168.1.9 -e vp
```

### WPScan Results

The scan identifies several vulnerabilities associated with the WordPress version and installed plugins. With admin access, we can now attempt to upload a shell using Metasploit.

## Uploading a Shell

We launch Metasploit and use the `wp_admin_shell_upload` exploit:

```bash
2series@kali:~# msfconsole
msf > use exploit/unix/webapp/wp_admin_shell_upload
```

After setting the required options, we successfully upload a payload and establish a Meterpreter session.

### Finding the Second Key

From the Meterpreter session, we navigate to the home directory of the robot user and find the second key:

```
Key 2: 822c73956184f694993bede3eb39f959
```

## Privilege Escalation

To access the root directory, we perform privilege escalation using an old version of Nmap that supports an interactive shell. After gaining root access, we retrieve the final key:

```
Key 3: 04787ddef27c3dee1ee161b21670b4e4
```

## Conclusion

Congratulations! successfully navigated the Mr. Robot VM, found all three keys, and learned valuable skills in penetration testing!

--->Part 1

### **Key 1: Initial Reconnaissance and Enumeration**
1. **Network Discovery**: You used `netdiscover` to identify the target IP address (`192.168.1.9`).
2. **Port Scanning**: You ran an `nmap` scan to identify open ports and services (Ports 80 and 443 running Apache HTTPD).
3. **Web Server Enumeration**: You used `nikto` to scan for vulnerabilities and discovered:
   - A WordPress installation.
   - The `/robots.txt` file, which revealed `fsocity.dic` and `key-1-of-3.txt`.
4. **Retrieving Key 1**: You accessed `http://192.168.1.9/key-1-of-3.txt` to obtain the first key:
   ```
   073403c8a58a1f80d943455fb30724b9
   ```

### **Key 2: Exploiting WordPress**
1. **WordPress Version Discovery**: You found the WordPress version (4.3.6) via `/readme.html`.
2. **Admin Credentials**: You decoded a base64 string from `/license.txt` to obtain the credentials:
   ```
   elliot:ER28-0652
   ```
3. **Admin Access**: You logged into the WordPress admin panel using the credentials.
4. **Shell Upload**: You used Metasploit’s `wp_admin_shell_upload` exploit to upload a reverse shell and gain a Meterpreter session.
5. **Privilege Escalation**: You discovered the `robot` user’s MD5 password hash in `/home/robot/password.raw-md5` and cracked it using HashKiller:
   ```
   robot:abcdefghijklmnopqrstuvwxyz
   ```
6. **Retrieving Key 2**: You logged in as the `robot` user and accessed the second key:
   ```
   822c73956184f694993bede3eb39f959
   ```

### **Key 3: Privilege Escalation**
1. **Local Enumeration**: You ran `nmap` on the localhost and discovered open ports (FTP, HTTP, HTTPS, MySQL).
2. **SUID Exploitation**: You exploited the SUID bit on an older version of `nmap` (3.81) to escalate privileges to root.
3. **Retrieving Key 3**: You accessed the `/root` directory and obtained the final key:
   ```
   04787ddef27c3dee1ee161b21670b4e4
   ```

### **Key Takeaways**
- **Reconnaissance is Critical**: Tools like `nmap`, `nikto`, and `wpscan` are essential for gathering information about the target.
- **Exploiting Misconfigurations**: The WordPress admin panel and the SUID bit on `nmap` were key to escalating privileges.
- **Password Cracking**: Weak passwords and hashes can be easily cracked using tools like HashKiller or Hashcat.
- **Privilege Escalation**: Always look for misconfigured permissions or outdated software that can be exploited.

### **Next Steps**
If you enjoyed this challenge, consider exploring more VulnHub VMs or other CTF platforms like Hack The Box, TryHackMe, or OverTheWire. Each platform offers a variety of machines and challenges to further hone your skills.

Keep practicing, and remember: **"When a bug finally makes itself known, it can be exhilarating, like you just unlocked something."** – Mr. Robot, 2016

Happy hacking! 🚀

--->Part 2

Here’s a detailed breakdown of the steps taken during the Mr. Robot VM walkthrough, highlighting each key discovery and action:

### **Step 1: Intelligence Gathering**
1. **Network Scanning**  
   - Used `netdiscover` to identify the target IP address: `192.168.1.9`.  
   - Ran an `nmap` scan to identify open ports and services:  
     - Ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) were open.  
     - Apache HTTPD was running on ports 80 and 443.  

2. **Web Server Enumeration**  
   - Ran `nikto` to scan for vulnerabilities and misconfigurations:  
     - Discovered `/robots.txt`, `/admin/`, `/wp-login/`, and other WordPress-related files.  
     - Identified WordPress version 4.3.6 and outdated plugins.  

### **Step 2: Initial Exploitation**
1. **Accessing `/robots.txt`**  
   - Found two files: `fsocity.dic` and `key-1-of-3.txt`.  
   - Accessed `key-1-of-3.txt` to retrieve the first key:  
     ```
     073403c8a58a1f80d943455fb30724b9
     ```  

2. **Analyzing `fsocity.dic`**  
   - Discovered it was a wordlist, potentially useful for brute-forcing.  

3. **Exploring Other Files**  
   - Accessed `/readme.html` to confirm WordPress version 4.3.6.  
   - Accessed `/license.txt` and found a base64-encoded string:  
     ```
     ZWxsaW90OkVSMjgtMDY1Mgo=
     ```  
   - Decoded the string to obtain credentials:  
     ```
     elliot:ER28-0652
     ```  

### **Step 3: WordPress Admin Access**
1. **Logging into WordPress**  
   - Used the credentials `elliot:ER28-0652` to log into the WordPress admin panel.  

2. **Enumerating Plugins**  
   - Identified outdated plugins with known vulnerabilities.  

3. **Running `wpscan`**  
   - Confirmed WordPress version 4.3.6 and identified multiple vulnerabilities.  

### **Step 4: Gaining a Shell**
1. **Using Metasploit**  
   - Attempted to use the `wp_admin_shell_upload` exploit but encountered an issue with WordPress detection.  
   - Edited the exploit to bypass the detection and successfully uploaded a payload.  
   - Gained a Meterpreter session on the target.  

2. **Exploring the File System**  
   - Found the `robot` user’s home directory containing:  
     - `key-2-of-3.txt` (read-protected).  
     - `password.raw-md5` containing an MD5 hash:  
       ```
       robot:c3fcd3d76192e4007dfb496cca67e13b
       ```  

3. **Cracking the MD5 Hash**  
   - Used HashKiller to crack the hash, revealing the password:  
     ```
     abcdefghijklmnopqrstuvwxyz
     ```  

### **Step 5: Privilege Escalation**
1. **Logging in as `robot`**  
   - Used the cracked password to log in as the `robot` user.  
   - Retrieved the second key:  
     ```
     822c73956184f694993bede3eb39f959
     ```  

2. **Enumerating Local Services**  
   - Ran `nmap localhost` and discovered open ports (FTP, HTTP, HTTPS, MySQL).  

3. **Exploiting Nmap SUID**  
   - Identified an old version of `nmap` (3.81) with the `--interactive` option.  
   - Used the interactive mode to spawn a root shell:  
     ```
     nmap --interactive
     !sh
     ```  

4. **Retrieving the Third Key**  
   - Accessed the `/root` directory and retrieved the third key:  
     ```
     04787ddef27c3dee1ee161b21670b4e4
     ```  

--->Part 3

# STEPS

<thinking>

The user is requesting a detailed analysis of a cybersecurity walkthrough, specifically focusing on the steps taken to find vulnerabilities and exploit them in a virtual machine (VM) based on the TV show Mr. Robot. The walkthrough involves network discovery, port scanning, web server analysis, credential discovery, WordPress exploitation, and privilege escalation.

Here's a breakdown of the approach to analyze the walkthrough:

1. **Summarize the Objectives:** Briefly state the goal of the walkthrough, which is to find three hidden keys in the Mr. Robot VM.
2. **Network Discovery and Reconnaissance:**
    -   Explain the use of `netdiscover` to find the VM's IP address.
    -   Detail the `nmap` scan parameters and their purpose in identifying open ports and services.
    -   Analyze the `nikto` scan results, highlighting potential vulnerabilities and misconfigurations.
3. **Initial Web Server Exploration:**
    -   Describe the interaction with the web server through a browser.
    -   Explain the significance of `/robots.txt` and the information found within it.
    -   Analyze the content of `fsocity.dic` and its potential use.
4. **WordPress Analysis:**
    -   Explain the process of identifying the WordPress version and installed plugins.
    -   Detail the use of `wpscan` to find vulnerabilities in the WordPress installation and plugins.
5. **Credential Discovery and Exploitation:**
    -   Explain the decoding of the base64 encoded string to obtain credentials.
    -   Describe the login process to the WordPress admin panel using the discovered credentials.
6. **Admin Shell Upload and Meterpreter Session:**
    -   Explain the attempt to use the `wp_admin_shell_upload` exploit in Metasploit.
    -   Detail the modification of the exploit to bypass the WordPress detection check.
    -   Describe the successful establishment of a Meterpreter session.
7. **Post-Exploitation and Privilege Escalation:**
    -   Explain the exploration of the file system using Meterpreter.
    -   Describe the discovery of an MD5 hash and its cracking.
    -   Detail the process of obtaining a shell and logging in as the user `robot`.
    -   Explain the use of `nmap`'s interactive mode to achieve privilege escalation and obtain the final key.
8. **Reflection and Conclusion:** Review the entire process, highlighting key steps, tools used, and the overall strategy employed to successfully complete the challenge.

</thinking>

<output>

# Walkthrough Analysis: Mr. Robot VM

## Objectives

The primary objective of this walkthrough is to locate three hidden keys within a virtual machine (VM) themed around the TV show Mr. Robot. The challenge involves a series of steps, from initial reconnaissance to privilege escalation, to uncover these keys.

## Network Discovery and Reconnaissance

1. **Network Discovery with `netdiscover`:**
    -   The walkthrough begins by using the `netdiscover` command to identify the IP address of the target VM within the local network. This tool passively sniffs ARP requests and responses to discover active hosts.
    -   **Command:** `root@kali:~# netdiscover`

    <reflection>
    - a. The reasoning behind using `netdiscover` is sound, as it's a non-intrusive way to discover hosts on a local network.
    - b. No immediate errors or oversights are apparent in this step.
    - c. The conclusion that `192.168.1.9` is the target IP is correct based on the output.
    </reflection>

2. **Port Scanning with `nmap`:**
    -   Once the IP address is known, `nmap` is used to scan for open ports, running services, and the operating system.
    -   **Command:** `root@kali:~# nmap -sS -O -A -n 192.168.1.9`
        -   `-sS`: Stealth SYN scan.
        -   `-O`: Operating system detection.
        -   `-A`: Aggressive scan (OS detection, version detection, script scanning, and traceroute).
        -   `-n`: No DNS resolution.
    -   The results indicate open ports 80 (HTTP) and 443 (HTTPS), both running Apache httpd, suggesting a web server.

    <reflection>
    - a. The `nmap` command is well-constructed, employing a comprehensive set of options for thorough reconnaissance.
    - b. The parameters are appropriate for the task and don't raise any concerns.
    - c. The identification of open ports and the Apache web server is accurate based on the output.
    </reflection>

3. **Web Server Vulnerability Scanning with `nikto`:**
    -   `nikto` is used to scan the web server for potential vulnerabilities and misconfigurations.
    -   **Command:** `2series@kali:~# nikto -h 192.168.1.9`
    -   The scan reveals several interesting findings, including:
        -   Inode leakage via ETags in `/robots.txt`.
        -   Enabled `mod_negotiation` with MultiViews.
        -   Presence of WordPress-related files and directories (`/readme.html`, `/wp-login/`, etc.).
        -   Admin login pages (`/admin/`, `/wp-login/`).

    <reflection>
    - a. Using `nikto` is a standard practice for web server vulnerability scanning, and the reasoning is valid.
    - b. No errors are apparent in the command or its execution.
    - c. The identified findings are significant and provide valuable information for further exploitation.
    </reflection>

## Initial Web Server Exploration

1. **Browser Interaction:** The walkthrough proceeds to access the web server through a browser, revealing an interactive interface with six commands.

    <reflection>
    - a. Accessing the web server through a browser is a logical step to understand its functionality.
    - b. No issues are identified with this step.
    - c. The observation about the interactive interface is accurate.
    </reflection>

2. **`/robots.txt` Analysis:**
    -   The `/robots.txt` file is accessed, revealing two entries: `fsocity.dic` and `key-1-of-3.txt`.
    -   Accessing `key-1-of-3.txt` yields the first key: `073403c8a58a1f80d943455fb30724b9`.

    <reflection>
    - a. Checking `/robots.txt` is a standard practice in web security assessments, as it can reveal hidden directories or files.
    - b. No errors are identified.
    - c. The discovery of the first key is a significant milestone in the walkthrough.
    </reflection>

3. **`fsocity.dic` Analysis:**
    -   `fsocity.dic` is found to be a word list, potentially useful for brute-forcing.

    <reflection>
    - a. The analysis of `fsocity.dic` as a word list is accurate.
    - b. No issues are found.
    - c. The identification of its potential use for brute-forcing is correct.
    </reflection>

## WordPress Analysis

1. **Version and Plugin Identification:**
    -   The WordPress version (4.3.6) is identified through `/readme.html`.
    -   Installed plugins and their versions are identified through the WordPress admin panel.

    <reflection>
    - a. Identifying the WordPress version and plugins is crucial for finding known vulnerabilities.
    - b. No errors are apparent in this step.
    - c. The identified version and plugins are accurate.
    </reflection>

2. **Vulnerability Scanning with `wpscan`:**
    -   `wpscan` is used to scan for vulnerabilities in the WordPress installation and its plugins.
    -   **Command:** `2series@kali:~# wpscan -u 192.168.1.9 -e vp`
    -   The scan reveals numerous vulnerabilities, including multiple instances of Cross-Site Scripting (XSS) and outdated plugin versions.

    <reflection>
    - a. Using `wpscan` is a standard practice for WordPress security assessments.
    - b. The command is correctly constructed for the task.
    - c. The identified vulnerabilities are significant and provide potential attack vectors.
    </reflection>

## Credential Discovery and Exploitation

1. **Base64 Decoding:**
    -   A base64 encoded string is found in `/license.txt`: `ZWxsaW90OkVSMjgtMDY1Mgo=`.
    -   This is decoded to `elliot:ER28-0652` using the command: `echo ZWxsaW90OkVSMjgtMDY1Mgo= | base64 --decode`.

    <reflection>
    - a. The identification of the base64 encoded string and its decoding are accurate.
    - b. The command used for decoding is correct.
    - c. The decoded credentials `elliot:ER28-0652` are a significant finding.
    </reflection>

2. **WordPress Admin Panel Login:**
    -   The decoded credentials are used to successfully log in to the WordPress admin panel via `/wp-login/`.

    <reflection>
    - a. Using the discovered credentials to log in is a logical step.
    - b. No errors are identified.
    - c. The successful login confirms the validity of the credentials.
    </reflection>

## Admin Shell Upload and Meterpreter Session

1. **Attempted `wp_admin_shell_upload` Exploit:**
    -   The `wp_admin_shell_upload` exploit in Metasploit is attempted but initially fails due to a WordPress detection check.
    -   **Command:** `msf exploit(wp_admin_shell_upload) > exploit`

    <reflection>
    - a. The attempt to use the exploit is a reasonable approach, given the admin credentials.
    - b. The initial failure is due to a specific check in the exploit code.
    - c. The identification of the cause of the failure is accurate.
    </reflection>

2. **Exploit Modification:**
    -   The exploit code is modified to bypass the WordPress detection check by commenting out the `fail_with` line.

    <reflection>
    - a. Modifying the exploit to bypass the check is a valid, albeit slightly risky, approach.
    - b. The modification is correctly implemented.
    - c. The decision to proceed with the modified exploit is justified by the context.
    </reflection>

3. **Successful Meterpreter Session:**
    -   The modified exploit is executed successfully, establishing a Meterpreter session.
    -   **Command:** `msf exploit(wp_admin_shell_upload) > exploit`

    <reflection>
    - a. The successful execution of the exploit demonstrates the effectiveness of the modification.
    - b. No errors are identified in this step.
    - c. The established Meterpreter session provides a powerful foothold on the target system.
    </reflection>

## Post-Exploitation and Privilege Escalation

1. **File System Exploration:**
    -   The file system is explored using Meterpreter commands (`pwd`, `cd`, `ls`).
    -   The `key-2-of-3.txt` file and `password.raw-md5` are discovered in the `/home/robot` directory.
    -   The second key cannot be accessed directly, but the MD5 hash is retrieved.

    <reflection>
    - a. Exploring the file system is a logical step after gaining access.
    - b. The commands used are appropriate for the task.
    - c. The discovery of the MD5 hash is significant.
    </reflection>

2. **MD5 Hash Cracking:**
    -   The MD5 hash `c3fcd3d76192e4007dfb496cca67e13b` is cracked online, revealing the password `abcdefghijklmnopqrstuvwxyz`.

    <reflection>
    - a. Cracking the MD5 hash is necessary to proceed.
    - b. Using an online service is a valid approach, though using HashCat locally is also an option.
    - c. The cracked password is a crucial piece of information.
    </reflection>

3. **Shell and User Login:**
    -   A shell is obtained using Meterpreter (`shell`), and a TTY shell is spawned using `python -c 'import pty; pty.spawn("/bin/sh")'`.
    -   The user `robot` is logged into using the cracked password, and the second key (`822c73956184f694993bede3eb39f959`) is retrieved.

    <reflection>
    - a. Obtaining a shell and logging in as `robot` is a logical progression.
    - b. The commands used are appropriate for the task.
    - c. The retrieval of the second key is a major milestone.
    </reflection>

4. **Privilege Escalation with `nmap`:**
    -   An `nmap` scan of localhost reveals open ports, including FTP and MySQL.
    -   The old version of `nmap` (3.81) installed on the system is identified as having an interactive mode.
    -   `nmap`'s interactive mode is used to execute a shell command (`!sh`) with root privileges, due to potential SUID misconfigurations.
    -   This allows access to the `/root` directory, where the third key (`04787ddef27c3dee1ee161b21670b4e4`) is found.

    <reflection>
    - a. The attempt to use `nmap` for privilege escalation is a clever and insightful approach.
    - b. The exploitation of `nmap`'s interactive mode is a known technique for older versions.
    - c. The successful retrieval of the third key demonstrates the effectiveness of this method.
    </reflection>

## Conclusion

The walkthrough demonstrates a methodical approach to compromising the Mr. Robot VM, employing a variety of tools and techniques. The steps taken are logical and well-reasoned, progressing from initial reconnaissance to privilege escalation. The analysis highlights the importance of each step and the significance of the findings. Overall, the walkthrough provides a comprehensive and insightful example of a successful penetration testing engagement.
</output>