## OWASP API #7: Server Side Request Forgery (SSRF)

SSRF Overview:

SSRF (Server Side Request Forgery) is a new entry in the OWASP API Top 10 in 2023.
It involves tricking a server into making unauthorized requests, often targeting internal systems or malicious third parties.
Exploits URL input fields to make the server send requests it should not be sending.

Impacts and Risks:

Can create a channel for malicious requests.
May expose internal data and resources to external attackers.
Exploits excessive permissions on the server to access other systems.

Example Scenario:

Users supply URLs (e.g., LinkedIn profile URL) but instead provide malicious URLs or local file paths.
The server then fetches unauthorized resources like sensitive local files or malware sites.

Real-World Example:

Capital One 2019 breach due to SSRF vulnerability.
Vulnerability exploited a misconfigured Web Application Firewall (WAF) with excessive permissions.
Attackers accessed AWS S3 buckets, stealing over 30 GB of data, including 100 million credit card applications and 100,000 social security numbers.
Resulted in a $190 million fine.

Prevention Measures:

Apply the Least Privilege Model to limit server permissions, especially for WAFs.
Strictly validate all user inputs; reject inputs not matching expected formats (e.g., LinkedIn URLs should start with linkedin.com).
Conduct SSRF attack simulations on APIs to detect vulnerabilities before exploitation.

These points summarize the nature, risks, examples, and prevention strategies related to SSRF attacks as presented in the APIsec University content.