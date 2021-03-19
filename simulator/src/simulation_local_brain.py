from typing import Any, Dict

import importlib
import requests

from simulator_session import SimulatorSession
from util import get_environment_variable

# Class to run simulations with a local Bonsai brain.
class SimulationLocalBrain():
    def __init__(
        self,
        model_name: str,
        render: bool = False,
        log_data: bool = False,
        random_actions: bool = False,
        num_episodes: int = 1,
        num_iterations: int = 50,
    ):
        """
        Parameters
        ----------
        model_name: str
            Name of the model to use. Must be an existing subfolder inside the "models" folder
        render: bool, optional
            Whether to visualize episodes during training, by default False
        log_data: bool, optional
            Whether to log data, by default False
        random_actions: bool, optional
            If true, random actions are used instead of getting them from a local brain, by default False
        num_episodes: int, optional
            Number of episodes to run, by default 1
        num_iterations: int, optional
            Number of iterations to run per episode, by default 50
        """
        self.model_name = model_name
        self.render = render
        self.log_data = log_data
        self.random_actions = random_actions
        self.num_episodes = num_episodes
        self.num_iterations = num_iterations

        self.local_brain_url = None
        self.random_policies = None
        if not self.random_actions:
            self.local_brain_url = get_environment_variable("LOCAL_BRAIN_URL")
        else:
            self.random_policies = importlib.import_module(f'models.{model_name}.policies')

        self.sim = SimulatorSession(model_name=model_name, render=render, log_data=log_data)

    def run(self) -> None:
        """ Run simulation using to a local running brain
        """
        try:
            while self.sim.num_episode < self.num_episodes:
                self.sim.episode_start()
                sim_state = self.sim.get_state()

                # If num_iterations == 0, we loop until the terminal condition is reached.
                while self.num_iterations == 0 or self.sim.num_iteration < self.num_iterations:
                    action = self._get_action_from_local_brain(sim_state) if not self.random_actions else self.random_policies.random_policy(sim_state)
                    self.sim.episode_step(action)
                    sim_state = self.sim.get_state()

                    print(f"Running iteration #{self.sim.num_iteration} for episode #{self.sim.num_episode}")
                    print(f"Action: {action}")
                    print(f"State: {sim_state}")
                    if self.sim.terminal():
                        break

        except KeyboardInterrupt:
            print("Simulation stopped.")
        except Exception as err:
            print("Simulation stopped because: {}".format(err))
            raise(err)

    def _get_action_from_local_brain(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """ Get the action to execute from a local running brain

        Parameters
        ----------
        state: Dict[str, Any]
            Current state of the simulation

        Returns
        -------
        Dict[str, Any]
            Next action taken by the brain
        """
        while True:
            try:
                headers = {'Content-type': 'application/json', 'accept': 'application/json'}
                resp = requests.post(self.local_brain_url, json=state, headers=headers, verify=False)

                if(resp.status_code != 200):
                    print("Waiting to connect to local brain...")

                    if(resp.status_code != 404):
                        print("Error: " + str(resp.status_code) + " Reason: " + str(resp.reason))
                        raise Exception("Http Error: " + str(resp.status_code) + " Reason: " + str(resp.reason))
                    else:
                        sleep(5)
                else:
                    return resp.json()

            except requests.exceptions.ConnectionError as connection_error:
                sleep(5)
