from environ import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

SSH_SERVER_COMMAND = env('DGIT_SSH_SERVER_COMMAND')