# Kioptrix 4

This challenge involved exploiting a Kioptrix VM to gain root access using network discovery, port scanning, SQL injection, and MySQL UDF.

## Action plan:

1.  **Reconnaissance (netdiscover, nmap):**
    *   `netdiscover`:  Finds the target VM's IP address on the local network.
    *   `nmap`:  Performs port scanning and service version detection. 
        *   `-sS` (SYN scan) performs TCP SYN scans, which are faster than full TCP scans but less stealthy.
        *   `-A` (OS and service detection) enables OS fingerprinting and service/version detection.
        *   `-n` (no DNS resolution) prevents DNS resolution for hostnames.
        *   The results reveal:
            *   OpenSSH (port 22)
            *   Apache web server (port 80)
            *   Samba (ports 139, 445) - This is a major clue.

2.  **Samba Enumeration (nmap, smbclient):**
    *   `nmap -sC --script=smb-enum-users`: Uses Nmap's scripting engine to enumerate users on the Samba service.  This is *very* important, as it reveals valid usernames (`john`, `loneferret`, `nobody`, `robert`, `root`).
    *   `smbclient -L`: Attempts to list shares on the Samba server.  While no accessible shares are found, the ability to connect anonymously (null session) is confirmed. The explanation of IPC$ is helpful.

3.  **Web Application Exploitation (SQL Injection):**
    *   We correctly identifies a SQL injection vulnerability on the login page. The single quote (`'`) test confirms the vulnerability.
    *   The classic `1' or '1'='1` payload is used, combined with the enumerated username `john`, to bypass authentication. 
    *   **Key Vulnerability:**  SQL Injection.  The web application fails to properly sanitize user input, allowing attackers to manipulate SQL queries.

4.  **SSH Access and Restricted Shell Escape:**
    *   The credentials obtained from the SQL injection (`john` and the revealed password) are used to gain SSH access.
    *   The user `john` is found to be in a restricted shell (lshell). This limits the commands that can be executed.
    *   **Key Vulnerability:**  Weak password/credential reuse (the password obtained from the SQL injection works for SSH).
    *   **Restricted Shell Escape:** The command `echo os.system('/bin/bash')` is used to break out of the restricted shell.  This leverages the `os.system()` function (likely within a Python context, given the `echo` syntax) to execute arbitrary commands.

5.  **Privilege Escalation (MySQL UDF):**
    *   `ps -ef | grep root`:  Lists running processes, filtering for those owned by root. This confirms that MySQL is running as root.
    *   The web application's configuration file (`checklogin.php`) is found in `/var/www`, revealing the MySQL root user's credentials (username: `root`, password:  *(empty)*).
    *   **Key Vulnerability:**  Hardcoded credentials (and a *blank* root password for MySQL!). This is a *huge* security flaw.
    *   **MySQL UDF Exploitation:** We leverage a User Defined Function (UDF) within MySQL. UDFs allow extending MySQL's functionality with custom code. The `sys_exec` function (part of the `lib_mysqludf_sys` library) is used to execute a system command.
    *   `select sys_exec('usermod -a -G admin john');`: This is the crucial privilege escalation command. It uses `sys_exec` to run the `usermod` command, adding the `john` user to the `admin` group (which likely has sudo privileges).
    *   `sudo su`:  Finally, `sudo su` is used to switch to the root user, confirming successful privilege escalation.
    *  **Key Vulnerability:** MySQL running as root, combined with a blank root password, allows for easy UDF exploitation.

**Suggestions for Improvement:**

*   **Nikto/Dirb/Gobuster:** Before attempting manual SQL injection, it would be good practice to use web application vulnerability scanners like Nikto, Dirb, or Gobuster. These tools can automatically identify common vulnerabilities and directories, potentially speeding up the process. This makes the challenge more realistic and even more comprehensive.

    ```zsh
    nikto -h 192.168.1.14
    dirb http://192.168.1.14 /usr/share/wordlists/dirb/common.txt
    gobuster dir -u http://192.168.1.14 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,txt,html
    ```

*   **SQLMap:** While the manual SQL injection is well-explained, introducing SQLMap would be beneficial. SQLMap is a powerful tool that automates SQL injection detection and exploitation.  This would demonstrate a more efficient approach.

    ```zsh
    sqlmap -u "http://192.168.1.14/login.php" --data "username=john&password=1" --level=5 --risk=3 --dbs  # Enumerate databases
    sqlmap -u "http://192.168.1.14/login.php" --data "username=john&password=1" --level=5 --risk=3 -D members --tables # Enumerate tables in 'members'
    sqlmap -u "http://192.168.1.14/login.php" --data "username=john&password=1" --level=5 --risk=3 -D members -T members --dump # Dump the 'members' table
    ```

*   **Metasploit:**  Mentioning (or even briefly demonstrating) the use of Metasploit would be valuable.  Metasploit has modules for many of the vulnerabilities exploited in this CTF, including Samba user enumeration, SQL injection, and MySQL UDF exploitation. This exposes readers to another powerful tool.  For example:

    ```zsh
    # In Metasploit:
    use auxiliary/scanner/smb/smb_enumusers
    set RHOSTS 192.168.1.14
    run

    use exploit/multi/http/php_mysql_udf_injection  # (If a suitable module exists)
    # ... (set options) ...
    run
    ```

*   **UDF Compilation (Optional):** For a more advanced audience, you could briefly mention that the `lib_mysqludf_sys.so` library might need to be compiled from source in some cases. This would add a layer of realism.

* **Alternative Restricted Shell Escapes**: There are other ways to escape the restricted shell. Mentioning `vi`, `more`, `less` or other commands that can be used to spawn a shell would add value.

* **Defensive Recommendations:**  A concluding section with recommendations for preventing the exploited vulnerabilities would be very beneficial. This could include:
    *   **Input Validation:**  Properly sanitize all user input to prevent SQL injection.  Use parameterized queries (prepared statements) whenever possible.
    *   **Strong Passwords:**  Enforce strong password policies and avoid default credentials.
    *   **Principle of Least Privilege:**  Run services with the minimum necessary privileges.  MySQL should *never* run as root.
    *   **Regular Updates:**  Keep software (Samba, Apache, MySQL, the OS) up to date to patch known vulnerabilities.
    *   **Web Application Firewall (WAF):**  A WAF can help detect and block SQL injection attempts.
    *  **Secure Configuration of lshell**: If a restricted shell is needed, configure it properly and test it thoroughly.

## Table of key steps and outcomes:

| Step | Tool/Method | Outcome |
| --- | --- | --- |
| Network Discovery | `netdiscover` | Identified IP 192.168.1.14 |
| Port Scanning | `nmap -sS -A -n` | Found open ports 22, 80, 139, 445 |
| User Enumeration | `nmap --script=smb-enum-users` | Listed usernames including "john", "root" |
| SMB Share Check | `smbclient -L` | No public shares, IPC$ found |
| SQL Injection | Crafted login as "john" | Gained user access |
| Restricted Shell Escape | `"echo os.system('/bin/bash')"` | Escaped to full bash shell |
| MySQL Credential Find | `cat /var/www/checklogin.php` | Found root MySQL with no password |
| Privilege Escalation | MySQL sys_exec for usermod | Added "john" to admin group, gained sudo |
| Root Access | `sudo su` | Confirmed root with `id`, `whoami` |
