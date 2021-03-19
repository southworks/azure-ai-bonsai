import os

def get_environment_variable(variable_name: str) -> str:
    """Get the value of an environment variable or throw an exception if it is not defined.

    Parameters
    ----------
    variable_name: str
        Name of the environment variable to read

    Returns
    -------
    str
        Value of the environment variable read
    """
    variable_value = os.getenv(variable_name)

    if variable_value is None:
        raise Exception(f"{variable_name} environment variable is not set!")

    return variable_value

def add_prefixes(d, prefix: str):
    return { f"{prefix}_{k}": v for k, v in d.items() }
