import logging
import os

from mitmproxy import command, ctx, http, types, flowfilter, exceptions
from mitmproxy.log import ALERT
from mitmproxy.tools.console import overlay


class ReplayServerMatchers:
    def __init__(self):
        self.matchermap = {}
        pass

    @command.command("replay.server.matchers.add")
    def add(self, filter_expr: str, code: int, path: types.Path):
        """
            Add a new matcher for server playback
        """
        filt = flowfilter.parse(filter_expr)
        if not filt:
            raise exceptions.CommandError("invalid flow filter: %s" % filter_expr)
        if not os.path.exists(path) or not os.path.isfile(path):
            raise exceptions.CommandError("file '%s' does not exists or is not a file" % path)
        self.matchermap[filter_expr] = FlowMatcher(filt, code, path)
        logging.getLogger().log(ALERT, "Added 1 matcher")

    @command.command("replay.server.matchers.clear")
    def clear(self):
        """
            Remove all matchers
        """
        size = len(self.matchermap)
        self.matchermap.clear()
        logging.getLogger().log(ALERT, f"Removed {size} matchers")

    @command.command("replay.server.matchers.list")
    def list(self):
        """
            Show added matchers
        """
        if len(self.matchermap) == 0:
            logging.getLogger().log(ALERT, "No matchers")
            return

        choices = []
        for (key, matcher) in self.matchermap.items():
            choices.append("%s | %s | %s" % (key, matcher.code, matcher.path))

        def callback(_):
            pass

        ctx.master.overlay(
            overlay.Chooser(ctx.master, "Matchers", choices, "", callback)
        )

    def response(self, flow: http.HTTPFlow):
        for matcher in self.matchermap.values():
            if matcher.match(flow):
                with open(matcher.path, "rt", encoding="utf8") as f:
                    try:
                        txt = f.read()
                    except IOError as e:
                        raise ValueError("can not read file '%s': %s" % (matcher.path, e))
                flow.response.status_code = matcher.code
                flow.response.set_text(txt)
                flow.is_replay = "response"
                break


class FlowMatcher:
    def __init__(self, filt: flowfilter.TFilter, code: int, path: types.Path):
        self.filt = filt
        self.code = code
        self.path = path

    def match(self, flow):
        return flowfilter.match(self.filt, flow)


addons = [
    ReplayServerMatchers()
]
