import json
import logging

logger = logging.getLogger(__name__)


def load_preferences(
    filename: str = "./tradotron/resources/preferences.json"
) -> dict:

    logger.debug("loading preferences")

    with open(filename, mode="r") as file:
        preference_dict = json.load(file)

    return preference_dict


def save_preferences(
    preference_dict: dict,
    filename: str = "./tradotron/resources/preferences.json"
) -> None:

    logger.debug("writing preferences")

    with open(filename, mode="w") as file:
        json.dump(preference_dict, file, indent=4)


# def update_preferences(
#     preference_dict: dict,
#     filename: str = "./tradotron/resources/preferences.json",
# ) -> None:

#     logger.debug("updating preferences")

#     with open(filename, mode="w") as file:
#         json.dump(preference_dict, file, indent=4)
