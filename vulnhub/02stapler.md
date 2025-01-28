# Stapler: 1 - VulnHub Challenge Walkthrough

## The Hack Process

Making a successful penetration test requires a well-rounded approach. In my previous write-up on the Mr. Robot VM, I highlighted the importance of enumeration as the first step in penetration testing. For this challenge, we'll again start by enumerating the network to find our target VM's IP address.

### Network Enumeration

We'll use `netdiscover` to identify any active IP addresses on our network:

```bash
2series@kali:~# netdiscover -r 192.168.23.0/16
```

After executing the command, we find the following results:

```
IP            At MAC Address     Count     Len  MAC Vendor / Hostname      
192.168.1.13  08:00:27:3d:e7:21  1         60   Cadmus Computer Systems 
```

The target IP is `192.168.1.13`. 

Next, we'll run an Nmap scan to enumerate open ports, services, versions, and the operating system.

### Nmap Scanning

```bash
2series@kali:~# nmap -sS -A -O -n -p1-60000 192.168.1.13
```

The Nmap results reveal several open ports of interest, particularly:

| Port    | Service    | Version                              |
|---------|------------|--------------------------------------|
| 21/tcp  | vsftpd     | 2.0.8 (anonymous FTP login allowed)  |
| 22/tcp  | OpenSSH    | 7.2p2                                |
| 80/tcp  | Apache HTTPD |                                      |
| 139/tcp | Samba      | smbd 4.3.9-Ubuntu (workgroup: WORKGROUP) |
| 3306/tcp| MySQL      | 5.7.12                               |

The presence of FTP with anonymous login allows us to gain initial access.

### Accessing FTP

Let’s log into the FTP service using the following credentials:

- **Username**: anonymous
- **Password**: anonymous

```bash
2series@kali:~# ftp 192.168.1.13
```

After a successful login, we check for files available on the FTP server. 

```bash
ftp> ls
```

This returns a file named `note`. We download it to inspect its contents.

```bash
ftp> get note
```

The file content reveals someone named `Elly`, which could be useful for user enumeration.

### Exploring Further

Next, we'll investigate the `SSH` service to see if we can log in as root. Unfortunately, this attempt fails:

```bash
2series@kali:~# ssh root@192.168.1.13
```

**Permission denied.**

### SMB Enumeration
Our next point of interest is `TCP port 139 (NetBIOS)`. We’ll use `smbclient` to list the available SMB shares:

```bash
2series@kali:~# smbclient -L 192.168.1.13 -N
```

We discover shares including `kathy` and `tmp`. The comment on the `kathy` share suggests that Fred may have access to it. Let's connect and enumerate this share:

```bash
2series@kali:~# smbclient //fred/kathy -I 192.168.1.13 -N
```

Inside the `kathy` share, we find files, including a `todo-list.txt`, which hints at ongoing projects at Initech.

We also explore the `tmp` share, retrieving additional files.

### Investigating the Web Server
Next, we access the `Apache web server` running on `port 12380`. We find some interesting directories via a Nikto scan:

```bash
2series@kali:~# nikto -h 192.168.1.13:12380
```

This reveals directories such as `/phpmyadmin/` and `/blogblog/`.

Entering `/robots.txt`, we discover that certain admin directory resources are available.

```
User-agent: *
Disallow: /admin112233/
Disallow: /blogblog/
```

Navigating to `/blogblog`, we identify a WordPress instance. Let's run a WPScan to enumerate users and vulnerabilities:

```bash
2series@kali:~# wpscan --url https://192.168.1.13:12380/blogblog/ --enumerate uap
```

### Finding Vulnerabilities

The scan reveals several registered users, correlating to names we previously encountered (e.g., John, Elly, Peter). Additionally, we find vulnerabilities associated with the WordPress site version.

One of the plugins found is vulnerable to `Local File Inclusion (LFI)`, allowing us to extract sensitive files such as the `wp-config.php`.

### Escalating Privileges

Using the extracted database credentials, we connect to MySQL:

```bash
2series@kali:~# mysql -u root -p -h 192.168.1.13
```

Once connected, we retrieve WordPress user passwords. Not requiring brute-forcing, we decide to upload a PHP shell through the uploads directory. From that point, we move on to setting up a reverse shell.

### Gaining Root Access

After executing the reverse shell, we gain an interactive session and escalate privileges to root by modifying the user shell for Peter in sudoers.

Finally, we navigate to the `/root` directory to retrieve the flag.

```bash
cat /root/flag.txt
```

## Conclusion
In this write-up, I successfully exploited the Stapler CTF from VulnHub, leveraging a combination of enumeration, service exploitation, and privilege escalation techniques.

I’d like to thank the creators for this challenging box and hope you found my process informative! Stay tuned for more write-ups, projects, and challenges.

