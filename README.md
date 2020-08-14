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

Commands:

* `replay.server.add` - add flows to server playback
* `replay.server.file.add` - add flows to server playback from file
* `replay.server.list` - show server playback buffer

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
