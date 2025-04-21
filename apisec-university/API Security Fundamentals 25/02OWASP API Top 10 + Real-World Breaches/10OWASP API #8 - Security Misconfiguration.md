## OWASP API #8: Security Misconfiguration

Security misconfiguration covers essential best practices for running and operating API servers securely.
Continuous validation and hardening of servers is vital to prevent automated attacks exploiting configuration gaps.

Common misconfiguration issues include:
Unpatched systems
Leaving unnecessary services enabled
Lack of encryption
Missing critical HTTP headers (CORS, HSTS, rate limiting)
Insecure cookies

Example case: Experian's private API was improperly access-controlled, allowing unauthorized users to retrieve sensitive credit information by simply supplying basic personal info, with no authentication.

Prevention advice includes:
Harden and patch all API infrastructure regularly
Enforce security headers and policies such as CORS, HSTS, and rate limiting
Provide error messages that are informative but do not leak sensitive information
Prevent vulnerabilities like path traversal and server info leakage
Implement security configuration review programs and automated testing to detect unexpected changes