# Kioptrix 3

This challenge highlighting the key concepts and techniques used, along with some improvements and additional considerations:

## Action plan:

1.  **Reconnaissance (Finding the Target):**

    *   `netdiscover`:  This tool uses ARP (Address Resolution Protocol) requests to discover live hosts on a local network.  It's a fundamental first step in many network penetration tests. The output shows the IP address and MAC address of active devices.
    *   `/etc/hosts` modification:  Adding `192.168.1.13 kioptrix3.com` to the `/etc/hosts` file creates a local DNS resolution. This is crucial because the web application on the target machine is likely configured to respond to the hostname `kioptrix3.com`.  Without this, links and resources within the web application might not load correctly.

2.  **Port Scanning and Service Enumeration:**

    *   `nmap -sS -A -n 192.168.1.13`: This is a powerful `nmap` command:
        *   `-sS`:  SYN scan (stealth scan).  It's faster and less likely to be detected than a full connect scan.
        *   `-A`:  Enable OS detection, version detection, script scanning, and traceroute. This provides a wealth of information about the target.
        *   `-n`:  Disable DNS resolution (speeds up the scan).
    *   The `nmap` output reveals:
        *   OpenSSH on port 22 (version 4.7p1)
        *   Apache httpd on port 80 (version 2.2.8) with PHP 5.2.4
        *   OS: Linux 2.6.X
        *   This information immediately suggests potential attack vectors (outdated software).

3.  **Web Application Reconnaissance:**

    *   **Browsing the website:**  Manually exploring the website is essential. The walkthrough identifies a blog, a login page, and a gallery.
    *   `nikto -h 192.168.1.13`:  `nikto` is a web server scanner. It checks for:
        *   Outdated software versions
        *   Dangerous files/CGIs
        *   Misconfigurations
        *   Security headers (or lack thereof)
    *   `nikto`'s findings:
        *   Outdated Apache and PHP versions (major vulnerabilities)
        *   Missing security headers (X-Frame-Options, X-XSS-Protection, X-Content-Type-Options)
        *   PHP information disclosure vulnerabilities
        *   Presence of `phpmyadmin` (a web-based MySQL administration tool)
        *   Directory indexing enabled

4.  **phpMyAdmin Exploration (and a Dead End):**

    *   The discovery correctly identifies the phpMyAdmin version (2.11.3).
    *   It finds a known RCE exploit (CVE-2009-1151) but correctly determines that it's not applicable because the installation method differs. This is a good example of why understanding the context of a vulnerability is crucial.

5.  **SQL Injection in the Gallery:**

    *   **Manual SQL Injection:**  This is the core of the successful attack. Website analysis identifies the `id` parameter in the gallery's URL as vulnerable.
    *   **Testing for Injection:**  Injecting a single quote (`'`) causes a SQL error, confirming the vulnerability. This is a classic SQL injection test.
    *   **Finding the Number of Columns:**  `-1 union select 1,2,3,4,5,6` This uses the `UNION` operator to combine the results of the original query with a crafted query.  The number of columns must match for `UNION` to work. The `-1` ensures the original query returns no results, making the injected data visible.
    *   **Identifying Vulnerable Columns:**  The output shows that columns 2 and 3 are vulnerable (they display the injected numbers).
    *   **Determining the Database Version:** `-1 union select 1,@@version,3,4,5,6`  `@@version` is a MySQL variable that returns the database version (5.0.51a).
    *   **Enumerating Tables:** `-1 union select 1,group_concat(table_name),3,4,5,6 from information_schema.tables where table_schema=database()--`
        *   `information_schema`:  A database that contains metadata about all other databases.
        *   `table_schema=database()`:  Filters the results to the current database.
        *   `group_concat(table_name)`:  Combines all table names into a single string.
        *   `--`:  A SQL comment, used to comment out the rest of the original query.
    *   **Enumerating Columns:** `-1 union select 1,group_concat(column_name),3,4,5,6 FROM information_schema.columns WHERE table_name=CHAR(100, 101, 118, 95, 97, 99, 99, 111, 117, 110, 116, 115)--`
        *   `CHAR()`:  Converts ASCII codes to characters (used to obfuscate the table name `dev_accounts`).
    *   **Extracting Data:** `-1 union select 1,group_concat(username,0x3a,password),3,4,5,6 FROM dev_accounts--`
        *   `0x3a`:  Hexadecimal representation of a colon (`:`), used as a separator.
        *   This query retrieves the usernames and (hashed) passwords.

6.  **Password Cracking:**

    *   `hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt`:  `hashcat` is a powerful password cracking tool.
        *   `-m 0`:  Specifies the hash type (MD5 in this case).
        *   `hashes.txt`:  The file containing the extracted hashes.
        *   `/usr/share/wordlists/rockyou.txt`:  A common wordlist used for cracking.
    *   The cracked passwords are "starwars" and "Mast3r".

7.  **SSH Login:**

    *   `ssh loneferret@192.168.1.13`:  We successfully logged in using the cracked credentials for the `loneferret` user.

8.  **Privilege Escalation:**

    *   **Reconnaissance:**  `ls` and `cat CompanyPolicy.README` reveal a clue about a custom editing tool (`ht`) and a company policy.
    *   `sudo -l`:  Lists the commands the current user can run with `sudo`.  This shows that `loneferret` can run `/usr/local/bin/ht` as root without a password.
    *   **Exploiting `ht`:**  The `ht` editor is vulnerable to a command injection. By editing `/etc/sudoers` and adding `/bin/sh` after `/usr/local/bin/ht`, we are granted the ability to run a shell as root.
        *   `export TERM=xterm-color`:  This sets the terminal type, which might be necessary for `ht` to function correctly.
        *   `sudo ht /etc/sudoers`: Opens the sudoers file with the vulnerable editor.
        *   The modification adds `, /bin/sh` to the `loneferret` sudoers entry.
    *   `sudo /bin/sh`:  Executes a shell as root.
    *   `whoami`:  Confirms root access.

**Improvements and Additional Considerations**

*   **SQLMap:** While the manual SQL injection is excellent for learning, using `sqlmap` would be much faster in a real-world scenario.  `sqlmap` automates the entire process of detection, exploitation, and data extraction.  A command like `sqlmap -u "http://kioptrix3.com/gallery.php?id=1" --dump -D <database_name> -T dev_accounts -C username,password` would likely achieve the same result much more quickly.
*   **Web Application Firewall (WAF) Bypass:** If a WAF were in place, more sophisticated SQL injection techniques might be needed (e.g., encoding, obfuscation).
*   **OpenSSH Vulnerability:**  The OpenSSH version (4.7p1) is very old and likely has known vulnerabilities. Searching for exploits for this specific version could provide an alternative entry point.
*   **Apache and PHP Vulnerabilities:** Similarly, the outdated Apache and PHP versions are prime targets for exploitation. Metasploit or other exploit frameworks could be used to find and exploit vulnerabilities in these services.
*   **Kernel Exploits:** The Linux kernel version (2.6.24) is also old. Local privilege escalation exploits targeting this kernel version might exist.
* **Security Headers:** We correctly noted the lack of X-Frame-Options. If the site had a login form, it could be vulnerable to clickjacking.
* **Error Handling:** The SQL injection exploit relies on verbose error messages. If error reporting were disabled (as it should be in a production environment), different SQL injection techniques (like blind SQL injection) would be required.

**Overall, we've demonstrates several fundamental penetration testing techniques. We also highlighted the importance of staying updated with security patches and best practices. The challenge emphasizes manual exploitation, which is valuable for understanding the underlying principles. The inclusion of `hashcat` and the `sudo` privilege escalation are excellent additions. The improvements suggested above would make the challenge even more comprehensive and applicable to a wider range of scenarios.**


---

The challenge is a beginner-oriented penetration testing exercise designed to teach foundational skills in network scanning, web application exploitation, and privilege escalation.

## 1. Network Enumeration & Initial Setup

### Tool: netdiscover

Scanned the network (192.168.9.0/16) to identify the Kioptrix VM IP (192.168.1.13).

### Hosts File Configuration

Added 192.168.1.13 kioptrix3.com to /etc/hosts to resolve the VM's domain name.

## 2. Port Scanning & Service Identification

### Tool: Nmap

Command: `nmap -sS -A -n 192.168.1.13`

### Open Ports

* 22/TCP: SSH (OpenSSH 4.7p1).
* 80/TCP: HTTP (Apache 2.2.8 with PHP 5.2.4).

### OS Detection

Linux 2.6.X (Ubuntu).

## 3. Web Application Analysis

### Tool: nikto

Command: `nikto -h 192.168.1.13`

### Key Findings

* Outdated PHP (5.2.4) and Apache (2.2.8).
* phpMyAdmin directory exposed (/phpmyadmin/).
* Missing security headers (X-Frame-Options, X-XSS-Protection).
* SQL injection vulnerability in the gallery page's id parameter.

## 4. Manual SQL Injection Exploitation

### Vulnerability

SQL error in the gallery page's id parameter.

### Steps

1. Determine Column Count:
`-1 union select 1,2,3,4,5,6` → 6 columns (columns 2 and 3 vulnerable).
2. Extract Database Version:
`-1 union select 1,@@version,3,4,5,6` → MySQL 5.0.51a.
3. List Tables:
`-1 union select 1,2,group_concat(table_name),4,5,6 from information_schema.tables where table_schema=database()`-- → Identified dev_accounts table.
4. Extract Credentials:
`-1 union select 1,group_concat(username,0x3a,password),3,4,5,6 FROM dev_accounts`-- → Retrieved two MD5 hashes.
5. Crack Hashes:
Used hashcat with rockyou.txt wordlist:
	* starwars (user: loneferret).
	* Mast3r (user: root).

## 5. SSH Access & Privilege Escalation

### SSH Login

ssh loneferret@192.168.1.13 with password starwars.

### Privilege Escalation

1. Sudo Permissions:
User loneferret had passwordless sudo access to `/usr/local/bin/ht` (a text editor).
2. Exploit:
Edited `/etc/sudoers` via `sudo ht /etc/sudoers`.
Added `/bin/sh` to the sudoers file (after `/usr/local/bin/ht`).
Gained root shell: `sudo /bin/sh`.

## 6. Final Access

### Root Shell

Successfully escalated privileges to root using the modified sudoers file.

### Proof

Command `whoami` confirmed root access.

## Key Tools & Techniques

* Network Scanning: netdiscover, Nmap.
* Web Vulnerability Scanning: nikto.
* SQL Injection: Manual payload crafting (no reliance on sqlmap).
* Hash Cracking: hashcat with a large wordlist.
* Privilege Escalation: Sudoers file manipulation via ht.

## Lessons Learned

* Manual Exploitation:
Understanding SQL injection mechanics is critical for bypassing automated tool limitations.
* Privilege Escalation:
Leveraging sudo permissions to modify system files (e.g., /etc/sudoers) is a common technique in CTFs.
* Documentation:
Editing /etc/hosts ensures consistent domain resolution during attacks.