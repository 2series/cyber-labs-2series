
### API Security Monitoring

Overview of Monitoring:

Monitoring is crucial for understanding API performance and operations in production.
It is divided into 3 main categories: runtime protection, threat detection, and control validation.

Runtime Protection:

Involves active, real-time protection mechanisms for APIs.
Key elements include:
Policy enforcement (e.g., authentication requirements for endpoints).
Traffic filtering (e.g., geographic traffic filters, IP whitelisting).

Threat Detection:

Analyzes traffic for identifying fraudulent activities and distributed attacks.
Allows for incident response through traffic logging and analysis to understand the nature of incidents.

Control Validation:

Ensures that security controls are functioning as intended at various layers (gateways, firewalls, applications).
Helps identify unexpected traffic or anomalies before they cause issues.

Approaches to Runtime Monitoring:

Proactive Blocking: Using gateways or firewalls to actively block unauthorized traffic.
Reactive Monitoring: Capturing and logging traffic to analyze later, often using SIEM tools. This approach relies on alerting to understand potential threats without blocking legitimate traffic.

API Discovery:

Monitoring can help identify APIs in use, aiding in inventory generation, and uncovering undocumented APIs.
A comprehensive API inventory requires more than just network monitoring; it should also include scanning code repositories and collaboration with development teams.

Challenges in Monitoring:

Even robust monitoring tools may fail to identify legitimate-looking malicious traffic.
Example of SQL Injection: Clear threats can be detected, but sophisticated attacks may bypass defenses if they resemble legitimate actions.
Context is often lacking in runtime protection solutions, making it difficult to differentiate between valid and malicious requests.

Importance of Comprehensive Security:

While monitoring tools are essential, they are not foolproof. Determined attackers can exploit gaps in monitoring systems.
Continuous and comprehensive testing should complement monitoring efforts to strengthen API security.

Final Notes:

Recognizing that many organizations faced breaches despite using monitoring tools emphasizes the need for a layered security approach that includes both monitoring and proactive testing strategies.