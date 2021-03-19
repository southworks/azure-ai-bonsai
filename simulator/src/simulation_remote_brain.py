from typing import Any

from time import sleep, strftime

from azure.core.exceptions import HttpResponseError
from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import (
    SimulatorInterface,
    SimulatorState,
    SimulatorSessionResponse,
    Event,
)

from simulator_session import SimulatorSession
from util import get_environment_variable

# Class to run simulations with a remote Bonsai brain.
class SimulationRemoteBrain:
    def __init__(
        self,
        model_name: str,
        render: bool = False,
        log_data: bool = False,
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
        """
        self.model_name = model_name
        self.render = render
        self.log_data = log_data

        self.sim = SimulatorSession(model_name=model_name, render=render, log_data=log_data)

        # The SIM_WORKSPACE and SIM_ACCESS_KEY are used internally by the BonsaiClient. So even if we don't use them, we check for their existence.
        get_environment_variable("SIM_WORKSPACE")
        get_environment_variable("SIM_ACCESS_KEY")
        sim_prefix = get_environment_variable("SIM_PREFIX")

        # Configure client to interact with Bonsai service
        self.config_client = BonsaiClientConfig()
        self.client = BonsaiClient(self.config_client)

        # Create simulator session
        self.registration_info = SimulatorInterface(
            name=f"{sim_prefix}_{self.sim.model_name}",
            timeout=60,
            simulator_context=self.config_client.simulator_context,
        )

        self.registered_session = None
        self.sequence_id = None

    def run(self):
        """ Leave simulator running to be used by a Bonsai-hosted brain
        """
        self._recreate_bonsai_session()

        try:
            while True:
                # Get next event from Bonsai.
                try:
                    event = self._get_next_event()
                    print("[{}] Event: {}".format(strftime("%H:%M:%S"), event.type))
                except Exception as err:
                    # If there is any exception while trying to get the next event from Bonsai, we re-create the session
                    # to continue the simulation.
                    self._recreate_bonsai_session()
                    continue

                # Event loop
                if event.type == "Idle":
                    print("Idling...")
                    sleep(event.idle.callback_time)
                elif event.type == "EpisodeStart":
                    print(event.episode_start.config)
                    self.sim.episode_start(event.episode_start.config)
                elif event.type == "EpisodeStep":
                    self.sim.episode_step(event.episode_step.action)
                elif event.type == "EpisodeFinish":
                    print("Episode Finishing...")
                elif event.type == "Unregister":
                    print("Simulator Session unregistered by platform, Registering again!")
                    self._recreate_bonsai_session()
                    continue

        except Exception as err:
            # Gracefully unregister for any other exceptions
            self._unregister_simulator()
            print("Unregistered simulator because: {}".format(err))
            raise(err)

    def _recreate_bonsai_session(self) -> None:
        """Recreates the instance Bonsai Session
        """

        try:
            print("config: {}, {}".format(self.config_client.server, self.config_client.workspace))

            self.registered_session: SimulatorSessionResponse = self.client.session.create(
                workspace_name=self.config_client.workspace,
                body=self.registration_info,
            )

            print("Registered simulator. {}".format(self.registered_session.session_id))

            self.sequence_id = 1
        except HttpResponseError as ex:
            print(
                "HttpResponseError in Registering session: StatusCode: {}, Error: {}, Exception: {}".format(
                    ex.status_code, ex.error.message, ex
                )
            )
            raise ex
        except Exception as ex:
            print(
                "Unexpected error: {}, Most likely, it's some network connectivity issue, make sure you are able to reach bonsai platform from your network.".format(
                    ex
                )
            )
            raise ex

    def _get_next_event(self) -> Event:
        """Gets next event to execute by the simulator from Bonsai.

        Returns
        -------
        Event
            Next Bonsai event to process by the simulator
        """
        # Map the simulation state to the Bonsai state (adds extra parameters needed by Bonsai).
        bonsai_state = SimulatorState(sequence_id=self.sequence_id, state=self.sim.get_state(), halted=self.sim.halted())

        try:
            # Get next event from Bonsai.
            event = self.client.session.advance(
                workspace_name=self.config_client.workspace,
                session_id=self.registered_session.session_id,
                body=bonsai_state,
            )
            self.sequence_id = event.sequence_id
            return event
        except HttpResponseError as ex:
            print(
                "HttpResponseError in Advance: StatusCode: {}, Error: {}, Exception: {}".format(
                    ex.status_code, ex.error.message, ex
                )
            )
            raise(ex)
        except Exception as ex:
            print("Unexpected error in Advance: {}".format(ex))
            # Ideally this shouldn't happen, but for very long-running sims It can happen with various reasons.
            # If possible try to notify Bonsai team to see, if this is platform issue and can be fixed.
            raise(ex)

    def _unregister_simulator(self) -> None:
        """ Unregister simulator from Bonsai umanaged simulators
        """
        self.client.session.delete(
            workspace_name=self.config_client.workspace,
            session_id=self.registered_session.session_id,
        )
