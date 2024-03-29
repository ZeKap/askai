# What is AskAI?
AskAI's purpose is to help you making commands in your shell.
For example, if you want to see you git log but forgot the command, just ask:
```sh
$ askai see my last git commits
```
If your AI isn't too bad, you'll see something like:
```sh
$ askai see my last git commits
AI found this, execute it? [Y/n]
git log --graph
```
If your AI is really dumb, you could have something like:
```sh
$ askai see my last git commits
AI didn't return a command, here is its output:

If you want to see you last commits in git, first install git:
`apt install git`
then you can see the commits by using this command:
`git log`

If you have any question, feel free to ask.
```
But it depends on what AI you use. On this topic:

# Installation

There are several ways to install askAI

## pipx (easiest)
```sh
pipx install git+https://github.com/ZeKap/askai
```

## Manual
Just copy askAI.py somewhere, and install its dependencies. Since it will probably be in a venv, you can use this script to call it easily:
```sh
#!/bin/sh

params=("$*")
bash -c "\
source ~/[where you put askai]/venv/bin/activate; \
python3 ~/[where you put askai]/askAI.py ${params[@]}; \
"
```

# Your config, your AI.
In the first launch, askai will tell you it's missing a lot of parameters to work.
In fact, it will first create the directory needed in `.config/askAI/config.yaml` and the YAML file for you to fill. When you don't add "default" settings in the config file, you'll need to set the parameters when calling askai and that's why its telling you it's missing parameters.

# Other API
With askai, you can of course use openAI chatGPT, but you can also use ollama if you want to use a local AI.
If you want to use another API, feel free to make the function and do a pull request if you want so we can all enjoy aswell.

# Small project
As this is a really small project, don't expect a lot support nor updates. I only made functions to use chatGPT and ollama because that the ones I use, if any other API can be used, it's thanks to somebody else.
