# import required libraries
from pyngrok import ngrok
import logging
import ctypes
import sys
import os

# sets up an ngrok tunnel and returns its url
def host(auth: str, port: int) -> str:
    ngrok.set_auth_token(auth)
    # request auth
    admin = False
    if os.name == "nt": # linux user gives windows support?!
        try:
            admin = ctypes.windll.shell32.IsUserAnAdmin()
        except:
            admin = False
    else:
        os.system("pkexec ls -l") # I’d just like to interject for a moment. What you’re refering to as Linux, is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.
    # disable ngrok logging
    ngrok.logger.disabled = True
    logging.getLogger("ngrok").disabled = True
    # tunnel
    tunnel = ngrok.connect(port, "http")
    return tunnel.public_url

# shuts down any running ngrok tunnels
def close(url: str) -> None:
    ngrok.disconnect(url)
