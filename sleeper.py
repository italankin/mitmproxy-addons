import time
from typing import Optional

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy.script import concurrent
from mitmproxy.exceptions import OptionsError


matchall = flowfilter.parse(".")

class Sleeper:
    def __init__(self):
        self.filter: Optional[flowfilter.TFilter] = matchall

    def load(self, loader):
        loader.add_option(
            "sleep", Optional[int], None,
            "Delay client requests (milliseconds)",
        )
        loader.add_option(
            "sleep_filter", Optional[str], None,
            "Apply delay to flows which match the filter"
        )

    def configure(self, updates):
        if "sleep" in updates:
            sleep = ctx.options.sleep
            if sleep and sleep < 0:
                raise OptionsError("'sleep' must be >= 0")
        if "sleep_filter" in updates:
            filt_str = ctx.options.sleep_filter
            filt = matchall if not filt_str else flowfilter.parse(filt_str)
            if not filt:
                raise OptionsError("Invalid filter expression: %s" % filt_str)
            self.filter = filt

    @concurrent
    def request(self, flow):
        delay = ctx.options.sleep
        if delay and delay > 0 and flowfilter.match(self.filter, flow):
            time.sleep(delay / 1000)


addons = [
    Sleeper()
]
