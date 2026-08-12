---
title: Telegram messages sent as you, not as a bot
layout: hextra-home
---

{{< hextra/hero-badge >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>MIT licensed · Python 3.13 · MTProto</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  Telegram messages sent as you,&nbsp;<br class="hx:sm:block hx:hidden" />not as a bot
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  `tguser` is a CLI that speaks MTProto from your own account,&nbsp;<br class="hx:sm:block hx:hidden" />so an AI agent can write to private chats, groups and channels like a person.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx:mb-6">
{{< hextra/hero-button text="Get Started" link="docs" >}}
</div>

<div class="hx:mt-6"></div>

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git
tguser login                           # one interactive sign-in, done by a human
tguser chat add work -1001234567890    # save the chat under the name "work"
tguser send "Build finished" --to work
```

<div class="hx:mt-12"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="A user account, not a bot"
    subtitle="Bots cannot start conversations, cannot join arbitrary groups, and are visibly bots. `tguser` uses the MTProto protocol with your own account, so messages arrive from you."
  >}}
  {{< hextra/feature-card
    title="Built for AI agents"
    subtitle="Designed from the start for Claude Code, Codex CLI, OpenClaw, Hermes-Agent and the like. The agent runs one plain shell command and the message goes out."
  >}}
  {{< hextra/feature-card
    title="Chat aliases like `git remote`"
    subtitle="Name a chat once and forget the numeric ID: `--to work` instead of `-1001234567890`. Aliases live in a local SQLite database."
  >}}
  {{< hextra/feature-card
    title="Runs from any directory"
    subtitle="After `uv tool install` the `tguser` command is on your PATH with no `uv run` and no project root. An agent's working directory is never known in advance."
  >}}
  {{< hextra/feature-card
    title="Agent Skill in one command"
    subtitle="`npx skills add https://github.com/yerza06/tguser-cli --skills tguser` teaches your agent the whole CLI — following the open Agent Skills spec."
  >}}
  {{< hextra/feature-card
    title="Ten kinds of messages"
    subtitle="Text, documents, photos, videos, audio, voice notes, video notes, stickers and contacts — with albums, captions and stable exit codes 0 / 1 / 130."
  >}}
{{< /hextra/feature-grid >}}

<div class="hx:mt-12"></div>

## How it fits together

A human signs in **once** — `tguser login` is interactive and asks for a phone number, a code and
possibly a 2FA password. After that the session persists in `~/.config/tguser/`, and every later
send runs unattended. The agent never handles your credentials; it only calls `tguser send`.

Everything stays on your machine: the session file, the alias database and the API credentials
live in `~/.config/tguser/`, with `.env` at mode 600. There is no server component.
