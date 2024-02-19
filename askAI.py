import argparse
import yaml
import os
from pathlib import Path
import re

personnal_system_message: str = """
You have to create a shell command for the user.
The user will ask for a quick command to do something in their shell,
and you can only respond with the shell command that will help them.
You CAN'T ASK for more informations, do with what you have.
The command HAVE TO BE BETWEEN the brackets '<CODE>' and '</CODE>'
and this part will be ON ONE LINE ONLY.
For example, if the user ask 'add modifications to last git commit'
You can do :

To add the last modifications [...]
<CODE>git add -a && git commit --amend</CODE>
The first command do [...] and the second command do [...]

The user query is:

"""


def import_settings()->dict:
    if not os.path.isdir(Path.home()/".config"/"askAI"):
        os.mkdir(Path.home()/".config"/"askAI")
    if not os.path.isfile(Path.home()/".config"/"askAI"/"config.yaml"):
        file = open(Path.home()/".config"/"askAI"/"config.yaml", 'w')
        file.write("""
# api point can be "chatGPT", "ollama", "lm studio", or an URL
api-point: null
# model to use in this api point (ex: gpt-3.5-turbo, codellama:13b)
model: null
# if using chatgpt, please provide the api key
api-key: null
""")
        file.close()
    with open(Path.home()/".config"/"askAI"/"config.yaml", 'r') as file:
        config: dict = {"api-point": None, "model": None, "api-key": None}
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
    parser.add_argument('-m', '--model',
                        help="model to use in this api point (ex: gpt-3.5-turbo, codellama:13b)",
                        required=config["model"] is None,
                        default=config["model"])
    parser.add_argument('-k', '--api-key',
                        help="please provide an API key if needed by the api point",
                        required=config["api-key"] is None,
                        default=config["api-key"])
    parser.add_argument('query',
                        metavar='Query',
                        help='Query send to AI')
    return parser.parse_args()


def send_query(args: argparse.Namespace)->str:
    match args.api_point:
        case "chatGPT":
            raise SystemExit("not implemented yet (chatGPT)")
        case "ollama":
            return askOllama(args)
        case _:
            raise SystemExit("api not found")


def askOllama(args: argparse.Namespace)->str:
    from langchain_community.llms import Ollama
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate
    output_parser = StrOutputParser()
    llm = Ollama(model=args.model)
    prompt = ChatPromptTemplate.from_messages([
        ("system", personnal_system_message),
        ("user", "{input}")
    ])
    chain = prompt | llm | output_parser
    return chain.invoke({"input": args.query})


def parseOutput(resp: str)->str:
    match =  re.search(r'<CODE>(.*)</CODE>', resp)
    if match:
        return match.group(1)
    raise Exception(resp)


if __name__ == "__main__":
    config: dict = import_settings()
    args: argparse.Namespace = parse(config)
    #print(args)
    print(parseOutput(send_query(args)))
