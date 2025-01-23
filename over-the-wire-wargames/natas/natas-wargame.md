# Natas Wargame Progress Documentation

## Table of Contents

- [Natas Wargame Progress Documentation](#natas-wargame-progress-documentation)
  - [Table of Contents](#table-of-contents)
  - [Progress Summary](#progress-summary)
  - [Level Walkthroughs](#level-walkthroughs)
    - [Beginner Track (0-5)](#beginner-track-0-5)
    - [Intermediate Track (6-11)](#intermediate-track-6-11)
    - [Advanced Track (12-18)](#advanced-track-12-18)
  - [Technical Skills Overview](#technical-skills-overview)
  - [Toolset \& Resources](#toolset--resources)
    - [Primary Tools](#primary-tools)
    - [Automation Scripts](#automation-scripts)

## Progress Summary

**Current Status:**
- Highest Level Achieved: 18
- Total Levels Completed: 19/34
- Progression: Beginner → Advanced

## Level Walkthroughs

### Beginner Track (0-5)

- **Level 0 → 1**
  - Challenge: Hidden credentials in page source
  - Solution: Basic source code inspection
  - Key Learning: Web page structure analysis
  - Difficulty: ★☆☆☆☆

- **Level 1 → 2**
  - Challenge: Restricted right-click functionality
  - Solution: Developer tools navigation
  - Key Learning: Browser security bypass techniques
  - Difficulty: ★☆☆☆☆

- **Level 2 → 3**
  - Challenge: Directory exploration
  - Solution: Located hidden files through image references
  - Key Learning: Web server directory structure
  - Difficulty: ★☆☆☆☆

- **Level 3 → 4**
  - Challenge: Hidden directory discovery
  - Solution: robots.txt analysis
  - Key Learning: Web crawler directives
  - Difficulty: ★☆☆☆☆

- **Level 4 → 5**
  - Challenge: Referrer validation
  - Solution: HTTP header manipulation via Burp Suite
  - Key Learning: HTTP request components
  - Difficulty: ★★☆☆☆

- **Level 5 → 6**
  - Challenge: Authentication bypass
  - Solution: Cookie manipulation
  - Key Learning: Session management
  - Difficulty: ★★☆☆☆

### Intermediate Track (6-11)

- **Level 6 → 7**
  - Challenge: Server-side code exposure
  - Solution: Source code analysis
  - Key Learning: PHP include vulnerabilities
  - Difficulty: ★★★☆☆

- **Level 7 → 8**
  - Challenge: Path traversal vulnerability
  - Solution: Directory traversal exploitation
  - Key Learning: File system navigation security
  - Difficulty: ★★★☆☆

- **Level 8 → 9**
  - Challenge: Encoded secret
  - Solution: Reverse engineering encryption
  - Key Learning: Base64 and hex encoding
  - Difficulty: ★★★☆☆

- **Level 9 → 10**
  - Challenge: Command injection
  - Solution: Shell command manipulation
  - Key Learning: Input sanitization importance
  - Difficulty: ★★★★☆

- **Level 10 → 11**
  - Challenge: Filtered command injection
  - Solution: Regex bypass techniques
  - Key Learning: Input validation evasion
  - Difficulty: ★★★★☆

- **Level 11 → 12**
  - Challenge: XOR encryption
  - Solution: Cryptographic analysis
  - Key Learning: Basic cryptography
  - Difficulty: ★★★★★

### Advanced Track (12-18)

- **Level 12 → 13**
  - Challenge: File upload vulnerability
  - Solution: Extension bypass
  - Key Learning: Upload security measures
  - Difficulty: ★★★★☆

- **Level 13 → 14**
  - Challenge: File type validation
  - Solution: MIME type manipulation
  - Key Learning: File signature analysis
  - Difficulty: ★★★★★

- **Level 14 → 15**
  - Challenge: SQL injection
  - Solution: Basic SQL injection techniques
  - Key Learning: Database query manipulation
  - Difficulty: ★★★★★

- **Level 15 → 16**
  - Challenge: Blind SQL injection
  - Solution: Automated boolean-based extraction
  - Key Learning: Advanced SQL injection
  - Difficulty: ★★★★★

- **Level 16 → 17**
  - Challenge: Advanced command injection
  - Solution: Command substitution techniques
  - Key Learning: Shell command chaining
  - Difficulty: ★★★★★

- **Level 17 → 18**
  - Challenge: Time-based SQL injection
  - Solution: Timing attack implementation
  - Key Learning: Advanced database exploitation
  - Difficulty: ★★★★★

- **Level 18 → 19**
  - Challenge: Session management
  - Solution: Session ID enumeration
  - Key Learning: Session security
  - Difficulty: ★★★★★

## Technical Skills Overview

| Category | Technique | Application | Complexity |
|----------|-----------|-------------|------------|
| **Web Inspection** | Source Analysis, DOM Manipulation | Levels 0-2 | Basic |
| **Server Security** | Directory Traversal, Robots.txt | Levels 2-3 | Basic |
| **HTTP Security** | Header Manipulation, Cookies | Levels 4-5 | Intermediate |
| **Code Analysis** | PHP, Source Review | Levels 6-7 | Intermediate |
| **Encryption** | XOR, Base64, Hex | Levels 8, 11 | Advanced |
| **Injection** | Command, SQL, Time-based | Levels 9-10, 14-17 | Advanced |
| **Upload Security** | MIME Types, File Headers | Levels 12-13 | Advanced |
| **Authentication** | Session Management | Level 18 | Advanced |

## Toolset & Resources

### Primary Tools
1. **Browser Tools**
   - Chrome DevTools
   - Firefox Developer Edition
   - Network Inspector

2. **Security Suite**
   - Burp Suite Professional
     - Proxy
     - Repeater
     - Intruder
     - Decoder

3. **Development Environment**
   - VSCode
   - Sublime Text
   - Python 3.x

4. **Specialized Tools**
   - CyberChef
   - Postman
   - SQLmap
   - Custom Python Scripts

### Automation Scripts
- SQL Injection Automator
- Session Brute Forcer
- Time-based Attack Framework
- Cookie Manipulator
