# Natas Wargame Progress

## Table of Contents

- [Natas Wargame Progress](#natas-wargame-progress)
  - [Table of Contents](#table-of-contents)
  - [Progress Overview](#progress-overview)
  - [Completed Levels](#completed-levels)
    - [Beginner Levels (0-5)](#beginner-levels-0-5)
    - [Intermediate Levels (6-11)](#intermediate-levels-6-11)
    - [Advanced Levels (12-13)](#advanced-levels-12-13)
  - [Skills \& Techniques](#skills--techniques)
  - [Tools Used](#tools-used)

## Progress Overview

Current Progress: Level 17 completed
Total Levels Completed: 18
Difficulty: Beginner to Advanced

## Completed Levels

### Beginner Levels (0-5)

- **Natas Level 0**: Successfully obtained the password for natas1 by viewing the page source.
  - Difficulty: Easy
  - Technique: Basic web inspection
- **Natas Level 1**: Successfully obtained the password for natas2 by editing the HTML code and finding the password in the source code.
  - Difficulty: Easy
  - Technique: Browser developer tools
- **Natas Level 2**: Successfully obtained the password for natas3 by finding a linked image file and accessing the users.txt file.
  - Difficulty: Easy
  - Technique: Directory enumeration
- **Natas Level 3**: Successfully obtained the password for natas4 by accessing the robots.txt file and finding the password in the s3cr3t directory.
  - Difficulty: Easy
  - Technique: Web crawler investigation
- **Natas Level 4**: Successfully obtained the password for natas5 by spoofing the HTTP Referrer using Burp.
  - Difficulty: Easy-Medium
  - Technique: HTTP header manipulation
- **Natas Level 5**: Successfully obtained the password for natas6 by changing the loggedin cookie value using Burp.
  - Difficulty: Easy-Medium
  - Technique: Cookie manipulation

### Intermediate Levels (6-11)

- **Natas Level 6**: Successfully obtained the password for natas7 by finding the secret code in the includes directory.
  - Difficulty: Medium
  - Technique: Source code analysis
- **Natas Level 7**: Successfully obtained the password for natas8 by performing a Directory Traversal Attack.
  - Difficulty: Medium
  - Technique: Path traversal vulnerability
- **Natas Level 8**: Successfully obtained the password for natas9 by reverse-engineering the encoded secret key.
  - Difficulty: Medium
  - Technique: Encoding/decoding algorithms
- **Natas Level 9**: Successfully obtained the password for natas10 by injecting arbitrary code using the ; command separator.
  - Difficulty: Medium-Hard
  - Technique: Command injection
- **Natas Level 10**: Successfully obtained the password for natas11 by using regular expressions to bypass the ; and & command filtering.
  - Difficulty: Medium-Hard
  - Technique: Regular expression bypass
- **Natas Level 11**: Successfully obtained the password for natas12 by reverse-engineering the XOR Encryption key and creating a new cookie.
  - Difficulty: Hard
  - Technique: Cryptography analysis

### Advanced Levels (12-17)

- **Natas Level 12**: Successfully obtained the password for natas13 by exploiting file upload vulnerability.
  - Difficulty: Medium-Hard
  - Technique: File upload exploitation
- **Natas Level 13**: Successfully obtained the password for natas14 by bypassing image upload restrictions using file headers.
  - Difficulty: Hard
  - Technique: File upload bypass, MIME type spoofing
- **Natas Level 14**: Successfully obtained the password for natas15 by exploiting SQL injection vulnerability.
  - Difficulty: Hard
  - Technique: SQL Injection Attack
- **Natas Level 15**: Successfully obtained the password for natas16 using blind SQL injection and brute force techniques.
  - Difficulty: Hard
  - Technique: Blind SQL Injection, Python Scripting
- **Natas Level 16**: Successfully obtained the password for natas17 by exploiting command injection with grep and command substitution.
  - Difficulty: Hard
  - Technique: Command Injection, Python Scripting
- **Natas Level 17**: Successfully obtained the password for natas18 using time-based blind SQL injection.
  - Difficulty: Hard
  - Technique: Time-Based Blind SQL Injection, Python Scripting

## Skills & Techniques

| Technique                    | Description                                              | Levels Used | Difficulty |
| ---------------------------- | -------------------------------------------------------- | ----------- | ---------- |
| **Viewing page source**      | Inspecting HTML source code to find hidden information   | 0, 1, 2     | Easy       |
| **Editing HTML code**        | Modifying webpage elements using browser developer tools | 1           | Easy       |
| **Directory enumeration**    | Discovering hidden directories and files                 | 2, 3        | Easy       |
| **Web crawler analysis**     | Examining robots.txt and other crawler-related files     | 3           | Easy       |
| **HTTP manipulation**        | Modifying HTTP headers and requests                      | 4, 5        | Medium     |
| **Cookie manipulation**      | Analyzing and modifying browser cookies                  | 5, 11       | Medium     |
| **Directory traversal**      | Exploiting path traversal vulnerabilities                | 7           | Medium     |
| **Cryptography**             | Understanding and breaking basic encryption              | 8, 11       | Hard       |
| **Command injection**        | Exploiting command injection vulnerabilities             | 9, 10       | Hard       |
| **Regular expressions**      | Understanding and bypassing regex filters                | 10          | Medium     |
| **File upload exploitation** | Exploiting vulnerable file upload mechanisms             | 12, 13      | Hard       |
| **MIME type spoofing**       | Bypassing file type restrictions by manipulating headers | 13          | Hard       |
| **SQL Injection**            | Exploiting SQL query vulnerabilities                     | 14          | Hard       |
| **Blind SQL Injection**      | Using boolean-based SQL injection with Python scripting  | 15          | Hard       |
| **Command Substitution**     | Using $() syntax to inject commands within commands      | 16          | Hard       |
| **Time-Based SQL Injection** | Exploiting SQL injection using time delays               | 17          | Hard       |

## Tools Used

1. **Browser Developer Tools**
   - Purpose: Source code inspection, HTML modification
   - Levels: 0-3

2. **Burp Suite**
   - Purpose: HTTP traffic interception and modification
   - Features used: Proxy, Repeater
   - Levels: 4-5, 11, 12-13

3. **Text Editors**
   - Purpose: Code analysis, script writing
   - Levels: 6-17

4. **Encoding/Decoding Tools**
   - Purpose: Cryptographic analysis
   - Levels: 8, 11

5. **Python Scripts**
   - Purpose: Automated exploitation and brute forcing
   - Levels: 15, 16, 17
