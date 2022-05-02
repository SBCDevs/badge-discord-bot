# Discord bot that communicates with the badge tracker backend

Easy to use discord bot that lets users count their badges from a discord server

## Setup the repository for local development

* [Download GitHub CLI](https://cli.github.com/)
* [Download Git](https://git-scm.com/downloads)
* [Download Python 3.8.10](https://www.python.org/downloads/release/python-3810/) (Scroll down and you should be able to see the download links)
* Authenticate Git with GitHub CLI (Use the `gh auth login` and it should guide you thru the process)
* Clone the repo with `git clone https://github.com/SBCDevs/badge-discord-bot`
* Change the directory into the folder with `cd badge-discord-bot`
* Type in `pip install -r requirements.txt` to install all the needed packages
* Type in `cp .env.example .env` and edit the `.env` file to suit your needs
* Start the server with `python main.py`
