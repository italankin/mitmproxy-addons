import logging
from typing import List

import mitmproxy.types
from mitmproxy import command
from mitmproxy import ctx
from mitmproxy import exceptions
from mitmproxy import hooks
from mitmproxy import io
from mitmproxy.addons import serverplayback
from mitmproxy.flow import Flow
from mitmproxy.http import HTTPFlow
from mitmproxy.log import ALERT
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
            raise exceptions.CommandError(e, str(e))
        self._add_flows(flows)

    @command.command("replay.server.list")
    def list_flows(self) -> None:
        """
            Show server responses list.
        """
        recorded_flows: List[Flow] = []
        for flows in _find_addon().flowmap.values():
            for f in flows:
                recorded_flows.append(f)

        if len(recorded_flows) == 0:
            logging.getLogger().log(ALERT, "No flows")
            return

        choices = []
        for f in recorded_flows:
            if not isinstance(f, HTTPFlow):
                continue
            c = FlowChoice(f.request.url)
            c.flow = f
            choices.append(c)

        def callback(opt):
            if opt.flow not in ctx.master.view:
                logging.getLogger().log(ALERT, "Not found")
            else:
                ctx.master.view.focus.flow = opt.flow

        ctx.master.overlay(
            overlay.Chooser(ctx.master, "Flows", choices, "", callback)
        )

    def _add_flows(self, flows: list[Flow]) -> None:
        """
            Replay server responses from flows.
        """
        addon = _find_addon()
        updated = 0
        for f in flows:
            if isinstance(f, HTTPFlow) and f.response:
                flowlist = addon.flowmap.setdefault(addon._hash(f), [])
                flowlist.append(f)
                updated = updated + 1
        ctx.master.addons.trigger(hooks.UpdateHook([]))
        logging.getLogger().log(ALERT, "Added %d flows" % updated)


class FlowChoice(str):
    """
        A str subclass which holds 'flow' instance
    """
    pass


addons = [
    ReplayServerEx()
]
