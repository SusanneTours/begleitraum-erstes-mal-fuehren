"""Baut die Fassung "so gelaufen in Köln, 12./13.10.2026": Folien der Vollversion, die genutzt wurden,
plus Fotos der Flipcharts und Pinnwände aus dem Training und die OKR-Folien.
Aufruf: python3 koeln.py <out.pptx>"""
import sys
_src = open('/home/claude/erstes-mal-fuehren/src/deck.py', encoding='utf-8').read()
exec(_src.split('# ---------- Inhalt ----------')[0])
OUT = sys.argv[1]
FOTO = '/home/claude/erstes-mal-fuehren/src/fotos_training/'
LIGHT = RGBColor(0xF4, 0xF1, 0xF8)


# ---------- Foto-Folien ----------
def foto(t, imgs, paras, eyebrow='Aus unserem Training'):
    """Ein oder zwei Hochformat-Fotos rechts, ungeschnitten. Links ein kurzer Text."""
    s = blank_title(t)
    h = 5.75; w = h * 3 / 4; gap = 0.2; y = 1.15
    x = 13.33 - 0.45 - len(imgs) * w - (len(imgs) - 1) * gap
    for i, img in enumerate(imgs):
        s.shapes.add_picture(FOTO + img + '.jpg', Inches(x + i * (w + gap)), Inches(y), Inches(w), Inches(h))
    tw = x - 0.45 - 0.45
    tbox(s, 0.45, 1.35, tw, 5.4, [(eyebrow.upper(), 13, PURPLE, True, 0)] + paras)
    return s


def p(t, size=19, color=None, bold=False, before=12):
    return (t, size, color or DARK, bold, before)


# ---------- OKR ----------
def okr_was():
    s = blank_title('OKR: Ziele für kurze Strecken')
    tbox(s, 0.45, 1.15, 12.4, 0.6, [('OKR steht für Objectives and Key Results. Damit setzt ihr Ziele für die nächsten drei Monate und steuert unterwegs nach.', 17, SOFT, False, 0)])
    card(s, 0.45, 1.95, 6.0, 2.0, PURPLE)
    tbox(s, 0.75, 2.2, 5.4, 1.6, [('OBJECTIVE', 13, RGBColor(0xD6, 0xB4, 0xFF), True, 0), ('Was wollen wir erreichen?', 22, WHITE, True, 4),
                                   ('Ein Ziel in Worten, klar und motivierend. Es gibt die Richtung vor.', 15, WHITE, False, 6)])
    card(s, 0.45, 4.1, 6.0, 2.0, LAV)
    tbox(s, 0.75, 4.35, 5.4, 1.6, [('KEY RESULTS', 13, PURPLE, True, 0), ('Woran merken wir, dass wir es geschafft haben?', 20, DARK, True, 4),
                                    ('Zwei bis vier Ergebnisse, die man messen kann, mit Zahl und Datum.', 15, SOFT, False, 6)])
    card(s, 6.85, 1.95, 6.03, 4.15, LIGHT)
    tbox(s, 7.15, 2.2, 5.5, 3.8, [('DER RHYTHMUS', 13, PURPLE, True, 0),
                                  ('3 Monate', 22, DARK, True, 8), ('So lange gilt ein OKR. Danach setzt ihr das nächste.', 14, SOFT, False, 2),
                                  ('Sprints à 2 bis 3 Wochen', 22, DARK, True, 14), ('Kurze Etappen. Am Ende jedes Sprints schaut ihr gemeinsam: Stimmt der Weg noch?', 14, SOFT, False, 2),
                                  ('Stand-ups', 22, DARK, True, 14), ('Kurz und regelmäßig: Was ist erledigt? Was ist als Nächstes dran? Wo hakt es?', 14, SOFT, False, 2)])
    tbox(s, 0.45, 6.3, 12.4, 0.7, [('Warum das bei stetiger Veränderung hilft: Ein Jahresziel ist oft nach wenigen Monaten überholt. Mit OKR plant ihr so weit, wie ihr sicher sehen könnt, und passt alle paar Wochen an.', 14, PURPLE, True, 0)])


def okr_wie():
    s = blank_title('OKR in vier Schritten')
    rows = [('Objective finden', 'Was ist in den nächsten drei Monaten das Wichtigste? Formuliert das Ziel gemeinsam mit dem Team.'),
            ('Key Results festlegen', 'Zwei bis vier messbare Ergebnisse. Sie beschreiben die Wirkung, nicht die Aufgaben.'),
            ('In Sprints arbeiten', 'Alle zwei bis drei Wochen: Was haben wir geschafft? Was ist der nächste Schritt? Dazwischen kurze Stand-ups.'),
            ('Auswerten und neu setzen', 'Nach drei Monaten: Was haben wir erreicht? Was lernen wir daraus? Dann folgt das nächste OKR.')]
    for i, (h, t) in enumerate(rows):
        y = 1.3 + i * 1.22
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.45), Inches(y), Inches(0.62), Inches(0.62))
        o.fill.solid(); o.fill.fore_color.rgb = PURPLE; o.line.fill.background(); o.shadow.inherit = False
        tf = o.text_frame; tf.margin_left = tf.margin_right = 0; pp = tf.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER
        r = pp.add_run(); r.text = str(i + 1); r.font.size = Pt(20); r.font.bold = True; r.font.color.rgb = WHITE
        tbox(s, 1.3, y - 0.02, 5.75, 1.15, [(h, 19, DARK, True, 0), (t, 14, SOFT, False, 3)])
    tbox(s, 0.45, 6.25, 6.6, 0.7, [('Im Führungskorridor gibt das Ziel die Richtung. Das OKR ist die nächste Etappe dorthin.', 14, PURPLE, True, 0)])
    card(s, 7.45, 1.3, 5.43, 5.65, DARK)
    L = RGBColor(0xD6, 0xB4, 0xFF)
    tbox(s, 7.8, 1.6, 4.8, 5.2, [('EIN BEISPIEL', 13, L, True, 0),
                                 ('Objective', 13, L, True, 14), ('Unser Team arbeitet sicher mit dem neuen System.', 20, WHITE, True, 2),
                                 ('Key Results', 13, L, True, 16),
                                 ('Alle acht im Team haben die Schulung bis 15. November abgeschlossen.', 15, WHITE, False, 4),
                                 ('Die Rückfragen an den Support halbieren sich bis Ende Dezember.', 15, WHITE, False, 8),
                                 ('Jede Woche zeigt eine Person im Stand-up einen Kniff, der ihr Zeit spart.', 15, WHITE, False, 8),
                                 ('Kein Key Result: „Schulung anbieten“. Das ist eine Aufgabe, keine Wirkung.', 13, L, False, 16)])


# ---------- Inhalt ----------
haufe_title('Das erste Mal führen 1', 'Vom Rollenwechsel bis zu ersten Führungsgesprächen: dein Fundament für einen erfolgreichen Start in die Führung', 'image10.jpg')
trainer()
agenda('Tag 1', [('09:00', 'Ankommen'), ('09:45', 'Die Veränderungskurve'), ('10:30', 'Perspektivwechsel'),
                 ('11:30', 'Erwartungen klären'), ('13:30', 'Dein Führungskorridor und OKR'), ('15:30', 'Fünf Grundbedürfnisse'),
                 ('16:15', 'Psychologische Sicherheit'), ('17:00', 'Ende')],
       '10:15-10:30 Uhr, 15:15-15:30 Uhr', '12:30-13:30 Uhr')
box('Ankommen im Raum', 'Stellt euch im Halbkreis auf, sortiert nach eurer Führungserfahrung. Ganz links steht, wer noch in Vorbereitung auf die Rolle oder ganz frisch dabei ist. Ganz rechts steht, wer am längsten führt.',
    'Sprecht miteinander, bis die Reihenfolge stimmt.', None, 'ca. 5 Minuten')
box('Wer bist du, was erwartest du?', 'Stell dich der Gruppe kurz vor:',
    'Welche Rolle hast du? Wie viele Mitarbeitende führst du? Was muss hier passieren, damit sich die zwei Tage für dich wirklich gelohnt haben?', 'Schreib deine Erwartungen dabei als Hashtag an das Flipchart, zum Beispiel #KritikgesprächeFühren.', 'ca. 1 bis 2 Minuten pro Person')

chapter(1, 'Die Veränderungskurve')
foto('Die Veränderungskurve', ['veraenderungskurve'], [
    p('Jede Veränderung löst Gefühle aus: Schock, Widerstand, Verunsicherung, dann Ausprobieren und neue Sicherheit.'),
    p('Wer neu führt, ist selbst mitten in dieser Kurve. Und das Team auch.'),
    p('Wo steht dein Team gerade? Und wo stehst du?', 19, PURPLE, True, 20)])
pause('coffee', 'Kaffeepause', '10:15 bis 10:30 Uhr')

chapter(2, 'Perspektivwechsel')
steps('Du bekommst eine neue Führungskraft', '1-2-4-alle', '20 Min.', [
    ('Allein', 'Stell dir vor, du bist Mitarbeiterin oder Mitarbeiter und bekommst morgen eine neue Führungskraft. Was geht dir durch den Kopf? Notiere deine Fragen.', '2 Minuten'),
    ('Zu zweit', 'Tauscht euch aus. Was habt ihr beide? Was ergänzt ihr?', '3 Minuten'),
    ('Zu viert', 'Wählt die Fragen, die euch am wichtigsten sind. Eine Frage pro Karte.', '5 Minuten'),
    ('Alle', 'Wir hängen die Karten an die Pinnwand und sortieren sie gemeinsam.', '10 Minuten')])
foto('Was passiert mit dem Team?', ['perspektivwechsel_pinnwand'], [
    p('Eine neue Führungskraft löst bei Mitarbeitenden viel aus: Sorgen und Fragen, aber auch Hoffnung und Chancen.'),
    p('Eure Pinnwand zeigt, was dein Team gerade beschäftigen könnte, auch wenn es niemand ausspricht.'),
    p('Welche Frage beantwortest du deinem Team zuerst?', 19, PURPLE, True, 20)])
foto('Die Teamuhr', ['teamuhr'], [
    p('Mit einer neuen Führungskraft startet das Team neu, auch wenn sich alle schon lange kennen.'),
    p('Forming: Wir finden uns. Storming: Wir ringen um Rollen. Norming: Wir einigen uns. Performing: Wir arbeiten gut zusammen.'),
    p('Im Storming helfen klare Regeln und Rollenklarheit.', 19, PURPLE, True, 20)])

chapter(3, 'Erwartungen klären')
foto('Das Erwartungsgespräch', ['erwartungsgespraech'], [
    p('Unser Fahrplan vom Flipchart: vorab einladen und um eigene Erwartungen bitten, dann die eigenen Erwartungen konkret klären.'),
    p('Offene Fragen klären, Ziele und Aufgaben besprechen, nach Unterstützung und Ideen fragen.'),
    p('Und vor allem: den Menschen kennenlernen. Was hat er schon gemacht? Was liegt ihm?', 19, PURPLE, True, 20)])
pause('lunch', 'Mittagspause', '12:30 bis 13:30 Uhr')

chapter(4, 'Dein Führungskorridor')
foto('Dein Führungskorridor', ['fuehrungskorridor'], [
    p('Der Korridor ist der Rahmen, in dem dein Team selbstständig arbeiten kann.'),
    p('Ziel: Wohin wollen wir?'), p('Erwartungen: Was braucht es dafür?', before=4),
    p('Werte und Prinzipien: Wie arbeiten wir zusammen?', before=4), p('Kommunikation: Wie bleiben wir im Gespräch?', before=4),
    p('Je klarer der Korridor, desto mehr Freiraum hat dein Team.', 19, PURPLE, True, 20)])
foto('Eure Erwartungswand', ['erwartungswand'], [
    p('Was erwartest du an dich selbst? An deine Mitarbeitenden? An deinen Chef?'),
    p('Eure Wand zeigt: Viele Erwartungen sind sich ähnlich. Ausgesprochen werden sie selten.'),
    p('Sprich deine Erwartungen aus, in beide Richtungen. Das ist der Kern deines Korridors.', 19, PURPLE, True, 20)])
foto('Kurzfristige Ziele mit OKR', ['okr'], [
    p('Wenn sich ständig etwas verändert, tragen Jahresziele oft nicht weit.'),
    p('Objectives and Key Results setzen Ziele für drei Monate. Gearbeitet wird in Sprints von drei Wochen, mit kurzen Stand-ups dazwischen.'),
    p('So bleibt das Ziel im Korridor klar, und der Weg dorthin darf sich anpassen.', 19, PURPLE, True, 20)])
okr_was()
okr_wie()

chapter(5, 'Fünf Grundbedürfnisse')
needs_overview()
POSTER = [('Bindung', ['bindung']), ('Orientierung und Kontrolle', ['kontrolle_orientierung']), ('Selbstwert', ['selbstwert']),
          ('Lustgewinn und Unlustvermeidung', ['unlust']), ('Kohärenz', ['kohaerenz', 'kohaerenz_kreise'])]
for _i, _img in enumerate(['image101.png', mirrored('image17.jpg'), mirrored('image10.jpg'), mirrored('image6.jpg'), mirrored('image11.jpg')]):
    need_detail(_i, _img)
    _name, _imgs = POSTER[_i]
    if len(_imgs) == 1:
        foto('Euer Plakat: ' + _name, _imgs, [
            p('Was stärkt dieses Bedürfnis im Team? Was verletzt es? Eure Ideen aus der Gruppenarbeit.'),
            p('Wähle eine Idee aus, die du ab Montag umsetzt.', 19, PURPLE, True, 20)])
    else:
        foto('Euer Plakat: ' + _name, _imgs, [
            p('Kohärenz heißt: Was ich tue, passt zu dem, was mir wichtig ist.', 17),
            p('Private Welt, Ausbildung und berufliche Welt: Je mehr sich überschneidet, desto stimmiger fühlt sich die Arbeit an.', 17, DARK, False, 12),
            p('Wo passt es bei deinem Team, wo nicht?', 17, PURPLE, True, 16)])
ps_slides()
foto('Unser Flipchart: drei Seiten der Sicherheit', ['psychologische_sicherheit'], [
    p('Psychologische Sicherheit steht auf drei Seiten: Vertrauen, Verantwortung und Verletzlichkeit.'),
    p('Wer als Führungskraft selbst Fehler zugibt, macht es für alle leichter.'),
    p('Wie reagierst du, wenn jemand einen Fehler meldet?', 19, PURPLE, True, 20)])

agenda('Tag 2', [('09:00', 'Ankommen'), ('09:15', 'Können und Wollen'), ('10:30', 'Auf Augenhöhe und offene Fragen'),
                 ('13:30', 'Gespräche führen'), ('14:30', 'Schwierige Gespräche'), ('16:30', 'Dein Begleitraum und Abschluss'),
                 ('17:00', 'Ende')],
       '10:15-10:30 Uhr, 15:15-15:30 Uhr', '12:30-13:30 Uhr')

chapter(6, 'Können und Wollen')
task('group', 'Euer Führungsverhalten', 'image10.jpg',
     [('p', 'Jede Gruppe übernimmt ein Feld der Matrix. Überlegt gemeinsam:'),
      ('b', 'Wie führe ich eine Person in diesem Feld?'), ('b', 'Was braucht sie von mir? Was hilft ihr nicht?'),
      ('b', 'Welches Beispiel aus eurem Alltag passt dazu?'),
      ('p', 'Schreibt eure Ergebnisse auf das Plakat. Danach stellt jede Gruppe in drei Minuten vor.')],
     '20 Minuten in Gruppen, dann Vorstellung')

chapter(7, 'Auf Augenhöhe und offene Fragen')
task('group', 'Die Matrix ergänzen', shifted('image8.jpg', 0.18),
     [('p', 'Ihr geht zurück zu eurem Plakat aus dem Vormittag. Ergänzt euer Feld:'),
      ('b', 'Welche offenen Fragen stelle ich einer Person in diesem Feld?'), ('b', 'Was will ich von ihr eigentlich wissen?'),
      ('p', 'Nutzt Fragen, die mit einem W-Wort beginnen.')],
     '10 Minuten in Gruppen')
foto('Eure Matrix: Können und Wollen', ['skill_will'], [
    p('Vier Felder, vier Arten zu führen. Farbig: was eine Person in diesem Feld von dir braucht. Weiß: eure offenen Fragen dazu.'),
    p('Denk an eine Person aus deinem Team: In welchem Feld steht sie bei ihrer wichtigsten Aufgabe?', 19, PURPLE, True, 20)])

chapter(8, 'Gespräche führen')
foto('Der Eisberg', ['eisberg'], [
    p('Nur rund 20 Prozent eines Gesprächs laufen über Worte.'),
    p('Darunter wirken Stimmlage, Werte und Erfahrungen. Bei dir und bei deinem Gegenüber.'),
    p('Deshalb: nachfragen statt deuten.', 19, PURPLE, True, 20)])
foto('Das GROW-Modell', ['grow'], [
    p('Goal: Was ist das Ziel?'), p('Reality: Wie ist die Lage gerade?', before=4),
    p('Opportunities: Welche Möglichkeiten gibt es?', before=4), p('Way: Was ist der nächste Schritt?', before=4),
    p('So findet dein Gegenüber den eigenen Weg. Das stärkt Selbstreflexion, Flexibilität und Antrieb.'),
    p('Du fragst, dein Gegenüber denkt.', 19, PURPLE, True, 20)])

chapter(9, 'Schwierige Gespräche')
johari()
steps('Dein blinder Fleck', 'Zu zweit', '12 Min.', [
    ('Allein', 'Wie möchtest du als Führungskraft wirken? Notiere drei Eigenschaften.', '2 Minuten'),
    ('Fragen', 'Frag dein Gegenüber: Wie hast du mich in diesen zwei Tagen erlebt? Was fällt dir an mir auf?', '3 Minuten'),
    ('Vergleichen', 'Was passt zu deinem Bild? Was überrascht dich? Dann tauscht ihr die Rollen.', '3 Minuten'),
    ('Mitnehmen', 'Wen in deinem Team fragst du als Erstes nach Feedback? Formuliere deine Frage.', '4 Minuten')])
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
qr_slide()
end('Danke für zwei starke Tage', 'Dein Startplan und die Satzstarter bleiben im Begleitraum für dich offen. Ich wünsche dir einen guten Start in deiner Rolle.')

ids = list(prs.slides._sldIdLst)
for sid in ids[:len(orig)]:
    prs.part.drop_rel(sid.rId)
    prs.slides._sldIdLst.remove(sid)
for _s in prs.slides:
    for _sh in list(_s.shapes):
        if 'Slide Number' in _sh.name or 'Foliennummer' in _sh.name:
            _sh._element.getparent().remove(_sh._element)
prs.save(OUT)
print('Folien:', len(prs.slides))
