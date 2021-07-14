- **Load Database Stored Procedure**

  The application calls a stored procedure on the database which must be created before running the application.  You will need the RDS instance hostname, the database name and the username used to connect to the database.
  You can install the procedure from the install.sql file with the following command:
  ``` psql -h <RDS_HOSTNAME> -U <DB_USER> -f install.sql <DB_NAME> ``` 
- **Configure Database Connection**

  You will also need to configure the application to connect to the database by editing the [`config/database.ini`](https://raw.githubusercontent.com/ACloudGuru/elastic-cache-challenge/master/config/database.ini) file.  Use the database name, username and password you created when deploying the database.
- **Configure HTTP Server**

  If you are running the application on your workstation, you can access it at http://127.0.0.1:5000.  Alternately, you can configure an HTTP server listening on the public interface as a proxy.  I've provided such a configuration for the nginx http server in [`config/nginx-app.conf`](https://raw.githubusercontent.com/ACloudGuru/elastic-cache-challenge/master/config/nginx-app.conf).









```


aws  --region us-east-1 ec2 describe-vpcs


aws ec2 describe-subnets --query "Subnets[?AvailabilityZone=='us-east-1a'].SubnetId"


aws cloudformation create-stack --stack-name postgres-example --template-body file://template.yaml --capabilities CAPABILITY_AUTO_EXPAND

aws ec2 describe-security-groups --query "SecurityGroups[?Description=='cache'].GroupId"




sudo yum install postgresql

psql \
   --host=webapp-db.<id change this>.us-east-1.rds.amazonaws.com \
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



sam build

sam deploy -g



```
