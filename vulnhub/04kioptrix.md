# Kioptrix: 1.0

These are a series of challenges. The object of the game is to acquire root access via any means possible (except actually hacking the VM server or player). These games are to learn the basic tools and techniques in vulnerability assessment and exploitation.

## Action plan:

1. **Intelligence Gathering:**
    *   Use `netdiscover` to find the target machine's IP address on the network.
    *   Use `nmap` to scan for open ports and running services on the target.
2. **Vulnerability Identification:**
    *   Identify outdated Apache and OpenSSL versions from the `nmap` results.
    *   Research known exploits for these versions, leading to the "OpenSSL OpenF\*\*k Exploit."
3. **Exploit Preparation:**
    *   Download or copy the exploit code.
    *   Modify the exploit code to work with current systems:
        *   Add necessary header files (`openssl/rc4.h`, `openssl/md5.h`).
        *   Update the URL for downloading the `ptrace-kmod.c` file.
        *   Install the correct version of the `libssl-dev` library (v1.0).
        *   Update variable declarations in the code.
    *   Compile the modified exploit code using `gcc`.
4. **Exploit Execution:**
    *   Run the compiled exploit with the correct target parameters (target version, IP address, port, and connection count).
    *   The exploit establishes an SSL connection, sends shellcode, and attempts to gain root access.
5. **Verification:**
    *   Use the `whoami` command to confirm root access.

# Challenge Analysis: Kioptrix: Level 1
## 1. Intelligence Gathering

Discovering the target machine's IP address and scanning its open ports and services.

**CoT:**

1. Use `netdiscover` to find the target's IP address within the local network. This tool sends ARP requests and listens for responses to identify active hosts.
2. The output of `netdiscover` reveals the target's IP address as 192.168.1.104.
3. Then employs `nmap` with specific flags (`-sS` for SYN scan, `-A` for OS and service detection, `-n` for no DNS resolution) to perform a detailed scan of the target.
4. The `nmap` scan reveals open ports (22, 80, 111, 139, 443, 1024) and identifies running services, including Apache 1.3.20 and OpenSSL 2.8.4.

<reflection>

**Reasoning:** `netdiscover` is appropriate for local network discovery, and `nmap` is the standard tool for port and service scanning. The chosen `nmap` flags provide a comprehensive scan.

**Potential Errors:** The accuracy of `netdiscover` depends on network configuration and the target's responsiveness to ARP requests. The `nmap` scan might be affected by firewalls or intrusion detection systems.

</reflection>

## 2. Vulnerability Identification

Identifying potential vulnerabilities based on the gathered information.

**CoT:**

1. We observe that Apache 1.3.20 and OpenSSL 2.8.4 are outdated.
2. A Google search for these versions leads to the discovery of the "OpenSSL OpenF\*\*k Exploit."

<reflection>

**Reasoning:** Identifying outdated software is a crucial step in vulnerability assessment. Searching for known exploits based on version numbers is a standard practice.

**Potential Errors:** The specific exploit found might not be the only one applicable. There could be other vulnerabilities in the identified software versions or in other services running on the target.

</reflection>

## 3. Exploit Preparation

Preparing the exploit code for execution.

**CoT:**

1. We download or copy the exploit code.
2. Then modify the exploit code:
    *   Adds `#include <openssl/rc4.h>` and `#include <openssl/md5.h>`.
    *   Updates the `wget` command's URL to `http://dl.packetstormsecurity.net/0304-exploits/ptrace-kmod.c`.
    *   Installs `libssl1.0-dev` using `apt-get install libssl1.0-dev`.
    *   Changes `unsigned char *p, *end;` to `const unsigned char *p, *end;` on line 916.
3. Then compiles the code using `gcc -o OpenFu**k 764.c -lcrypto`.


<reflection>

**Reasoning:** Modifications are necessary to make the old exploit code compatible with modern systems and libraries. Installing the correct `libssl-dev` version is crucial for successful compilation.

**Potential Errors:** There might be other compatibility issues not addressed in the provided instructions. The compilation process could fail due to missing dependencies or incorrect compiler flags.

</reflection>

## 4. Exploit Execution

Running the compiled exploit against the target.

**CoT:**

1. We run the exploit with the command `./OpenF**k 0x6b 192.168.1.104 443 -c 40`.
    *   `0x6b` is the target identifier for Apache 1.3.20.
    *   `192.168.1.104` is the target's IP address.
    *   `443` is the target port (HTTPS).
    *   `-c 40` specifies the number of connections to open.
2. The exploit establishes an SSL connection, sends shellcode, and attempts to spawn a shell.
3. The exploit downloads and executes `ptrace-kmod.c`, which is another exploit aimed at gaining root privileges.


<reflection>

**Reasoning:** The exploit is executed with the correct parameters based on the target's information and the exploit's usage instructions. The use of `ptrace-kmod.c` suggests a multi-stage exploit to escalate privileges.

**Potential Errors:** The exploit might fail due to various reasons, such as network issues, target patching, or incorrect exploit parameters.

</reflection>

## 5. Verification

Verifying if the exploit was successful in gaining root access.

**CoT:**

1. We executes the `whoami` command within the spawned shell.
2. The output `root` confirms that the exploit successfully gained root privileges.

<reflection>

**Reasoning:** `whoami` command is a standard way to check the current user's identity. The output `root` clearly indicates successful privilege escalation.

</reflection>

