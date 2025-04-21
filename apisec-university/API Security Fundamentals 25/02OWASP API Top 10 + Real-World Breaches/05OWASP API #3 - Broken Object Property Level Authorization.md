## OWASP API #3 - Broken Object Property Level Authorization

This vulnerability combines two categories from OWASP 2019: Mass Assignment and Excess Data Exposure.
Mass Assignment involves unauthorized or improper manipulation of data via APIs.
Excess Data Exposure happens when APIs return too much or sensitive information unnecessarily.

Example: Venmo’s public API exposed full transaction details (including PII) beyond what was anonymized on the UI.

The root cause: API returned complete data without authorization checks; the UI only filtered what was displayed.

Key takeaway: APIs must be tailored to use cases and follow the principle of data minimization—return only the data necessary for the business case.

Prevention includes:
Defining data access and manipulation controls early in the API design phase.
Involving security teams during design to avoid excess data leakage.
Testing APIs with automated tools to detect PII and sensitive data exposure.
Implementing strict authorization controls on what data users can access and modify.
This vulnerability is also known as Broken Object Property Level Authorization (BOPLA).