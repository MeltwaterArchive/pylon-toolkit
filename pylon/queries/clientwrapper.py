class ClientWrapper(object):

    def __init__(self, client):
        self.client = client

        # Setup aliases
        if (self.client_type(client) == 'datasift.client.Client'):
            self.aliases_ds_client()

    def client_type(self, o):
        return o.__module__ + "." + o.__class__.__name__

    def aliases_ds_client(self):
        self.create_task = self.client.pylon.task.create
        self.get_task = self.client.pylon.task.get