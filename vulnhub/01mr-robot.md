# Mr. Robot VM

A detailed analysis of the Mr. Robot VM cybersecurity challenge, focused on how to use `netdiscover`, `nmap`, `nikto`, and `wpscan` to find vulnerabilities and exploit them in a virtual machine (VM) based on the TV show Mr. Robot

Challenge involves *network discovery, port scanning, web server analysis, credential discovery, WordPress exploitation, and privilege escalation*

## Action plan:

1. **Summarize the Objectives:** Briefly state the goal of the challenge, which is to find three hidden keys in the Mr. Robot VM.
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

# Challenge Analysis: Mr. Robot VM

## Network Discovery and Reconnaissance

1. **Network Discovery with `netdiscover`:**
    -   The challenge begins by using the `netdiscover` command to identify the IP address of the target VM within the local network. This tool passively sniffs ARP (Address Resolution Protocol) requests and responses to discover active hosts.
    -   **Command:** `2series@kali:~$ netdiscover`

    <reflection>
    - a. The reasoning behind using `netdiscover` is sound, as it's a non-intrusive way to discover hosts on a local network.
    </reflection>

2. **Port Scanning with `nmap`:**
    -   Once the IP address is known, `nmap` is used to scan for open ports, running services, and the operating system.
    -   **Command:** `2series@kali:~$ nmap -sS -O -A -n 192.168.1.9`
        -   `-sS`: Stealth SYN scan.
        -   `-O`: Operating system detection.
        -   `-A`: Aggressive scan (OS detection, version detection, script scanning, and traceroute).
        -   `-n`: No DNS resolution.
    -   The results indicate open ports 80 (HTTP) and 443 (HTTPS), both running Apache httpd, suggesting a web server.

3. **Web Server Vulnerability Scanning with `nikto`:**
    -   `nikto` is used to scan the web server for potential vulnerabilities and misconfigurations.
    -   **Command:** `2series@kali:~$ nikto -h 192.168.1.9`
    -   The scan reveals several interesting findings, including:
        -   Inode leakage via ETags in `/robots.txt`.
        -   Enabled `mod_negotiation` with MultiViews.
        -   Presence of WordPress-related files and directories (`/readme.html`, `/wp-login/`, etc.).
        -   Admin login pages (`/admin/`, `/wp-login/`).

    <reflection>
    - a. The identified findings are significant and provide valuable information for further exploitation.
    </reflection>

## Initial Web Server Exploration

1. **Browser Interaction:** The challenge proceeds to access the web server through a browser, revealing an interactive interface with six commands.

2. **`/robots.txt` Analysis:**
    -   The `/robots.txt` file is accessed, revealing two entries: `fsocity.dic` and `key-1-of-3.txt`.
    -   Accessing `key-1-of-3.txt` yields the first key: `073403c8a58a1f80d943455fb30724b9`.

    <reflection>
    - a. Checking `/robots.txt` is a standard practice in web security assessments, as it can reveal hidden directories or files.
    </reflection>

3. **`fsocity.dic` Analysis:**
    -   `fsocity.dic` is found to be a word list, potentially useful for brute-forcing.
## WordPress Analysis

1. **Version and Plugin Identification:**
    -   The WordPress version (4.3.6) is identified through `/readme.html`.
    -   Installed plugins and their versions are identified through the WordPress admin panel.

    <reflection>
    - a. Identifying the WordPress version and plugins is crucial for finding known vulnerabilities.
    </reflection>

2. **Vulnerability Scanning with `wpscan`:**
    -   `wpscan` is used to scan for vulnerabilities in the WordPress installation and its plugins.
    -   **Command:** `2series@kali:~$ wpscan -u 192.168.1.9 -e vp`
    -   The scan reveals numerous vulnerabilities, including multiple instances of Cross-Site Scripting (XSS) and outdated plugin versions.

    <reflection>
    - a. Using `wpscan` is a standard practice for WordPress security assessments.
    </reflection>

## Credential Discovery and Exploitation

1. **Base64 Decoding:**
    -   A base64 encoded string is found in `/license.txt`: `ZWxsaW90OkVSMjgtMDY1Mgo=`.
    -   This is decoded to `elliot:ER28-0652` using the command: `echo ZWxsaW90OkVSMjgtMDY1Mgo= | base64 --decode`.

    <reflection>
    - a. The decoded credentials `elliot:ER28-0652` are a significant finding.
    </reflection>

2. **WordPress Admin Panel Login:**
    -   The decoded credentials are used to successfully log in to the WordPress admin panel via `/wp-login/`.

    <reflection>
    - a. Using the discovered credentials to log in is a logical step.
    </reflection>

## Admin Shell Upload and Meterpreter Session

1. **Attempted `wp_admin_shell_upload` Exploit:**
    -   The `wp_admin_shell_upload` exploit in Metasploit is attempted but initially fails due to a WordPress detection check.
    -   **Command:** `msf exploit(wp_admin_shell_upload) > exploit`

2. **Exploit Modification:**
    -   The exploit code is modified to bypass the WordPress detection check by commenting out the `fail_with` line.

    <reflection>
    - a. Modifying the exploit to bypass the check is a valid, albeit slightly risky, approach.
    </reflection>

3. **Successful Meterpreter Session:**
    -   The modified exploit is executed successfully, establishing a Meterpreter session.
    -   **Command:** `msf exploit(wp_admin_shell_upload) > exploit`

    <reflection>
    - a. The successful execution of the exploit demonstrates the effectiveness of the modification.
    </reflection>

## Post-Exploitation and Privilege Escalation

1. **File System Exploration:**
    -   The file system is explored using Meterpreter commands (`pwd`, `cd`, `ls`).
    -   The `key-2-of-3.txt` file and `password.raw-md5` are discovered in the `/home/robot` directory.
    -   The second key cannot be accessed directly, but the MD5 hash is retrieved.

    <reflection>
    - a. Exploring the file system is a logical step after gaining access.
    </reflection>

2. **MD5 Hash Cracking:**
    -   The MD5 hash `c3fcd3d76192e4007dfb496cca67e13b` is cracked online [John-the-Ripper-password-cracker](https://www.techtarget.com/searchsecurity/tutorial/How-to-use-the-John-the-Ripper-password-cracker), revealing the password `abcdefghijklmnopqrstuvwxyz`.

3. **Shell and User Login:**
    -   A shell is obtained using Meterpreter (`shell`), and a TTY shell is spawned using `python -c 'import pty; pty.spawn("/bin/sh")'`.
    -   The user `robot` is logged into using the cracked password, and the second key (`822c73956184f694993bede3eb39f959`) is retrieved.

    <reflection>
    - a. Obtaining a shell and logging in as `robot` is a logical progression.
    </reflection>

4. **Privilege Escalation with `nmap`:**
    -   An `nmap` scan of localhost reveals open ports, including FTP and MySQL.
    -   The old version of `nmap` (3.81) installed on the system is identified as having an interactive mode.
    -   `nmap`'s interactive mode is used to execute a shell command (`!sh`) with root privileges, due to potential SUID misconfigurations.
    -   This allows access to the `/root` directory, where the third key (`04787ddef27c3dee1ee161b21670b4e4`) is found.

    <reflection>
    - a. The attempt to use `nmap` for privilege escalation is a clever and insightful approach.
    - b. The exploitation of `nmap`'s interactive mode is a known technique for older versions.
    </reflection>

## Conclusion

Here i've demonstrates a methodical approach to compromising the Mr. Robot VM, employing a variety of tools and techniques. The steps taken are logical and well-reasoned, progressing from initial reconnaissance to privilege escalation. The analysis highlights a comprehensive and insightful example of a successful penetration testing engagement.