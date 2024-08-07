'''
1. Creating the virtual environments
-pip install virtualenv
-virtualenv myenv
-source myenv/bin/activate
-myenv/bin/pip install google-cloud-compute
2.Run the file after creating the virtual environment
-python3 gcpAuthentication.py
'''
import os
import time
import telebot
from google.cloud import compute_v1 #fetching from the cloid
from google.api_core.exceptions import NotFound, GoogleAPIError
from dotenv import load_dotenv

# Set the environment variable for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'praxis-dolphin-333916-a2c5c36f4d21.json'

project_id = 'praxis-dolphin-333916'
zone = 'asia-east2-a'
instance_name = 'devserver'
def wait_for_operation(operation_client, project_id, zone, operation_name):
    while True:
        operation = operation_client.get(project=project_id, zone=zone, operation=operation_name)
        if operation.status == compute_v1.Operation.Status.DONE:
            if operation.error:
                raise Exception(f"Error during operation: {operation.error}")
            return
        time.sleep(1)

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
load_dotenv()
API_KEY = os.getenv("API_KEY") # getting the API_KEY variable from .env
bot = telebot.TeleBot(API_KEY)
chat_id = 7346012683

@bot.message_handler(commands=['start_instance'])
def start_instance(message):
    try:
        instance_client = compute_v1.InstancesClient()
        request = compute_v1.StartInstanceRequest(project=project_id, zone=zone, instance=instance_name)
        operation = instance_client.start(request=request)
        wait_for_operation(compute_v1.ZoneOperationsClient(), project_id, zone, operation.name)
        bot.reply_to(message, f"Instance {instance_name} started successfully.")
    except NotFound as e:
        bot.reply_to(message, f"Error: {str(e)}")
    except GoogleAPIError as e:
        bot.reply_to(message, f"API error: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"Unexpected error: {str(e)}")

@bot.message_handler(commands=['stop_instance'])
def stop_instance(message):
    try:
        instance_client = compute_v1.InstancesClient()
        request = compute_v1.StopInstanceRequest(project=project_id, zone=zone, instance=instance_name)
        operation = instance_client.stop(request=request)
        wait_for_operation(compute_v1.ZoneOperationsClient(), project_id, zone, operation.name) #after wait for operation is done, stop_instance promps
        bot.reply_to(message, f"Instance {instance_name} stopped successfully.")
    except NotFound as e:
        bot.reply_to(message, f"Error: {str(e)}")
    except GoogleAPIError as e:
        bot.reply_to(message, f"API error: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"Unexpected error: {str(e)}")
@bot.message_handler(commands=['create_instance'])
def create_instance(message):
    try:
        instance_client = compute_v1.InstancesClient()
        instance = compute_v1.Instance(
            name='new-instance',
            machine_type=f"zones/{zone}/machineTypes/n1-standard-1",
            disks=[compute_v1.AttachedDisk(
                boot=True,
                auto_delete=True,
                initialize_params=compute_v1.AttachedDiskInitializeParams(
                    source_image='projects/debian-cloud/global/images/family/debian-11'
                )
            )],
            network_interfaces=[compute_v1.NetworkInterface(
                name='global/networks/default'
            )]
        )
        operation = instance_client.insert(project=project_id, zone=zone, instance_resource=instance)
        wait_for_operation(compute_v1.ZoneOperationsClient(), project_id, zone, operation.name)
        bot.reply_to(message, "New instance created successfully.")
    except NotFound as e:
        bot.reply_to(message, f"Error: {str(e)}")
    except GoogleAPIError as e:
        bot.reply_to(message, f"API error: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"Unexpected error: {str(e)}")
if __name__ == '__main__':
    bot.polling()