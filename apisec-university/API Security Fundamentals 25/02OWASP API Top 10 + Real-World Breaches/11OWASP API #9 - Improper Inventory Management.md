## OWASP API #9: Improper Inventory Management

Improper Inventory Management is #9 in the 2023 OWASP API Top 10, but is a common and critical issue.

It involves two main aspects:
Awareness and visibility of all APIs running in your environment.
Control over those APIs (whether they should run, are up to date, retired, documented, and secure).

Problems include:
Zombie or shadow APIs: APIs running without awareness.
Outdated API versions still accessible.
Version control issues allowing attackers to access older, less secure versions.

Example breach: Optus (Australian telco) API breach exposing 9.8 million subscriber records due to:
Publicly accessible API with no authentication.
API exposing sensitive PII (driver’s license numbers, phone numbers, DOB, addresses).
Use of incremental IDs aiding mass data harvesting.
The breach highlighted the risks of unknown APIs and lack of governance.

Recommendations:
Establish a cross-functional team (security, development, operations, compliance, risk) for API governance.
Define and enforce standardized API deployment policies and processes.

Maintain a comprehensive inventory of APIs using multiple discovery methods:
Traffic-based discovery (e.g., leveraging WAF tools).
Code-based discovery (scanning code repositories).
App crawling discovery.
Dictionary/brute force discovery.
Direct communication with engineering teams for insight.
Use a common API gateway to centralize visibility, policy enforcement, and management.
Properly retire deprecated APIs and ensure clients/partners upgrade to supported versions.
Conduct periodic audits to verify access rights and remove unnecessary access.