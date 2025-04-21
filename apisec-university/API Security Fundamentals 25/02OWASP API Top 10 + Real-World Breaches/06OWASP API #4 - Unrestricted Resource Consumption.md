## OWASP API #4: Unrestricted Resource Consumption

OWASP API Top 10 #4 focuses on Unrestricted Resource Consumption, previously called Lack of Resources and Rate Limiting.

This issue involves vulnerabilities to volumetric or brute force attacks on APIs, such as mass data harvesting and excessive resource use.

Common manifestations include:
Absence of proper rate limiting controls.
Lack of execution timeouts.
No limit on memory use, response size, or upload file size.

Consequences of these vulnerabilities:
Excessive operational load.
Large amounts of data leakage.
Denial of Service (DoS).
Application performance degradation.

Real-world example: Trello’s publicly accessible API allowed attackers to send 500 million requests using a large email list, harvesting profile data of users due to lack of restrictions on that endpoint.

Despite existing defenses like web application firewalls (WAF), rate limiting, and bot detection, attackers can bypass them by:

Gradually increasing attack rates.
Distributing requests across many IPs.
Using proxy networks.
Conducting attacks over extended timespans.
The effective mitigation by Trello/Atlassian was to secure the endpoint by requiring authentication to access user information, making it easier to detect and stop abuse by associating requests with a user identity.

Recommendations:

Implement traffic controls such as WAFs and API gateways.
Test the effectiveness of those controls regularly.
Use authentication and authorization to limit data access, preventing anonymous or unauthorized data disclosure.
Do not rely solely on traffic controls since determined attackers can circumvent them.
Overall, the focus is on balancing technical rate limiting controls with secure API design and proper authentication to prevent misuse and data leakage from brute force or volumetric attacks.