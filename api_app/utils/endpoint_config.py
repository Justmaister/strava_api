from dataclasses import dataclass
from typing import Callable

@dataclass
class EndpointConfig:
    url_template: Callable[[int], str]
    filename_template: Callable[[int], str]
    endpoint_name: str

class StravaEndpoints:
    ACTIVITIES = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}?include_all_efforts=true",
        filename_template=lambda aid: f"activity_{aid}.json",
        endpoint_name="detailed activity"
    )

    LAPS = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}/laps",
        filename_template=lambda aid: f"activity_{aid}_laps.json",
        endpoint_name="laps"
    )

    ZONES = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}/zones",
        filename_template=lambda aid: f"activity_{aid}_zones.json",
        endpoint_name="zones"
    )