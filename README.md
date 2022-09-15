# Webthon

Webthon is a webinterface to make and controll python scripts. That runs on one or more Raspberry or almost any Linux system.

## What is Webthon
Webthon is a Kubernetes look a like, but is made only for python scripts and python code. It is an easy way to make and monitor multiple python scripts. All from AI/ML to small automation home controlls and discord bots. I is made to run on one or multipel raspberry pi's. For better ease and faster code.

## Documentation
the documentation page is still under construction.
[Click Here]()


## Installation and preparation

First you need to install "The Visual Studio Code Server"

```bash
  wget -O- https://aka.ms/install-vscode-server/setup.sh | sh
```
And the follow the installation 
```bash
  code-server
```
or just follow [this](https://code.visualstudio.com/docs/remote/vscode-server#_quick-start)

You also need python 3.11+ 
```bash
    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.11
```

Clone the project

```bash
  git clone https://github.com/dron3flyv3r/Webthon
```

Go to the project directory

```bash
  cd webthon
```

Install dependencies

```bash
  pip install requirements.txt
```
or
```bash
  pip3 install requirements.txt
```
or
```bash
  python -m pip install requirements.txt
```

## Start the server


```bash
  nohup python main.py > .output.log &
```
or
```bash
  nohup python3 main.py > .output.log &
```


## FAQ

#### Dose it run on windows?

As of now, no you can't deploy it on window.

#### How is it made?

The backend is made with flask.


## Authors

- [@dron3flyv3r](https://www.github.com/dron3flyv3r)

