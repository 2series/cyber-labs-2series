# Convert CLI credentials into AWS Console access with AWS Consoler

Ever had temporary credentials from assuming a role or long-term AWS credentials like an access key and struggled to log in to the AWS Management Console? AWS_Consoler is an open source tool that simplifies the process by generating an AWS console sign-in link from API/CLI credentials using the federation endpoint. In this lab, I’ll receive credentials and learn how to use AWS_Consoler with both IAM user access keys and IAM role temporary credentials.

**Core Concept: AWS Consoler**

AWS Consoler is a tool that generates a temporary AWS Management Console sign-in URL from AWS CLI credentials (either long-term access keys or temporary credentials from `sts:AssumeRole`).  It leverages the AWS Federation endpoint to achieve this.  This is *extremely* useful for quickly accessing the console when we only have programmatic access credentials.

**Key Benefits:**

*   **Convenience:**  Avoids the manual process of converting CLI credentials into a console session.
*   **Security (Indirectly):**  Encourages the use of temporary credentials (via `sts:AssumeRole`) which are best practice.
*   **Speed:** Faster than manually constructing federation URLs.

**Installation (Two Methods):**

1.  **Recommended: Using `pip` (Python Package Installer):**

    ```zsh
    pip install aws-consoler
    ```

    *   **Pros:**  Gets the latest stable release, handles dependencies.
    *   **Cons:** Requires `pip` to be pre-installed.  If you don't have Python and pip set up, this can be a hurdle.
    *   **Important Note:** The command to run the tool is `aws_consoler` (with an underscore), *not* `aws-consoler` (with a hyphen, which is the package name). This is a common point of confusion.

2.  **Alternative: Cloning the GitHub Repository:**

    ```zsh
    git clone git://github.com/netspi/aws_consoler
    ```

    *   **Pros:**  Quick and easy if you don't have `pip`.
    *   **Cons:**  Might not be the latest stable version; you're getting the code directly from the repository. You'll also need to manually manage dependencies.  You'll likely need to run it as a Python script (e.g., `python aws_consoler/aws_consoler.py`).

**Verification (after either installation method):**

Run `aws_consoler` with no arguments. You should see an error message like this:

```markdown
2025-03-14 10:47:43,822 [aws_consoler.logic] WARNING: Creds still permanent, creating federated session.
2025-03-14 10:47:44,146 [aws_consoler.cli] CRITICAL: Error obtaining federation token from STS. Ensure the IAM user has sts:GetFederationToken permissions, or provide a role to assume.
```

This error *confirms* that the tool is installed correctly.  It's expecting credentials or a role ARN.

**Usage Scenarios and Commands:**

Our lab covers three primary usage scenarios:

1.  **Using Long-Term IAM User Credentials (Access Key & Secret Key):**

    ```zsh
    aws_consoler -a <ACCESS_KEY_ID> -s <SECRET_ACCESS_KEY>
    ```

    *   **`<ACCESS_KEY_ID>`:**  Your IAM user's Access Key ID (starts with `AKIA`).
    *   **`<SECRET_ACCESS_KEY>`:** Your IAM user's Secret Access Key.
    *   **Output:** A long URL that you paste into your browser to sign in to the AWS console.

    **Example from the lab:**

    ```zsh
    aws_consoler -a <ACCESS_KEY_ID> -s <SECRET_ACCESS_KEY>
    ```

2.  **Using IAM User Credentials to Assume a Role (Recommended):**

    This is the preferred approach, as it uses temporary credentials.

    *   **Step 1: Configure AWS CLI Profile (if not already done):**

        ```zsh
        aws configure --profile cybr  # Or any profile name
        ```
        You'll be prompted to enter your Access Key ID, Secret Access Key, default region, and output format.

    *   **Step 2: (Optional, but helpful) Get the Role ARN:**
        This step is specific to the lab environment to find the pre-created role.  In a real-world scenario, we would *know* the Role ARN we need to assume.

        ```zsh
        aws iam list-roles --query "Roles[?RoleName=='ConsoleAccessRole']" --profile cybr
        ```

    *   **Step 3: Use `aws_consoler` with the Role ARN:**

        ```zsh
        aws_consoler -a <ACCESS_KEY_ID> -s <SECRET_ACCESS_KEY> -r <ROLE_ARN> -R <REGION>
        ```

        *   **`-r <ROLE_ARN>`:** The Amazon Resource Name (ARN) of the IAM role we want to assume.
        *   **`-R <REGION>`:**  (Optional) The AWS region we want the console to open in (e.g., `us-east-1`).

        **Example from the lab:**
        ```zsh
        aws_consoler -a <ACCESS_KEY_ID> -s <SECRET_ACCESS_KEY>> -r arn:aws:iam::272281913033:role/ConsoleAccessRole -R us-east-1
        ```

3.  **Using Temporary Credentials (Directly):**

    This method is used *after* we've already assumed a role and have the temporary credentials.

    *   **Step 1: Assume the Role (using the AWS CLI):**

        ```zsh
        aws sts assume-role --role-arn <ROLE_ARN> --role-session-name <SESSION_NAME> --profile <PROFILE_NAME>
        ```

        *   **`<ROLE_ARN>`:** The ARN of the role.
        *   **`<SESSION_NAME>`:** A name we choose for the session (e.g., "ConsoleSession").
        *   **`<PROFILE_NAME>`:** The AWS CLI profile we configured.
        *   **Output:**  This command returns a JSON object containing the temporary `AccessKeyId`, `SecretAccessKey`, and `SessionToken`.

        **Example from the lab:**

        ```zsh
        aws sts assume-role --role-arn arn:aws:iam::272281913033:role/ConsoleAccessRole --role-session-name ConsoleRole --profile cybr
        ```

    *   **Step 2: Use `aws_consoler` with the Temporary Credentials:**

        ```zsh
        aws_consoler -a <TEMP_ACCESS_KEY_ID> -s <TEMP_SECRET_ACCESS_KEY> -t <SESSION_TOKEN> -R <REGION>
        ```

        *   **`<TEMP_ACCESS_KEY_ID>`:** The temporary Access Key ID (starts with `ASIA`).
        *   **`<TEMP_SECRET_ACCESS_KEY>`:** The temporary Secret Access Key.
        *   **`<SESSION_TOKEN>`:** The Session Token.
        *   **`-R <REGION>`:** (Optional) The AWS region.

**Key Command-Line Options (from `aws_consoler -h`):**

*   **`-h`, `--help`:**  Displays the help menu.
*   **`-p PROFILE`, `--profile PROFILE`:** Use a named AWS CLI profile.  This is *instead of* providing `-a`, `-s`, and `-t`.
*   **`-a ACCESS_KEY_ID`, `--access-key-id ACCESS_KEY_ID`:**  The Access Key ID.
*   **`-s SECRET_ACCESS_KEY`, `--secret-access-key SECRET_ACCESS_KEY`:** The Secret Access Key.
*   **`-t SESSION_TOKEN`, `--session-token SESSION_TOKEN`:** The Session Token (required for temporary credentials).
*   **`-r ROLE_ARN`, `--role-arn ROLE_ARN`:** The ARN of the role to assume.
*   **`-R REGION`, `--region REGION`:** The desired AWS region for the console.
*   **`-o`, `--open`:**  *Automatically* open the generated URL in our default browser.  This is very convenient!
*   **`-v`, `--verbose`:** Increase verbosity (use multiple times for more detail, up to `-vvv`).
*   **`-eS STS_ENDPOINT`, `--sts-endpoint STS_ENDPOINT` (Advanced):** Specify a custom STS endpoint (e.g., for corporate proxies).
*   **`-eF FEDERATION_ENDPOINT`, `--federation-endpoint FEDERATION_ENDPOINT` (Advanced):** Specify a custom federation endpoint.
*   **`-eC CONSOLE_ENDPOINT`, `--console-endpoint CONSOLE_ENDPOINT` (Advanced):** Specify a custom console endpoint.

**Important Considerations + Improvements:**

*   **Permissions:** The IAM user whose credentials we're using (either long-term or to assume a role) needs the `sts:GetFederationToken` permission.  If assuming a role, the user also needs `sts:AssumeRole` permission for that specific role.  The error message from `aws_consoler` clearly indicates if this is the issue.
*   **Temporary Credentials are Best Practice:** Our lab demonstrates both long-term and temporary credentials, but always prefer using `sts:AssumeRole` to obtain temporary credentials.  This limits the blast radius of compromised credentials.
*   **Profile Usage:** Our lab could be improved by demonstrating the `-p` (profile) option more thoroughly.  This is often the cleanest way to use `aws_consoler` if we have our AWS CLI configured.
*   **Error Handling:** Our lab doesn't explicitly cover error handling.  If `aws_consoler` fails, check:
    *   **Correct Credentials:**  Make sure we've entered the Access Key ID, Secret Access Key, and Session Token (if applicable) correctly.
    *   **Permissions:**  Verify the IAM user/role has the necessary permissions (`sts:GetFederationToken`, `sts:AssumeRole`).
    *   **Network Connectivity:** Ensure we can reach the AWS STS and Federation endpoints.
    *   **AWS CLI Configuration:** If using profiles, double-check our `~/.aws/credentials` and `~/.aws/config` files.
* **Open Option:** Our lab doesn't use the `-o` or `--open` option. Using it makes the process even smoother.

**Revised Lab Steps (Improved and More Concise):**

Here's a streamlined version of the lab, incorporating best practices and clarifications:

1.  **Installation:**

    ```zsh
    pip install aws-consoler  # Or git clone if pip is unavailable
    ```

2.  **Configuration (One-Time):**

    ```zsh
    aws configure --profile my-profile  # Replace 'my-profile'
    # Enter your long-term Access Key ID, Secret Access Key, region, and output format.
    ```

3.  **Scenario 1: Console Access with Long-Term Credentials (Less Recommended):**

    ```zsh
    aws_consoler -p my-profile -o # Opens directly in browser
    ```

4.  **Scenario 2: Console Access via Role Assumption (Recommended):**

    *   **Know your Role ARN:**  (e.g., `arn:aws:iam::123456789012:role/MyConsoleAccessRole`)
    *   **Assume the Role and Get Console Access:**

        ```zsh
        aws_consoler -p my-profile -r arn:aws:iam::123456789012:role/MyConsoleAccessRole -R us-east-1 -o
        ```

5.  **Scenario 3: Console Access with *Existing* Temporary Credentials:**

    *   **Assume the Role (if you haven't already):**

        ```zsh
        aws sts assume-role --role-arn arn:aws:iam::123456789012:role/MyConsoleAccessRole --role-session-name MySession --profile my-profile > temp_creds.json
        ```
       *This stores the credentials in the temp_creds.json file.*

    *   **Extract Credentials (using `jq` - a command-line JSON processor - install if needed):**
        ```zsh
        TEMP_ACCESS_KEY=$(jq -r .Credentials.AccessKeyId temp_creds.json)
        TEMP_SECRET_KEY=$(jq -r .Credentials.SecretAccessKey temp_creds.json)
        TEMP_SESSION_TOKEN=$(jq -r .Credentials.SessionToken temp_creds.json)
        ```

    *   **Use `aws_consoler`:**

        ```zsh
        aws_consoler -a "$TEMP_ACCESS_KEY" -s "$TEMP_SECRET_KEY" -t "$TEMP_SESSION_TOKEN" -R us-east-1 -o
        ```
        *The double quotes are important to handle any special character.*

Our revised structure is more organized, uses profiles where appropriate, emphasizes the preferred `AssumeRole` method, and includes the `-o` option for a better user experience. It also shows how to handle the output of `sts assume-role` more robustly using `jq`. This revised set of instructions is clearer, safer, and more aligned with best practices.

