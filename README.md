# mitmproxy-addons

Some addons which can be used for developing and testing client-server applications.

# Usage

Run `mitmproxy` with one or more addons:

```sh
$ mitmproxy \
    -s replayserverex.py \
    -s sleeper.py
```

Or while running:

```
: set scripts=replayserverex.py
```

Or via [config.yaml](https://docs.mitmproxy.org/stable/concepts-options/):

```yaml
scripts: [
    '~/mitmproxy-addons/offline.py',
    '~/mitmproxy-addons/sleeper.py'
]
```

# Addons

## [`replayserverex.py`](./replayserverex.py)

Extensions for built in ServerPlayback addon.

Commands:

* `replay.server.file.add` - add flows to server playback from file
* `replay.server.list` - show server playback buffer

## [`replayservermatchers.py`](./replayservermatchers.py)

This addon allows to add a [filter](https://docs.mitmproxy.org/stable/concepts-filters/) and for any flow matching it status code and contents of the response will be replaced.

For example, to replace any response from `google.com` with a status code of `200` and contents from `response.json`:

```
: replay.server.matchers.add google.com 200 response.json
```

Commands:

* `replay.server.matchers.add` - add a matcher for server playback
* `replay.server.matchers.clear` - clear all matchers
* `replay.server.matchers.list` - show matchers list

## [`sleeper.py`](./sleeper.py)

Adds a delay before sending a request.

Options:

* `sleep` - delay client requests by this amount of time (milliseconds)
* `sleep_filter` - delay only flows which match the [filter](https://docs.mitmproxy.org/stable/concepts-filters/)

## [`offline.py`](./offline.py)

Simulate offline mode by killing all (or matching a filter) requests.

Options:

* `offline` - kill all flows
* `offline_filter` - kill only flows matching the [filter](https://docs.mitmproxy.org/stable/concepts-filters/)
