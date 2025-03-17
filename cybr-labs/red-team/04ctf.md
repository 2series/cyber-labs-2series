# Backdoor an S3 Bucket via its Bucket Policy with Stratus Red Team

using Stratus Red Team to simulate an S3 bucket policy backdooring attack! the distinction between `warmup` and `detonate`. Here are some of my thoughts and elaborations on the process:

**Key Concepts and Observations**

*   **Automated Red Teaming:** Stratus Red Team is a powerful tool for automating red team exercises. This significantly reduces the manual effort required to set up and execute attacks, making security testing more efficient.
*   **Bucket Policy Vulnerability:** The core of this attack lies in modifying the S3 bucket policy. Bucket policies are JSON documents that define who has access to what within an S3 bucket. By adding a statement that allows access from an external AWS account (even a fictitious one) we creates a persistent backdoor.
*   **Persistence:** The crucial point about this attack is its persistence. Even if the initial compromised credentials (like an access key) are revoked, the backdoor in the bucket policy *remains*. This is why it's so dangerous and why proper monitoring of bucket policy changes is essential.
*   **Warmup vs. Detonate:**  We clearly explained this, but it's worth reiterating.  `warmup` prepares the environment (creates the S3 bucket in this case), and `detonate` executes the actual attack (modifies the bucket policy). This separation allows for controlled testing and easier cleanup.
*   **State Management:** Stratus Red Team's state management (`status`, `WARM`, `DETONATED`, `COLD`) is a very useful feature. It helps track the state of attacks, especially when dealing with multiple techniques or interrupted workflows.
*   **Revert and Cleanup:**  The `revert` and `cleanup` commands are essential for responsible red teaming. `revert` undoes the specific attack actions (removes the malicious bucket policy), while `cleanup` removes the entire infrastructure created during the `warmup` phase (deletes the S3 bucket).
*   **Detection Methods:** We outlined detection methods:
    *   **CloudTrail `PutBucketPolicy`:** Monitoring CloudTrail for `PutBucketPolicy` events is the most direct way to detect this attack. Any change to a bucket policy should trigger an alert and be investigated.
    *   **GuardDuty `Policy:S3/BucketAnonymousAccessGranted`:** This finding is helpful, but as we noted, it only applies to *public* access, not access granted to a specific external account.
    *   **IAM Access Analyzer:** Access Analyzer is a powerful tool for identifying overly permissive policies, including those that grant cross-account access to S3 buckets.

**Practical Example and Elaboration**

Let's consider a slightly more concrete example to illustrate the attack and its implications. Suppose a company, "ExampleCorp," uses an S3 bucket named `examplecorp-data` to store sensitive customer information. We compromises an IAM user's credentials.

1.  **Initial Access:** We uses the compromised credentials to gain initial access to ExampleCorp's AWS environment. However, these credentials might have limited permissions.

2.  **Stratus Red Team Setup:** We installs and configures Stratus Red Team.

3.  **Warmup:**
    ```zsh
    stratus warmup aws.exfiltration.s3-backdoor-bucket-policy
    ```
    This creates a *new* bucket (e.g., `stratus-red-team-bdbp-abcdefgh`).  It's important to understand that Stratus Red Team, by default, doesn't target an *existing* bucket. It creates its own to demonstrate the vulnerability.

4.  **Detonate:**
    ```zsh
    stratus detonate aws.exfiltration.s3-backdoor-bucket-policy
    ```
    This modifies the bucket policy of the *newly created* bucket (e.g., `stratus-red-team-bdbp-abcdefgh`) to allow read access from the fictitious AWS account `193672423079`.

5.  **Data Exfiltration (Hypothetical):**  We now controlling the fictitious AWS account (in theory), and use the AWS CLI to access the backdoored bucket:
    ```zsh
    aws s3 ls s3://stratus-red-team-bdbp-abcdefgh --profile fictitious-account
    aws s3 cp s3://stratus-red-team-bdbp-abcdefgh/sensitive-file.txt . --profile fictitious-account
    ```
    **Important Note:** The `--profile fictitious-account` part would require us to have configured a profile named `fictitious-account` using AWS CLI, pointing to credentials that *we* control. The <account ID> is just a placeholder in the bucket policy. We didn't actually need to control that specific AWS account.  The policy simply *allows* access from that account ID; we leverage this by using *any* credentials and specifying the allowed account ID in the policy. This is a crucial subtlety.

6.  **Credential Revocation:** ExampleCorp detects the initial compromise and revokes the IAM user's credentials. However, the bucket policy remains unchanged.

7.  **Persistent Access:** Because the bucket policy was modified, we *still* have access to the data in the `stratus-red-team-bdbp-abcdefgh` bucket, even after the original compromised credentials are revoked.

8.  **Revert and Cleanup:**
    ```zsh
    stratus revert aws.exfiltration.s3-backdoor-bucket-policy  # Removes the malicious policy
    stratus cleanup aws.exfiltration.s3-backdoor-bucket-policy # Deletes the bucket
    ```

**Improving (Suggestions)**

1.  **Explicitly State New Bucket Creation:** Make it *very* clear in the challenge that Stratus Red Team creates a *new* S3 bucket for this attack, rather than modifying an existing one. This avoids potential confusion and accidental modification of production resources.

2.  **Clarify Fictitious Account Usage:** Explain in more detail how the "fictitious AWS account" is used. Emphasize that we don't need to control the fictitious account itself; we just need to configure the AWS CLI to use *any* credentials and leverage the permission granted to the fictitious account in the bucket policy.  The example with `--profile fictitious-account` I provided above is a good example.

3.  **Detection with CloudTrail:** Provide a specific example of a CloudTrail event for `PutBucketPolicy`. Show what the event looks like in the CloudTrail logs, highlighting the `eventSource`, `eventName`, `requestParameters`, and `responseElements` that would indicate the policy modification. This would make the detection section more practical. For example:

    ```json
    {
        "eventVersion": "1.08",
        "userIdentity": {
            "type": "IAMUser",
            "principalId": "AIDA...",
            "arn": "arn:aws:iam::123456789012:user/attacker",
            "accountId": "123456789012",
            "accessKeyId": "AKIA...",
            "userName": "attacker"
        },
        "eventTime": "2025-03-16T12:00:00Z",
        "eventSource": "s3.amazonaws.com",
        "eventName": "PutBucketPolicy",
        "awsRegion": "us-east-1",
        "sourceIPAddress": "192.0.2.1",
        "userAgent": "aws-cli/2.0.0",
        "requestParameters": {
            "bucketName": "stratus-red-team-bdbp-abcdefgh",
            "policy": "{\\"Version\\":\\"2012-10-17\\",\\"Statement\\":[{\\"Effect\\":\\"Allow\\",\\"Principal\\":{\\"AWS\\":\\"arn:aws:iam::193672423079:root\\"},\\"Action\\":[\\"s3:GetObject\\",\\"s3:GetBucketLocation\\",\\"s3:ListBucket\\"],\\"Resource\\":[\\"arn:aws:s3:::stratus-red-team-bdbp-abcdefgh/*\\",\\"arn:aws:s3:::stratus-red-team-bdbp-abcdefgh\\"]}]}"
        },
        "responseElements": null,
        "requestID": "...",
        "eventID": "...",
        "eventType": "AwsApiCall",
        "managementEvent": true,
        "readOnly": false,
        "recipientAccountId": "123456789012"
    }
    ```

    We then explain how to set up CloudTrail to log data events for S3 and how to create alerts based on the `PutBucketPolicy` event.

4.  **IAM Access Analyzer Example:**  Show an example of how IAM Access Analyzer would generate a finding for the modified bucket policy. This would involve showing the Access Analyzer console and the details of the finding.

5.  **Prevention:** Add a section on *preventing* this type of attack. This would include:

    *   **Principle of Least Privilege:** Grant only the necessary permissions to IAM users and roles.
    *   **Bucket Policy Best Practices:**  Use condition keys (e.g., `aws:SourceIp`, `aws:PrincipalOrgID`) to restrict access further, even within allowed accounts.
    *   **Regular Audits:** Regularly review bucket policies and IAM roles to identify and remediate overly permissive configurations.
    *   **S3 Block Public Access:** Use S3 Block Public Access settings to prevent accidental public exposure of buckets.
    *   **Infrastructure as Code (IaC):** Use IaC tools like Terraform or CloudFormation to manage bucket policies, allowing for version control, review, and automated enforcement of security best practices.
