"Holds configuration classes and a config loader."

# import required libraries
from typing import Any
import toml

# simple configuration container classes

class Config:
    def __init__(self, n: str, d: dict[str, Any]) -> None:
        self._type = n
        self._data = d
        self._port: int = d[n]["port"]
        self._to_console: bool = d[n]["logging"]["to_console"]
        self._to_dump: bool = d[n]["logging"]["to_dump"]

    @property
    def host(self) -> str:
        return "0.0.0.0"

    @property
    def ngrok_auth(self) -> str:
        return self._data["ngrok_auth"]

    @property
    def static(self) -> str:
        return self._data["static"]

    @property
    def port(self) -> int:
        return self._port

    @property
    def to_console(self) -> bool:
        return self._to_console
    
    @property
    def to_dump(self) -> bool:
        return self._to_dump

class ProductionConfig(Config):
    def __init__(self, d: dict[str, Any]) -> None:
        super().__init__("prd", d)

class DevelopmentConfig(Config):
    def __init__(self, d: dict[str, Any]) -> None:
        super().__init__("dev", d)

# simply retrieves the configuration and returns it in its suitable class
def load(dev: bool = True) -> Config:
    d = toml.load("config.toml")
    return DevelopmentConfig(d) if dev else ProductionConfig(d)
