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
