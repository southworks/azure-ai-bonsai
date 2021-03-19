# Issues and limitations
During our experience using the Bonsai platform we ran into several issues and limitations.

## Current issues
These are some current unexpected behaviors found in the Bonsai platform. We believe that these are probably bugs, which is to be expected for a platform in preview state, that should be ironed out in future versions:
* The most effective way of training in Bonsai is to push a Docker image with the simulated environment and have Bonsai use it as a base to spawn Azure Container Instances. This works correctly but there are situations in which these container instances are not cleaned up properly, which can lead to an increased amount of resource consumption until these instances are manually stopped.

* After a brain has been trained, Bonsai allows exporting it as a Docker image. This Docker image can be used to create containers, either locally or in an Azure Container Instance, that implement an API that can be used to communicate with the trained brain. This image currently has multiple issues including:
    * It stops responding to incoming requests after a few minutes of not being used when deployed to an Azure Container Instance.
    * Only responding to requests that come from the first source that contacted it, ignoring requests from other sources.

* When using goals instead of reward functions, users must define the objective as a range of values, single values are not supported. According to the Microsoft Tech Community, a workaround to allow single values would be using the same value for both limits in the range. However, trying to use this approach results in errors. Questions we posted on the Microsoft Tech Community forum and their respective answers are documented here.

## Limitations
These are some limitations we ran into when using Bonsai:
* The Bonsai platform can have issues when trying to train an agent if the evolution of the system state does not depend only on the previous state and the action taken but also on factors outside of the agent’s control (for instance, if the environment changes the system state depending on random factors).

* Exported brains from the platform do not implement any kind of authorization mechanism or HTTPS support, this has to be provided on a separate layer.

[Continue reading..](../08-conclusions/README.md)
