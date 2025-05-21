from dataclasses import dataclass
from typing import Callable

@dataclass
class EndpointConfig:
    url_template: Callable[[int], str]
    filename_template: Callable[[int], str]
    endpoint_name: str
    section: str

class StravaEndpoints:
    ACTIVITIES = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}?include_all_efforts=true",
        filename_template=lambda aid: f"activity_{aid}.json",
        endpoint_name="detailed activity",
        section="activities"
    )

    ACTIVITIES_LAPS = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}/laps",
        filename_template=lambda aid: f"activity_{aid}_laps.json",
        endpoint_name="laps",
        section="activities"
    )

    # 402, Payment Required
    ACTIVITIES_ZONES = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}/zones",
        filename_template=lambda aid: f"activity_{aid}_zones.json",
        endpoint_name="zones",
        section="activities"
    )

    ACTIVITIES_COMMENTS = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}/comments",
        filename_template=lambda aid: f"activity_{aid}_comments.json",
        endpoint_name="comments",
        section="activities"
    )

    ACTIVITIES_KUDOS = EndpointConfig(
        url_template=lambda aid: f"https://www.strava.com/api/v3/activities/{aid}/kudos",
        filename_template=lambda aid: f"activity_{aid}_kudos.json",
        endpoint_name="kudos",
        section="activities"
    )

    ROUTES = EndpointConfig(
        url_template=lambda rid: f"https://www.strava.com/api/v3/routes/{rid}",
        filename_template=lambda rid: f"route_{rid}.json",
        endpoint_name="route",
        section="routes"
    )