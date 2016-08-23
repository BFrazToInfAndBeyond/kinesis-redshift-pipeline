#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Documentation section
DOCUMENTATION = '''
---
module: get_jdbc
short_description: create or delete a delivery stream
description:
  - create or delete a delivery stream
options:
  cluster_id:
    description:
      the unique identifier of the redshift cluster
    required: yes
  vpc_id:
    description:
      the unique identifier of the vpc
    required: yes
  db_name:
    description:
      the name of the db for the redshift cluster
    required: yes
  region:
    description:
      the region to create the redshift cluster
    required: yes

'''

import boto3
import time


def describe_cluster(redshift_client, cluster_id):
    response = redshift_client.describe_clusters(
        ClusterIdentifier=cluster_id,
        MaxRecords=20,
        TagKeys=[
            'name',
        ],
        TagValues=[
            'redshift_automated',
        ]
    )
    return response


def get_cluster_jdbc(redshift_client, vpc_id, cluster_id, db_name):
    response = describe_cluster(redshift_client, cluster_id)
    clusters = response['Clusters']
    i = 0
    jdbc = 'jdbc:redshift://'
    while(i < len(clusters)):
        cluster = clusters[i]
        if cluster['VpcId'] == vpc_id and cluster['ClusterIdentifier'] == cluster_id:
            jdbc += cluster['Endpoint']['Address'] + ':' + str(cluster['Endpoint']['Port']) + '/' + db_name
        i += 1
    return jdbc


def main():
    argument_spec = {}
    argument_spec.update(
        dict(
            cluster_id=dict(type='str', default=None, required=True),
            vpc_id=dict(type='str', default=None, required=True),
            db_name=dict(type='str', default=None, required=True),
            region=dict(type='str', default=None, required=True)
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    cluster_id = module.params.get('cluster_id')
    vpc_id = module.params.get('vpc_id')
    db_name = module.params.get('db_name')
    region = module.params.get('region')
    redshift_client = boto3.client('redshift', region_name=region)
    jdbc = get_cluster_jdbc(redshift_client, vpc_id, cluster_id, db_name)

    module.exit_json(changed=True, jdbc=jdbc)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
