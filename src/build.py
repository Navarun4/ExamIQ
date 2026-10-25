"""Builds index.html and physics.html from src/ (fonts + shared base CSS embedded). Never touches the lesson file."""
import base64, pathlib, sys
SRC = pathlib.Path(__file__).resolve().parent; OUT = SRC.parent
FONTS = SRC / 'fonts'
faces = [("Instrument Serif", 400, "normal", "InstrumentSerif-Regular.woff"), ("Instrument Serif", 400, "italic", "InstrumentSerif-Italic.woff"),
         ("Barlow Condensed", 600, "normal", "BarlowCondensed-SemiBold.woff"), ("ExamiQ Mono", 400, "normal", "ExamiQMono-Regular.woff")]
css = "\n".join(f'@font-face{{font-family:"{f}";font-weight:{w};font-style:{s};font-display:swap;src:url(data:font/woff;base64,{base64.b64encode((FONTS/n).read_bytes()).decode()}) format("woff")}}' for f, w, s, n in faces)
base = (SRC / 'base.css').read_text(encoding='utf-8')
motion = (SRC / 'motion.js').read_text(encoding='utf-8')
for name in ('index', 'physics'):
    t = (SRC / f'{name}.src.html').read_text(encoding='utf-8')
    assert t.count('/*__FONTS__*/') == 1 and t.count('/*__BASE__*/') == 1 and t.count('/*__MOTION__*/') == 1
    t = t.replace('/*__FONTS__*/', css).replace('/*__BASE__*/', base).replace('/*__MOTION__*/', motion)
    # Motion is opt-in: the class is set before first paint only when reduced motion is NOT requested,
    # so with JS off or reduced motion on, nothing is ever hidden or animated.
    flag = "<script>if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('motion')</script>"
    assert t.count('</head>') == 1
    t = t.replace('</head>', flag + '\n</head>')
    (OUT / f'{name}.html').write_text(t, encoding='utf-8')
    print('built', name + '.html')
