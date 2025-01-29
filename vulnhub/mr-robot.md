> sys prompt: extract_ctf_write

# SUMMARY
The Mr. Robot VM CTF involves finding three hidden keys through various penetration testing techniques. Key vulnerabilities include outdated WordPress versions and misconfigurations. Key learnings emphasize the importance of intelligence gathering and exploiting known vulnerabilities.

# VULNERABILITIES
- CVE-2003-1418: ETags leaking inodes via HTTP headers.
- CVE-2016-5833: Authenticated Attachment Name Stored XSS in WordPress.
- CVE-2016-5835: Authenticated Revision History Information Disclosure in WordPress.
- CVE-2016-5837: Unauthorized Category Removal from Post in WordPress.
- CVE-2016-7168: Authenticated Stored Cross-Site Scripting via Image Filename in WordPress.
- CVE-2016-7169: Path Traversal in Upgrade Package Uploader in WordPress.

# TIMELINE
- **Initial Setup**
  - Download Mr. Robot VM from VulnHub.
  
- **Intelligence Gathering**
  - Run `netdiscover` to find target IP.
  - Execute `nmap -sS -O -A -n 192.168.1.9` to scan for open ports.
  
- **Vulnerability Scanning**
  - Use `nikto -h 192.168.1.9` to identify vulnerabilities.
  
- **Accessing the Web Server**
  - Navigate to `http://192.168.1.9/robots.txt` to find key locations.
  - Access `http://192.168.1.9/key-1-of-3.txt` to retrieve Key 1.
  - Explore `http://192.168.1.9/readme.html` to identify WordPress version.
  - Visit `http://192.168.1.9/license.txt` to find base64 encoded password.

- **Exploitation**
  - Log in to WordPress using credentials `elliot:ER28-0652`.
  - Run `wpscan -u 192.168.1.9 -e vp` to identify plugin vulnerabilities.
  - Use Metasploit with `use exploit/unix/webapp/wp_admin_shell_upload` to upload a shell.

- **Post-Exploitation**
  - Access Meterpreter session and navigate to `/home/robot`.
  - Retrieve Key 2 from `key-2-of-3.txt` and MD5 hash from `password.raw-md5`.
  - Crack MD5 hash using HashKiller to find password for user robot.
  - Gain shell access as user robot and retrieve Key 3 from `/root/key-3-of-3.txt`.

# REFERENCES
- PTES Technical Guidelines
- Nmap documentation: https://nmap.org
- Nikto documentation: https://cirt.net/Nikto2
- Metasploit documentation: http://rapid7.com/metasploit
- HashKiller: https://hashkiller.co.uk
- Resource for spawning a TTY shell: [Spawning a TTY Shell](https://www.example.com)