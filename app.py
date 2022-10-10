# import required libraries
import flask.cli
import datetime
import logging
import secrets
import typing
import config
import parser
import flask
import text
import sys
import os

# development or production mode
args = sys.argv[1:]
if len(args) == 1:
    DEV = False if args[0].lower() == "prd" else True
    SECRET_KEY = secrets.token_hex() if not DEV else "dev"
else:
    text.terminate("No mode selected: 'prd' (production) or 'dev' (development).")

# completely useless, just removes pycache (pedantic but oh well)
if DEV:
    if os.path.isdir("__pycache__"):
        text.log("Removing '__pycache__', run with '-B' next time!", text.LogState.Warning)
        if os.name != "nt":
            os.system("rm -rf __pycache__")
        else:
            os.system("rmdir /s __pycache__")

# load static configuration
CONFIG = config.load()

# create server
server = flask.Flask(__name__, static_url_path="/", static_folder=CONFIG.static)
server.secret_key = SECRET_KEY
# disable logging
server.logger.disabled = True
log = logging.getLogger("werkzeug").disabled = True
flask.cli.show_server_banner = lambda *args : None

DAILY = text.motd()
text.log(f"Up and running on '{CONFIG.host}:{CONFIG.port}'.", text.LogState.Success)
text.log(f"  -> In {'production' if not DEV else 'development'} mode.", special=[("production", text.Clr.LIGHTMAGENTA_EX), ("development", text.Clr.LIGHTCYAN_EX)])
text.log(f"  -> MOTD: '{DAILY}'", special=[(DAILY, text.Clr.LIGHTYELLOW_EX)])

# returns the current time in string form
def current_time() -> str:
    return datetime.datetime.now().strftime("%d/%m/%Y | %H:%M:%S")

# log requests
@server.after_request
def after_request(response: flask.Response) -> None:
    text.log(f"[{current_time()}] ({response.status_code}) : {flask.request.method} {flask.request.full_path if len(flask.request.full_path.split('?')) > 2 else flask.request.full_path.strip('?')}", special=[
        ("[", text.Clr.LIGHTBLACK_EX), ("]", text.Clr.LIGHTBLACK_EX),
        ("(", text.Clr.LIGHTBLACK_EX), (")", text.Clr.LIGHTBLACK_EX),
        (str(response.status_code), text.Clr.LIGHTGREEN_EX if response.status_code in range(200, 299) else text.Clr.LIGHTRED_EX if response.status_code in range(400, 499) else text.Clr.LIGHTBLUE_EX)
    ])
    return response

# log exceptions
@server.errorhandler(500)
def error_handler(e: Exception):
    return text.log(f"{e}:\n{e.with_traceback(None)}", text.LogState.Error)

@server.route("/", methods=["GET"])
def index_html() -> None:
    return parser.parse(f"{CONFIG.static}/index.html", DAILY)

@server.route("/chat", methods=["GET"])
def chat_html() -> None:
    return parser.quick(f"{CONFIG.static}/chat.html")

messages = []
@server.route("/chat/messages", methods=["POST", "GET"])
def chat_messages() -> None:
    if flask.request.method == "POST":
        # get message content
        content = flask.request.get_json(True, True)
        if content != None:
            content = content.get("content", None)
        else:
            return flask.make_response("Message content is empty.", 400)
        if len(content) > 100:
            return flask.make_response("Message content is longer than 100 characters.", 400)
        else:
            # clear chat if too long
            if len(globals()["messages"]) > 500:
                globals()["messages"] = []
        # if it contains or is a url, disallow
        if parser.contains_url(content):
            return flask.make_response("Message content contains URL.", 400)
        # add message to list
        globals()["messages"].append(content)
        return flask.make_response("Success, your message has been created.", 200)
    else:
        count = flask.request.args.get("count", 500)
        try:
            count = int(count)
        except:
            return flask.make_response("Count must be an integer.", 400)
        if count < 1 or count > 500:
            return flask.make_response("Invalid message count. Must be over 0 and below 500.", 400)
        if count > len(messages):
            return flask.jsonify(globals()["messages"])
        return flask.jsonify(globals()["messages"][:count])

@server.route("/games", methods=["GET"])
def games_html():
    return parser.quick(f"{CONFIG.static}/games.html")

# run server
if __name__ == "__main__":
    server.run(CONFIG.host, CONFIG.port)
