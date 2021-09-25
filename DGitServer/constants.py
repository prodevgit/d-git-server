from environ import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

SSH_AUTHORIZED_KEYS = env('SSH_AUTHORIZED_KEYS')
SSH_SERVER_COMMAND = env('DGIT_SSH_SERVER_COMMAND')
DGIT_DATA_PATH = env('DGIT_DATA_PATH')