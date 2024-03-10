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

    if agent_data.accelerometer.z>-100 and agent_data.accelerometer.z<100:
        return ProcessedAgentData(
            road_state = 'FINE',
            agent_data = agent_data
        )

    return ProcessedAgentData(
        road_state = 'NEED TO BE REPAIRED',
        agent_data = agent_data
    )