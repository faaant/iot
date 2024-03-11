from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData
import logging

def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """

    if 14000 > agent_data.accelerometer.z < 18000:
        return ProcessedAgentData(
            road_state = 'FINE',
            agent_data = agent_data
        )
    elif 13000 > agent_data.accelerometer.z < 19000:
        return ProcessedAgentData(
            road_state = 'SLIGHTLY DAMAGED ROAD',
            agent_data = agent_data
        )

    return ProcessedAgentData(
        road_state = 'VERY DAMAGED ROAD',
        agent_data = agent_data
    )