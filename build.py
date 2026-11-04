# ── GTA 6 новини за Instagram (@vr_varna): карусел 1080×1350 ─────────────────
#  Стилът е по примерите, които собственикът харесва (@grandtheftauto6):
#  снимката заема горните ~2/3 и потъва в черно; отдолу огромен condensed текст
#  с главни букви, центриран, на 1–4 балансирани реда; ключовите думи в преливащ
#  лилаво→розово→оранжево (палитрата на логото на GTA VI). Без етикети, броячи и
#  източници в кадъра — източниците са в текста под поста. Корица: кръгъл бадж с
#  логото горе вляво + малко лого на линия над заглавието. Финал: Джейсън и Лусия
#  на залеза от gta-6.bg + логото + призив да ни последват.
#  В "text": *думи* = в градиент; "all": true = целият текст в градиент;
#  неразделен интервал (U+00A0) държи думите на един ред.
#  Пътищата в issue.json са спрямо корена на хранилището.
#   python3 build.py issues/<дата>/issue.json issues/<дата>/out
import sys, os, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
BLACK = (8, 6, 12)
GRAD = [(178, 72, 255), (236, 72, 170), (255, 176, 112)]   # лилаво → розово → оранжево
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, 'assets/fonts/Oswald.ttf')  # Oswald Bold (OFL): condensed, с кирилица; най-близо до шрифта в примерите
LOGO = os.path.join(HERE, 'assets/logo.png')         # „VI varna gta hub“ — само това лого
TEXT_W, MARGIN_B = 990, 64

def font(size):
    f = ImageFont.truetype(FONT, size); f.set_variation_by_name('Bold'); return f

def cover(path, w, h, fy=.5):
    im = Image.open(path).convert('RGB'); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = (im.width - w) // 2; y = round((im.height - h) * fy)
    im = im.crop((x, y, x + w, y + h))
    return im.filter(ImageFilter.UnsharpMask(1.2, 60, 2)) if s > 1.05 else im

def gradient(w, h):
    w = max(w, 2); row = Image.new('RGB', (w, 1)); px = row.load()
    for x in range(w):
        t = x / (w - 1) * (len(GRAD) - 1); i = min(int(t), len(GRAD) - 2); k = t - i
        px[x, 0] = tuple(round(GRAD[i][j] + (GRAD[i + 1][j] - GRAD[i][j]) * k) for j in range(3))
    return row.resize((w, h))

def tokens(text, all_hot):  # „*две думи*“ → всяка дума в звездичките е гореща
    out, on = [], False
    for w in [w for w in text.upper().split(' ') if w]:
        start = w.startswith('*'); end = w.rstrip('.,;:!?—“”„').endswith('*')
        out.append((w.replace('*', ''), all_hot or on or start)); on = (on or start) and not end
    return out

def balance(widths, sp, n):
    """Делим думите на n реда така, че най-дългият ред да е възможно най-къс (без висящи думи)."""
    m = len(widths)
    def span(i, j): return sum(widths[i:j]) + sp * (j - i - 1)
    best = {(0, 0): (0, [])}
    for k in range(1, n + 1):
        for j in range(1, m + 1):
            cand = [(max(best[(k - 1, i)][0], span(i, j)), best[(k - 1, i)][1] + [j]) for i in range(j) if (k - 1, i) in best]
            if cand: best[(k, j)] = min(cand)
    return best[(n, m)]

def headline(text, all_hot=False, max_lines=4, max_h=420, max_size=150):
    """1–4 балансирани реда; размерът е най-големият, който се побира в TEXT_W × max_h. Връща RGBA блок."""
    d = ImageDraw.Draw(Image.new('L', (1, 1))); toks = tokens(text, all_hot); U = 100
    f0 = font(U); ws = [d.textlength(w, font=f0) for w, _ in toks]; sp0 = d.textlength(' ', font=f0)
    pick = None
    for n in range(1, min(max_lines, len(toks)) + 1):
        wmax, cuts = balance(ws, sp0, n)
        size = min(max_size, TEXT_W / wmax * U * .98, max_h / n)
        if not pick or size > pick[0] + 4: pick = (size, cuts)   # още ред — само ако шрифтът става осезаемо по-едър
    size = int(pick[0]); f = font(size); sp = d.textlength(' ', font=f); lh = round(size * 1.0)
    lines, i = [], 0
    for j in pick[1]:
        lines.append([(w, h_, d.textlength(w, font=f)) for w, h_ in toks[i:j]]); i = j
    top = f.getbbox('ЙQ')[1]; blk = Image.new('RGBA', (W, len(lines) * lh + 12), (0, 0, 0, 0))
    for li, line in enumerate(lines):
        lw = sum(ww for _, _, ww in line) + sp * (len(line) - 1); x0 = (W - lw) / 2; y = li * lh - top
        white = Image.new('L', blk.size, 0); hot = Image.new('L', blk.size, 0)
        dw, dh = ImageDraw.Draw(white), ImageDraw.Draw(hot); x = x0
        for w, h_, ww in line:
            (dh if h_ else dw).text((x, y), w, font=f, fill=255); x += ww + sp
        blk.paste((255, 255, 255, 255), (0, 0), white)
        g = Image.new('RGB', blk.size, BLACK); g.paste(gradient(round(lw), blk.height), (round(x0), 0))
        blk.paste(g, (0, 0), hot)
    return blk

def logo(h):
    lg = Image.open(LOGO).convert('RGBA'); return lg.resize((round(lg.width * h / lg.height), h), Image.LANCZOS)

def badge(d_px):  # кръгъл бадж горе вляво: нашето лого в преливащ пръстен
    s = d_px * 2; b = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    m = Image.new('L', (s, s), 0); ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    b.paste(gradient(s, s), (0, 0), m)
    ImageDraw.Draw(b).ellipse((16, 16, s - 17, s - 17), fill=(40, 14, 52, 255))
    lg = logo(round(s * .62)); b.alpha_composite(lg, ((s - lg.width) // 2, (s - lg.height) // 2))
    return b.resize((d_px, d_px), Image.LANCZOS)

def sky(w, h):  # залезът от gta-6.bg (горе синьо → долу оранжево)
    col = Image.new('RGB', (1, h)); top, bot = (96, 142, 181), (255, 177, 111)
    col.putdata([tuple(round(top[i] + (bot[i] - top[i]) * y / h) for i in range(3)) for y in range(h)])
    return col.resize((w, h))

def slide(s, first=False, last=False):
    blk = headline(s['text'], s.get('all', False), max_lines=s.get('lines', 4))
    ty = H - MARGIN_B - blk.height                         # текстът е закотвен долу
    img_h = ty + (110 if first else 60)                    # снимката свършва малко под горния ред и потъва в черно
    im = Image.new('RGB', (W, H), BLACK)
    if s.get('cutout'):                                    # финалът: персонажите на фона на залеза от сайта
        im.paste(sky(W, img_h), (0, 0))
        cu = Image.open(s['cutout']).convert('RGBA'); cu = cu.crop(cu.getbbox())
        sc = (img_h + 40) / cu.height; cu = cu.resize((round(cu.width * sc), round(cu.height * sc)), Image.LANCZOS)
        base = im.convert('RGBA'); base.alpha_composite(cu, ((W - cu.width) // 2, 40)); im = base.convert('RGB')
    else:
        im.paste(cover(s['img'], W, img_h, s.get('focus', .5)), (0, 0))
    fade = 300; g = Image.new('L', (1, fade)); g.putdata([round(255 * (i / fade) ** 1.5) for i in range(fade)])
    im.paste(Image.new('RGB', (W, fade), BLACK), (0, img_h - fade), g.resize((W, fade)))
    im = im.convert('RGBA'); im.alpha_composite(blk, (0, ty))
    if first:
        lg = logo(92); ly = ty - lg.height - 22; cx = W // 2; d = ImageDraw.Draw(im)
        for x0, x1 in ((80, cx - lg.width // 2 - 24), (cx + lg.width // 2 + 24, W - 80)):
            d.line((x0, ly + lg.height // 2, x1, ly + lg.height // 2), fill=(236, 72, 170, 255), width=3)
        im.alpha_composite(lg, (cx - lg.width // 2, ly))
        im.alpha_composite(badge(300), (36, 36))
    if last:
        lg = logo(150); im.alpha_composite(lg, ((W - lg.width) // 2, ty - lg.height - 30))
    return im.convert('RGB')

if __name__ == '__main__':
    issue = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    slides = issue['slides']
    for i, s in enumerate(slides, 1):
        for k in ('img', 'cutout'):
            if s.get(k): s[k] = os.path.normpath(os.path.join(HERE, s[k]))
        im = slide(s, first=(i == 1), last=(i == len(slides)))
        p = os.path.join(out, f'{i:02d}.jpg'); im.save(p, quality=93, subsampling=0); print('OK', p)
