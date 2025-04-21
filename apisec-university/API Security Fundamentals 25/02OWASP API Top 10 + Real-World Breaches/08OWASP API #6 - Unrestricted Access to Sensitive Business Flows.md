## OWASP API #6: Unrestricted Access to Sensitive Business Flows

OWASP API #6 focuses on unrestricted access to sensitive business flows, a critical addition to the 2023 OWASP API Top 10.

Business Logic Flaws: Exploits arise from logic flaws that allow abuse or misuse of legitimate business flows beyond their intended design.

Examples of Abuse: Excessive use, automated abuse, brute-forcing incremental IDs, and manipulation can lead to losses such as ticket sales, referral fraud, or unauthorized access.

Instagram Case Study:

Password reset flow vulnerability allowed brute force of a 6-digit code via API.
Protections included a 10-minute timeout and 200 guess limit per IP address.
Attackers bypassed limits by rotating IP addresses and automating guesses, able to guess all one million possible codes within timeout.

Lessons Learned / Recommendations:

Avoid relying on IP address restrictions alone, as attackers can rotate IPs.
Limit guess attempts drastically (4-5 tries, not 200).
Expire reset codes quickly after limited failed attempts.
Avoid incremental or numeric IDs for sensitive operations to prevent easy brute force.

Prevention Focus:

Train developers, product managers, and security teams to consider not only intended use ("happy path") but also how attackers might abuse or manipulate business logic.
Always think about possible abuse and exploit attempts during design and security reviews.