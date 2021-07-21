This repo is for the [A Cloud Guru - #CloudGuruChallenge: Improve application performance using Amazon ElastiCache](https://acloudguru.com/blog/engineering/cloudguruchallenge-improve-application-performance-using-amazon-elasticache)

Challenge Goal	- Implement a Redis cluster using Amazon ElastiCache to cache database queries in a simple Python application.

Part of the challenge included writing a python application that calls a stored procedure in a Postgres database that simulates a poor performing database.
I deviated from the challenge.  I am focusing my AWS learning on serverless applications, so I skipped the python application on EC2 and wrote python Lambda functions.
Even if we are writing shiny new serverless applications, we may still need to access legacy databases, so the Redis cache can still be a valid tool to learn.



Clone this repo into your favorite IDE.
I use AWS Cloud9 to make it easier to run commands from the terminal while changing code.

```
git clone https://github.com/WayneGreeley/elastic-cache-challenge.git
cd elastic-cache-challenge/
```

I also use an Playground Cloud account, so each time I start working on a project, the account is empty except for the default VPC.
These steps assume your are using AWS US-EAST-1 region.
The template.yaml in the root of this project allows CloudFormation to provision the RDS database and Redis instances.

Update VpcId in template.yaml with the default VPC id found by...
```
aws --region us-east-1 ec2 describe-vpcs --query "Vpcs[?isDefault==true].VpcId"
```

Update SubnetIds in template.yaml with subnet id for us-east-1a subnet of the default VPC found by...
```
aws ec2 describe-subnets --query "Subnets[?AvailabilityZone=='us-east-1a'].SubnetId"
```

Deploy the CloudFormation template...
```
aws cloudformation create-stack --stack-name postgres-example --template-body file://template.yaml --capabilities CAPABILITY_AUTO_EXPAND
```

When the CloudFormation stack is successfully deployed...

Postgres is not installed in Cloud9 by default, so you will need to...
```
sudo yum install postgresql
```

Add the simulated poor performing stored procedure to your database...
```
psql \
   --host=<rds host in cloudformation output> \
   --port=5432 \
   --username=postgres \
   --password \
   --dbname=postgres


create function slow_version() RETURNS text AS
            $$
              select pg_sleep(5);
              select version();
            $$
            LANGUAGE SQL;
```


Open the sam-app folder and update database.ini with outputs from CloudFormation stack above.
Update SubnetIds in template.yaml with SubnetId from above.
Update SecurityGroupIds in template.yaml with...
```
aws ec2 describe-security-groups --query "SecurityGroups[?Description=='cache'].GroupId"
```

Build and deploy the Lambda functions and API Gateway for testing using the SAM CLI...
```
sam build

sam deploy -g
```

For SAM guided options, I choose...


Test the application using the outputs from the SAM deploy.
I like to use the Postman application as it provides and easy way to store tests that you run often.
When you test the helloworld endpoint, the response is always greater than five seconds.
The cache time-to-live for redis is set to 10 secounds, so the first helloredis test will take over five seconds.
For the next ten seconds, the helloredis test will take under one second.











There is room for improvement.
The security needs major review for a real AWS account.
I could create a VPC from scratch to eliminate a few of the look ups.
I could also combine the two templates.
Or I could write a Lambda function that looks up the ids while the stacks are being created...
```
import boto3

def lambda_handler(event, context):
    
    ec = boto3.client('ec2')

    response = ec.describe_security_groups(
        Filters=[{
                'Name': 'description',
                'Values': ['cache',]
            },]
    )
    
    return response['SecurityGroups'][0]['GroupId']
```






