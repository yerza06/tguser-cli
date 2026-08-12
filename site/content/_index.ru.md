---
title: Сообщения в Telegram от вашего имени, а не от бота
layout: hextra-home
---

{{< hextra/hero-badge >}}
  <div class="hx:w-2 hx:h-2 hx:rounded-full hx:bg-primary-400"></div>
  <span>Лицензия MIT · Python 3.13 · MTProto</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}

<div class="hx:mt-6 hx:mb-6">
{{< hextra/hero-headline >}}
  Сообщения в Telegram&nbsp;<br class="hx:sm:block hx:hidden" />от вашего имени, а не от бота
{{< /hextra/hero-headline >}}
</div>

<div class="hx:mb-12">
{{< hextra/hero-subtitle >}}
  `tguser` — CLI, говорящий по MTProto от вашего аккаунта,&nbsp;<br class="hx:sm:block hx:hidden" />чтобы ИИ-агент писал в личные чаты, группы и каналы как человек.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx:mb-6">
{{< hextra/hero-button text="Начать" link="docs" >}}
</div>

<div class="hx:mt-6"></div>

```bash
uv tool install git+https://github.com/yerza06/tguser-cli.git
tguser login                           # один интерактивный вход, его делает человек
tguser chat add work -1001234567890    # сохранить чат под именем «work»
tguser send "Сборка готова" --to work
```

<div class="hx:mt-12"></div>

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Пользователь, а не бот"
    subtitle="Бот не может начать переписку первым, не может вступить в произвольную группу и всегда видно, что он бот. `tguser` работает по MTProto от вашего аккаунта — сообщения приходят от вас."
  >}}
  {{< hextra/feature-card
    title="Создан для ИИ-агентов"
    subtitle="Изначально рассчитан на Claude Code, Codex CLI, OpenClaw, Hermes-Agent и подобных. Агент выполняет одну обычную команду оболочки — и сообщение уходит."
  >}}
  {{< hextra/feature-card
    title="Алиасы чатов как `git remote`"
    subtitle="Назовите чат один раз и забудьте про числовой ID: `--to work` вместо `-1001234567890`. Алиасы хранятся в локальной базе SQLite."
  >}}
  {{< hextra/feature-card
    title="Работает из любой директории"
    subtitle="После `uv tool install` команда `tguser` доступна в PATH — без `uv run` и без корня проекта. Рабочая директория агента заранее неизвестна."
  >}}
  {{< hextra/feature-card
    title="Skill для агента одной командой"
    subtitle="`npx skills add https://github.com/yerza06/tguser-cli --skills tguser` обучает агента всему CLI — по открытой спецификации Agent Skills."
  >}}
  {{< hextra/feature-card
    title="Десять типов сообщений"
    subtitle="Текст, документы, фото, видео, аудио, голосовые, кружки, стикеры и контакты — с альбомами, подписями и стабильными кодами выхода 0 / 1 / 130."
  >}}
{{< /hextra/feature-grid >}}

<div class="hx:mt-12"></div>

## Как это устроено

Человек входит в аккаунт **один раз** — `tguser login` интерактивен и спрашивает номер телефона,
код и, если включена, пароль двухфакторной аутентификации. Дальше сессия сохраняется в
`~/.config/tguser/`, и каждая последующая отправка проходит без участия человека. Агент не работает
с вашими учётными данными — он лишь вызывает `tguser send`.

Всё остаётся на вашей машине: файл сессии, база алиасов и учётные данные API лежат в
`~/.config/tguser/`, причём `.env` — с правами 600. Серверной части нет.
