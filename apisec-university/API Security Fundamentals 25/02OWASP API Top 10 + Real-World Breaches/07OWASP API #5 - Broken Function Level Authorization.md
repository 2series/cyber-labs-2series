## OWASP API #5: Broken Function Level Authorization

Definition: Broken Function Level Authorization involves improper control over which API functions or actions a user can perform, not just what data they can access.

Difference from Broken Object Authorization: Focuses on function access rather than data access.

Function Abuse Examples:
Escalating user privileges.
Converting a free account to paid without payment.
Modifying or deleting sensitive resources like invoices or loan balances.

Typical Vulnerability Scenario:
APIs expose both passive (GET) methods to view data and active (POST, PUT, DELETE) methods to modify it.
Failure to restrict active methods leads to unauthorized function execution.

Real-World Example (Bumble):
Users could change account type from free to paid by exploiting an exposed POST request on the same endpoint used to view account type.
The account upgrade function was accessible without proper authorization or payment.

Preventive Measures:
Identify sensitive functions and endpoints that perform critical actions.
Implement strict access controls and logic to restrict who can perform certain functions.
Test permissions for every user role against all endpoints to detect unauthorized access.

Role-Based Access Control (RBAC):
Essential to apply and regularly test RBAC across all API functions and endpoints.
Prevent permission drift or unintended exposure over time.

Testing Recommendation:
Conduct thorough permission tests for each user type to uncover and fix access control gaps.

These points summarize the risk, impact, example, and mitigation of Broken Function Level Authorization in API security.