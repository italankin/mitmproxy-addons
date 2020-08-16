# Usage

Run `mitmproxy` with one or more addons:

```sh
$ mitmproxy \
    -s replayserverex.py \
    -s sleeper.py \
    -s showurl.py
```

Or while running:

```
: set scripts=replayserver.py
```

# Addons

## replayserverex.py

Extensions for built in ServerPlayback addon.

Commands:

* `replay.server.add` - add flows to server playback
* `replay.server.file.add` - add flows to server playback from file
* `replay.server.list` - show server playback buffer

## replayservermatchers.py

Addons allows to add a [filter](https://docs.mitmproxy.org/stable/concepts-filters/) and for any flow matching it status code and contents of the response will be replaced.

For example, to replace any response from `google.com` with a status code of `200` and contents from `response.json`:

```
: replay.server.matchers.add google.com 200 response.json
```

Commands:

* `replay.server.matchers.add` - add a matcher for server playback
* `replay.server.matchers.clear` - clear all matchers
* `replay.server.matchers.list` - show matchers list

## showurl.py

Commands:

* `view.showurl` - show the URL of the flow

## sleeper.py

Options:

* `sleep` - delay client requests by this amount of time (milliseconds)
* `sleep_filter` - delay only flows which match the filter ([filter expressions](https://docs.mitmproxy.org/stable/concepts-filters/) supported)

## offline.py

Options:

* `offline` - kill all flows
* `offline_filter` - kill only flows matching the filter ([filter expressions](https://docs.mitmproxy.org/stable/concepts-filters/) supported)
