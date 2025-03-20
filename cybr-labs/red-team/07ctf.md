# Intro to S3 Enumeration

S3 enumeration! It's one of the most critical aspects of assessing the security posture of an organization using Amazon Web Services (AWS). Understanding how to effectively enumerate S3 resources is not just about finding hidden assets; it's about identifying potential vulnerabilities and misconfigurations that could lead to unauthorized access or data leakage. In this guide, we'll walk through the basics of enumerating S3 resources using the AWS Command Line Interface (CLI), focusing on both identity-based and resource-based policies. We'll also discuss best practices and common pitfalls to avoid during your assessment.

**Key Concepts**

*   **Amazon S3 (Simple Storage Service):** AWS's object storage service.  Think of it as a giant, highly scalable, and durable <hard drive> in the cloud.
*   **Buckets:**  Top-level containers in S3.  They are globally unique (across all AWS accounts).  Think of them like <folders>, but at the highest level.  <Bucket names are part of the URL used to access objects>.
*   **Objects:**  The actual <files> stored within buckets.  Each object has a key (its name), data, and metadata.
*   **Enumeration:** The process of listing and discovering resources (buckets and objects in this case).  This is crucial for security assessments to understand what exists and what might be vulnerable.
*   **AWS CLI (Command Line Interface):**  The primary tool for interacting with AWS services from the command line.  It's essential for scripting and automation.
*   **IAM (Identity and Access Management):**  AWS's service for <controlling access to resources>.  It uses <users, roles, groups, and policies to define permissions>.
*   **Identity-Based Policies:**  Policies attached to IAM users, groups, or roles.  They define what actions those identities are allowed to perform.  (e.g., "This user can list S3 buckets.")
*   **Resource-Based Policies:** Policies attached directly to resources (like S3 buckets).  They define who can access the resource and what actions they can perform.  (e.g., "Only this user can access this bucket.")  *These override identity-based policies.*
*   **`sts get-caller-identity`:**  A fundamental command to determine *who you are* in the AWS context.  It tells you your user ID, account ID, and ARN (Amazon Resource Name).  This is always a good first step.
*   **ARN (Amazon Resource Name):** A <unique identifier for every resource> in AWS.  They have a specific format, and understanding them is important.
*   **S3 API Quirks:** S3 has some historical quirks, including different command sets (`s3`, `s3api`) and the `list-objects` vs. `list-objects-v2` distinction.

**Commands and Workflow**

1.  **Configure AWS CLI:**
    ```zsh
    aws configure
    # or, with a profile
    aws configure --profile <your_profile_name>
    ```
    You'll be prompted for your Access Key ID, Secret Access Key, default region (us-east-1 for the lab), and default output format (JSON is recommended).

2.  **Identify Yourself:**
    ```zsh
    aws sts get-caller-identity
    # or, with a profile
    aws sts get-caller-identity --profile <your_profile_name>
    ```
    This tells you which user/role you're authenticated as.

3.  **Enumerate IAM Permissions (Identity-Based):**
    *   **List User Policies:**  Find the policies attached directly to the user.
        ```zsh
        aws iam list-user-policies --user-name <your_username>
        ```
    *   **Get User Policy:** Retrieve the details of a specific policy.
        ```zsh
        aws iam get-user-policy --user-name <your_username> --policy-name <policy_name>
        ```
        This is crucial to understand what S3 actions the user is *supposed* to be able to perform.

4.  **Enumerate S3 Resources:**
    *   **List Buckets:**
        ```zsh
        aws s3api list-buckets
        ```
        This lists all buckets your identity has permission to see.
    *   **List Objects (v2 - recommended):**
        ```zsh
        aws s3api list-objects-v2 --bucket <bucket_name>
        ```
        This lists the objects within a specific bucket.  You *must* specify the bucket name.
    *   **Get Object:** Download an object.
        ```zsh
        aws s3api get-object --bucket <bucket_name> --key <object_key> <local_file_path>
        ```
        This downloads the specified object to your local machine.  You need the bucket name, object key, and a path to save the file.

5.  **Check for Resource-Based Policies (Bucket Policies):**
    ```zsh
    aws s3api get-bucket-policy --bucket <bucket_name>
    ```
    This retrieves the bucket policy, *if you have permission to view it*.  This is where you'll see if there are any restrictions that override your identity-based permissions.

**Key Takeaways and Potential Issues**

*   **Access Denied (Even with IAM Permissions):**  The most important lesson is that resource-based policies (bucket policies) can *deny* access even if your IAM permissions say you should have access.  This is a common source of confusion.
*   **`s3` vs. `s3api`:**  The `s3` commands are higher-level and more user-friendly for common tasks (like `cp` for copying).  The `s3api` commands provide more granular control and access to the full S3 API.  For security assessments, `s3api` is generally preferred.
*   **`list-objects-v2`:**  Always use `list-objects-v2` instead of `list-objects`.  It's the newer, recommended version.
*   **Bucket Naming:** Remember that bucket names are globally unique.
*   **Object Keys:** Object keys are the "filenames" within the bucket.  They can include slashes (`/`) to simulate a folder structure, but S3 is fundamentally a flat key-value store.
*   **Lab Goal:** Our lab's objective is to find the contents of `object.txt` and submit the flag wrapped in `CTF{}`.

**Expanded Explanation and Best Practices**

1.  **Profiles:** Using AWS CLI profiles (`--profile`) is highly recommended, especially when working with multiple AWS accounts or sets of credentials.  This keeps your credentials organized and prevents accidental use of the wrong credentials.

2.  **Error Handling:** When scripting, always check for errors.  The AWS CLI returns error codes and messages.  Pay attention to "AccessDenied" errors, but also other errors that might indicate throttling, network issues, or incorrect parameters.

3.  **Least Privilege:** The principle of least privilege is fundamental to security.  Users and roles should only have the minimum necessary permissions.  Our lab demonstrates how even seemingly broad permissions can be restricted by resource policies.

4.  **Bucket Policy Analysis:** Carefully examine bucket policies. Look for:
    *   **`Effect: Deny`:**  These statements explicitly block access.
    *   **`Principal`:**  Who is being granted or denied access?  `*` means everyone (public access – usually bad!).  Specific ARNs are better.
    *   **`Action`:** What actions are allowed or denied?  `s3:*` is very broad.
    *   **`Resource`:**  Which buckets or objects does the policy apply to?
    *   **`Condition`:**  Are there any conditions that further restrict access (e.g., based on IP address, time of day, etc.)?

5.  **Beyond Basic Enumeration:** Our lab covers basic listing and downloading.  More advanced S3 enumeration might involve:
    *   **Checking for versioning:**  S3 can keep multiple versions of objects.  Previous versions might contain sensitive data.
    *   **Checking for lifecycle policies:**  These policies can automatically delete or move objects to cheaper storage classes.
    *   **Checking for encryption:**  Is data encrypted at rest?  What encryption method is used?
    *   **Checking for logging:**  Is S3 access logging enabled?  This can help with auditing and incident response.
    *   **Checking for public access:**  Are any buckets or objects publicly accessible?
    *   **Checking Bucket ACLs** Access Control Lists are another, older way of managing permissions on Buckets and Objects.

6.  **Tools:** While the AWS CLI is essential, there are other tools that can help with S3 enumeration and security assessments:
    *   **ScoutSuite:** A multi-cloud security auditing tool.
    *   **Prowler:** Another AWS security auditing tool.
    *   **s3scanner:** A tool specifically for finding open S3 buckets.
    *   **CloudMapper:** can help enumerate permissions

7. **Challenge with Solutions**

```zsh
# 1. Configure AWS CLI (replace with your lab credentials)
aws configure
# AWS Access Key ID [None]: AKIAT6...
# AWS Secret Access Key [None]: sa3CB4...
# Default region name [None]: us-east-1
# Default output format [None]: json

# 2. Identify Yourself
aws sts get-caller-identity

# Example Output (yours will be different):
# {
#     "UserId": "<UserID>",
#     "Account": "<YourAccountID>",
#     "Arn": "arn:aws:iam::<YourAccountID>:user/s3-enumerate-Derek"
# }

# 3. Enumerate IAM Permissions
aws iam list-user-policies --user-name s3-enumerate-Derek  # Replace with your username
# Example Output:
# {
#     "PolicyNames": [
#         "s3-enumerate-AllowS3Operations"
#     ]
# }

aws iam get-user-policy --user-name s3-enumerate-Derek --policy-name s3-enumerate-AllowS3Operations # Replace with your username and policy name

# 4. Enumerate S3
aws s3api list-buckets
# Example Output:
# {
#     "Buckets": [
#         {
#             "Name": "cybr-data-bucket1-272281913033",
#             "CreationDate": "2024-02-06T01:45:25+00:00"
#         },
#         {
#             "Name": "cybr-data-bucket2-272281913033",
#             "CreationDate": "2024-02-06T01:45:25+00:00"
#         }
#     ]
# }

aws s3api list-objects-v2 --bucket cybr-data-bucket1-272281913033
# Example Output:
# {
#     "Contents": [
#         {
#             "Key": "object.txt",
#             "LastModified": "2024-02-06T01:46:02+00:00",
#             "ETag": "\"cd38bb14cd7a736994f03d28e325b8a5\"",
#             "Size": 1349,
#             "StorageClass": "STANDARD"
#         }
#     ],
#     "RequestCharged": null
# }

# Download and get the flag
aws s3api get-object --bucket cybr-data-bucket1-272281913033 --key object.txt object.txt
cat object.txt  # Display the contents of the file, which will contain the flag.

# Wrap the flag in CTF{} and submit.  For example, if the flag is "ThisIsTheFlag", you would submit "CTF{ThisIsTheFlag}".

# Try bucket 2 (will fail - this demonstrates the resource policy)
aws s3api list-objects-v2 --bucket cybr-data-bucket2-272281913033
# Expected Output: An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied

aws s3api get-bucket-policy --bucket cybr-data-bucket2-272281913033
# Expected Output: An error occurred (AccessDenied) when calling the GetBucketPolicy operation: Access Denied

```