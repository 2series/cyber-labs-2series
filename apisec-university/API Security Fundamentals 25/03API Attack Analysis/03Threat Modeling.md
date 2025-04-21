### Threat Modeling

Threat modeling is a fundamental starting point in API security frameworks.

Threat modeling process includes:

Identifying the attack surface and footprint (APIs, business flows, API functions, access methods).
Identifying vulnerabilities such as logic flaws, access control gaps, third-party risks.
Assessing likelihood of attacks and potential impact (data loss, operational damage).
Prioritizing threats based on risk and creating mitigation plans.
Important to consider "What do you have that attackers want?" Possible valuable targets include:

Personal Identifiable Information (PII).
Banking and credit card information.
Corporate data and intellectual property.
Opportunities for fraud or theft.
Critical infrastructure data (energy, healthcare, communications, banking).
Understand how APIs are used in business:

Which APIs access sensitive data.
API exposure to trusted customers, partners, and the public.
APIs between internal microservices and containers.
Third-party API usage and data exchange.
Risk formula in threat modeling: Risk = Threat × Vulnerability × Likelihood × Impact

Example: Unknown (rogue) APIs can pose significant risk if exploited, as shown in the Optus breach case.

The purpose of threat modeling is to identify and prioritize risks and then develop effective mitigation strategies.