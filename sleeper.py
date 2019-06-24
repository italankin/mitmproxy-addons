import time

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy.script import concurrent


class Sleeper:
    def __init__(self):
        self.filter: flowfilter.TFilter = None

    def load(self, loader):
        loader.add_option(
            "sleep", int, 0,
            "Delay client requests (milliseconds)",
        )
        loader.add_option(
            "sleep_filter", str, "",
            "Delay only matching flows"
        )

    def configure(self, updates):
        if "sleep" in updates:
            value = ctx.options.sleep
            if value is not None and value < 0:
                raise ValueError("'sleep' must be >= 0")
        if "sleep_filter" in updates:
            self.filter = flowfilter.parse(ctx.options.sleep_filter)

    @concurrent
    def request(self, flow):
        delay = ctx.options.sleep
        if delay > 0 and flowfilter.match(self.filter, flow):
            time.sleep(delay / 1000)


addons = [
    Sleeper()
]
