"""
MSFT Bonsai SDK3 Template for Simulator Integration using Python
Copyright 2020 Microsoft
"""

import argparse

from dotenv import load_dotenv
from distutils.util import strtobool

from simulation_remote_brain import SimulationRemoteBrain
from simulation_local_brain import SimulationLocalBrain

parser = argparse.ArgumentParser(description="Bonsai and Simulator Integration...")
parser.add_argument(
    "--model",
    default="",
    help="Model used by the simulator [Required].",
)
parser.add_argument(
    "--render",
    type=lambda x: bool(strtobool(x)),
    default=False,
    help="Render training episodes. Default: False.",
)
parser.add_argument(
    "--log-iterations",
    type=lambda x: bool(strtobool(x)),
    default=False,
    help="Log iterations during training. Default: False.",
)
parser.add_argument(
    "--use-env-file",
    type=lambda x: bool(strtobool(x)),
    default=True,
    help="Get environment variables from an environment file. Default: True.",
)
parser.add_argument(
    "--local-brain",
    type=lambda x: bool(strtobool(x)),
    default=False,
    help="Run simulator locally by connecting to local model API. Default: False.",
)
parser.add_argument(
    "--random-actions",
    type=lambda x: bool(strtobool(x)),
    default=False,
    help="Execute a simulation using random actions without connecting to a brain. Default: False.",
)

args = parser.parse_args()

if args.use_env_file:
    load_dotenv(verbose=True, override=True)

if not args.local_brain and not args.random_actions:
    simulation = SimulationRemoteBrain(
        model_name=args.model,
        render=args.render,
        log_data=args.log_iterations,
    )
else:
    simulation = SimulationLocalBrain(
        model_name=args.model,
        render=args.render,
        log_data=args.log_iterations,
        random_actions=args.random_actions,
        num_episodes=1 if not args.random_actions else 100,
        num_iterations=0 if not args.random_actions else 50,
    )

simulation.run()
