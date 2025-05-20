import boto3
from datetime import datetime, timedelta
from send_report import send_email
from utils import check_active_services


def lambda_handler(event=None, context=None):
    ec2 = boto3.client('ec2')
    cloudwatch = boto3.client('cloudwatch', region_name='ap-south-1')

    # Time range: last 24 hours
    end = datetime.utcnow()
    start = end - timedelta(days=1)

    # Get EC2 instance IDs
    instance_ids = []
    reservations = ec2.describe_instances()['Reservations']
    for r in reservations:
        for i in r['Instances']:
            instance_ids.append(i['InstanceId'])

    report = ""
    # Step 4: Check CPU Usage and Take Action
    for instance_id in instance_ids:
        stats = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start,
            EndTime=end,
            Period=86400,
            Statistics=['Average']
        )

        datapoints = stats['Datapoints']
        if datapoints:
            avg = datapoints[0]['Average']
            if avg < 10:
                report += f"⚠️ Instance {instance_id} is idle. Avg CPU: {avg:.2f}%\n"
                # Step 7: Stop idle EC2 instance
                try:
                    ec2.stop_instances(InstanceIds=[instance_id])
                    report += f"🛑 Instance {instance_id} stopped to save the cost.\n"
                except Exception as e:
                    report += f"❌ Failed to stop {instance_id}: {e}\n"
            else:
                report += f"✅ Instance {instance_id} is Active. Avg CPU {avg:.2f}%\n"
        else:
            report += f"❓ No data for instance {instance_id}\n"

    # Add active services check
    report = check_active_services() + "\n" + report

    # 1. Load the HTML Template
    try:
        with open("report_template.html", "r") as file:
            html_template = file.read()
    except Exception as e:
        html_template = "<html><body><pre>{{Report}}</pre></body></html>"
        report = f"⚠️ Could not load HTML template: {e}\n\n" + report

    # 2. Insert the report content
    html_report = html_template.replace("{{Report}}", report)

    # 3. Email subject
    subject = "💸 Daily EC2 Usage Summary"

    # 4. Send email
    send_email(subject, html_report)



