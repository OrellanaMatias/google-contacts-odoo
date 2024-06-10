import logging

class LoggerModule:
    _name = 'LoggerModule'
    _description = 'put in place a logger capability'

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('/var/log/odoo/odoo.googleContact.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
