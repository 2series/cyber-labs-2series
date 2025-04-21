## OWASP API #10 - Unsafe Consumption of APIs

OWASP API Security Top 10 includes a new entry for 2023: Unsafe Consumption of APIs (#10), focusing on risks from external third party APIs.
Many organizations use dozens or hundreds of third party APIs (e.g., Salesforce, DocuSign, Stripe), but these are not inherently safe or vulnerability-free.
Risks often come not just from the third party API itself, but from how it is integrated and implemented in one’s own code.
Improper integration can lead to data theft, breaches, account takeover, and other exploits.

Example: A UK government department (Companies House) had a cross site scripting (XSS) vulnerability exploited by someone registering a business with a malicious script in its name, which executed when viewing the record.
This example highlights dangers of consuming APIs that do not properly sanitize inputs and the potential downstream impact on other sites using that data.

Recommendations for managing third party API risks:
Identify all third party APIs in use, even if not centrally documented.
Do not assume third party APIs are safe; treat them like your own APIs.
Perform your own input validation and authorization testing to prevent cross-account data leaks and other vulnerabilities.
Request third parties to share their security testing results and penetration testing reports.
Conduct your own API security testing, complying with license agreements.

The OWASP API Security Top 10 threats are based on real-world breaches and provide practical guidance for securing APIs.
The course will continue with strategies for defending APIs against these threats.