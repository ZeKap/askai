import sys
import os
from pathlib import Path
import re
from typing import Tuple
# --- imports to be installed (the ones required only to use a model have to be imported right before their call (see openAI for example))
import argparse
import yaml
import getch

personnal_system_message: str = \
"""
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
    """
    Import settings from '.config'
    """
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
    """
    Verify arguments from user dynamically from config file
    """
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
                        help='Query send to AI',
                        nargs='+')
    return parser.parse_args()


def send_query(args: argparse.Namespace)->str:
    """
    Send query to api point chosen by user
    """
    match args.api_point:
        case "chatGPT" | "openai" | "openAI":
            return askChatGPT(args)
        case "ollama" | "Ollama":
            return askOllama(args)
        case _:
            raise SystemExit("api not found")


def askChatGPT(args: argparse.Namespace)->str:
    """
    Send query to chatGPT using
    """
    from openai import OpenAI
    client = OpenAI(api_key=args.api_key)
    completion = client.chat.completions.create(
        model=args.model,
        messages=[
            {"role": "system", "content": personnal_system_message},
            {"role": "user", "content": args.query}
        ]
    )
    return completion.choices[0].message.content or 'There was an issue with openAI'


def askOllama(args: argparse.Namespace)->str:
    """
    Send query to ollama using langchain lib
    """
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


def parseOutput(resp: str)->Tuple[bool, str]:
    """
    Take an str with the '<CODE>' and </CODE>' brackets and return what's between
    """
    match =  re.search(r'<CODE>(.*)</CODE>', resp)
    if match: return True, match.group(1)
    else: return False, resp


def askExecuteCommand(command)->bool:
    print('AI found this, execute it? [Y/n]\n'+command, end='')
    exe = getch.getch()
    if exe.lower().rstrip().lstrip() in ['', 'y', 'yes']:
        print()
        if 0 == os.system(command): return True
        else: return False
    else : return True

def main():
    config: dict = import_settings()
    args: argparse.Namespace = parse(config)
    args.query = ''.join(args.query)
    #print(args)
    isCommand, output = parseOutput(send_query(args))
    if isCommand:
        askExecuteCommand(output)
    else:
        print("AI didn't return a command, here is its output:\n"+output)

if __name__ == "__main__":
    main()
