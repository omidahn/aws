import boto3

AWS_ACCESS_KEY_ID = 'your-username'
AWS_SECRET_ACCESS_KEY = 'your-password'

def get_session_token():
    # Create a session object.
    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Get the session token.
    credentials = session.get_credentials()
    session_token = credentials.session_token

    return session_token


def create_instance(ami_id, instance_type, key_name, user_data_file):
    # Get the session token.
    session_token = get_session_token()

    # Create the EC2 client.
    ec2 = boto3.client('ec2', config=botocore.client.Config(signature_version='s3v4', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, aws_session_token=session_token))

    # Create the user data script.
    with open(user_data_file, 'r') as f:
        user_data = f.read()

    # Create the instance.
    response = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        UserData=user_data.encode('utf-8'),
    )

    # The response object contains the ID of the newly created instance.
    instance_id = response['Instances'][0]['InstanceId']

    print(f'Instance created with ID: {instance_id}')


if __name__ == '__main__':
    ami_id = 'ami-0c3472daea3f355b7'
    instance_type = 't2.micro'
    key_name = 'my-keypair'
    user_data_file = 'my-init-script.sh'

    create_instance(ami_id, instance_type, key_name, user_data_file)
