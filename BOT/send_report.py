import boto3

def send_email(subject, message):
    ses = boto3.client('ses', region_name='ap-south-1')
    response = ses.send_email(
        Source="sparshkmr17@gmail.com",  # Verified sender
        Destination={"ToAddresses": ["sparshkmr17@gmail.com"]},
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Html": {"Data": message}
            }
        }
    )
    print("✅ Email sent! Message ID:", response['MessageId'])



