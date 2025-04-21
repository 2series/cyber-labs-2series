### OWASP API #2 - Broken Authentication 

Broken Authentication refers to weak or poor authentication mechanisms on APIs, including:
No CAPTCHA
No two-factor authentication
Vulnerability to brute forcing and credential stuffing
Many API breaches occur due to APIs left completely unsecured without any authentication.

Risks of broken authentication include:
Data harvesting
Abuse of APIs through unauthenticated requests
Exposure of personally identifiable information (PII)
Potential for ransom attacks

Real-world example: Duolingo API exposed over 2 million user records because several APIs were left unsecured.
The API returned user profile data when queried with an email address without requiring credentials.

Reasons APIs may be left unsecured:
Pressure on developers to release features quickly
Misperception that APIs are hidden and don’t need protection

Recommendations:
Consider authentication and controls during the design phase.
Tailor authentication methods to the sensitivity of the application.
Low sensitivity apps (e.g., weather apps) may not need authentication.
High sensitivity apps (e.g., banking) need strong authentication.
Implement continuous testing to verify authentication is properly enforced.
Do not assume APIs are secure simply because they are "hidden."
Overall emphasis: Always "lock the door" with proper authentication to protect APIs.