# gta6-ig-news

Дневният Instagram карусел „GTA 6 новини“ на GTA Hub Варна (@vr_varna).

- `build.py` — генераторът на слайдове 1080×1350 (Pillow).
- `AGENT.md` — пълната инструкция за облачния агент, който пуска поста всеки ден.
- `NASOKI.md` — насоките на собственика. Агентът ги чете всеки ден.
- `POSTED.md` — какво е публикувано.
- `issues/<дата>/` — `issue.json` (текстовете) и `out/` (готовите слайдове; оттук Metricool ги взима по публичен линк).
- `assets/` — шрифт Oswald (SIL OFL, виж `assets/fonts/OFL.txt`), логото на GTA Hub, снимки от играта (© Rockstar Games) и от модела на залата.

Локално: `python3 build.py issues/2026-11-03/issue.json /tmp/out`.
