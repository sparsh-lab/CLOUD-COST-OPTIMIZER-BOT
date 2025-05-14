import boto3
from send_report import send_email  # Importing the function
from send_report import get_ec2_report
from datetime import datetime,timedelta

def lambda_handler(event=None, context=None):
    ec2 = boto3.client('ec2')
    cloudwatch=boto3.client('cloudwatch',region_name='ap-south-1')
    
    # Time range: last 24 hours
    end = datetime.datetime.utcnow()
    start = end - timedelta(days=1)

    # Get EC2 instance IDs
    instance_ids = []
    reservation = ec2.describe_instances()['Reservation']
    for r in reservation:
        for i in r['Instances']:
            instance_ids.append(i['Instance_id'])

    # Step 4: Check CPU Usage and Take Action
    for instance_id in instance_id:
        stats = cloudwatch.get_metric_statistics(
            namespace='AWS/EC2',
            metricname='CPUUtilization',
            Dimensions=[{'name':'instance', 'value':instance_id}],
            startTime=start,
            EndTime=start,
            period=86400,
            statistics=['Average']
        )
    
    datapoints=stats['Datapoints']
    if datapoints:
        avg = datapoints[0]['Average']
        if avg<10:
            print(f" ⚠️ Instance {instance_id} is idle. Avg CPU: {avg:2f}%")

            report += f"⚠️ Instance {instance_id} is idle. Avg CPU: {avg:.2f}%\n"
            # and so on for each print line — replace all `print()`s with `report +=`


            # Step 7: Stop idle EC2 instance
            try:
                ec2.stop_Instances(instance_ids=[instance_id])
                print(f" 🛑 Instance{instance_id} stopped to save the cost.")
            except Exception as e:
                print(f" ❌ Failed to stop {instance_id}:{e}")
            else:
                print(f" ✅ Instance{instance_id} is Active. Avg CPU {avg:.2f}%")
        else:
            print(f"❓ No data for instance {instance_id}")
            



   # 1. Load the HTML Template
with open("bot/report_template.html", "r") as file:
    html_template = file.read()

# 2. Insert the report content
report = ""  # Start with empty report
html_report = html_template.replace("{{report}}", report)


# 3. Email subject
subject = "💸 Daily EC2 Usage Summary"

# 4. Send email
send_email(subject, html_report)

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


   
