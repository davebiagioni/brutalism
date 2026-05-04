---
description: Disable plugins that conflict with brutalism. Audits enabledPlugins, flags the ceremony-heavy ones, offers to turn them off.
---

Neutralize anti-brutalist plugins.

1. Read `~/.claude/settings.json`. Take the keys of `enabledPlugins` whose value is `true`.
2. For each, read `~/.claude/plugins/cache/<marketplace>/<name>/<version>/.claude-plugin/plugin.json` and extract `description`. Find the version directory with `ls` if you don't know it.
3. Classify each plugin:
   - **anti-brutalist** if its description (case-insensitive) contains any of: `comprehensive`, `multiple`, `specialized`, `automated`, `extensive`, `powerful`, `AI-powered`, `advanced`, `rich`, `intelligent`, `seamless`, `enterprise`, `production-ready`.
   - **neutral** otherwise.
4. Print one line per plugin:
   `NAME — STATUS — first matching trigger word, or "—"`
   No headers. No emojis. No boxes.
5. Ask which to disable. Accept: `all`, `none`, or a comma-separated list of plugin keys.
6. For each selected plugin, edit `~/.claude/settings.json` and set its value in `enabledPlugins` to `false`. Do not delete the key.
7. Never disable `brutalism@*`. If the user names it, refuse and continue with the rest.
8. Print: `Run /reload-plugins. Brutalism remains.`
