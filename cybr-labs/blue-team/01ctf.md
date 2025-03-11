## Generate IAM Credentials Reports

**Core Concepts**

*   **IAM Credentials Report:** A built-in AWS tool that provides a snapshot of the security status of your IAM users.  It's a CSV file containing critical information for security audits and compliance.
*   **Security Implications:** The report helps identify potential risks, such as:
    *   Inactive users with active credentials (passwords or access keys).
    *   Users who haven't rotated their access keys in a long time.
    *   Users without MFA enabled.
    *   Root user activity (which should be minimized).
*   **Report Frequency:** AWS generates a new report every 4 hours.  If you request a report within that 4-hour window, you'll get the previously generated one.

**Generating the Report (AWS Console)**

1.  **Navigate to IAM:** In the AWS Management Console, go to the IAM service.
2.  **Find Credential Report:** In the left-hand navigation pane, look for "Credential report" (it's usually under "Access reports").
3.  **Download:** Click the "Download Report" button. This downloads a CSV file to your local machine.

**Generating the Report (AWS CLI)**

The CLI provides more flexibility for automation.  Here's a breakdown of the commands and a more robust script:

1.  **Generate the Report (if needed):**

    ```zsh
    aws iam generate-credential-report
    ```

    *   **Output:**
        *   `"State": "STARTED"`:  Indicates a new report is being generated.
        *   `"State": "COMPLETE"`:  Indicates a report is ready (or was already ready).  You might also see `"State": "INPROGRESS"`.
    *   **Important:**  You only need to run this command if a report hasn't been generated in the last 4 hours.

2.  **Retrieve the Report:**

    ```zsh
    aws iam get-credential-report
    ```

    *   **Output:** This command returns a JSON object.  The key parts are:
        *   `"Content"`:  A base64-encoded string containing the CSV data.
        *   `"ReportFormat"`:  Should be "text/csv".
        *   `"GeneratedTime"`:  The timestamp when the report was generated.

3.  **Decode and Process (Basic):**

    ```zsh
    aws iam get-credential-report --output text --query Content | base64 -d
    ```

    *   `--output text`:  Changes the output format to plain text.
    *   `--query Content`:  Extracts only the base64-encoded content.
    *   `| base64 -d`: Pipes the output to the `base64` command with the `-d` flag (for decode).  On some systems (like macOS), you might need `-D` instead of `-d`.  Use `base64 --help` to check your system's correct flag.

4.  **Decode and Process (Formatted Output - Recommended):**

    ```zsh
    aws iam get-credential-report --output text --query Content | base64 -d | awk -F, '
    NR==1 {next}
    {
        print "User:", $1;
        print "ARN:", $2;
        print "Creation Time:", $3;
        print "Password Enabled:", $4;
        print "Password Last Used:", $5;
        print "Password Last Changed:", $6;
        print "Password Next Rotation:", $7;
        print "MFA Active:", $8;
        print "Access Key 1 Active:", $9;
        print "Access Key 1 Last Rotated:", $10;
        print "Access Key 1 Last Used Date:", $11;
        print "Access Key 1 Last Used Region:", $12;
        print "Access Key 1 Last Used Service:", $13;
        print "Access Key 2 Active:", $14;
        print "Access Key 2 Last Rotated:", $15;
        print "Access Key 2 Last Used Date:", $16;
        print "Access Key 2 Last Used Region:", $17;
        print "Access Key 2 Last Used Service:", $18;
        print "Cert 1 Active:", $19;
        print "Cert 1 Last Rotated:", $20;
        print "Cert 2 Active:", $21;
        print "Cert 2 Last Rotated:", $22;
        print "-------------------"
    }'
    ```

    *   `awk -F,`:  Uses the `awk` command to process the CSV data. `-F,` sets the field separator to a comma.
    *   `NR==1 {next}`:  Skips the header row (the first line).
    *   The rest of the `awk` script formats the output for readability, printing each field with a label.

**Scripting for Automation (Bash)**

Here's a more complete Bash script that handles report generation, checks the state, and decodes the content:

```bash
#!/bin/bash

# Generate the report (if needed)
aws iam generate-credential-report

# Wait for the report to be ready (with a timeout)
MAX_ATTEMPTS=10
SLEEP_TIME=5
attempt=0

while [ $attempt -lt $MAX_ATTEMPTS ]; do
  state=$(aws iam get-credential-report --output text --query State 2>/dev/null) # 2>/dev/null supresses errors if report not generated

  if [ "$state" = "COMPLETE" ]; then
    break
  elif [ "$state" = "STARTED" ] || [ "$state" = "INPROGRESS" ] ; then
    echo "Waiting for report to be generated..."
    sleep $SLEEP_TIME
    attempt=$((attempt + 1))
  else
      echo "Error: Report not generated. State: $state"
      exit 1
  fi

done

if [ $attempt -eq $MAX_ATTEMPTS ]; then
  echo "Timeout: Report generation took too long."
  exit 1
fi


# Retrieve, decode, and pretty-print the report
aws iam get-credential-report --output text --query Content | base64 -d | awk -F, '
NR==1 {next}
{
    print "User:", $1;
    print "ARN:", $2;
    print "Creation Time:", $3;
    print "Password Enabled:", $4;
    print "Password Last Used:", $5;
    print "Password Last Changed:", $6;
    print "Password Next Rotation:", $7;
    print "MFA Active:", $8;
    print "Access Key 1 Active:", $9;
    print "Access Key 1 Last Rotated:", $10;
    print "Access Key 1 Last Used Date:", $11;
    print "Access Key 1 Last Used Region:", $12;
    print "Access Key 1 Last Used Service:", $13;
    print "Access Key 2 Active:", $14;
    print "Access Key 2 Last Rotated:", $15;
    print "Access Key 2 Last Used Date:", $16;
    print "Access Key 2 Last Used Region:", $17;
    print "Access Key 2 Last Used Service:", $18;
    print "Cert 1 Active:", $19;
    print "Cert 1 Last Rotated:", $20;
    print "Cert 2 Active:", $21;
    print "Cert 2 Last Rotated:", $22;
    print "-------------------"
}'

# Or, save the decoded report to a file:
# aws iam get-credential-report --output text --query Content | base64 -d > credential_report.csv

exit 0
```

Key improvements in this script:

*   **Error Handling:** Checks the `State` of the report generation and handles potential errors.
*   **Timeout:**  Includes a timeout mechanism to prevent the script from waiting indefinitely.
*   **Readability:** Uses comments and clear variable names.
*   **Flexibility:** Shows how to both print the formatted output and save the raw CSV to a file.
*   **Robust Decoding:** Uses `base64 -d` (or `-D` if needed) to decode the report content correctly.
*   **Suppressed STDERR**: Added `2>/dev/null` to suppress the STDERR when querying the state and the report hasn't been generated.

**Security Recommendations (Based on Report Findings)**

After generating the report, here's what to look for and recommended actions:

1.  **`password_enabled` = `true` and `mfa_active` = `false`:**
    *   **Risk:**  Users are relying solely on passwords, making them vulnerable to brute-force and phishing attacks.
    *   **Recommendation:** Enforce MFA for all IAM users.  This is a critical security best practice.

2.  **`password_last_used` or `access_key_1_last_used_date` / `access_key_2_last_used_date` is very old or `N/A`:**
    *   **Risk:**  Indicates inactive users or unused credentials.  These are potential targets for attackers.
    *   **Recommendation:**
        *   Disable or delete inactive users.
        *   Rotate access keys that haven't been used recently.
        *   Implement a policy for regular access key rotation (e.g., every 90 days).

3.  **`<root_account>` activity:**
    *   **Risk:**  The root user has full access to your AWS account.  Its use should be extremely limited.
    *   **Recommendation:**
        *   Enable MFA for the root user.
        *   *Never* use the root user for day-to-day tasks.  Create IAM users with appropriate permissions instead.
        *   Monitor root user activity closely.

4.  **`access_key_1_active` = `true` or `access_key_2_active` = `true` for users who should only use the console:**
    *   **Risk:**  Access keys are meant for programmatic access.  If a user only needs console access, they shouldn't have active access keys.
    *   **Recommendation:**  Disable or delete the access keys for these users.

5.  **Missing or outdated information:**
    *    If the report does not reflect expected users or credential states, investigate and correct IAM configurations.

**Integrating with System Prompt (from your first response)**

You can integrate the output of the credential report (or a summary of its findings) into a system prompt for an LLM.  For example:

```python
import subprocess
import json
from datetime import datetime

def generate_credential_report_summary():
    """Generates a summary of the IAM credential report."""

    try:
        # Run the AWS CLI command and capture the output
        result = subprocess.run(
            ["bash", "-c", "aws iam get-credential-report --output text --query Content | base64 -d"],
            capture_output=True,
            text=True,
            check=True,
        )
        decoded_report = result.stdout

        # Basic parsing (you might want to use a CSV library for more robust parsing)
        lines = decoded_report.strip().split('\n')
        header = lines[0].split(',')
        report_data = [dict(zip(header, line.split(','))) for line in lines[1:]]

        # Create a summary
        summary = {
            "report_generated_time": datetime.now().isoformat(),  # Use current time, as report time isn't easily available in this context
            "users_without_mfa": [],
            "inactive_users": [],
            "users_with_old_access_keys": [],
        }

        for user_data in report_data:
            if user_data.get('password_enabled') == 'true' and user_data.get('mfa_active') == 'false':
                summary["users_without_mfa"].append(user_data['user'])

            # Check for inactive users (example: last used > 90 days ago)
            # This requires date parsing, which is simplified here
            try:
                last_used_date_str = user_data.get('password_last_used') or user_data.get('access_key_1_last_used_date') or user_data.get('access_key_2_last_used_date')
                
                if last_used_date_str and last_used_date_str != 'N/A':
                    last_used_date = datetime.strptime(last_used_date_str.split('T')[0], '%Y-%m-%d') #parse only date part
                    days_since_last_use = (datetime.now() - last_used_date).days
                    if days_since_last_use > 90:
                        summary["inactive_users"].append(user_data['user'])
            except (ValueError, TypeError):
                pass  # Handle cases where date parsing fails

            # Check for old access keys (example: last rotated > 90 days ago)
            try:
                last_rotated_str = user_data.get('access_key_1_last_rotated') or user_data.get('access_key_2_last_rotated')
                if last_rotated_str and last_rotated_str != 'N/A':
                    last_rotated_date = datetime.strptime(last_rotated_str.split('T')[0], '%Y-%m-%d')
                    days_since_rotation = (datetime.now() - last_rotated_date).days
                    if days_since_rotation > 90:
                        summary["users_with_old_access_keys"].append(user_data['user'])
            except (ValueError, TypeError):
                pass
        return json.dumps(summary, indent=2)

    except subprocess.CalledProcessError as e:
        return f"Error generating report: {e}"

# Example usage:
summary = generate_credential_report_summary()
print(summary)

now = datetime.now().toLocaleDateString()
sys_prompt = f"""You are an expert security analyst. Today is {now}.

Here is a summary of the latest IAM Credentials Report:

{summary}

Based on this report, provide prioritized security recommendations.  Consider the following:

- Inactive users and credentials.
- Users without MFA enabled.
- Access key rotation policies.
- Root user activity.
- Any other potential security risks.
"""
print(sys_prompt)

```

Key changes and explanations in this Python script:

*   **`subprocess.run`:**  Executes the AWS CLI command to get the credential report.  The `capture_output=True` argument captures the output, and `text=True` ensures the output is treated as text. `check=True` raises an exception if the command fails.  Uses `bash -c` to handle the pipe.
*   **Simplified Parsing:** Uses a basic approach to parse the CSV data.  For production use, consider the `csv` module for more robust parsing.  It splits the output into lines and then splits each line by commas. It creates a list of dictionaries, where each dictionary represents a user and their credentials.
*   **Summary Generation:** Creates a summary dictionary containing:
    *   `report_generated_time`:  The current time (since we're generating the report on demand).
    *   `users_without_mfa`:  A list of users with passwords enabled but MFA disabled.
    *   `inactive_users`: A list of users who haven't used their credentials recently (example: 90 days).
    *   `users_with_old_access_keys`:  A list of users whose access keys haven't been rotated recently (example: 90 days).
*   **Date Handling:**  Includes *simplified* date parsing to determine inactive users and old access keys. It handles potential `ValueError` or `TypeError` exceptions that might occur if date parsing fails.  It parses only the date portion of the datetime strings.
*   **Error Handling:**  Catches `subprocess.CalledProcessError` to handle errors from the AWS CLI command.
*   **System Prompt Integration:**  Creates a system prompt that includes the generated summary and instructions for the LLM.
* **JSON Output**: The summary is converted to JSON for easier parsing by other systems.
