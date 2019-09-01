# -*- coding: UTF-8 -*-

from sanic import Sanic


class NotifierApp(Sanic):

    def __init__(self, *args, **kwargs):
        super().__init__('notifier', *args, **kwargs)
        self.setup_views()

    def setup_views(self):
        from .views import bp
        self.blueprint(bp)
