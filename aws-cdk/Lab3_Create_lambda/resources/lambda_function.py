def handler(event, context):
 print("Hello from AWS Lambda!")
 return {
     'statusCode': 200,
     'body': 'Hello from Lambda!'
 }