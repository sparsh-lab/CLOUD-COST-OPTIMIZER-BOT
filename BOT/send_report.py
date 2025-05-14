import boto3

def send_email(subject, html_body):
    ses = boto3.client('ses', region_name='ap-south-1')

    #change region if needed
    response=ses.send_email(
        Source="sparshkmr17@gmail.com", # your verified send email
        Destination={
            "ToAddresses": ["sparshkmr17@gmail.com"] # receiver email con be same 
        },
        Message = {
            "Subject": {
                "Data": subject
            },
            "Body": {
                "HTML": {
                    "Data": html_body
                }
            }
        }
    )

    print("✅ Email sent! Message ID:", response['MessageId'])

# adjust if it's in the same file
from send_report import check_active_services  

report_msg = check_active_services()

# Use `report_msg` inside your SES email body or template
send_email(subject="Cloud Cost Report", body=report_msg)
