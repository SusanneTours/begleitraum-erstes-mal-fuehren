"""Baut die Teilnehmerfolien "Das erste Mal führen 1" aus der Haufe-Vorlage des Crashkurses."""
import copy, sys
from pptx import Presentation
from lxml import etree

SRC = '/home/claude/erstes-mal-fuehren/src/vorlage_haufe.pptx'
MEDIA = '/tmp/claude-0/-home-claude/88d19f3e-f7e3-5f34-a7b4-c0d4a0c4e6fc/scratchpad/pptx/ppt/media/'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'Das_erste_Mal_fuehren_Folien.pptx'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'

import os
from PIL import Image
SHIFT = '/tmp/claude-0/-home-claude/88d19f3e-f7e3-5f34-a7b4-c0d4a0c4e6fc/scratchpad/shifted/'
os.makedirs(SHIFT, exist_ok=True)
def shifted(img, frac):
    """Verschiebt das Motiv nach rechts, damit der Kopf neben dem Aufgabenkasten frei bleibt. Nichts wird abgeschnitten, links wird gespiegelt aufgefüllt."""
    im = Image.open(MEDIA + img).convert('RGB').resize((1600, 900))
    dx = int(1600 * frac)
    out = Image.new('RGB', (1600, 900))
    out.paste(im.crop((0, 0, 1600 - dx, 900)), (dx, 0))
    out.paste(im.crop((0, 0, dx, 900)).transpose(Image.FLIP_LEFT_RIGHT), (0, 0))
    name = 'shift_' + os.path.splitext(img)[0] + '.jpg'
    out.save(SHIFT + name, quality=88)
    return SHIFT + name

prs = Presentation(SRC)
orig = list(prs.slides)
T = {'title': 1, 'trainer': 2, 'agenda': 3, 'box': 4, 'chapter': 6, 'steps': 7,
     'solo': 9, 'group': 10, 'coffee': 11, 'lunch': 21, 'end': 38}


def dup(key):
    src = orig[T[key] - 1]
    new = prs.slides.add_slide(src.slide_layout)
    for ph in list(new.placeholders):
        ph._element.getparent().remove(ph._element)
    remap = {}
    for rId, rel in src.part.rels.items():
        if rel.reltype.endswith('/slideLayout') or rel.reltype.endswith('/notesSlide'):
            continue
        if rel.is_external:
            remap[rId] = new.part.rels.get_or_add_ext_rel(rel.reltype, rel.target_ref)
        else:
            remap[rId] = new.part.rels.get_or_add(rel.reltype, rel.target_part)
    if src._element.cSld.bg is not None:
        new._element.cSld.insert(0, copy.deepcopy(src._element.cSld.bg))
    tree = new.shapes._spTree
    for el in src.shapes._spTree.iterchildren():
        if el.tag.endswith('}nvGrpSpPr') or el.tag.endswith('}grpSpPr'):
            continue
        e = copy.deepcopy(el)
        for node in e.iter():
            for att in (R + 'embed', R + 'link', R + 'id'):
                v = node.get(att)
                if v in remap:
                    node.set(att, remap[v])
        tree.append(e)
    return new


def shape(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError(name)


def fill(sh, items):
    """items: Liste von (proto_index, text) oder (proto_index, (text1, text2))."""
    txBody = sh.text_frame._txBody
    ps = txBody.findall(A + 'p')
    protos = [copy.deepcopy(p) for p in ps]
    for p in ps:
        txBody.remove(p)
    for idx, text in items:
        p = copy.deepcopy(protos[idx])
        runs = p.findall(A + 'r')
        texts = text if isinstance(text, tuple) else (text,)
        for r, t in zip(runs, texts):
            r.find(A + 't').text = t
        for r in runs[len(texts):]:
            p.remove(r)
        txBody.append(p)


def set_text(sh, text):
    fill(sh, [(0, text)])


def photo(slide, img):
    """Tauscht das Foto im Bildplatzhalter, ohne Zuschnitt (Fotos sind 16:9)."""
    _, rId = slide.part.get_or_add_image_part(img if img.startswith('/') else MEDIA + img)
    for sh in slide.shapes:
        if sh.is_placeholder and 'Picture' in sh.name:
            blip = sh._element.find('.//' + A + 'blip')
            blip.set(R + 'embed', rId)
            for ext in blip.findall(A + 'extLst'):
                blip.remove(ext)
            src = sh._element.find('.//' + A + 'srcRect')
            if src is not None:
                for k in list(src.attrib):
                    del src.attrib[k]
            return
    raise RuntimeError('kein Bildplatzhalter')


# ---------- Bausteine ----------
def title(t, sub):
    s = dup('title'); fill(shape(s, 'Title 2'), [(0, t), (1, sub)])


def trainer():
    dup('trainer')


def agenda(t, rows, pausen, mittag):
    s = dup('agenda')
    set_text(shape(s, 'Title 2'), t)
    fill(shape(s, 'Text Placeholder 3'), [(0, (z + ' Uhr  ', txt)) for z, txt in rows])
    set_text(shape(s, 'Rounded Rectangle 10'), pausen)
    set_text(shape(s, 'Rounded Rectangle 11'), mittag)


def box(t, intro, highlight, after, zeit):
    s = dup('box')
    set_text(shape(s, 'Title 4'), t)
    items = [(0, 'Aufgabe:'), (1, intro), (2, highlight)]
    if after:
        items.append((3, after))
    items.append((4, ('Zeit: ', zeit)))
    fill(shape(s, 'TextBox 2'), items)


def chapter(n, t):
    s = dup('chapter'); set_text(shape(s, 'Subtitle 1'), str(n)); set_text(shape(s, 'Title 2'), t)


def task(kind, t, img, parts, zeit, head='Aufgabe:'):
    """parts: Liste aus ('p', text) oder ('b', text)."""
    s = dup('solo' if kind == 'solo' else 'group')
    photo(s, img)
    set_text(shape(s, 'Title 4'), t)
    items = [(0, head)]
    for k, txt in parts:
        items.append((1 if k == 'p' else 3, txt))
    items.append((6, ('Zeit: ', zeit)))
    fill(shape(s, 'TextBox 14'), items)


def steps(t, badge1, badge2, cols):
    s = dup('steps')
    set_text(shape(s, 'Title 1'), t)
    fill(shape(s, 'Oval 2'), [(0, badge1), (1, badge2)])
    for box_name, (head, body, minutes) in zip(['TextBox 5', 'TextBox 7', 'TextBox 9', 'TextBox 11'], cols):
        fill(shape(s, box_name), [(0, head), (1, body), (2, minutes)])


def pause(kind, t, zeit, img=None):
    s = dup(kind)
    if img:
        photo(s, img)
    set_text(shape(s, 'Title 1'), t)
    set_text(shape(s, 'Title 2'), zeit)


def end(t, sub):
    s = dup('end'); fill(shape(s, 'Title 2'), [(0, t), (1, sub)])



# ---------- freie Formen ----------
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
PURPLE = RGBColor(0x6F, 0x01, 0xF5); DARK = RGBColor(0x19, 0x03, 0x33); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0x5B, 0x4F, 0x72); LAV = RGBColor(0xF3, 0xE7, 0xFF); ROSE = RGBColor(0xFA, 0xE6, 0xE6)

def drop(slide, *names):
    for sh in list(slide.shapes):
        if sh.name in names:
            sh._element.getparent().remove(sh._element)

def tbox(slide, x, y, w, h, paras, anchor=None):
    """paras: Liste von (text, groesse, farbe, fett, abstand_vorher)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    if anchor: tf.vertical_anchor = anchor
    for i, (t, size, color, bold, before) in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(before)
        r = p.add_run(); r.text = t; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color
    return tb

def card(slide, x, y, w, h, color, radius=0.06):
    c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    c.adjustments[0] = radius; c.fill.solid(); c.fill.fore_color.rgb = color; c.line.fill.background(); c.shadow.inherit = False
    return c

def mirrored(img):
    im = Image.open(MEDIA + img).convert('RGB').resize((1600, 900)).transpose(Image.FLIP_LEFT_RIGHT)
    name = SHIFT + 'mirror_' + os.path.splitext(img)[0] + '.jpg'; im.save(name, quality=88); return name

LOGO = None
for _sh in orig[0].shapes:
    if _sh.name == 'Haufe Akademie Logo':
        LOGO = copy.deepcopy(_sh._element)

def haufe_title(t, sub, img):
    """Titelfolie nach Haufe-Vorlage: grosses Foto, violetter Kasten unten, Name und Hinweis Vertragspartnerin."""
    s = dup('solo')
    photo(s, img)
    drop(s, 'Title 4', 'Graphic 8', 'Graphic 18', 'Graphic 7', 'TextBox 14', 'Footer Placeholder 3', 'Slide Number Placeholder 5')
    box = shape(s, 'Rounded Rectangle 1')
    box.left, box.top, box.width, box.height = Inches(0.62), Inches(4.0), Inches(12.1), Inches(2.92)
    tbox(s, 1.05, 4.32, 11.2, 2.5, [(t, 44, WHITE, False, 0), (sub, 20, WHITE, False, 8),
                                    ('Susanne Tours', 16, WHITE, False, 26), ('Vertragspartnerin der Haufe Akademie', 16, WHITE, False, 2)])
    if LOGO is not None:
        lg = copy.deepcopy(LOGO)
        xf = lg.find('.//' + A + 'xfrm')
        xf.find(A + 'off').set('x', str(int(Inches(10.15)))); xf.find(A + 'off').set('y', str(int(Inches(0.55))))
        xf.find(A + 'ext').set('cx', str(int(Inches(2.6)))); xf.find(A + 'ext').set('cy', str(int(Inches(2.6) * 351846 / 2833785)))
        s.shapes._spTree.append(lg)

NEEDS5 = [
 ('Bindung', 'Ich gehöre dazu und kann mich auf andere verlassen.', 'Zugehörigkeit, Verbundenheit und Unterstützung durch andere Menschen. Erfüllte Bindung gibt Sicherheit und Vertrauen.', 'Echtes Interesse aneinander, gemeinsame Rituale, niemand wird übergangen.', 'Rückzug, Grüppchen, Gespräche nur noch über Dritte.'),
 ('Orientierung und Kontrolle', 'Ich verstehe, was passiert, und kann mitgestalten.', 'Klarheit, Stabilität und das Gefühl, Situationen verstehen und beeinflussen zu können.', 'Klare Zuständigkeiten, früh informieren, Entscheidungen erklären.', 'Gerüchte, viele Rückfragen, Festhalten am Alten.'),
 ('Selbstwertschutz und Selbstwerterhöhung', 'Ich werde gesehen und kann wachsen.', 'Anerkennung, Respekt und Wertschätzung. Und die Möglichkeit, an Herausforderungen zu wachsen.', 'Anerkennung konkret aussprechen, Kritik unter vier Augen, Neues zutrauen.', 'Rechtfertigen, Verteidigen, Kränkung, Rückzug aus Verantwortung.'),
 ('Lustgewinn und Unlustvermeidung', 'Die Arbeit macht auch Freude.', 'Angenehme Erfahrungen suchen, Belastendes vermeiden. Das sorgt für Wohlbefinden und Gleichgewicht.', 'Erfolge feiern, Ärgernisse abbauen, Humor zulassen.', 'Lustlosigkeit, Dienst nach Vorschrift, Gereiztheit.'),
 ('Kohärenz', 'Was ich tue, ergibt Sinn.', 'Sinn, Zusammenhang und Stimmigkeit. Was ich tue, passt zu meinen Werten.', 'Das Wozu klären, Widersprüche offen ansprechen.', 'Zynismus, „Das bringt doch eh nichts“.')]

def needs_overview():
    s = dup('steps')
    set_text(shape(s, 'Title 1'), 'Die fünf psychologischen Grundbedürfnisse')
    keep = {'Title 1', 'Footer Placeholder 3', 'Slide Number Placeholder 4'}
    for sh in list(s.shapes):
        if sh.name not in keep:
            sh._element.getparent().remove(sh._element)
    tbox(s, 0.45, 1.2, 11.5, 0.8, [('Wenn Menschen gereizt, still oder blockiert reagieren, steckt fast immer ein Bedürfnis dahinter, das gerade nicht erfüllt ist.', 18, SOFT, False, 0)])
    w, gap, x0 = 2.33, 0.18, 0.45
    SHORT = ['Bindung', 'Orientierung\nund Kontrolle', 'Selbstwert-\nschutz und\n-erhöhung', 'Lustgewinn\nund Unlust-\nvermeidung', 'Kohärenz']
    for i, (name, kern, *_r) in enumerate(NEEDS5):
        name = SHORT[i]
        x = x0 + i * (w + gap)
        card(s, x, 2.3, w, 3.9, LAV)
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.25), Inches(2.6), Inches(0.75), Inches(0.75))
        o.fill.solid(); o.fill.fore_color.rgb = PURPLE; o.line.fill.background(); o.shadow.inherit = False
        tf = o.text_frame; tf.margin_left = tf.margin_right = 0; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = str(i + 1); r.font.size = Pt(24); r.font.bold = True; r.font.color.rgb = WHITE
        tbox(s, x + 0.22, 3.6, w - 0.4, 2.5, [(name, 17, DARK, True, 0), (kern, 15, SOFT, False, 10)])

def need_detail(i, img):
    name, kern, desc, ok, fehlt = NEEDS5[i]
    s = dup('solo')
    photo(s, img)
    drop(s, 'Title 4', 'Graphic 8', 'TextBox 14')
    box = shape(s, 'Rounded Rectangle 1')
    box.left, box.top, box.width, box.height = Inches(5.55), Inches(0.95), Inches(7.33), Inches(6.05)
    box.fill.solid(); box.fill.fore_color.rgb = WHITE
    tbox(s, 6.0, 1.3, 6.45, 3.0, [(f'GRUNDBEDÜRFNIS {i + 1} VON 5', 12, PURPLE, True, 0), (name, 30, DARK, False, 6),
                                   (kern, 20, PURPLE, True, 8), (desc, 15, SOFT, False, 10)])
    card(s, 6.0, 4.45, 3.12, 2.2, LAV); card(s, 9.33, 4.45, 3.12, 2.2, ROSE)
    tbox(s, 6.2, 4.65, 2.75, 1.9, [('Im Team erfüllt, wenn …', 14, PURPLE, True, 0), (ok, 14, DARK, False, 6)])
    tbox(s, 9.53, 4.65, 2.75, 1.9, [('Woran man merkt, dass es fehlt', 14, RGBColor(0xCB, 0x01, 0x01), True, 0), (fehlt, 14, DARK, False, 6)])

# ---------- Inhalt ----------
haufe_title('Das erste Mal führen 1', 'Vom Rollenwechsel bis zu ersten Führungsgesprächen: dein Fundament für einen erfolgreichen Start in die Führung', 'image10.jpg')
trainer()
agenda('Tag 1', [('09:00', 'Ankommen'), ('09:45', 'Die Veränderungskurve'), ('10:30', 'Perspektivwechsel'),
                 ('11:30', 'Erwartungen klären'), ('13:30', 'Dein Führungskorridor'), ('15:30', 'Fünf Grundbedürfnisse'),
                 ('16:40', 'Tagesabschluss'), ('17:00', 'Ende')],
       '10:15-10:30 Uhr, 15:15-15:30 Uhr', '12:30-13:30 Uhr')
box('Ankommen im Raum', 'Stellt euch im Halbkreis auf, sortiert nach eurer Führungserfahrung. Ganz links steht, wer noch in Vorbereitung auf die Rolle oder ganz frisch dabei ist. Ganz rechts steht, wer am längsten führt.',
    'Sprecht miteinander, bis die Reihenfolge stimmt.', None, 'ca. 5 Minuten')
box('Wer bist du, was erwartest du?', 'Stell dich der Gruppe kurz vor:',
    'Welche Rolle hast du? Wie viele Mitarbeitende führst du? Was muss hier passieren, damit sich die zwei Tage für dich wirklich gelohnt haben?', 'Schreib deine Erwartungen dabei als Hashtag an das Flipchart, zum Beispiel #KritikgesprächeFühren.', 'ca. 1 bis 2 Minuten pro Person')
task('group', 'Was ist Führung?', 'image11.jpg',
     [('p', 'Wir falten den Halbkreis: Die Person ganz links geht zur Person ganz rechts, und so weiter. So sprechen immer wenig und viel Erfahrung miteinander.'),
      ('b', 'Führen heißt für mich …'), ('b', 'Wer war deine beste Führungskraft, und was hat sie ausgemacht?'),
      ('p', 'Einigt euch zu zweit auf einen Satz „Führung ist …“ und schreibt ihn auf eine Karte.')],
     '2 × 5 Minuten zu zweit, Karte 2 Minuten')

chapter(1, 'Die Veränderungskurve')
task('solo', 'Wo steht dein Team?', 'image13.jpg',
     [('p', 'Am Flipchart siehst du die Veränderungskurve. Klebe zwei Punkte:'),
      ('b', 'Einen für dein Team: Wo steht es gerade?'), ('b', 'Einen für dich: Wo stehst du selbst?'),
      ('p', 'Erzähl danach einer anderen Person: Woran merkst du das? Was braucht dein Team jetzt von dir?')],
     '3 Minuten Punkte, 2 × 4 Minuten zu zweit')
pause('coffee', 'Kaffeepause', '10:15 bis 10:30 Uhr')

chapter(2, 'Perspektivwechsel')
steps('Du bekommst eine neue Führungskraft', '1-2-4-alle', '20 Min.', [
    ('Allein', 'Stell dir vor, du bist Mitarbeiterin oder Mitarbeiter und bekommst morgen eine neue Führungskraft. Was geht dir durch den Kopf? Notiere deine Fragen.', '2 Minuten'),
    ('Zu zweit', 'Tauscht euch aus. Was habt ihr beide? Was ergänzt ihr?', '3 Minuten'),
    ('Zu viert', 'Wählt die Fragen, die euch am wichtigsten sind. Eine Frage pro Karte.', '5 Minuten'),
    ('Alle', 'Wir hängen die Karten an die Pinnwand und sortieren sie gemeinsam.', '10 Minuten')])
task('group', 'Brille wechseln', shifted('image14.jpg', 0.08),
     [('p', 'Jetzt bist du wieder Führungskraft. Jede Gruppe übernimmt einen Bereich von der Pinnwand. Haltet auf einem Plakat fest:'),
      ('b', 'Was tue ich in den ersten Tagen?'), ('b', 'Was tue ich in den ersten Wochen?'), ('b', 'Was vermeide ich auf jeden Fall?'),
      ('p', 'Danach stellt jede Gruppe ihr Plakat in zwei Minuten vor.')],
     '15 Minuten in Gruppen, dann Vorstellung')

chapter(3, 'Erwartungen klären')
task('solo', 'Deine Antworten', 'image17.jpg',
     [('p', 'Nimm dir die Fragen von der Pinnwand vor und denk an dein eigenes Team:'),
      ('b', 'Welche Fragen kannst du heute schon beantworten?'), ('b', 'Welche noch nicht? Bis wann klärst du sie?'),
      ('b', 'Was erwartest du von deinem Team?'), ('b', 'Was musst du mit deiner eigenen Führungskraft klären?'),
      ('p', 'Halte es im Startplan unter Schritt 3 oder auf deinem Arbeitsblatt fest.')],
     '10 Minuten, Einzelarbeit')
steps('Das Erwartungsgespräch üben', 'Trio', '3 Runden à 12 Min.', [
    ('Vorbereiten', 'A überlegt sich den Einstieg ins Gespräch. B nimmt zwei Fragen von der Pinnwand. C bereitet sich aufs Beobachten vor.', '2 Minuten'),
    ('Gespräch', 'A führt das Erwartungsgespräch. B spielt ein Teammitglied und stellt seine Fragen. C beobachtet.', '6 Minuten'),
    ('Rückmeldung', 'Zuerst B, dann C: Was hat dir Sicherheit gegeben? Was hat gefehlt?', '4 Minuten'),
    ('Wechsel', 'Ihr tauscht die Rollen, bis jede Person einmal A war.', '')])
pause('lunch', 'Mittagspause', '12:30 bis 13:30 Uhr')

chapter(4, 'Dein Führungskorridor')
task('solo', 'Dein Führungskorridor', 'image18.jpg',
     [('p', 'Beantworte die vier Fragen für deinen Bereich. Schreib so, als würdest du es deinem Team erklären:'),
      ('b', 'Welche Ziele habe ich für meinen Bereich?'), ('b', 'Was erwarte ich, damit wir die Ziele erreichen?'),
      ('b', 'Welche Werte und Prinzipien gelten für unsere Zusammenarbeit?'), ('b', 'Welche Kommunikation braucht es dafür?')],
     '25 Minuten, Einzelarbeit')
steps('Deinen Korridor vorstellen', 'Zu zweit', '2 × 10 Min.', [
    ('Vorstellen', 'A stellt den eigenen Führungskorridor vor, so als stünde das Team vor ihr oder ihm.', '4 Minuten'),
    ('Nachfragen', 'B fragt nach, wie es ein Teammitglied tun würde: Was heißt das konkret für mich?', '3 Minuten'),
    ('Rückmeldung', 'B sagt: Was ist klar angekommen? Was ist noch offen?', '2 Minuten'),
    ('Nachschärfen', 'A ergänzt den Korridor. Dann tauscht ihr die Rollen.', '1 Minute')])
pause('coffee', 'Kaffeepause', '15:15 bis 15:30 Uhr', 'image102.png')

chapter(5, 'Fünf Grundbedürfnisse')
needs_overview()
for _i, _img in enumerate(['image101.png', mirrored('image17.jpg'), mirrored('image10.jpg'), mirrored('image6.jpg'), mirrored('image11.jpg')]):
    need_detail(_i, _img)
task('group', 'Ein Bedürfnis, viele Ideen', 'image6.jpg',
     [('p', 'Jede Gruppe übernimmt ein Grundbedürfnis. Haltet auf eurem Plakat fest:'),
      ('b', 'Woran merke ich im Alltag, dass es bedroht ist?'), ('b', 'Was tue ich ab Montag konkret, um es zu stärken?'),
      ('b', 'Was vermeide ich auf jeden Fall?')],
     '15 Minuten in Gruppen')
steps('Galeriegang', 'Gruppen', '25 Min.', [
    ('Wandern', 'Jede Gruppe geht zum nächsten Plakat und liest, was dort steht.', '3 Minuten pro Station'),
    ('Ergänzen', 'Schreibt eure Ideen mit einer anderen Farbe dazu.', ''),
    ('Zurück', 'Zurück am eigenen Plakat: Welche Ergänzungen überraschen euch?', '3 Minuten'),
    ('Auswählen', 'Jede Person wählt eine Idee pro Bedürfnis für das eigene Team und notiert sie im Startplan.', '5 Minuten')])
box('Rückblick auf heute', 'Wir stellen uns in einen Kreis. Jede Person sagt einen Satz:',
    '„Mein wichtigster Gedanke von heute ist …“', 'Wir hören zu und kommentieren nicht.', '10 Minuten')

agenda('Tag 2', [('09:00', 'Ankommen'), ('09:15', 'Können und Wollen'), ('10:30', 'Auf Augenhöhe'),
                 ('11:30', 'Offene Fragen'), ('13:30', 'Gespräche führen'), ('15:30', 'Schwierige Gespräche'),
                 ('16:30', 'Dein Startplan'), ('17:00', 'Ende')],
       '10:15-10:30 Uhr, 15:15-15:30 Uhr', '12:30-13:30 Uhr')
box('Guten Morgen', 'Tauscht euch zu zweit aus:', 'Was ist dir seit gestern durch den Kopf gegangen?',
    'Danach hören wir einige Stimmen in der großen Runde.', 'ca. 10 Minuten')

chapter(6, 'Können und Wollen')
task('group', 'Euer Führungsverhalten', 'image10.jpg',
     [('p', 'Jede Gruppe übernimmt ein Feld der Matrix. Überlegt gemeinsam:'),
      ('b', 'Wie führe ich eine Person in diesem Feld?'), ('b', 'Was braucht sie von mir? Was hilft ihr nicht?'),
      ('b', 'Welches Beispiel aus eurem Alltag passt dazu?'),
      ('p', 'Schreibt eure Ergebnisse auf das Plakat. Danach stellt jede Gruppe in drei Minuten vor.')],
     '20 Minuten in Gruppen, dann Vorstellung')
pause('coffee', 'Kaffeepause', '10:15 bis 10:30 Uhr', 'image103.png')

chapter(7, 'Auf Augenhöhe')
steps('Sätze übersetzen', 'Zu zweit', '15 Min.', [
    ('Sammeln', 'Welche Sätze hört man im Alltag, die von oben herab klingen? Sammelt drei bis fünf.', '4 Minuten'),
    ('Zuordnen', 'Aus welchem Ich-Zustand kommt der Satz? Was löst er beim Gegenüber aus?', '2 Minuten'),
    ('Übersetzen', 'Formuliert jeden Satz ins Erwachsenen-Ich um. Oft wird aus einer Aussage eine Frage.', '6 Minuten'),
    ('Teilen', 'Jedes Paar schreibt seine beste Übersetzung ans Flipchart.', '3 Minuten')])

chapter(8, 'Offene Fragen')
task('group', 'Die Matrix ergänzen', shifted('image8.jpg', 0.18),
     [('p', 'Ihr geht zurück zu eurem Plakat aus dem Vormittag. Ergänzt euer Feld:'),
      ('b', 'Welche offenen Fragen stelle ich einer Person in diesem Feld?'), ('b', 'Was will ich von ihr eigentlich wissen?'),
      ('p', 'Nutzt Fragen, die mit einem W-Wort beginnen.')],
     '10 Minuten in Gruppen')
task('solo', 'Dein Team einordnen', 'image9.jpg',
     [('p', 'Denk an die Menschen in deinem Team und an eine konkrete Aufgabe:'),
      ('b', 'Ordne jede Person mit einem Kürzel in ein Feld ein.'), ('b', 'Formuliere für jede Person eine offene Frage: Was will ich von ihr wissen?'),
      ('p', 'Nutze dein Arbeitsblatt oder den Startplan, Schritt 6. Das bleibt nur bei dir.')],
     '10 Minuten, Einzelarbeit')
pause('lunch', 'Mittagspause', '12:30 bis 13:30 Uhr')

chapter(9, 'Gespräche führen')
task('solo', 'Dein Gesprächsplan', shifted('image12.jpg', 0.08),
     [('p', 'Wähle eine Person aus deiner Matrix, mit der du bald ein Gespräch führen willst. Bereite es vor:'),
      ('b', 'Ziel: Was soll am Ende klar sein?'), ('b', 'Realität: Wie siehst du die Situation? Wie sieht sie die andere Person?'),
      ('b', 'Möglichkeiten: Welche Fragen stellst du? Was bietest du an?'), ('b', 'Vereinbarung: Was soll bis wann passieren?'),
      ('p', 'Formuliere auch deinen ersten Satz.')],
     '12 Minuten, Einzelarbeit')
steps('Das Gespräch im Trio', 'Trio', '3 Runden à 15 Min.', [
    ('Briefing', 'A erklärt B kurz die Rolle: Wer ist die Person, wie reagiert sie üblicherweise?', '2 Minuten'),
    ('Gespräch', 'A führt das Gespräch. B spielt die Person. C beobachtet entlang der vier Schritte.', '8 Minuten'),
    ('Rückmeldung', 'Zuerst B, dann C: Welche Frage hat gewirkt? Wo ist das Gespräch hängen geblieben?', '4 Minuten'),
    ('Wechsel', 'Ihr tauscht die Rollen, bis jede Person einmal A war.', '1 Minute')])
pause('coffee', 'Kaffeepause', '15:15 bis 15:30 Uhr', 'image102.png')

chapter(10, 'Schwierige Gespräche')
task('solo', 'Dein offenes Gespräch', shifted('image4.jpg', 0.4),
     [('p', 'Denk an ein Gespräch, das du schon länger vor dir herschiebst:'),
      ('b', 'Seit wann schiebst du es auf?'), ('b', 'Was kostet es dich jede Woche, dass du es nicht führst?'),
      ('b', 'Wann führst du es?')],
     '3 Minuten, Einzelarbeit')
task('solo', 'Kritik in drei Schritten', shifted('image16.jpg', 0.27),
     [('p', 'Formuliere für dein Gespräch die ersten Sätze:'),
      ('b', 'Wahrnehmung: Was habe ich beobachtet, ohne Wertung?'), ('b', 'Wirkung: Was löst das aus, bei mir, im Team, beim Kunden?'),
      ('b', 'Wunsch: Was wünsche ich mir für die Zukunft?'),
      ('p', 'Im Begleitraum findest du Satzstarter, die dir den Einstieg erleichtern.')],
     '6 Minuten, Einzelarbeit')
steps('Wenn es blockiert', 'Trio', '3 Runden à 10 Min.', [
    ('Einstieg', 'A spricht die Kritik mit den drei Schritten an.', '2 Minuten'),
    ('Blockade', 'B macht dicht: schweigt, antwortet einsilbig oder sagt nur „Passt schon“.', ''),
    ('Dreiklang', 'A bleibt dran mit „Ich weiß …“, „Mir ist wichtig …“, „Ich bin offen …“. C beobachtet.', '5 Minuten'),
    ('Rückmeldung', 'B und C: Welcher Satz hat die Tür geöffnet? Dann wechselt ihr.', '3 Minuten')])
task('solo', 'Dein Startplan', 'image90.jpeg',
     [('p', 'Was tust du in den nächsten 30 Tagen? Halte im Startplan unter Schritt 8 fest:'),
      ('b', 'Drei konkrete Schritte, jeweils mit Datum'), ('b', 'Deinen Transfer-Buddy aus dieser Gruppe'),
      ('b', 'Deinen wichtigsten Satz aus den zwei Tagen'),
      ('p', 'Tauscht mit eurem Buddy die Kontaktdaten aus und vereinbart einen Termin in drei Wochen.')],
     '15 Minuten')
box('Zum Abschluss', 'Wir stellen uns in einen Kreis. Jede Person sagt einen Satz:',
    '„Mein erster Schritt ist … bis …“', 'Wir hören zu und kommentieren nicht. Applaus gibt es am Ende für alle.', '10 Minuten')
end('Danke für zwei starke Tage', 'Dein Startplan und die Satzstarter bleiben im Begleitraum für dich offen. Ich wünsche dir einen guten Start in deiner Rolle.')

# Originalfolien entfernen
sldIdLst = prs.slides._sldIdLst
for s in orig:
    for sid in list(sldIdLst):
        if prs.slides.part.related_part(sid.rId) is s.part if False else False:
            pass
ids = list(sldIdLst)
for sid in ids[:len(orig)]:
    prs.part.drop_rel(sid.rId)
    sldIdLst.remove(sid)
# Keine Foliennummern
for _s in prs.slides:
    for _sh in list(_s.shapes):
        if 'Slide Number' in _sh.name or 'Foliennummer' in _sh.name:
            _sh._element.getparent().remove(_sh._element)
prs.save(OUT)
print('Folien:', len(prs.slides))
