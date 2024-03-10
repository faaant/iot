import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        try:
            # Prepare the data as a list of dictionaries
            data = []
            for item in processed_agent_data_batch:
                # Convert datetime to ISO 8601 format string
                timestamp_isoformat = item.agent_data.timestamp.isoformat()
                # Create a dictionary with timestamp as string
                data_item = item.model_dump()
                data_item['agent_data']['timestamp'] = timestamp_isoformat
                data.append(data_item)
            
            # Make the POST request
            response = requests.post(f"{self.api_base_url}/processed_agent_data/", json=data)

            # Check if the request was successful (status code 200)
            if response.status_code == 200 or response.ok :
                return True
            else:
                return False
        except Exception as e:
            logging.info(f"Error occured {e}")
            return False
