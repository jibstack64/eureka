"Contains code to make the console pretty."

# import required libraries
from colorama import Fore as Clr
from colorama import Back as Bck
import colorama
import random
import enum
import os

MOTDS = [
    "You found me, ha!", "I thought Overwatch was porn.", "https://github.com/jibstack64",
    "LETS FUCKING GO!!!!", "rm -rf /", "Let your parents watch.", "Science department best department.",
    "Weybetter 2.0."
]

# for windows nerds
if os.name == "nt":
    colorama.init(convert=True)

# logging types!!
class LogState(enum.Enum):
    Neutral = Clr.WHITE
    Error = Clr.LIGHTRED_EX
    Success = Clr.GREEN
    Warning = Clr.YELLOW

# makes text colourful
def colourise(text: str, colour: str) -> str:
    l = colour.lower()
    for k, v in Clr.__annotations__.items():
        r = k.lower()
        if r.startswith("light"):
            r = r.strip("_ex")
        if l == r:
            return f"{v}{text}{Clr.RESET}"

# logs the provided text to the console
# colourful and nice
def log(text: str, log_state: LogState = LogState.Neutral, special: list[tuple[str, Clr]] = []) -> None:
    if len(special) > 0:
        for s in special:
            text = text.replace(s[0], s[1]+s[0]+Clr.RESET)
    print(f"{log_state._value_}{text}{Clr.RESET}")

# just log but with quit and error
def terminate(text: str) -> None:
    log(text, LogState.Error); quit()

# presented on app startup and on the index page
def motd() -> str:
    return random.choice(MOTDS)
