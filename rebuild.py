#!/usr/bin/env python3
"""
Rebuild the EQ Legends item reference as a screen HTML page from the markdown source.

    python3 rebuild.py eqlegends-recommended-items.md

Outputs eqlegends-recommended-items.html next to the source file.

Standard library only — no dependencies to install.
Editing rule: keep the table columns as Item | Description | How to Obtain,
and keep `## ` section headings — the layout keys off both.
"""

import html as ihtml
import pathlib
import re
import sys

# --------------------------------------------------------------------------
# shared markdown helpers
# --------------------------------------------------------------------------


def inline(t):
    t = ihtml.escape(t, quote=False)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t


def split_row(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def parse(src):
    """Markdown -> list of (kind, payload) blocks."""
    lines = src.split('\n')
    blocks = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('# ') and not ln.startswith('##'):
            blocks.append(('h1', ln[2:].strip())); i += 1
        elif ln.startswith('### '):
            blocks.append(('h3', ln[4:].strip())); i += 1
        elif ln.startswith('## '):
            blocks.append(('h2', ln[3:].strip())); i += 1
        elif ln.startswith('---'):
            blocks.append(('hr', None)); i += 1
        elif ln.startswith('|'):
            head = split_row(ln)
            i += 2  # skip the |---|---| separator
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(split_row(lines[i])); i += 1
            blocks.append(('table', (head, rows)))
        elif ln.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append(lines[i][2:].strip()); i += 1
            blocks.append(('ul', items))
        elif ln.strip() == '':
            i += 1
        else:
            para = [ln.strip()]; i += 1
            while (i < len(lines) and lines[i].strip()
                   and not re.match(r'^(#|\||-{3}|- )', lines[i])):
                para.append(lines[i].strip()); i += 1
            blocks.append(('p', ' '.join(para)))
    return blocks


# --------------------------------------------------------------------------
# screen HTML
# --------------------------------------------------------------------------

SCREEN_CSS = r"""
:root{--bg:#101319;--panel:#1a1f29;--panel-2:#212734;--edge:#333c4e;--edge-hi:#4a566d;
--link:#7fd6dc;--gold:#d9ae5a;--text:#c7ccd6;--dim:#818a9c;
--shadow:0 1px 0 rgba(255,255,255,.05),0 10px 30px rgba(0,0,0,.45)}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:112px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{margin:0;background:var(--bg);color:var(--text);
font-family:Spectral,"Iowan Old Style",Palatino,Georgia,serif;font-size:16px;line-height:1.6;
background-image:radial-gradient(1200px 500px at 50% -10%,rgba(127,214,220,.06),transparent 70%),
repeating-linear-gradient(0deg,rgba(255,255,255,.014) 0 1px,transparent 1px 3px)}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px 90px}
header.mast{padding:60px 0 30px;border-bottom:1px solid var(--edge)}
.eyebrow{font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:11px;
letter-spacing:.22em;text-transform:uppercase;color:var(--gold);margin:0 0 14px}
h1{font-family:Cinzel,"Trajan Pro",Georgia,serif;font-weight:600;font-size:clamp(30px,5vw,50px);
line-height:1.08;margin:0 0 16px;color:#eef1f6}
.lede{max-width:70ch;color:var(--dim);font-size:15px;margin:0 0 10px}
.srcline{max-width:70ch;font-size:13.5px;color:var(--dim);margin:0}
a{color:var(--link);text-decoration:none;border-bottom:1px solid rgba(127,214,220,.3)}
a:hover{border-bottom-color:var(--link)}
a:focus-visible,input:focus-visible,.navlink:focus-visible{outline:2px solid var(--gold);outline-offset:3px;border-radius:2px}
.bar{position:sticky;top:0;z-index:20;margin-top:26px;background:rgba(16,19,25,.94);
backdrop-filter:blur(8px);border-bottom:1px solid var(--edge)}
.bar-in{max-width:1180px;margin:0 auto;padding:12px 22px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.field{position:relative;flex:1 1 260px;min-width:220px}
.field input{width:100%;padding:9px 12px 9px 34px;background:var(--panel);color:var(--text);
border:1px solid var(--edge);border-radius:3px;
font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:13px}
.field input::placeholder{color:#5f687a}
.field svg{position:absolute;left:11px;top:50%;transform:translateY(-50%);width:14px;height:14px;
stroke:var(--dim);fill:none;stroke-width:2}
.count{font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:12px;color:var(--dim);white-space:nowrap}
.count b{color:var(--gold);font-weight:600}
nav.jump{display:flex;gap:4px;flex-wrap:wrap;overflow-x:auto}
.navlink{font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:11px;
letter-spacing:.04em;color:var(--dim);padding:5px 9px;border:1px solid transparent;
border-radius:3px;white-space:nowrap;border-bottom:none}
.navlink:hover{color:var(--link);border-color:var(--edge);background:var(--panel)}
.sec{padding:44px 0 8px;scroll-margin-top:110px}
.sec[hidden]{display:none}
h2{display:flex;align-items:baseline;gap:14px;margin:0 0 6px;
font-family:Cinzel,"Trajan Pro",Georgia,serif;font-weight:600;font-size:clamp(19px,2.4vw,25px);color:#e7ebf2}
.sec-idx{font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:12px;
color:var(--gold);letter-spacing:.1em;border:1px solid rgba(217,174,90,.35);padding:2px 7px;
border-radius:2px;flex:none;position:relative;top:-2px}
h2::after{content:"";flex:1 1 auto;height:1px;background:var(--edge)}
h3{font-family:Cinzel,"Trajan Pro",Georgia,serif;font-weight:600;font-size:16px;color:var(--gold);margin:30px 0 4px}
p{margin:12px 0;max-width:78ch}
ul{max-width:78ch;padding-left:20px}
li{margin:6px 0}
li::marker{color:var(--gold)}
strong{color:#e8ecf3;font-weight:600}
code{font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:.86em;
background:var(--panel-2);border:1px solid var(--edge);padding:1px 5px;border-radius:2px;color:var(--gold)}
.twrap{margin:18px 0 8px;border:1px solid var(--edge);border-radius:4px;overflow:hidden;
box-shadow:var(--shadow);background:var(--panel)}
table{width:100%;border-collapse:collapse}
thead th{background:linear-gradient(180deg,var(--panel-2),#1b202b);border-bottom:1px solid var(--edge-hi);
font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:10.5px;
letter-spacing:.16em;text-transform:uppercase;color:var(--dim);text-align:left;padding:11px 16px;font-weight:500}
tbody td{padding:16px;vertical-align:top;font-size:14.5px;border-top:1px solid rgba(51,60,78,.6)}
tbody tr:first-child td{border-top:none}
tbody tr:nth-child(even){background:rgba(255,255,255,.017)}
tbody tr:hover{background:rgba(127,214,220,.045)}
tbody tr[hidden]{display:none}
td:nth-child(1){width:19%}
td:nth-child(2){width:42%}
td:nth-child(3){width:39%;color:#b9bfcb}
.ilink{color:var(--link);font-weight:600;text-shadow:0 0 14px rgba(127,214,220,.28);
display:inline-block;line-height:1.35}
.ilink::before{content:"[";color:var(--edge-hi);margin-right:1px}
.ilink::after{content:"]";color:var(--edge-hi);margin-left:1px}
td strong{color:#eef1f6}
.empty{display:none;margin:40px 0;padding:26px;text-align:center;border:1px dashed var(--edge);
border-radius:4px;color:var(--dim);font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:13px}
.empty.on{display:block}
footer{margin-top:56px;padding-top:22px;border-top:1px solid var(--edge);color:var(--dim);
font-size:12.5px;font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace}
@media (max-width:760px){
.wrap{padding:0 14px 70px}header.mast{padding:38px 0 24px}.bar-in{padding:10px 14px}
nav.jump{width:100%}
.twrap{background:transparent;border:none;box-shadow:none;border-radius:0}
thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
tbody tr{display:block;margin:0 0 14px;background:var(--panel);border:1px solid var(--edge);
border-radius:4px;box-shadow:var(--shadow)}
tbody tr:nth-child(even){background:var(--panel)}
tbody td{display:block;width:auto!important;border-top:1px solid rgba(51,60,78,.6);padding:12px 14px}
tbody td:first-child{border-top:none;background:rgba(255,255,255,.02)}
tbody td::before{content:attr(data-label);display:block;margin-bottom:5px;
font-family:ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;font-size:9.5px;
letter-spacing:.16em;text-transform:uppercase;color:var(--dim)}
tbody td:first-child::before{display:none}}
@media print{body{background:#fff;color:#111}.bar,.empty{display:none}.twrap{box-shadow:none}a{color:#111}}
"""

SCREEN_JS = r"""
(function(){
  var q=document.getElementById('q');
  var rows=[].slice.call(document.querySelectorAll('[data-row]'));
  var secs=[].slice.call(document.querySelectorAll('[data-sec]'));
  var out=document.getElementById('count'), none=document.getElementById('empty');
  var total=rows.length;
  function apply(){
    var term=q.value.trim().toLowerCase(), shown=0;
    rows.forEach(function(r){
      var hit=!term||r.getAttribute('data-find').indexOf(term)>-1;
      r.hidden=!hit; if(hit)shown++;
    });
    secs.forEach(function(s){
      var rs=s.querySelectorAll('[data-row]');
      if(!rs.length){s.hidden=!!term;return;}
      s.hidden=![].some.call(rs,function(r){return !r.hidden;});
    });
    out.innerHTML='<b>'+shown+'</b> / '+total+' items';
    none.classList.toggle('on',shown===0);
  }
  q.addEventListener('input',apply);
  q.addEventListener('keydown',function(e){if(e.key==='Escape'){q.value='';apply();}});
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus();}});
  apply();
})();
"""


def build_screen_html(blocks):
    title = subtitle = sources = ''
    out, nav = [], []
    sec_open, sec_n = False, 0
    for kind, payload in blocks:
        if kind == 'h1':
            title = payload; continue
        if kind == 'hr':
            continue
        if kind == 'h2':
            if sec_open:
                out.append('</section>')
            sec_n += 1
            sid = slug(payload)
            nav.append((sid, payload))
            out.append(f'<section class="sec" id="{sid}" data-sec>')
            out.append(f'<h2><span class="sec-idx">{sec_n:02d}</span>'
                       f'<span class="sec-name">{inline(payload)}</span></h2>')
            sec_open = True; continue
        if kind == 'h3':
            out.append(f'<h3>{inline(payload)}</h3>'); continue
        if kind == 'p':
            if not sec_open:
                if not subtitle: subtitle = inline(payload)
                elif not sources: sources = inline(payload)
                continue
            out.append(f'<p>{inline(payload)}</p>'); continue
        if kind == 'ul':
            out.append('<ul>' + ''.join(f'<li>{inline(x)}</li>' for x in payload) + '</ul>')
            continue
        if kind == 'table':
            head, rows = payload
            trs = []
            for r in rows:
                name, desc, how = (r + ['', '', ''])[:3]
                plain = re.sub(r'[*`\[\]]', '', ' '.join(r)).lower()
                trs.append(
                    f'<tr data-row data-find="{ihtml.escape(plain, quote=True)}">'
                    f'<td data-label="Item"><span class="ilink">{inline(name)}</span></td>'
                    f'<td data-label="What it is">{inline(desc)}</td>'
                    f'<td data-label="How to get it">{inline(how)}</td></tr>')
            out.append('<div class="twrap"><table><thead><tr>'
                       + ''.join(f'<th>{inline(h)}</th>' for h in head)
                       + '</tr></thead><tbody>' + ''.join(trs) + '</tbody></table></div>')
    if sec_open:
        out.append('</section>')

    navhtml = ''.join(f'<a href="#{s}" class="navlink">{ihtml.escape(n)}</a>' for s, n in nav)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{ihtml.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Spectral:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{SCREEN_CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="mast">
    <p class="eyebrow">Norrath &middot; Field Reference</p>
    <h1>{inline(title)}</h1>
    <p class="lede">{subtitle}</p>
    <p class="srcline">{sources}</p>
  </header>
</div>
<div class="bar"><div class="bar-in">
  <div class="field">
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
    <input id="q" type="search" placeholder="Filter items, zones, or mobs&hellip;  (press / )" aria-label="Filter items, zones, or mobs" autocomplete="off">
  </div>
  <span class="count" id="count" role="status" aria-live="polite"></span>
  <nav class="jump" aria-label="Jump to section">{navhtml}</nav>
</div></div>
<div class="wrap">
  {''.join(out)}
  <div class="empty" id="empty">No item matches that. Try a zone name, a mob, or an effect.</div>
  <footer>
    Regenerated from the markdown source &middot; verify drops in&nbsp;game<br>
    Text licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>
    &middot; unofficial fan reference, not affiliated with the publisher
  </footer>
</div>
<script>{SCREEN_JS}</script>
</body>
</html>
"""


# --------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    md = pathlib.Path(sys.argv[1]).resolve()
    src = md.read_text()

    html_path = md.with_suffix('.html')
    html_path.write_text(build_screen_html(parse(src)))
    print(f'wrote {html_path}')


if __name__ == '__main__':
    main()
