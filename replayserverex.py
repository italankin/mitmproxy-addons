from collections.abc import Sequence

import mitmproxy.types
from mitmproxy import command
from mitmproxy import ctx
from mitmproxy import exceptions
from mitmproxy import flow
from mitmproxy import hooks
from mitmproxy import io
from mitmproxy.addons import serverplayback
from mitmproxy.tools.console import overlay


def _find_addon() -> serverplayback.ServerPlayback:
    addon = ctx.master.addons.get("serverplayback")
    if not addon:
        raise ValueError("Cannot find addon 'serverplayback'")
    return addon


class ReplayServerEx:
    @command.command("replay.server.file.add")
    def load_file(self, path: mitmproxy.types.Path) -> None:
        """
            Append server responses from file.
        """
        try:
            flows = io.read_flows_from_paths([path])
        except exceptions.FlowReadException as e:
            raise exceptions.CommandError(str(e))
        self.add_flows(flows)

    @command.command("replay.server.list")
    def list_flows(self) -> None:
        """
            Show server responses list.
        """
        recorded_flows = []
        for flows in _find_addon().flowmap.values():
            for f in flows:
                recorded_flows.append(f)

        if len(recorded_flows) == 0:
            ctx.log.alert("No flows.")
            return

        choices = []
        for flow in recorded_flows:
            c = FlowChoice(flow.request.url)
            c.flow = flow
            choices.append(c)

        def callback(opt):
            if opt.flow not in ctx.master.view:
                ctx.log.alert("Not found.")
            else:
                ctx.master.view.focus.flow = opt.flow

        ctx.master.overlay(
            overlay.Chooser(ctx.master, "Flows", choices, "", callback)
        )


class FlowChoice(str):
    """
        A str subclass which holds 'flow' instance
    """
    pass


addons = [
    ReplayServerEx()
]
