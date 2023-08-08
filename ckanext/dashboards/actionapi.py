import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.model as model 

import ckanext.dashboards.db as db

import uuid
import boto3
import json

def add_dashboard(context, data_dict):
    newDashboard = db.dashboard()

    newDashboard.dashboard_Type_Id = "PhantomLoad"
    newDashboard.dashboard_Arns = {"test": "arn:something"}
    newDashboard.SME = data_dict["organizationName"]
    newDashboard.user_Id = model.User.get(context['user']).id
    newDashboard.state = "Startup"

    newDashboard.save()

    session = context['session']
    session.add(newDashboard)
    session.flush(newDashboard)
    session.refresh(newDashboard)
    DashboardInfo = newDashboard
    session.commit()

    print("Dashboard = ", DashboardInfo)

    jobID = DashboardInfo.dashboard_Id

    sqs = boto3.client('sqs', region_name='eu-west-2')  #client is required to interact with 
    sqs.send_message(
        QueueUrl="https://sqs.eu-west-2.amazonaws.com/450869586150/Testqueue.fifo",
        MessageBody=
        json.dumps({
            "JobID": jobID, 
            "Username": data_dict["Username"],
            "organizationName": data_dict["organizationName"],
            "datasetName": data_dict["datasetName"],
            "URL": data_dict["URL"]
        }),
        MessageGroupId= jobID
    )

    newDashboard.state = "Processing"
    session.commit()

    return DashboardInfo

def pollCreationQueue(context, data_dict):
    # Create SQS client

    while (True):
        sqs = boto3.client('sqs', region_name='eu-west-2') 

        queue_url = 'https://sqs.eu-west-2.amazonaws.com/450869586150/phantomtestnormal'

        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=60
        )

        if 'Messages' in response:
            for message in response['Messages']:
                receipt_handle = message['ReceiptHandle']

                messageBody = json.loads(message["Body"])

                dashboardObj = db.dashboard.get(dashboard_Id=messageBody["JobID"])[0]

                if (dashboardObj):
                    session = context['session']
                    dashboardObj.state = messageBody["Status"]
                    session.commit()

                    sqs.delete_message(
                        QueueUrl=queue_url,
                        ReceiptHandle=receipt_handle
                    )            
        else:
            break