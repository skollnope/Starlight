import os

def get_openai_key(env_key:str = "STARLIGHT_OPENAI_KEY"):
    """
    summmary: 
        request your private Open AI API key

    Args:
        env_key: the name of the environment key, default is: STARLIGHT_OPENAI_KEY

    return:
        None if the specified key isn't found, otherwise return the environment key value
    """

    return os.environ.get(env_key, None)
