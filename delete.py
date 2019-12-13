import boto3   
import os
import json
from botocore.exceptions import ClientError 
import datetime
import json
aws_access_key_id='XXXXXX'
aws_secret_access_key='XXXXXX'

try:
    #cloudfront clean
		cloudfrontclient = boto3.client('cloudfront',aws_access_key_id=aws_access_key_id,aws_secret_access_key=aws_secret_access_key,region_name='us-east-1')
		response = cloudfrontclient.list_distributions()
		if len(response['DistributionList']['Items']) !=0:
			for k in response['DistributionList']['Items']:
				DistributionConfig = cloudfrontclient.get_distribution(Id=k['Id'])
				#response = cloudfrontclient.delete_distribution(Id=k['Id'],IfMatch=Etage['ETag'])
				#print(k['LastModifiedTime'])
				time  = k['LastModifiedTime']
				lunch_time = datetime.datetime(time.year,time.month,time.day,time.hour,time.minute,time.second) 
				now = datetime.datetime.utcnow()
				current_time = datetime.datetime(now.year,now.month,now.day,now.hour,now.minute,now.second) 
				result = current_time-lunch_time  
				#print('Difference: ', result) 
				minutes = result.seconds / 60
				#print('Difference in minutes: ', minutes) 
				if minutes >= 60:
					if k['Status']=="Deployed":	
						dist_list = cloudfrontclient.get_distribution_config(Id=k['Id'])
						dist_list['DistributionConfig'].update(Enabled = "False" )
						
						with open('result.json', 'w') as fp:
							json.dump(dist_list, fp)

						print(dist_list)
						dist_update=cloudfrontclient.update_distribution(DistributionConfig=dist_list,Id=k['Id'],IfMatch=DistributionConfig['ETag'])
						print(dist_update)
					else:
						if k['Status']=="Disabled":
							print("Disabled")	
except ClientError as e:
	print(e)
except Exception as e:
	print(e)
