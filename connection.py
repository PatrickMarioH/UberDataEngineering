import random
import uuid
import json
from datetime import datetime, timedelta
from faker import Faker
from azure.eventhub import EventHubProducerClient, EventData
import logging
from dotenv import load_dotenv
load_dotenv()  # Load Environment Variables From .env File
import os

# Pulling Data Generator Function
from data import generate_uber_ride_confirmation

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
EVENT_HUBNAME = os.getenv("EVENT_HUBNAME")

def send_to_event_hub(ride_data=None, batch_size=1):

    try:
        # Initialize Event Hub Producer Client
        producer = EventHubProducerClient.from_connection_string(
            CONNECTION_STRING,
            eventhub_name=EVENT_HUBNAME
        )
        
        # Prepare Ride Records
        ride_json = json.dumps(ride_data) 
        
        # Create Batch of Events
        event_batch = producer.create_batch()

        # Create Event With Ride Data 
        event = EventData(ride_json)
            
        # Add Event To Batch
        event_batch.add(event)

        # Send Batch To Event Hub
        producer.send_batch(event_batch)
        
        producer.close()

        return "Successfully Sent To Event Hub"
        
    except Exception as e:
        print(f"Error Sending Data To Event Hub: {str(e)}")
        return False

if __name__ == "__main__":
    
    print("=" * 80)
    print("SINGLE RIDE CONFIRMATION")
    print("=" * 80)
    ride = generate_uber_ride_confirmation()
    print(json.dumps(ride, indent=2))

    
    print("\n" + "=" * 80)
    print("SENDING SINGLE RIDE TO EVENT HUB")
    result = send_to_event_hub(ride)
    print(f"Single Ride Sent To Event Hub: {result}")