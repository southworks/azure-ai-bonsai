from typing import Any, Dict

import datetime
import os
import pathlib
import importlib
import pandas as pd

from util import add_prefixes

# Wrapper around models that add capabilities to log and render.
class SimulatorSession:
    def __init__(
        self,
        model_name: str,
        render: bool = False,
        log_data: bool = False,
        log_file: str = None,
    ):
        """Simulator Interface with the Bonsai Platform

        Parameters
        ----------
        model_name: str
            Name of the model to use. Must be an existing subfolder inside the "models" folder
        render: bool, optional
            Whether to visualize episodes during training, by default False
        log_data: bool, optional
            Whether to log data, by default False
        log_file: str, optional
            where to log data, by default None
        """
        model = importlib.import_module(f'models.{model_name}.model')
        self.model_name = model_name
        self.simulator = model.model()
        self.render = render
        self.log_data = log_data
        self.log_path = "logs"
        self.log_file = log_file if log_file is not None else self._gen_logfile_name()
        self.num_episode = 0
        self.num_iteration = 0

    def get_state(self) -> Dict[str, Any]:
        """Extract current states from the simulator

        Returns
        -------
        Dict[str, Any]
            Returns current state values from the simulator
        """
        return self.simulator.get_state()

    def halted(self) -> bool:
        """Halt current episode. Note, this should only return True if the simulator has reached an unexpected state.

        Returns
        -------
        bool
            Whether to terminate current episode due to simulator running into an unexpected state
        """
        return False

    def episode_start(self, config: Dict = None) -> None:
        """Initialize simulator environment using scenario parameters from inkling.

        Parameters
        ----------
        config: Dict, optional
            Configuration used for the model
        """

        self.num_episode += 1
        self.num_iteration = 0
        self.simulator.reset(config) if config is not None else self.simulator.reset()

    def terminal(self) -> None:
        """Check if the simulator met the termination condition

        Returns
        -------
        bool
            Whether the current episode should be terminated
        """
        return self.simulator.terminal()

    def episode_step(self, action: Dict[str, Any]) -> None:
        """Step through the environment for a single iteration.

        Parameters
        ----------
        action : Dict[str, Any]
            An action to take to modulate environment.
        """
        self.num_iteration += 1

        self.simulator.step(action)
        if self.render:
            self.sim_render()

        if self.log_data:
            self._log_iterations(action=action)

    def sim_render(self) -> None:
        """Renders the current state of the simulation.
        """
        self.simulator.render()

    def _gen_logfile_name(self) -> str:
        """Generates the logfile name based on the model name and the current time.

        Returns
        -------
        str
            Name of the logfile
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        log_file = f"{self.model_name}_{current_time}.csv"
        log_file = os.path.join(self.log_path, log_file)
        logs_directory = pathlib.Path(log_file).parent.absolute()
        if not pathlib.Path(logs_directory).exists():
            print(
                "Directory does not exist at {0}, creating now...".format(
                    str(logs_directory)
                )
            )
            logs_directory.mkdir(parents=True, exist_ok=True)

        return log_file

    def _log_iterations(self, action: Dict[str, Any]) -> None:
        """Log iterations during training to a CSV.

        Parameters
        ----------
        action: Dict[str, Any]
            Last action taken by the brain
        """
        state = self.get_state()
        state = add_prefixes(state, "state")
        action = add_prefixes(action, "action")
        data = {**state, **action}
        data["episode"] = self.num_episode
        data["iteration"] = self.num_iteration
        log_df = pd.DataFrame(data, index=[0])

        if os.path.exists(self.log_file):
            log_df.to_csv(
                path_or_buf=self.log_file, mode="a", header=False, index=False
            )
        else:
            log_df.to_csv(path_or_buf=self.log_file, mode="w", header=True, index=False)
