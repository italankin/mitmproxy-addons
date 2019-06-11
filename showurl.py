import typing

from mitmproxy import command
from mitmproxy import flow
import mitmproxy.types

class ShowUrl:
    @command.command("view.showurl")
    def show_url(self, flow: flow.Flow) -> str:
        """
            Show flow's request URL.
        """
        return flow.request.url

addons = [
    ShowUrl()
]