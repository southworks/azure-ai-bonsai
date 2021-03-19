# Bonsai simulator

## Introduction
This code generates simulators in Python to use with [Microsoft Bonsai](https://docs.microsoft.com/en-us/bonsai/product/). It allows creating simulators for any scenario that can be executed either locally for debugging or pushed to the cloud for training.

## Architecture
The files directly inside the src folder contain the simulator code that executes simulation communicating with either a local brain or a brain hosted in Bonsai. It is built in a generic manner in order to be used for any type of reinforcement learning scenario. Inside the src/models folder, there is a folder for each model that the simulator can use. Each model is designed to simulate a specific scenario (example: leaving a house) and contains the following files:
- `model.py`: The definition of the model itself, this file needs to implement a prespecified interface in order to be used by the simulator correctly.
- `policies.py`: Includes function to generate valid random actions for the scenario. It can be used to quickly test locally if the model defined in `model.py` can be executed by the simulator without errors.
- `machine_teacher.ink`: The [inkling file](https://docs.microsoft.com/en-us/bonsai/inkling/) deployed in Bonsai. This file defines the requirements for the Bonsai brain and needs to be manually copied and executed in Bonsai. Having this file in the repository is only intended for archiving purposes.

## Local simulator with remote Bonsai brain
Executing the simulator locally is pretty slow (less than 10 iterations/second vs 100-200 iterations/second for executing it in the cloud) and should only be done for debugging purposes, not for actual training.

In order to do this follow the next steps:
- Install a virtual environment of Python 3.8.8 using [pyenv](https://github.com/pyenv/pyenv) and [virtualenv](https://virtualenv.pypa.io/en/latest/).
- Enter the virtual environment by executing the "Scripts/activate.bat" file in the Windows command prompt or sourcing "bin/activate" in Bash. This will have to be done each time a new terminal is opened where the simulator will be run.
- Install the required dependencies by doing `pip install -r requirements.txt`.
- Copy the .env.template file inside the src folder (not the one in the root of the simulator folder!) and rename the copy to ".env".
- Complete the values for the SIM_WORKSPACE and SIM_ACCESS_KEY variables by copying them from the Bonsai workspace (clicking on your name on the top-right corner > Workspace info, the value specified in "Workspace ID" and a the only-shown-once value of a new access key created by clicking in "new access key").
- Complete the SIM_PREFIX variable value with a prefix that will be used when creating simulators to be able to easily recognize them to connect them to Bonsai brains. If working on a team, it is recommended to use the name of the person executing them in order to be able to easily track which simulator was created by whom.
- Execute the simulator by going to the "src" folder and running "python `main.py` --model \$MODEL_NAME" being MODEL_NAME the name of the folder inside src/models where the model is defined (example: "python `main.py` --model leaving_home").
- In the Bonsai workspace go to the brain you want to train, click "Train" and select the Unmanaged simulator with name \$SIM_PREFIX-$MODEL_NAME.
- After a few minutes, on the simulator terminal you should start receiving "EpisodeStart" and "EpisodeStep" events.

## Remote simulator with remote Bonsai brain
Executing a simulator in the cloud allows much faster iteration than local execution and should be always be prefered for actually training Bonsai brains. In order to do follow the next steps:
- Make sure the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) is installed in the computer and the [Docker daemon](https://www.docker.com/) is installed and running.
- Copy the .env.template file in the "simulator" folder (not the one inside simulator/src) and rename the copy to ".env".
- Replace the value of the IMAGE_PREFIX variable to a prefix that will be used to identify images pushed from this computer. It is recommended to use the same value used for the SIM_PREFIX variable specified in the "Local simulator with remote Bonsai brain" section.
- Replace the value of the REPOSITORY variable by the name of the ACR used by Bonsai. This can be found by opening the Bonsai resource in the Azure portal and looking in the "Registry" value in the Overview tab.
- Execute "./build.sh \$MODEL_NAME" to build the Docker image related to the model. The MODEL_NAME should be the name of the folder inside src/models where the model is defined. The image will be locally tagged as \$IMAGE_PREFIX-$MODEL_NAME.
- Execute "./login.sh" to login to the Azure Container Registry. This should only be necessary once per day if the `push.sh` command below throws an authentication error. If the `login.sh` script throws an authentication error, the "az login" command should be executed.
- Execute "./push.sh \$MODEL_NAME" to push the image to the ACR.
- Add the simulator to Bonsai by clicking "Add sim" > "Other", appending the image name (\$IMAGE_PREFIX-$MODEL_NAME) to the ACR URL and selecting a display name.
- Run the Bonsai brain by clicking "Train" and selecting the simulator from the "Simulator packages" list with the selected display name.

## Local simulator with local Bonsai brain
Once the brain has been trained, we can export the brain and download it for local execution. In order to do so, follow these steps:
- Make sure the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) is installed in your computer and the [Docker daemon](https://www.docker.com/) is installed and running.
- Go to the brain and version that you trained and want to export, navigate to the Train panel and click in "Export Brain". Provide the name for the exported brain, select the operating system the brain will run on and select the procesor architecture the brain will run on. Then click the "Export" button. An image of the exported brain is packaged as a Docker container, saved to the ACR associated with your workspace, and added to the list of available brains under Exported Brains in the left-hand menu.
To download the docker container do the following:
- Go to the exported brain in the list of available brains under Exported Brains in the left-hand menu and click on the "location" link. Copy all sentences that the platform shows and execute them in your local terminal. With this sentence you can the brain on a local docker.
- You can visit "http://localhost:5000/v1/doc/index.html" to show the swagger of the api that you execute when ran the docker. You can test the actions that the brain will perform if you change the state values.
- Copy the .env.template file inside the src folder (not the one in the root of the simulator folder!) and rename the copy to ".env".
- Complete the value for the LOCAL_BRAIN_URL variable to the URL used to contact the brain (if its running locally: "http://localhost:5000/v1/prediction").
- When you have the docker image running you can execute the simulator using this docker image. To do this you must execute the following sentence: "python `main.py` --model \$MODEL_NAME --local-brain True"

## Local simulator with random actions
When a new model is created, a quick local test can be performed in order to quickly validate the correct definition of the model without needing to connect it to Bonsai. This is done by using the policies defined in `policies.py` to select random actions in place of the Bonsai brain. This can be done by preparing the virtual environment as specified in the "Local simulator with remote Bonsai brain" section and executing the command "python `main.py` --model $MODEL_NAME --random-actions True".
