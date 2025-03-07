# Discover AWS Account ID via S3 Bucket

how the `s3-account-search` tool works and the underlying AWS IAM principles that make it possible.

**Key Concepts Explained and Expanded**

1.  **`s3:ResourceAccount` Condition Key:** This is the heart of the technique.  It allows us to restrict access to S3 resources based on the *owning* AWS account ID, *without* needing to know the specific bucket names in that account.  This is crucial for both legitimate security policies (e.g., "Allow access only to buckets owned by our organization's accounts") and, as demonstrated, for this enumeration technique.

2.  **`sts:AssumeRole` with Inline Policies:** The tool cleverly uses the `sts:AssumeRole` API call, which allows temporary assumption of an IAM role.  Crucially, it leverages the `--policy` parameter.  This parameter allows us to pass an *inline session policy*.  This inline policy *further restricts* the permissions granted by the role's attached policies.  It *doesn't* grant additional permissions; it only narrows them down.  This is why the tool can add the `s3:ResourceAccount` condition without needing the target role to already have overly permissive policies.

3.  **Iterative Guessing with Wildcards:** The tool combines the `s3:ResourceAccount` condition with the `StringLike` operator and wildcards (`*`).  This allows it to perform a binary-search-like approach:
    *   It starts by testing `0*`, `1*`, `2*`, etc., for the first digit.  An "Access Denied" response means the account ID doesn't start with that digit.  An "Access Granted" (or a different error indicating the bucket exists but access is restricted for other reasons) means the first digit has been found.
    *   It then proceeds to the second digit, prepending the discovered first digit (e.g., `70*`, `71*`, `72*`).
    *   This continues until all 12 digits are found.

4.  **CloudTrail Analysis (Hypothetical):** The provided CloudTrail logs illustrate *exactly* how the tool interacts with the AWS API.  We see the `AssumeRole` calls, and most importantly, you see the dynamically generated inline policies with the changing `s3:ResourceAccount` condition values.  This is excellent for understanding the process and for auditing/detecting such activity.

5.  **Rate Limiting and Detection:** The explanation correctly points out that AWS has rate limits.  While 120 attempts are far fewer than a trillion, repeated `AssumeRole` calls with rapidly changing policies *could* trigger security alerts or throttling.  A sophisticated attacker might introduce delays or use multiple source IPs to mitigate this.

6. **Efficiency:** The efficiency gain is huge. The script reduces the search space from 10<sup>12</sup> to 10 * 12.

**Improvements and Considerations**

*   **Error Handling:** The original text mentions, "An 'Access Granted' (or a different error indicating the bucket exists but access is restricted for other reasons) means the first digit has been found."  A robust tool should differentiate between:
    *   **True Access Granted:** The `AssumeRole` call succeeds, and subsequent `s3:ListBucket` or `s3:GetObject` calls also succeed.
    *   **Bucket Exists, Other Restrictions:** The `AssumeRole` call might succeed (because the account ID prefix is correct), but later S3 operations might fail due to other policy restrictions (e.g., missing `s3:ListBucket` permission).  The tool needs to handle this gracefully and not prematurely conclude it has found the full account ID.
    *   **Bucket Doesn't Exist:**  A 404 error on `s3:ListBucket` after a successful `AssumeRole` would indicate the bucket name itself is incorrect, even if the account ID prefix is right.
    * **AssumeRole Failure**: The assume role call itself could fail for reasons unrelated to the account ID.

*   **Stealth:**  As mentioned, rapid-fire `AssumeRole` calls are noisy.  A more stealthy approach might involve:
    *   **Slower Attempts:** Introduce significant delays between attempts.
    *   **Multiple Source IPs:** Distribute the requests across different IP addresses (if possible).
    *   **User-Agent Spoofing:** Modify the `User-Agent` header to make the requests appear less like a script.
    *   **Targeted Guessing:** If some information about the target account ID is known (e.g., it's a partner company, and their account IDs follow a pattern), start with more likely prefixes.

*   **Alternative Techniques (Beyond the Scope):** While this technique is effective, there are other ways to *potentially* enumerate account IDs, though they often require different preconditions or vulnerabilities:
    *   **Error Messages:** Some AWS services, if misconfigured, might leak account IDs in error messages.
    *   **DNS Records:**  If the S3 bucket is used for a website and has a custom domain, DNS records (CNAME, etc.) might reveal information.
    *   **Publicly Accessible Resources:**  If any objects in the bucket are unintentionally public, their URLs will contain the bucket name, and sometimes the account ID can be inferred or discovered through other means.
    *   **Cross-Account Roles:** If there are misconfigured cross-account roles that trust the attacker's account, more direct enumeration might be possible.
    * **Resource-Based Policies**: Examining resource based policies.

*   **Defense:**
    *   **Least Privilege:**  The most important defense is to follow the principle of least privilege.  The IAM user in this scenario should *only* have the absolute minimum permissions required.
    *   **CloudTrail Monitoring:**  Enable CloudTrail and actively monitor for suspicious `AssumeRole` activity, especially with unusual inline policies.
    *   **GuardDuty:**  AWS GuardDuty can detect anomalous API calls and potentially flag this type of enumeration.
    *   **IAM Access Analyzer:** Use IAM Access Analyzer to identify overly permissive policies and potential cross-account access issues.
    * **Explicit Deny:** Although not directly relevant to stopping this specific technique, consider explicit deny statements in your policies where appropriate.

* **Tool Usage Clarification:** The instructions could be slightly clearer:

    ```zsh
    # Install the tool
    pip install s3-account-search

    # Configure AWS CLI with the compromised IAM User credentials
    aws configure

    # Get the ARN of the S3AccessImages role (replace with the actual ARN from our lab)
    ROLE_ARN=$(aws iam list-roles --query "Roles[?RoleName=='S3AccessImages'].Arn" --output text)

    # Run the tool (replace with your actual ROLE_ARN)
    s3-account-search "$ROLE_ARN" s3://img.cybrlabs.io
    ```