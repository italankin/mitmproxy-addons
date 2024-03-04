from typing import Optional

from mitmproxy import ctx
from mitmproxy import flowfilter
from mitmproxy.exceptions import OptionsError
from mitmproxy.optmanager import OptManager


class Offline:
    def __init__(self):
        self.offline = False
        self.matchall = flowfilter.parse(".")
        self.filter: Optional[flowfilter.TFilter] = self.matchall

    def load(self, loader: OptManager):
        loader.add_option(
            "offline", bool, False,
            "Kill all flows",
        )
        loader.add_option(
            "offline_filter", Optional[str], None,
            "Kill only flows matching the filter"
        )

    def configure(self, updates: set[str]):
        if "offline" in updates:
            value = ctx.options.offline
            if value is not None:
                self.offline = value
        if "offline_filter" in updates:
            filt_str = ctx.options.offline_filter
            filt = self.matchall if not filt_str else flowfilter.parse(filt_str)
            if not filt:
                raise OptionsError("Invalid filter expression: %s" % filt_str)
            self.filter = filt

    def request(self, flow):
        if self.offline and flowfilter.match(self.filter, flow):
            flow.kill()


addons = [
    Offline()
]
