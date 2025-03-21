# Creating Buckets + Uploading Objects, Assume Role

This lab focuses on creating Amazon S3 buckets and uploading objects while demonstrating the concept of assuming IAM roles.  It covers key AWS concepts such as IAM Users vs. IAM Roles, `sts:AssumeRole`, temporary credentials, and managing permissions through roles.

**Key Concepts**

*   **IAM Users vs. IAM Roles:**
    *   **IAM Users:**  Represent individual users or applications that need *long-term* access to AWS resources.  They have access keys (Access Key ID and Secret Access Key) that are stored and managed.  These are like permanent passwords.
    *   **IAM Roles:**  Designed for *temporary* access.  They don't have permanent credentials.  Instead, they are "assumed" by users or services, granting them temporary permissions.  This is safer because if the temporary credentials are compromised, they expire quickly.

*   **`sts:AssumeRole`:**  This is the core AWS Security Token Service (STS) action that allows an IAM User (or another entity) to *temporarily* assume the permissions of an IAM Role.

*   **Temporary Credentials:** When we assume a role, we receive:
    *   **Access Key ID:**  Starts with `ASIA` (different from the `AKIA` prefix for IAM User access keys).
    *   **Secret Access Key:**
    *   **Session Token:**  A critical component; it's a string that proves the credentials are valid and temporary.  It's used alongside the Access Key ID and Secret Access Key.
    *   **Expiration:**  A timestamp indicating when the credentials will expire.

*   **Profiles (`aws configure --profile`)**: The AWS CLI uses profiles to store different sets of credentials.  This allows me to easily switch between IAM User credentials and the temporary credentials of the assumed role.

*   **Permission Delegation:**  IAM Roles are a primary way to delegate permissions in AWS.  We grant a role specific permissions (e.g., to create S3 buckets), and then allow users or services to assume that role, inheriting those permissions *temporarily*.

**Step-by-Step Walkthrough with Explanations and System Prompt Integration**

1.  **Initial Setup (IAM User):**

    *   **`aws configure --profile s3`:**  Initially, start by configuring the AWS CLI with the long-term credentials of an IAM User.  This profile is named `s3`.  Our lab provides the Access Key ID, Secret Access Key, and sets the default region to `us-east-1`.

    *   **`aws sts get-caller-identity --profile s3`:** This command verifies *who* we are currently authenticated as.  The output shows the IAM User's ARN (`arn:aws:iam::...:user/...`).  This confirms we are using the `s3` profile and are authenticated as an IAM User.

2.  **Finding the Role:**

    *   **`aws iam list-roles --query "Roles[?RoleName=='AssumableS3Role']" --profile s3`:**  This command lists IAM roles in our account.  The `--query` parameter filters the results to find the role named "AssumableS3Role".  This is a crucial step to get the Role's ARN.
        *   **`AssumeRolePolicyDocument`:** Within the output, pay attention to the `AssumeRolePolicyDocument`.  My notes on this specifies *who* is allowed to assume the role. Our lab, it's configured to allow the specific IAM User we're using (`arn:aws:iam::...:user/S3User-...`) to assume the role.  This is a critical security control.

3.  **Assuming the Role:**

    *   **`aws sts assume-role --role-arn <ROLE_ARN> --role-session-name S3Role --profile s3`:**  This is the *key* command.
        *   **`--role-arn`:**  We provide the ARN of the `AssumableS3Role` we found in the previous step.
        *   **`--role-session-name`:**  We give the temporary session a name (e.g., `S3Role`).  This helps with auditing and tracking.
        *   **`--profile s3`:**  Important! We are still using the `s3` profile (the IAM User credentials) to *initiate* the `assume-role` call.  The IAM User needs permission to call `sts:AssumeRole` on the target role.

    *   **Output:** The command returns the temporary credentials (Access Key ID, Secret Access Key, Session Token, and Expiration).

4.  **Configuring the Role Profile:**

    *   **`aws configure --profile s3role`:**  We create a *new* AWS CLI profile named `s3role`. You'll be prompted to enter the temporary `AccessKeyId` and `SecretAccessKey` you received.

    *   **`aws configure set aws_session_token "<SESSION_TOKEN>" --profile s3role`:**  Crucially, we *must* also set the `aws_session_token` for the `s3role` profile.  Without this, the CLI won't be able to use the temporary credentials.

5.  **Verifying the Assumed Role:**

    *   **`aws sts get-caller-identity --profile s3role`:**  Now, we run `get-caller-identity` again, but this time using the `s3role` profile. The output should show an ARN that looks like `arn:aws:sts::...:assumed-role/AssumableS3Role/S3Role`. This confirms we are now authenticated *as the role*, not the user.

6.  **Issuing S3 Commands:**

    *   **`aws s3 ls --profile s3role`:**  We can now use standard S3 commands, but we *must* specify `--profile s3role` to use the role's credentials.

    *   **`aws s3api create-bucket --bucket <BUCKET_NAME> --profile s3role`:**  Create a bucket.

    *   **`aws s3 cp example.txt s3://<BUCKET_NAME>/ --profile s3role`:** Upload a file.

    *   **Demonstrating Access Denied:** The lab shows that if we try to run `aws s3api create-bucket` with the `--profile s3` (the IAM User profile), we get an "Access Denied" error. This highlights the difference in permissions between the user and the assumed role.

7.  **Accessing the AWS Console (Optional):**

    *   This section uses `awsume` (and the `awsume-console-plugin`), a third-party tool, to generate a sign-in URL for the AWS Management Console using the assumed role's temporary credentials. This is a convenient way to visually interact with AWS using the role's permissions.
        *   **`pip install awsume`**
        *   **`awsume-configure`**
        *   **`pip3 install awsume-console-plugin`**
        *   **`awsume s3role -cl`** : This command generates the sign-in URL.

**Integrating the System Prompt**

The system prompt you provided is excellent for setting the context for an AI assistant. Here's how it applies to this lab, and a few minor refinements:

```typescript
export const systemPrompt = () => {
  const now = new Date().toISOString();
  return `You are an expert AWS administrator and security specialist. Today is ${now}. Follow these instructions when responding to questions or providing assistance related to AWS:

  - Assume the user is familiar with AWS concepts but may need help with specific commands or configurations.
  - Be highly organized and provide step-by-step instructions.
  - Explain the *why* behind each step, not just the *what*.  For example, explain *why* IAM Roles are preferred over IAM Users for temporary access.
  - Suggest alternative solutions or best practices where applicable (e.g., using environment variables instead of profiles, mentioning the principle of least privilege).
  - Be proactive and anticipate potential issues or follow-up questions.
  - Treat the user as knowledgeable, but don't hesitate to provide detailed explanations.
  - Accuracy is paramount. Double-check commands and configurations.
  - Provide detailed explanations, especially regarding security implications.
  - Value best practices and security principles over convenience. Emphasize the importance of least privilege and temporary credentials.
  - Consider security best practices, like rotating credentials and using MFA.
  - If you need to make assumptions (e.g., about the user's environment), clearly state those assumptions.
  - **Specifically for this lab, focus on explaining the difference between IAM Users and Roles, the purpose of `sts:AssumeRole`, and how to manage temporary credentials.**`;
};
```

**How to Use This in Practice**

1.  **Code Implementation:** Use this `systemPrompt` function in your application where you're interacting with an AI model (like OpenAI's GPT models).  Pass the returned string as the "system" message in the API call.

2.  **User Interaction:** When a user asks questions about the lab, the AI will use this prompt as its guiding context. For example:

    *   **User:** "Why do I get 'Access Denied' when I try to create a bucket with `--profile s3`?"

    *   **AI (guided by the prompt):** "You are receiving an 'Access Denied' error because the AWS CLI profile named 's3' is configured with the credentials of your IAM User.  Your IAM User, as configured in the lab, does *not* have the necessary `s3:CreateBucket` permission.  IAM Users have long-term credentials.  To create the bucket, you need to use the `s3role` profile, which contains the *temporary* credentials obtained after assuming the `AssumableS3Role`.  This role *does* have the `s3:CreateBucket` permission. This is a security best practice: the role grants temporary access, and the credentials expire, reducing the risk compared to using long-term user credentials."

The AI's response is now much more helpful because it:

*   Understands the context (IAM User vs. Role).
*   Explains the *why* (permissions and temporary credentials).
*   Reinforces security best practices.
