import argparse
import yaml
import os
from pathlib import Path


def import_settings()->dict:
    if not os.path.isdir(Path.home()/".config"/"askAI"):
        os.mkdir(Path.home()/".config"/"askAI")
    if not os.path.isfile(Path.home()/".config"/"askAI"/"config.yaml"):
        file = open(Path.home()/".config"/"askAI"/"config.yaml", 'w')
        file.write("""
# api point can be "chatGPT", "ollama", "lm studio", or an URL
api-point: null
# model to use in this api point (ex: gpt-3.5-turbo, codellama:13b)
default-model: null
# if using chatgpt, please provide the api key
api-key: null
""")
        file.close()
    with open(Path.home()/".config"/"askAI"/"config.yaml", 'r') as file:
        config: dict = {"api-point": None, "default-model": None, "api-key": None}
        for key, value in yaml.safe_load(file).items():
            config[key] = value
    return config


def parse(config: dict)->argparse.Namespace:
    """verify arguments from user"""
    parser = argparse.ArgumentParser(description="Ask AI to create a command for you",
                                     epilog="You can always use the config file to not define every time")
    parser.add_argument('-a', '--api-point',
                        help='api point can be "chatGPT", "ollama", "lm studio", or an URL',
                        required=config["api-point"] is None,
                        default=config["api-point"])
    parser.add_argument('-m', '--default-model',
                        help="model to use in this api point (ex: gpt-3.5-turbo, codellama:13b)",
                        required=config["default-model"] is None,
                        default=config["default-model"])
    parser.add_argument('-k', '--api-key',
                        help="please provide an API key if needed by the api point",
                        required=config["api-key"] is None,
                        default=config["api-key"])
    parser.add_argument('message',
                        metavar='Message',
                        help='Query send to AI')
    return parser.parse_args()


def send_query(args: argparse.Namespace)->str:
    match args.api_point:
        case "chatGPT":
            raise SystemExit("not implemented yet (chatGPT)")
        case "ollama":
            raise SystemExit("not implemented yet (ollama)")
        case _:
            raise SystemExit("api not found")


if __name__ == "__main__":
    config: dict = import_settings()
    args: argparse.Namespace = parse(config)
    #print(args)
    send_query(args)
