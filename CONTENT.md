# Как писать контент Francais

Курс ведёт двоих русскоязычных взрослых по трём ступеням: **A1 → B1**, **B1 → B2** (DELF B2), **B2 → C1** (DALF C1). Теорию пишем по-русски, примеры, упражнения, тексты и аудио — по-французски. Курс публикуется на GitHub Pages.

После правок контента запусти `npm run validate`: он должен закончиться строкой `ok: … modules, … lessons, …`. При `npm run dev` курс перечитывается с диска на каждое сохранение, ошибка показывается прямо в браузере.

## Учебники задают структуру

| Ступень | Модули | Структура по учебнику | `content/` |
|---|---|---|---|
| A1 → B1 | `a-01` … `a-29`, повторения `a-16r`, `a-22r`, `a-29r` | Попова, Казакова, Ковальчук «Французский язык», учебник для I курса: 16 уроков фонетического курса, 13 уроков основного, Révision A/B/C | `book-pkk.yaml` |
| B1 → B2 | `b-00`, `b-01` … `b-08`, `b-09` | Cosmopolite 4: досье = модуль (4 leçons, Focus langue, Stratégies, DELF B2) | `book-cosmo.yaml` |
| B2 → C1 | `c-00` … `c-16` | Попова, Казакова «Грамматика французского языка. Практический курс» — по главам | `book-grammar.yaml` |

Грамматика Поповой–Казаковой — ещё и справочник для всех ступеней: грамматические уроки ссылаются на её параграфы.

**Из учебников берём структуру, порядок тем, набор правил и типы упражнений. Упражнения, примеры и тексты пишем свои.** Ни одного предложения, текста или упражнения из книги в курс не переносим: курс публичный. Упражнение «по образцу» — того же типа и на то же правило (книга: «поставьте глагол в passé composé» → наше `gap` на passé composé со своими предложениями). Тексты уроков основного курса — свои, на ту же тему, что текст книги («Le 14 juillet» → свой текст про 14 июля).

Модули сортируются по имени каталога: `a-` идёт раньше `b-` и `c-`. ID упражнений уникальны на весь курс: префикс модуля + суть (`a05-possessifs-gap`, `a17-texte`, `b02-passe-simple-choice`).

## Ссылки на учебник

`content/book-*.yaml` — **только оглавление**: номер, название раздела, печатная страница. Модуль указывает свою книгу, урок — разделы:

```yaml
# module.yaml
title: "Урок 5. Гласный [œ]"
level: b1
book: book-pkk
```

```yaml
# lesson.md (frontmatter)
book: [500, 501, 503]              # разделы книги модуля
also: {book-grammar: [1201]}       # разделы других книг
```

Нумерация в `book-pkk.yaml`: `n = урок·100 + §` (на ступени A1 используем только номера §; `0` — фонетика или текст урока, `50` — Commentaires, `90` — Dialogues — для полноты оглавления), `3001–3003` — Révision A–C. В `book-cosmo.yaml`: `n = досье·100 + k` (`0` — ouverture, `1–4` — leçons, `5–6` — Focus langue, `7` — Stratégies, `8` — Projets, `9` — DELF, `10` — S'exercer). В `book-grammar.yaml` (справочник): `n = глава·100 + пункт` (`1` Le nom, `2` L'article, `3` L'adjectif, `4` Le pronom, `5` L'adverbe, `6` Négations, `7` Le verbe, `8` Discours indirect, `9` Question indirecte, `10` Mise en relief, `11` Conjugaison); нумерация упражнений в книге начинается заново в каждом разделе, поэтому в `ex` пиши страницу: `ex: "с. 214, упр. 1–4"`. Грамматические уроки всех ступеней ссылаются на справочник через `also: {book-grammar: […]}`. На странице урока под теорией выводится блок «Учебник» со страницами; поле `ex` у раздела (`ex: "упр. 1–6"`) показывает, какие упражнения книги сделать после практики в курсе.

## Ступень A1 → B1: модуль = урок учебника I курса

Из каждого урока учебника берём грамматику (пункты ГРАММАТИКА / GRAMMAIRE) — уроки `01-…`–`06-…`. Тексты, диалоги и диктанты книги не переносим: уроки чтения, письма и аудирования (`07-lecture`, `08-ecriture`, `09-ecoute`, см. «Чтение, письмо, аудирование») — свои.

`module.yaml`: `title: "Урок 5. Притяжательные, артикль, отрицание"` — номер урока книги + его грамматические темы, `level: b1`, `book: book-pkk`, `summary` — что умеешь после урока, `topics` — пункты грамматики урока, `sources` — проверенные ссылки по этим темам. Каталог — `a-NN-<тема>` (`a-01-article`, `a-17-question-nombres`).

```
a-05-possessifs-negation/
  01-grammaire/   пункты грамматики урока (book: […] на эти §§, also: {book-grammar: […]})
  02-grammaire/   если пунктов много (больше 3–4) — делим на два урока по смыслу
```

- Теория 400–1000 слов: правило своими словами, отличие от русского, таблицы, «Типичная ошибка русскоговорящих», 1–3 блока ` ```quiz `.
- 2–3 упражнения по 8–12 пунктов на урок: `gap`, `choice`, `order`, `error`, `transform`, перевод с русского (`gap` без `___`: в `q` русская фраза, в `answers` все верные переводы). На модуль — хотя бы один `order` или `error`. Лексика — только из уже пройденных уроков и самых частотных слов.
- Замечания о произношении — только когда они нужны для грамматики (*cet* = [sɛt], немое *-d* в *il répond*).
- Карточки: 6–12 на урок, только на грамматику.

**Révision A, B, C** (`a-16r-revision-a`, `a-22r-revision-b`, `a-29r-revision-c` — так они сортируются сразу после уроков 16, 22 и 29; `book: [3001]` / `[3002]` / `[3003]`): один урок `kind: test`, `choice` на 30–40 пунктов по грамматике пройденных уроков, `pass: 1`, у каждого пункта `topic: "<id модуля>"` — результаты по темам видны на странице «Прогресс».

## lesson.md

```markdown
---
title: "Passé composé или imparfait"
kind: grammar          # grammar (по умолчанию) | reading | writing | listening | test
sources:
  - {title: "...", url: "..."}
---
Теория по-русски...

## Практика

```exercise m01-pc-imparfait-gap
```
```

Теория грамматического урока — 600–1200 слов:

- Начни с того, **зачем** это нужно и чем это отличается от русского (в русском нет артиклей, одно прошедшее, нет согласования причастий — это и есть главные источники ошибок).
- Правило: форма → значение → маркеры. Таблицы спряжений там, где они нужны.
- Примеры — живые французские предложения, перевод — где помогает.
- Блок `> ` — для «Типичная ошибка русскоговорящих» и заметок «Уровень B2/C1».
- 1–2 блока ` ```quiz ` (YAML: `q`, `options`, `answer` с отсчётом от 0, `explain`).
- Заголовки — `##` и `###`.
- Жирным выделяй изменяемую часть: `j'**ai mangé**`, `qu'il **vienne**`. Рендерер понимает и `l**'homme**`, и `fell**;**`, но проще выделять слово целиком.

## exercise.yaml

Общие поля: `title`, `type`, `intro`, `hints`, `items`, `pass` (по умолчанию 80). У каждого пункта обязательный `explain` по-русски: почему ответ именно такой.

| type | Поля | Что видит ученик |
|---|---|---|
| `gap` | `q` с одним `___`, `answers` | поле на месте `___` |
| `choice` | `q`, `options`, `answer` | радиокнопки |
| `transform` | `q`, `key`, `stem` с одним `___`, `answers` | перефразирование с ключевым словом |
| `error` | `q` с одной ошибкой, `answers` — исправленное предложение | исправить предложение |
| `order` | `q` — контекст, `answers[0]` — предложение | собрать из перемешанных слов |
| `reading` | `text`; пункты `choice` или с `answers` | текст и вопросы |
| `writing` | `prompt`, `words`, `target_grammar`, `checklist`, `model_answer` | редактор, самопроверка, промпт для Claude |
| `listening` | `audio` **или** `link`, `audio_source`, `transcript`; пункты как у `reading` | плеер или кнопка «Открыть запись», вопросы, после проверки — расшифровка |
| `dictation` | у каждого пункта `audio`, `audio_source` и либо `answers` (что слышно, целиком), либо `options` + `answer` (выбор: какой звук, какое слово); `explain` — перевод и разбор; `q` необязателен для ввода | плеер на каждый пункт, поле ввода или варианты |

### Ответы

Проверка прощает регистр, лишние и неразрывные пробелы (`Tu viens ?` = `Tu viens?`), запятые, финальную пунктуацию, кавычки «», `œ` = `oe`. **Акценты проверяются строго**: `ecole` вместо `école` — ошибка, но ученик увидит пометку «ошибка только в акцентах». Апострофы ’ и ' равны. Дефисы обязательны (`est-ce que`, `peut-être`).

**Перечисляй все грамматически верные варианты** (`["est allée", "était allée"]` — если оба уместны). Ученик не должен получить «неверно» за правильный ответ.

- Местоимения с элизией пиши как в норме: `qu'il`, `l'a`, `s'est`. Варианты вроде `que il` не принимаем.
- Женский род и множественное число причастий — отдельные ответы, если контекст их не определяет.
- `error`: ровно одна ошибка (часто — согласование, выбор вспомогательного, наклонение, предлог). Ответ — всё предложение.

### YAML

Строки с `:`, `?`, `#`, `'`, `"`, `[`, `]`, `{` и строки, начинающиеся с `*` или `-`, бери в двойные кавычки (во французском апострофов много — двойные кавычки по умолчанию). Неизвестные поля — ошибка загрузки.

```yaml
title: "Passé composé или imparfait"
type: gap
intro: "Поставь глагол в passé composé или imparfait."
items:
  - q: "Quand j'étais petit, je ___ (passer) mes étés chez ma grand-mère."
    answers: ["passais"]
    explain: "Повторяющееся действие в прошлом, фон (**quand j'étais petit**) → imparfait."
```

## Аудирование

### Локальное аудио (файлы в `content/audio/`)

Хранить в курсе можно **только** записи под CC0, CC BY, CC BY-SA, в общественном достоянии (PD) или свою озвучку (`TTS`). Загрузчик проверяет `audio_source.license` и наличие файла; для CC BY / CC BY-SA и `TTS` обязателен `author` — атрибуция (для TTS — голос) выводится под плеером.

```yaml
audio_source: {title: "Tatoeba #14314", url: "https://tatoeba.org/fr/sentences/show/14314", author: "vlecomte", license: "CC BY-SA 4.0"}
```

Источники:

- **Своя озвучка** — `scripts/tts.py`: сценарий `content/audio/tts/<id модуля: a-05, b-03>/<имя>.txt`, рядом собирается mp3 нейронными голосами Microsoft (edge-tts). Строка — реплика, префикс — диктор: `A:` Denise, `B:` Henri, `C:` Eloise, `D:` Rémy (Франция), `E:` Sylvie, `F:` Antoine (Квебек), `G:` Charline (Бельгия), `H:` Fabrice (Швейцария); настройки `# rate: -15%` (для A1), `# pause: 700`. `scripts/.venv/bin/python scripts/tts.py a-05` собирает устаревшие mp3. `audio_source`: `{title: "Enregistrement du cours (edge-tts)", url: "https://github.com/rany2/edge-tts", author: "<голоса>", license: "TTS"}`; `transcript` — текст сценария.
- **Tatoeba** — короткие фразы с русским переводом. `scripts/tatoeba.py pool --min 3 --max 20` строит `scripts/pool.tsv` (только CC BY / CC BY-SA / CC0; в основном короткие фразы — для A1–A2, на B2–C1 диктант строим на своей озвучке), `scripts/tatoeba.py fetch <id> …` скачивает mp3 и печатает готовые пункты для `dictation`. Перевод в `explain` дополни разбором грамматики.
- **Lingua Libre** — слова, произнесённые носителями (лицензия у каждого диктора своя: CC0 / CC BY / CC BY-SA). `scripts/lingualibre.py fetch <слово> …` скачивает mp3 в `content/audio/lingualibre/` и печатает готовый пункт с атрибуцией.
- **Mozilla Common Voice FR** (CC0) — добор фраз; уровень размечаем сами.
- **Français interactif** (UT Austin, CC BY 4.0) — интервью носителей: https://www.laits.utexas.edu/fi/ — для `listening` A2–B1.
- **LibriVox** (PD) + тексты Project Gutenberg — отрывки B2–C1 (Мопассан, Верн, Доде); длинные файлы пережимай в mono 48–64 kbps.

### Внешние записи (`link`)

RFI «Journal en français facile», TV5Monde, образцы DELF/DALF — под копирайтом: аудио **не копируем**, даём `link` на страницу записи, вопросы и `transcript` пишем свои (пересказ, не копия расшифровки источника). Загрузчик пускает только https-ссылки на известные сайты (`LINK_HOSTS` в `build/content.ts`).

## Чтение, письмо, аудирование

В каждом тематическом модуле после грамматики — три урока с одинаковыми именами: **`07-lecture`** (`kind: reading`), **`08-ecriture`** (`kind: writing`), **`09-ecoute`** (`kind: listening`). ID: `a05-lecture`, `a05-ecriture`, `a05-ecoute`, `a05-ecoute-<суть>`, `a05-dictee`. Тексты и записи свои, насыщены грамматикой модуля и опираются только на пройденное. Образцы — `a-05-possessifs-negation` (A1) и `b-03-comparaison-relatifs` (B2).

| Модули | Уровень | Чтение | Письмо (`words`) | Аудирование |
|---|---|---|---|---|
| `a-01`…`a-16` | A1 | 60–150 слов, 5–6 вопросов | [30, 60] | диалог 0:40–1:20, `rate: -15%`; диктант 8–10 (TTS + Tatoeba, пункты-выбор на звуки) |
| `a-17`…`a-29` | A2 → B1 | 150–300 слов, 6–8 вопросов | [60, 120] | 1:30–2:30, два `listening`, диктант 8–10 |
| `b-01`…`b-08` | B2 | 400–550 слов, 8–10 вопросов (vrai / faux / on ne sait pas, позиция автора) | [200, 280] | интервью 2–3:30 + короткий документ (один раз), диктант 8 |
| `c-01`…`c-15` | C1 | 500–700 слов, 8–10 вопросов | [220, 300] | 3–4 мин + короткий документ, диктант 8 |

- `07-lecture`: в теории — стратегия DELF нужного уровня и таблица 8–12 слов из текста.
- `08-ecriture`: устройство жанра, план, полезные фразы, «Типичная ошибка русскоговорящих»; чек-лист 5–7 пунктов, образец в пределах `words`. Запрос для Claude — по сетке production écrite уровня.
- `09-ecoute`: теория 200–400 слов — как слушать (DELF с 2025 года: compréhension de l'oral — вопросы с выбором; короткие документы звучат один раз); `listening` с `transcript` и `dictation`.
- Карточки: 4–6 на модуль из лексики текстов, в конец `cards/<модуль>.yaml`.
- Итоговые `b-09-final`, `c-16-final`: урок `ecoute` (`kind: test`) — compréhension de l'oral, `choice` с `topic` по модулям ступени.

## Ступень B1 → B2: модуль = досье Cosmopolite 4

Как и на A1 → B1, из досье берём грамматику — пункты «Grammaire» его четырёх leçons и Focus langue. Тексты, проекты и задания DELF книги не переносим; чтение, письмо и аудирование — свои уроки `07-lecture`, `08-ecriture`, `09-ecoute`.

| Модуль | Досье | Грамматика по Cosmopolite 4 |
|---|---|---|
| `b-00-diagnostic` | — | входной тест по темам `b-01` … `b-08` |
| `b-01-…` | 1. Modes et tendances | participe présent и adjectif verbal; participe composé (antériorité); futur antérieur; opposition и concession; conjonctions de temps |
| `b-02-…` | 2. Histoire et mémoire | temps du passé pour raconter avec précision (passé composé, imparfait, plus-que-parfait); hypothèses sur le passé; passé simple; prépositions de lieu |
| `b-03-…` | 3. Culture commune | comparatifs и superlatifs; pronoms relatifs; mise en relief; pronoms y и en |
| `b-04-…` | 4. Nouvelles technologies | question par inversion; expression de la durée; cause и conséquence |
| `b-05-…` | 5. Questions de société | voix passive; subjonctif для prise de position и alternative; nuancer une comparaison |
| `b-06-…` | 6. Faire évoluer la société | exprimer la condition; conditionnel présent (atténuation, hypothèse) и passé (reproche, regret); adjectifs и pronoms indéfinis; accord du participe passé avec le COD |
| `b-07-…` | 7. Au travail | discours indirect (présent и passé); double pronominalisation |
| `b-08-…` | 8. Modèles éducatifs | relatives au subjonctif (souhait, but); subjonctif dans l'opinion и la probabilité; négation ne… ni… ni… |
| `b-09-final` | — | итоговый тест в формате «грамматика DELF B2» по темам `b-01` … `b-08` |

`module.yaml`: `title: "Досье 2. Времена прошедшего, passé simple"`, `level: b2`, `book: book-cosmo`, `summary`, `topics`, `sources`. Уроки — `01-grammaire`, `02-grammaire`, … по одной-двум темам досье, обычно 3–5 уроков на модуль. В уроке `book: [<досье·100 + leçon>, <досье·100 + 5 или 6>, <досье·100 + 10>]` (leçon, Focus langue, S'exercer) и `also: {book-grammar: […]}`.

- Теория 600–1200 слов, уровень B1 → B2: тонкости и противопоставления (imparfait / passé composé / plus-que-parfait в одном рассказе, subjonctif / indicatif после глаголов мнения), «Типичная ошибка русскоговорящих», 1–3 ` ```quiz `.
- 2–3 упражнения по 10–12 пунктов: `gap`, `choice`, `transform`, `error`, `order`, перевод с русского. На модуль — хотя бы один `transform` и один `error`. Лексика — обычная B1–B2, без редких слов.
- Карточки: 8–12 на урок.
- Тесты `b-00-diagnostic` (4 вопроса на модуль) и `b-09-final` (5 вопросов, новые и потруднее): `choice`, `pass: 1`, у каждого `topic: "<id модуля>"`.

Cosmopolite 4 — скан без текста: страницы Focus langue и S'exercer читаем рендером в PNG (печатная страница = индекс PDF + 1, досье n начинается с с. 10 + 18·(n−1), Focus langue — с. начало + 6 и + 12, S'exercer — `book-cosmo.yaml`, юниты `…10`).

## Ступень B2 → C1: модуль = глава грамматики Поповой–Казаковой

Структура — главы и параграфы «Грамматики французского языка. Практический курс» (`book-grammar.yaml`). Глава Conjugaison (спряжения) — справочник, отдельных модулей нет.

| Модуль | Главы и пункты (`book-grammar.yaml`) |
|---|---|
| `c-00-diagnostic` | входной тест по темам `c-01` … `c-15` |
| `c-01-nom` | Le nom: 101–103 |
| `c-02-article` | L'article: 201–204 |
| `c-03-adjectif` | L'adjectif: 301–308 |
| `c-04-pronoms-personnels` | 401–407 (conjoints, le neutre, toniques, soi, y, en) |
| `c-05-relatifs-demonstratifs` | 408–411 (relatifs, démonstratifs, possessifs, interrogatifs) |
| `c-06-indefinis` | 412–414 (indéfinis, même, tout) |
| `c-07-adverbe-negation` | 501–503, 601–602 |
| `c-08-voix-pronominaux` | 701–703 (transitifs, forme passive, pronominaux) |
| `c-09-futurs` | 704–710 (présent, futurs, futur dans le passé, futur antérieur dans le passé) |
| `c-10-passes` | 711–719 (passé simple, imparfait, plus-que-parfait, passé immédiat, plus-que-parfait immédiat, passé antérieur) |
| `c-11-concordance-imperatif` | 720–721 |
| `c-12-conditionnel` | 722–725 |
| `c-13-subjonctif` | 726–734 |
| `c-14-formes-non-personnelles` | 735–742 (participes, adjectif verbal, gérondif, proposition participe, proposition infinitive, constructions causatives) |
| `c-15-discours-relief` | 801, 901, 1001 (discours indirect, question indirecte, mise en relief) |
| `c-16-final` | итоговый тест по темам `c-01` … `c-15` |

`module.yaml`: `title: "Глава. Субъюнктив"` (или по теме), `level: c1`, `book: book-grammar`, `summary`, `topics`, `sources`. Уроки — по параграфам главы, 3–6 на модуль, с `book: [пункты book-grammar]` и `ex: ` не пишем (ex — поле оглавления).

- Уровень C1: тонкости, исключения, стилистика и регистр (soutenu), литературные времена — на узнавание и понимание, «Типичная ошибка русскоговорящих», 1–3 ` ```quiz `. Теория 700–1300 слов.
- 2–3 упражнения по 10–12 пунктов: `gap`, `choice` (все варианты грамматичны, верен один по смыслу или норме), `transform`, `error` с тонкой ошибкой, `order`, перевод с русского. На модуль — хотя бы один `transform` и один `error`.
- Карточки: 8–12 на урок.
- Тесты `c-00-diagnostic` (3 вопроса на модуль) и `c-16-final` (4 новых, потруднее): `choice`, `pass: 1`, `topic: "<id модуля>"`.

Книга — скан разворотами без текста, в нём нет с. 156–157, 210–211, 268–269, 316–317; соответствие страниц и PDF — в `scratchpad/books/grammar_pk.md` (или считать по формуле: правая страница разворота R = 2i+3 для индекса i 1–76, затем со сдвигами +2 после каждой пропущенной пары).

## Источники

Только проверенные ссылки (в `sources:` урока и модуля):

- Tex's French Grammar (UT Austin, CC BY): `https://www.laits.utexas.edu/tex/` — страницы тем `https://www.laits.utexas.edu/tex/gr/...`.
- Français interactif (UT Austin, CC BY 4.0): `https://www.laits.utexas.edu/fi/`.
- Le Point du FLE: `https://www.lepointdufle.net/`.
- Wikibooks «Français»: `https://fr.wikibooks.org/wiki/Fran%C3%A7ais`.
- Bonjour de France: `https://www.bonjourdefrance.com/`; Français facile: `https://www.francaisfacile.com/`.
- Podcast Français Facile: `https://www.podcastfrancaisfacile.com/`.
- DELF / DALF: `https://www.france-education-international.fr/diplome/delf-tout-public`, `https://www.france-education-international.fr/diplome/dalf`.
- Lawless French `https://www.lawlessfrench.com/grammar/`, TV5Monde `https://apprendre.tv5monde.com/fr`, RFI `https://francaisfacile.rfi.fr/fr/` — блокируют запросы скриптом (403), открываются в браузере.

Учебники в `sources:` не пишем — для них блок «Учебник» (`book:` / `also:`).

## Авторское право

Курс публичный. Все тексты, упражнения, примеры и расшифровки пишем сами; из учебников и с сайтов не копируем — только ссылаемся (разделы и страницы через `book:` / `also:`). Чужое аудио храним только под открытыми лицензиями и с атрибуцией.
