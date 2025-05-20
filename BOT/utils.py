import boto3
from datetime import datetime, timedelta

# This function checks for active AWS services and returns a message
def check_active_services():
    ec2 = boto3.client("ec2")
    s3 = boto3.client("s3")

    # Check for running EC2 instances
    ec2_resp = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )
    running_instances = sum(len(r["Instances"]) for r in ec2_resp["Reservations"])

    # Check if any S3 buckets exist
    s3_resp = s3.list_buckets()
    s3_buckets = s3_resp.get("Buckets", [])

    if running_instances == 0 and len(s3_buckets) == 0:
        return "✅ No active AWS services running. You’re not being charged for any compute or storage."
    else:
        return (
            f"⚠️ Active AWS Services Detected:\n"
            f"🖥️ Running EC2 Instances: {running_instances}\n"
            f"📦 Total S3 Buckets: {len(s3_buckets)}"
        )

#Add Timestamp to the Report
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_header = f"🕒 Report Generated At: {timestamp}\n\n"
result_message = report_header + "your_existing_message"  # Replace with actual message variable
print(result_message)
