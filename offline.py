from mitmproxy import ctx


class Offline:
    def __init__(self):
        self.offline = False

    def load(self, loader):
        loader.add_option(
            "offline", bool, False,
            "Kill HTTP CONNECT requests",
        )

    def configure(self, updates):
        if "offline" in updates:
            value = ctx.options.offline
            if value is not None:
                self.offline = value

    def http_connect(self, flow):
        if self.offline:
            flow.kill()


addons = [
    Offline()
]
