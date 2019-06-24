from mitmproxy import command
from mitmproxy import flow


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
