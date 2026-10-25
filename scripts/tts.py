#!/usr/bin/env python3
"""Voices the course's own French texts with Microsoft neural voices (edge-tts).

A script is a text file under content/audio/tts/; next to it the mp3 is built:

    content/audio/tts/a-05/dialogue.txt  →  content/audio/tts/a-05/dialogue.mp3

Each line is one utterance. A prefix picks the speaker — French from France,
Quebec, Belgium and Switzerland, as in DELF / DALF recordings:

    A: Denise (France, female)     B: Henri (France, male)
    C: Eloise (France, female)     D: Rémy (France, male)
    E: Sylvie (Québec, female)     F: Antoine (Québec, male)
    G: Charline (Belgique, f.)     H: Fabrice (Suisse, male)

A line without a prefix uses A.
Empty lines and lines starting with "#" are skipped, except the settings:

    # rate: -10%       slower speech (edge-tts --rate)
    # pause: 700       silence between utterances, ms (default 600)

Usage (from the repo root, edge-tts in scripts/.venv):

    scripts/.venv/bin/python scripts/tts.py              # build every stale mp3
    scripts/.venv/bin/python scripts/tts.py --force a-05 # rebuild a module's audio
    scripts/.venv/bin/python scripts/tts.py --yaml content/audio/tts/a-05/dialogue.txt

--yaml prints the audio/audio_source block for exercise.yaml. The license is
"TTS": the text is the course's own, the voice is named in author.
"""
import argparse
import asyncio
import io
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TTS_DIR = ROOT / 'content' / 'audio' / 'tts'
VOICES = {
    'A': 'fr-FR-DeniseNeural',
    'B': 'fr-FR-HenriNeural',
    'C': 'fr-FR-EloiseNeural',
    'D': 'fr-FR-RemyMultilingualNeural',
    'E': 'fr-CA-SylvieNeural',
    'F': 'fr-CA-AntoineNeural',
    'G': 'fr-BE-CharlineNeural',
    'H': 'fr-CH-FabriceNeural',
}
DEFAULT = 'A'
SETTING = re.compile(r'^#\s*(rate|pause)\s*:\s*(\S+)\s*$')
LINE = re.compile(r'^([A-H]):\s*(.+)$')

# One frame of MPEG-2 Layer III silence at 24 kHz / 48 kbit/s, the format
# edge-tts returns (audio-24khz-48kbitrate-mono-mp3): 144 bytes, 24 ms.
SILENT_FRAME = bytes([0xFF, 0xF3, 0x64, 0xC4]) + bytes(140)
FRAME_MS = 24


def parse(path: pathlib.Path):
    rate, pause, lines = '+0%', 600, []
    for raw in path.read_text(encoding='utf-8').splitlines():
        s = raw.strip()
        if not s:
            continue
        m = SETTING.match(s)
        if m:
            if m[1] == 'rate':
                rate = m[2]
            else:
                pause = int(m[2])
            continue
        if s.startswith('#'):
            continue
        m = LINE.match(s)
        voice, text = (m[1], m[2]) if m else (DEFAULT, s)
        lines.append((VOICES[voice], text))
    return rate, pause, lines


async def speak(voice: str, text: str, rate: str) -> bytes:
    import edge_tts

    buf = io.BytesIO()
    async for chunk in edge_tts.Communicate(text, voice, rate=rate).stream():
        if chunk['type'] == 'audio':
            buf.write(chunk['data'])
    return buf.getvalue()


async def build(path: pathlib.Path):
    rate, pause, lines = parse(path)
    if not lines:
        raise SystemExit(f'{path}: no text')
    gap = SILENT_FRAME * max(1, pause // FRAME_MS)
    parts = []
    for i, (voice, text) in enumerate(lines):
        if i:
            parts.append(gap)
        parts.append(await speak(voice, text, rate))
    path.with_suffix('.mp3').write_bytes(b''.join(parts))


def stale(path: pathlib.Path) -> bool:
    mp3 = path.with_suffix('.mp3')
    return not mp3.exists() or mp3.stat().st_mtime < path.stat().st_mtime


def yaml_block(path: pathlib.Path) -> str:
    _, _, lines = parse(path)
    voices = ', '.join(sorted({v for v, _ in lines}))
    rel = path.with_suffix('.mp3').relative_to(ROOT / 'content').as_posix()
    return (
        f'audio: {rel}\n'
        f'audio_source: {{title: "Enregistrement du cours (edge-tts)", url: "https://github.com/rany2/edge-tts", '
        f'author: "{voices}", license: "TTS"}}'
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('only', nargs='*', help='module folders or .txt files to build (default: all)')
    ap.add_argument('--force', action='store_true', help='rebuild even if the mp3 is newer than the text')
    ap.add_argument('--yaml', action='store_true', help='print the exercise.yaml block instead of building')
    a = ap.parse_args()

    scripts = sorted(TTS_DIR.rglob('*.txt'))
    if a.only:
        want = [pathlib.Path(o).resolve() if o.endswith('.txt') else TTS_DIR / o for o in a.only]
        scripts = [s for s in scripts if any(s == w or w in s.parents for w in want)]
    if a.yaml:
        for s in scripts:
            print(f'# {s.relative_to(ROOT)}\n{yaml_block(s)}\n')
        return
    todo = [s for s in scripts if a.force or stale(s)]
    for s in todo:
        print('voicing', s.relative_to(ROOT), file=sys.stderr)
        asyncio.run(build(s))
    print(f'{len(todo)} built, {len(scripts) - len(todo)} up to date', file=sys.stderr)


if __name__ == '__main__':
    main()
