"""
generate_transcript_assets.py

Usage:
  python generate_transcript_assets.py path/to/example.json [--audio path/to/example.m4a] [--outdir path/to/output/dir]

Outputs (same folder by default):
  - example.srt
  - example.html
  - example.md

HTML includes embedded segments data and highlights current playing segment.
"""

import json
import os
import sys
import argparse
from datetime import timedelta
import html as html_module
import textwrap

def fmt_srt(t):
    td = timedelta(seconds=float(t))
    total = td.total_seconds()
    h = int(total // 3600)
    m = int((total % 3600) // 60)
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.',',')

def fmt_hhmmss_ms(t):
    td = timedelta(seconds=float(t))
    total = td.total_seconds()
    h = int(total // 3600)
    m = int((total % 3600) // 60)
    s = total % 60
    # use dot (.) for readable timestamp in MD/HTML
    return f"{h:02d}:{m:02d}:{s:06.3f}"

def find_audio_candidate(basepath):
    # Try common audio extensions
    exts = ['.m4a','.mp3','.wav','.ogg','.opus','.flac','.aac','.mp4']
    for e in exts:
        p = basepath + e
        if os.path.exists(p):
            return os.path.basename(p)
    return None

def make_srt(segments, out_srt_path):
    with open(out_srt_path, 'w', encoding='utf-8') as srt:
        for i, seg in enumerate(segments, start=1):
            start = fmt_srt(seg['start'])
            end = fmt_srt(seg['end'])
            text = seg.get('text','').strip()
            srt.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    print("Wrote SRT:", out_srt_path)

def make_html(segments, audio_file, out_html_path, title):
    segments_json = json.dumps(segments, ensure_ascii=False)

    html_content = textwrap.dedent(f"""\
    <!doctype html>
    <html lang="ko">
    <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <style>
      body {{ font-family: sans-serif; margin: 12px; }}
      .segment {{ padding: 6px; cursor: pointer; }}
      .active {{ background: #fff7c2; }}
      .transcript {{ height: 350px; overflow-y: auto; border:1px solid #eee; }}
    </style>
    </head>
    <body>

    <audio id="player" controls style="width:100%;">
      <source src="{audio_file}">
    </audio>

    <div class="transcript" id="transcript"></div>

    <script>
    const segments = {segments_json};
    const player = document.getElementById('player');
    const container = document.getElementById('transcript');

    function render() {{
        segments.forEach(s => {{
            const div = document.createElement('div');
            div.className = 'segment';
            div.dataset.start = s.start;
            div.dataset.end = s.end;
            div.textContent = '[' + s.start.toFixed(2) + '] ' + s.text;
            div.onclick = () => {{
                player.currentTime = s.start;
                player.play();
            }};
            container.appendChild(div);
        }});
    }}

    function highlight() {{
        const t = player.currentTime;
        document.querySelectorAll('.segment').forEach(el => {{
            const start = parseFloat(el.dataset.start);
            const end = parseFloat(el.dataset.end);
            el.classList.toggle('active', t >= start && t < end);
        }});
    }}

    player.addEventListener('timeupdate', highlight);

    render();
    </script>

    </body>
    </html>
    """)

    with open(out_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def make_md(out_md_path, html_filename, audio_filename, title):
    # Use iframe embed and also link fallback
    md = f"# {title}\n\n"
    md += ("> 이 페이지는 HTML 플레이어를 임베드합니다. Obsidian에서 정상 작동하려면\n"
           "> - Vault 내부 경로로 파일을 두거나\n"
           "> - 'HTML Viewer' 같은 플러그인을 사용하거나\n"
           "> - 미리보기를 통해 iframe을 허용해야 할 수 있습니다.\n\n")
    md += f"**Audio:** `{audio_filename}`  \n\n"
    md += f"<iframe src=\"{html_filename}\" width=\"100%\" height=\"520px\"></iframe>\n\n"
    md += f"또는 직접 열기: `![[{html_filename}]]` (플러그인에 따라 동작)\n"
    with open(out_md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print("Wrote MD:", out_md_path)

def main():
    p = argparse.ArgumentParser(description="Generate SRT, HTML (with highlight), and MD from Whisper JSON transcript.")
    p.add_argument('json', help='path to whisper json file')
    p.add_argument('--audio', '-a', help='audio filename or path to reference in HTML (if omitted, script will try same-name audio in same folder)')
    p.add_argument('--outdir', help='output directory (default: same as json folder)', default=None)
    args = p.parse_args()

    json_path = args.json
    if not os.path.exists(json_path):
        print("JSON file not found:", json_path)
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    segments = data.get('segments')
    if not segments:
        print("No 'segments' found in JSON. Exiting.")
        sys.exit(1)

    base = os.path.splitext(os.path.basename(json_path))[0]
    folder = os.path.dirname(os.path.abspath(json_path))
    outdir = args.outdir if args.outdir else folder
    os.makedirs(outdir, exist_ok=True)

    # determine audio file to reference in HTML
    if args.audio:
        audio_ref = args.audio
    else:
        candidate = find_audio_candidate(os.path.join(folder, base))
        audio_ref = candidate if candidate else ''

    srt_path = os.path.join(outdir, base + ".srt")
    html_path = os.path.join(outdir, base + ".html")
    md_path = os.path.join(outdir, base + ".md")

    make_srt(segments, srt_path)
    make_html(segments, audio_ref, html_path, title=base)
    make_md(md_path, os.path.basename(html_path), os.path.basename(audio_ref) if audio_ref else "(audio not linked)", title=base)

    print("\nDone. Files generated:")
    print(" -", srt_path)
    print(" -", html_path)
    print(" -", md_path)
    print("\nUsage tips:")
    print(" - Put the generated HTML + audio file in same folder in your vault, then embed the HTML in your note (iframe) or open HTML directly in browser.")
    print(" - If audio file path is non-local or different place, use --audio to set the src used in HTML, e.g.:")
    print("    python generate_transcript_assets.py example.json --audio ../audio/example.m4a")
    print(" - Obsidian may require community plugin to render local HTML; recommended: 'HTML Viewer' or use iframe in preview mode.")

if __name__ == '__main__':
    main()