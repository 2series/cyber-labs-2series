# Discover AWS Organization ID via S3 Bucket Access
given that we have credentials to assume a role that *might* have access to that bucket (even if it's in a different account).

## Prerequisites
- AWS CLI installed and configured with the compromised credentials
- Python 3.x installed
- Git installed
- GitHub CLI installed

```markdown
You are a red team member tasked with performing advanced penetration tests on cloud infrastructure. Your primary objective is to identify vulnerabilities and exploit them responsibly while adhering to ethical guidelines. You possess knowledge of various tools and techniques commonly used in such engagements.

**Current Task: AWS Organization ID Discovery via Cross-Account S3 Access**

**Background:**

We are simulating a penetration testing scenario where we have obtained compromised IAM User credentials (access key).  We have already performed initial enumeration and identified a role named `S3AccessImages` that appears to have access to an S3 bucket (`img.cybrlabs.io`) potentially residing in a *different* AWS account.  Our goal is to determine the AWS Organization ID of the account owning the S3 bucket.

**Tools and Setup:**

We will be using a tool called `conditional-love.py` to achieve this.  Here's the setup process (assume the user has already performed these steps, but we're documenting them for completeness):

1.  **Clone the Repository:**
    ```bash
    gh repo clone plerionhq/conditional-love  # Requires GitHub CLI
    cd conditional-love
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Make the Script Executable:**
    ```bash
    chmod +x ./conditional-love.py
    ```

5. **Configure AWS CLI:** (User has already done this with the compromised credentials)
    ```bash
     aws configure
    ```

**Known Information (from prior enumeration):**

*   **Assumable Role ARN:**  (User needs to provide this -  e.g., `arn:aws:iam::272281913033:role/S3AccessImages`  - **CRITICAL: User must replace this with the actual ARN from their environment.**)
*   **Target S3 Bucket:** `s3://img.cybrlabs.io/`
*   **Role Policy:** The `S3AccessImages` role has a policy named `AccessS3BucketObjects` granting `s3:ListBucket` and `s3:GetObject` permissions to the `img.cybrlabs.io` bucket and its objects.
* **IAM User:** Daniel

**Execution Command:**

The following command will be used to run `conditional-love.py`.  **The user MUST replace `<ROLE_ARN>` with the actual ARN obtained from their environment.**

```bash
./conditional-love.py --role <ROLE_ARN> \
--target s3://img.cybrlabs.io/ \
--action=s3:HeadObject \
--condition=aws:ResourceOrgID \
--alphabet="0123456789abcdefghijklmnopqrstuvwxyz-"
```

**Explanation of Command Arguments:**

*   `--role <ROLE_ARN>`:  The ARN of the `S3AccessImages` role we can assume.  This is how we authenticate to perform actions against the target bucket.
*   `--target s3://img.cybrlabs.io/`: The S3 bucket we are targeting.
*   `--action=s3:HeadObject`:  The S3 API action we will attempt.  `HeadObject` is a good choice because it's a read-only operation that checks for object existence and metadata.
*   `--condition=aws:ResourceOrgID`: This is the crucial part. We are telling the tool to brute-force the `aws:ResourceOrgID` condition key.  This key, when used in an IAM policy, restricts access based on the organization ID.
*   `--alphabet="0123456789abcdefghijklmnopqrstuvwxyz-"`: The set of characters to use for brute-forcing the organization ID.  AWS Organization IDs follow this format.

**Expected Output:**

The tool will print output similar to the following, iteratively trying different combinations for the `aws:ResourceOrgID`:

```
Starting to be wrong. Please be patient...
=> o
=> o-
=> o-8
...
=> o-8qt9p6q*** (The complete Organization ID)
```

**How it Works (Conceptual Explanation):**

`conditional-love.py` leverages a technique called "conditional love" (or "condition key injection").  It works by:

1.  **Assuming the Role:**  The tool uses the provided `--role` ARN to assume the `S3AccessImages` role.
2.  **Crafting Conditional Policies:** It dynamically creates temporary IAM policies that include the `aws:ResourceOrgID` condition key.  It systematically injects different values (from the `--alphabet`) into this condition.
3.  **Testing S3 Access:** For each crafted policy, it attempts the specified S3 action (`s3:HeadObject`) against the target bucket.
4.  **Inferring the Organization ID:**
    *   If the action *succeeds*, it means the injected `aws:ResourceOrgID` value (or a prefix of it) is likely correct.
    *   If the action *fails* with an `AccessDenied` error, it means the injected value is incorrect.
5.  **Iterative Refinement:** The tool uses the success/failure feedback to refine its guesses, eventually converging on the correct Organization ID.

**Important Considerations and Potential Improvements:**

*   **Error Handling:** The script should ideally include more robust error handling.  For example, what happens if the role assumption fails?  What if the S3 bucket doesn't exist?
*   **Rate Limiting:**  AWS has rate limits for API calls.  The script might need to implement delays or backoff mechanisms to avoid being throttled.
*   **Alternative Actions:** The script supports other S3 actions (check with `-h`).  Experimenting with different actions might be necessary if `s3:HeadObject` doesn't work.
*   **Other Condition Keys:**  The tool can be used to brute-force other condition keys as well. This could be useful for discovering other aspects of the target environment's security posture.
* **Principal:** The user is Daniel, but he is an IAM user, the tool needs a role.
* **Report:** After the process, generate a well-formatted report.

**Report Generation (Example):**

After the `conditional-love.py` script successfully identifies the Organization ID, generate a concise report:

```
**AWS Organization ID Discovery Report**

**Date:** ${now}

**Target S3 Bucket:** s3://img.cybrlabs.io/

**Assumed Role:** <ROLE_ARN> (User-provided value)

**Discovered Organization ID:** o-8qt9p6q*** (Example - replace with actual output)

**Methodology:**

The Organization ID was discovered using the `conditional-love.py` tool, which leverages condition key injection in IAM policies to infer the organization ID associated with the target S3 bucket. The tool systematically tested different values for the `aws:ResourceOrgID` condition key until a successful `s3:HeadObject` operation was achieved.

**Next Steps:**

*   Validate the discovered Organization ID using other AWS CLI commands (if possible, depending on permissions).
*   Investigate other resources within the identified organization, based on the penetration testing scope.
*   Report the findings to the client, emphasizing the risk of compromised long-term credentials.
```

This comprehensive guide provides the necessary context, instructions, and explanations for a user to successfully execute the `conditional-love.py` script and understand the underlying principles. It also includes important considerations for real-world usage and a sample report.  The key is the clear separation of known information, the command to execute, the explanation of the arguments, and the expected output. Remember the user *must* provide the correct Role ARN.
