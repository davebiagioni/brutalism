# brutalism

Claude Code plugin. The anti-superpowers plugin.

Writes code with minimal aesthetics and minimal extensibility. Gets it done in as few lines as possible.

![Engineering Center at the University of Colorado Boulder, a brutalist concrete building](assets/engineering-center.jpg)

<sub>Engineering Center, University of Colorado Boulder. Photo by [Jesse James](https://www.flickr.com/photos/jjes84/55029487863/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Engineering_Center_CU_Boulder_(55029487863).jpg). Resized.</sub>

## Install

    /plugin marketplace add davebiagioni/brutalism
    /plugin install brutalism@brutalism
    /reload-plugins

## Use

- `/brutalism:brutalize <path>` — strip a file to its essentials. Lists what it will remove first, waits for confirmation.
- `/brutalism:depower` — audit `enabledPlugins` and turn off the ceremony-heavy ones (multi-agent reviewers, comprehensive frameworks, etc).

The skill is opt-in. It won't auto-apply to ordinary code tasks. Invoke a slash command, or say "be brutal" / "brutalism mode".

That's it.
