import json
import sys
from pathlib import Path


def create_config():
    """
    Creates a merged dictionary between the `config.json` and
    the respective environment's config, by merging them.

    Sidenote: the implementation for the generic access token
    was made specific so that the request headers are easily generated
    with just changing the access token per environment.
    """
    with open("./config.json", "r") as config_file:
        default_config = json.load(config_file)

    if len(sys.argv) >= 1:
        env = sys.argv[1]
    else:
        env = "dev"

    if env not in {"dev", "prod", "staging", "test"}:
        raise ValueError("Invalid env name")

    env_config_path = Path("./config.{}.json".format(env))

    if env_config_path.exists():
        with open(env_config_path) as env_config_file:
            env_config = json.load(env_config_file)

    else:
        raise FileExistsError("The env config file does not exist")

    return dict(_merge_configs(default_config, env_config))


def _merge_configs(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(_merge_configs(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            if k == "generic_access_token":
                dict1["headers"]["authorization"] = (
                    dict1["headers"]["authorization"] + dict2[k]
                )
                yield (k, dict1["headers"]["authorization"])
            else:
                yield (k, dict2[k])


config = create_config()
