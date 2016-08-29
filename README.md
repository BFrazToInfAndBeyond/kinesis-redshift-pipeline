# kinesis-redshift-pipeline
A data pipeline, using nifi, to ingest twitter tweets from kinesis to redshift


##Get started

###Virtual Environment

A virtual env to manage your python dependencies is suggested. http://docs.python-guide.org/en/latest/dev/virtualenvs/

mkvirtualenv kinesis_redshift_pipeline (if the virtualenv does not exist)

workon kinesis_redshift_pipeline

pip install --upgrade pip (obtain version 8.1.2 for pip)

pip install -r requirements.txt


###AWS Credentials
Install the aws cli

Set the default credentials in ~/.aws/credentials.
The aws configure command can be used as an alternative. Below, is an example
```
[default]
aws_access_key_id=YOUR_ACCESS_KEY
aws_secret_access_key=
```

Set the credentials in your bash_profile. Be sure to source the profile once set.
```
export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=SECRET
```

###1) Update Variables

in group_vars/all/vars.yml
update the following variables:
region, vpc_id, vpc_subnet_ids, sg_ids, ami, bucket_for_redshift, and the subent az


###2) Update Security Group

The first security group id listed in 'sg_ids' will be used for nifi.
Be sure to open port 8080 to the desired ip addresses (0.0.0.0 for to open it up to anyone)

For the default sg, allow the cidr block for the respective firehose (varies by region).

Firehose currently uses one CIDR block for each available AWS Region:
52.70.63.192/27 for US East (N. Virginia), 52.89.255.224/27 for US West (Oregon), and 52.19.239.192/27 for EU (Ireland).

###3) Run the playbook

`ansible-playbook "-e state=present" nifi_pipeline.yml`

This command will start the redshift cluster, the kinesis delivery stream, the nifi instance,
and populate nifi with a data pipeline to ingest tweets into kinesis.
The pipeline requires the user to manually select 'play'.

###4) Start Data Pipeline

go to the ui of nifi with: http://ip_address_of_nifi:8080/nifi

Update the twitter creds in the 'GetTwitter' processor: consumer_key, access_token, consumer_secret, access_token_secret.
NOTE: The 'GetTwitter' processor can be found in the 'GetTweets' processor group.

Start the pipeline! Twitter tweets will be now ingested into redshift via kinesis.

###5) Shutdown the pipeline and Nifi instance

`ansible-playbook "-e state=absent" nifi_pipeline.yml`

This will terminate the nifi instance, the kinesis delivery stream, as well as the
redshift cluster.
