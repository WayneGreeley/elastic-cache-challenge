This repo is for the [A Cloud Guru - #CloudGuruChallenge: Improve application performance using Amazon ElastiCache](https://acloudguru.com/blog/engineering/cloudguruchallenge-improve-application-performance-using-amazon-elasticache)

Challenge Goal	- Implement a Redis cluster using Amazon ElastiCache to cache database queries in a simple Python application.

Part of the challenge included writing a python application that calls a stored procedure in a Postgres database that simulates a poor performing database.
I deviated from the challenge.  I am focusing my AWS learning on serverless applications, so I skipped the python application on EC2 and wrote python Lambda functions.
Even if we are writing shiny new serverless applications, we may still need to access legacy databases, so the Redis cache can still be a valid tool to learn.
There is a lot of craziness in this project because I wanted to learn some skills along the way.
It would have been much simplier if I had created a complete VPC from scratch, but I wanted to try adding to an existing VPC instead.

If you want to try this out, clone this repo into your favorite IDE.
I use AWS Cloud9 to make it easier to run AWS commands from the terminal while editing code.
I also use an AWS sandbox account, so each time I start working on a project, the account is empty except for the default VPC.

```
git clone https://github.com/WayneGreeley/elastic-cache-challenge.git
cd elastic-cache-challenge/

sam build
sam deploy -g
```

<!---
I really wanted to have a Lambda function create the SQL function for me during the stack create process.
However, that means the Lambda function needs access to the VPC and the internet, which is a tougher task than I realized...I will figure it out someday.
So, to add the SQL function in the meanwhile...

Postgres is not installed in Cloud9 by default, so you will need to...
```
sudo yum install postgresql
```

Add the simulated poor performing stored procedure to your database...
```
psql \
   --host=<rds host in stack output> \
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

--->


Test the application using the outputs from the SAM deploy.
I like to use the Postman application as it provides an easy way to store tests that you run often.
When you test the helloworld endpoint, the response is always greater than five seconds.
The cache time-to-live for redis is set to 10 secounds, so the first helloredis test will take over five seconds.
For the next ten seconds, the helloredis test will take under a second.


![cache miss](/img/api-no-cache.png "cache miss")

![cache hit](/img/api-yes-cache.png "cache hit")






There is room for improvement.
I could create a VPC from scratch to eliminate a few of the look ups.
The security needs major review for a real AWS account.
I could store the sensitive data in Secrets Manager.



