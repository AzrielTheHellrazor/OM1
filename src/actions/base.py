import time
import typing as T
from abc import ABC, abstractmethod
from dataclasses import dataclass

IT = T.TypeVar("IT")
OT = T.TypeVar("OT")


@dataclass
class MoveCommand:
    """
    Data class representing a movement command for robot navigation.

    Attributes
    ----------
    dx : float
        Distance to move in x direction
    yaw : float
        Rotation angle in yaw axis
    start_x : float
        Starting x coordinate (default: 0.0)
    start_y : float
        Starting y coordinate (default: 0.0)
    turn_complete : bool
        Whether turn is complete (default: False)
    speed : float
        Movement speed (default: 0.5)
    """
    dx: float
    yaw: float
    start_x: float = 0.0
    start_y: float = 0.0
    turn_complete: bool = False
    speed: float = 0.5


@dataclass
class ActionConfig:
    """
    Configuration class for Action implementations.

    Parameters
    ----------
    **kwargs : dict
        Additional configuration parameters
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@dataclass
class Interface(T.Generic[IT, OT]):
    """
    An interface for a action.
    """

    input: IT
    output: OT


class ActionConnector(ABC, T.Generic[OT]):
    """
    Base class for action connectors that interface with hardware or services.

    Action connectors are responsible for translating action commands into
    hardware-specific or service-specific operations.
    """
    def __init__(self, config: ActionConfig):
        self.config = config

    @abstractmethod
    async def connect(self, input_protocol: OT) -> None:
        """
        Execute the action using the provided input protocol.

        Parameters
        ----------
        input_protocol : OT
            The input protocol containing action parameters
        """
        pass

    def tick(self) -> None:
        """
        Periodic tick method for connector maintenance.

        Default implementation sleeps for 60 seconds.
        """
        time.sleep(60)


@dataclass
class AgentAction:
    """Base class for agent actions"""

    name: str
    llm_label: str
    interface: T.Type[Interface]
    connector: ActionConnector
    exclude_from_prompt: bool
