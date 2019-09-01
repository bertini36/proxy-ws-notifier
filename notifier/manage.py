# -*- coding: UTF-8 -*-

from app import NotifierApp
from app.settings import HOST, PORT, DEBUG


if __name__ == '__main__':
    app = NotifierApp()
    app.run(host=HOST, port=PORT, debug=DEBUG)

