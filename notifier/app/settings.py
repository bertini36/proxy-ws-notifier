# -*- coding: UTF-8 -*-

from environs import Env

env = Env()
env.read_env('.env')

DEBUG = env.bool('DEBUG', default=True)
HOST = env.str('HOST', default='0.0.0.0')
PORT = env.int('PORT', default=8000)
TASK_HOST = env.str('TASK_HOST', 'rabbit')
