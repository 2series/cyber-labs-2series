### OWASP API Top 10 #1: Broken Object Level Authorization (BOLA)

Topic Overview

Focuses on OWASP API Top 10 #1: Broken Object Level Authorization (BOLA).
BOLA remains the number one API security risk in both 2019 and 2023 lists.
It is highly dangerous and difficult to detect during runtime.
What is BOLA?

Occurs when unauthorized users can access or perform actions on objects (data) they shouldn’t.
Example: User A accessing User B’s data or performing unauthorized actions.
Coinbase Case Study

A hacker tested Coinbase APIs by mimicking valid requests but altered the asset id.
Despite owning Ethereum, the hacker substituted Bitcoin they did not own in the API request.
Unexpectedly, the API processed the transaction without error and confirmed the trade.
Root cause: Missing logic validation on the asset ID in the Brokerage API endpoint.
UI controls were ineffective since the vulnerability existed at the API layer, not the UI.
Peloton Case Study

Unsecured API endpoint exposed entire user database (4 million users) without credentials required.
Peloton fixed authentication by requiring credentials but did not enforce proper authorization.
Any valid user account could access other users' records, illustrating difference between authentication and authorization.
Security Lessons

UI is not a security boundary; API layers must enforce strict authorization.
Authorization logic must be correctly implemented and validated to prevent unauthorized access across accounts.
Best Practices for Prevention

Integrate security early during the design phase ("shift security left").
Include security experts in product requirements and design discussions.
Thoroughly review data access patterns and enforce controls to avoid cross-account data leakage.
Test authorization controls rigorously during development.
Cannot rely solely on runtime defenses like web app firewalls to fix these flaws.
Summary

Broken Object Level Authorization leads to serious risks including data loss and fraud.
Strong, validated authorization at the API layer is essential for API security.
Addressing these issues early in development is critical for secure API implementations.