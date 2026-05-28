from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# ── Page margins
for section in doc.sections:
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

# ── Color palette
RED    = RGBColor(0xC0, 0x39, 0x2B)
DARK   = RGBColor(0x1A, 0x1A, 0x2E)
GRAY   = RGBColor(0x55, 0x55, 0x55)
LGRAY  = RGBColor(0x99, 0x99, 0x99)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GOLD   = RGBColor(0xD4, 0xAA, 0x00)

# ══════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════
def centered(doc, text, size=11, bold=False, color=DARK, italic=False, space_before=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    r = p.add_run(text)
    r.bold = bold; r.italic = italic
    r.font.size = Pt(size); r.font.color.rgb = color
    return p

def heading1(doc, text):
    """Red chapter heading"""
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run(text.upper())
    r.bold = True; r.font.size = Pt(14); r.font.color.rgb = RED
    p2 = doc.add_paragraph()
    p2.add_run("━" * 65).font.color.rgb = LGRAY

def heading2(doc, text):
    """Section heading"""
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True; r.font.size = Pt(12); r.font.color.rgb = DARK

def part_header(doc, number, title, timecode):
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run(f"PART {number} — {title}  [{timecode}]")
    r.bold = True; r.font.size = Pt(11); r.font.color.rgb = RED
    doc.add_paragraph().add_run("─" * 55).font.color.rgb = LGRAY

def note(doc, text):
    p = doc.add_paragraph()
    r = p.add_run(f"[{text}]")
    r.italic = True; r.font.size = Pt(9); r.font.color.rgb = LGRAY

def body(doc, text):
    for line in text.strip().split("\n"):
        line = line.strip()
        p = doc.add_paragraph() if not line else doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(line)
        r.font.size = Pt(10.5)

def tag_block(doc, label, content):
    p = doc.add_paragraph()
    r1 = p.add_run(f"{label}: ")
    r1.bold = True; r1.font.size = Pt(10)
    r2 = p.add_run(content)
    r2.font.size = Pt(10); r2.font.color.rgb = GRAY

def divider(doc):
    p = doc.add_paragraph()
    r = p.add_run("═" * 65)
    r.font.color.rgb = LGRAY; r.font.size = Pt(9)

# ══════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()
doc.add_paragraph()
centered(doc, "⚔  WWII FACELESS CHANNEL", 13, bold=True, color=RED)
doc.add_paragraph()
centered(doc, "COMPLETE PRODUCTION PACKAGE", 22, bold=True, color=DARK)
centered(doc, "Scripts · SEO · Thumbnails", 13, italic=True, color=GRAY)
doc.add_paragraph()
divider(doc)
doc.add_paragraph()
centered(doc, "4 VIDEOS  |  8 FULL SCRIPTS  |  3 SEO PACKAGES  |  2 THUMBNAIL BRIEFS", 10, color=GRAY)
doc.add_paragraph()
divider(doc)
doc.add_paragraph()

videos = [
    ("VIDEO 1", "What If D-Day Had Failed?",                         "EN + ES scripts"),
    ("VIDEO 2", "Operation Barbarossa: The Decision That Doomed...", "EN + ES scripts · SEO · Thumbnail"),
    ("VIDEO 3", "Battle of Stalingrad: How 300,000 Germans...",      "EN script · SEO"),
    ("VIDEO 4", "Inside Hitler's Bunker: The Last 10 Days...",       "EN script · SEO · Thumbnail"),
]
for v, title, assets in videos:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run(f"{v}  "); r1.bold = True; r1.font.color.rgb = RED; r1.font.size = Pt(10)
    r2 = p.add_run(f"{title}"); r2.font.size = Pt(10); r2.font.color.rgb = DARK
    r3 = p.add_run(f"  [{assets}]"); r3.font.size = Pt(9); r3.italic = True; r3.font.color.rgb = LGRAY

doc.add_paragraph()
centered(doc, "ElevenLabs Settings: Speed 0.93 · Stability 0.75 · Clarity 0.80", 9, italic=True, color=LGRAY)
centered(doc, 'Recommended Voices: EN → "Daniel" or "Antoni"  |  ES → "Mateo" or "Sergio"', 9, italic=True, color=LGRAY)
doc.add_page_break()

# ══════════════════════════════════════════════
# VIDEO 1 — D-DAY
# ══════════════════════════════════════════════
heading1(doc, "VIDEO 1 — WHAT IF D-DAY HAD FAILED?")
centered(doc, "How Hitler Would Have Won the War", 13, bold=True, color=DARK)
centered(doc, "~1,420 words  |  ~10:50 min  |  Formula: Counterfactual", 9, italic=True, color=GRAY)
doc.add_paragraph()

# EN Script
heading2(doc, "SCRIPT — ENGLISH (AMERICAN)")
divider(doc)

parts_dday_en = [
    (1, "COLD OPEN", "0:00 – 0:45",
     "B-roll: Omaha Beach archival footage, landing craft, bodies in surf",
     """It is 6:30 in the morning on June 6th, 1944.

Off the coast of Normandy, 156,000 Allied soldiers are crossing the Channel. Behind them, the largest naval armada ever assembled... 6,939 ships. Above them, 11,590 aircraft. The plan has taken two years to build. The logistics alone required moving the equivalent of a small nation across open water.

And in the first four hours... it is going catastrophically wrong.

On Omaha Beach, American troops are being cut down the moment they step off the landing craft. German gun positions the planners believed had been destroyed... are intact. And firing. In some sectors, entire companies are wiped out before they reach the waterline. By mid-morning, the commanding general is composing a message recommending evacuation.

What no one in that moment can know... is how close the entire operation actually is to total collapse.

And what no one has ever fully asked... is what happens to the world if it does."""),

    (2, "THE PROMISE", "0:45 – 1:30", None,
     """History remembers D-Day as a triumph. A story of Allied resolve overcoming the Atlantic Wall. The turning point that broke Nazi Germany.

But that story skips the part where it almost didn't happen.

In this video, we're going to do something most D-Day documentaries refuse to do... we're going to follow the failure. We're going to trace exactly what would have happened, chain link by chain link, if the Allies had been driven back into the sea on June 6th, 1944.

Because this isn't just a war game thought experiment. The consequences of a failed D-Day reach into 1945... into the atomic program... into Stalin's calculations... into the Holocaust... into the entire postwar world order.

The reality is this. A failed Normandy landing would not simply have delayed Allied victory. It may have fundamentally changed the kind of world we live in today."""),

    (3, "CONTEXT", "1:30 – 3:30",
     "Map animation: Normandy vs Pas-de-Calais, 15th Army position, Panzer reserve locations",
     """By June 1944, the war has been running for nearly five years. Germany is under pressure on every front... but it is not broken.

In the East, the Soviet Union has pushed the Wehrmacht back nearly 800 kilometers from its 1942 high-water mark. But Army Group Centre still holds a massive defensive salient in Belarus. The Eastern Front is costing Germany 900 men a day... and costing the Soviets three times that.

Three men hold the outcome of D-Day in their hands.

Dwight D. Eisenhower. Supreme Commander of Allied forces. A man who has never personally commanded troops in combat, chosen not for battlefield brilliance... but for the political skill to hold a fractious coalition together.

Erwin Rommel. Commanding Army Group B. He believes the invasion must be defeated on the beaches themselves... within the first 24 hours. If the Allies get off the sand, he tells his staff... they will never be pushed back.

And Adolf Hitler. Who controls the Panzer reserve. Three armored divisions sitting within striking distance of Normandy. Hitler alone holds the release authority.

And on the morning of June 6th... he is asleep."""),

    (4, "THE BUILD", "3:30 – 6:00", None,
     """Operation Fortitude has convinced the German high command that Normandy is a feint. A fictional army group, commanded by General Patton himself, has been constructed entirely from fake radio signals and inflatable tanks. This holds 19 German divisions frozen at Calais.

When the first wave of American troops lands at Omaha at 6:30 AM, they walk into pre-sighted killing grounds. 27 of 29 amphibious tanks sink before reaching the shore. American casualties exceed 2,000 men in the first two hours.

General Omar Bradley orders the landings halted.

By 11:00 AM, the surviving forces on Omaha Beach begin withdrawing to the water. Without Omaha, the landing zone has a 30-kilometer gap in the middle.

Rommel recognizes it immediately. He picks up the phone to OKW headquarters. He doesn't ask for the Panzers anymore. He demands them."""),

    (5, "MID-ROLL RE-HOOK", "6:00 – 6:30",
     "Music cue: shift to darker, minor-key score",
     """In just a moment, we're going to see what happens when those Panzer divisions hit the exposed Allied flanks... and we're going to follow the chain of consequences all the way to 1945... and a decision that would have rewritten the entire postwar world.

Stay with us."""),

    (6, "THE CLIMAX", "6:30 – 10:00",
     "Slow narration — let dramatic lines breathe",
     """At 2:00 PM on June 6th, Hitler wakes up. Normandy is repelling the landings. The Führer is delighted. He releases two Panzer divisions.

By June 12th, the last Allied forces are evacuating Normandy. Total Allied casualties... 28,000 dead. 40,000 wounded or captured.

In Moscow, Stalin receives the news with cold fury. His foreign minister Molotov begins quiet talks with German intermediaries in Stockholm.

In New Mexico, the Manhattan Project approaches completion. The first atomic bomb will be ready by July 1945. In this altered timeline... it will not be used against Japan.

On August 6th, 1945... a city burns. Not Hiroshima. Hamburg."""),

    (7, "AFTERMATH & LEGACY", "10:00 – 12:30",
     "Map animation: alternate Iron Curtain line at the French border",
     """The atomic bombing of Hamburg ends German resistance within three weeks. Germany surrenders on September 2nd, 1945.

But the map of Europe looks nothing like the one we know. The Red Army reaches Berlin and continues west. Soviet forces stand on the Rhine.

The Iron Curtain does not fall at the Elbe. It falls at the French border. The Cold War begins with the Soviet Union controlling 70% of the European continent's industrial capacity.

All of it... every institution of the postwar liberal order... flows from those first six hours on the beaches of Normandy."""),

    (8, "CLOSING HOOK", "12:30 – 13:30", None,
     """D-Day succeeded because of deception. Because of courage. But also... because of luck. Because Hitler was asleep. Because the 352nd Division moved without Allied intelligence noticing.

Remove any one of those factors... and the chain breaks differently.

Next week, we're going inside the intelligence operation that made Normandy possible — Operation Fortitude... and the single agent whose false reports kept 19 German divisions frozen at Calais on June 6th.

If that story sounds impossible... subscribe, and I'll show you the documents."""),
]

for num, title, tc, prod_note, text in parts_dday_en:
    part_header(doc, num, title, tc)
    if prod_note:
        note(doc, prod_note)
    body(doc, text)

doc.add_page_break()

# ES Script D-Day
heading2(doc, "SCRIPT — SPANISH (LATIN AMERICAN)")
divider(doc)

parts_dday_es = [
    (1, "COLD OPEN", "0:00 – 0:45",
     "B-roll: imágenes de archivo Playa Omaha, lanchas de desembarco",
     """Son las 6:30 de la madrugada del 6 de junio de 1944.

Frente a las costas de Normandía, 156,000 soldados aliados cruzan el Canal de la Mancha. Detrás de ellos, la armada naval más grande jamás reunida... 6,939 barcos. Sobre ellos, 11,590 aviones.

Y en las primeras cuatro horas... está saliendo catastróficamente mal.

En la Playa Omaha, los soldados americanos están siendo abatidos en el momento en que bajan de las lanchas. Las posiciones alemanas que los planificadores creían destruidas... están intactas. Y disparando.

Lo que nadie en ese momento puede saber... es cuán cerca está la operación entera de un colapso total. Y lo que nadie se ha preguntado realmente... es qué le ocurre al mundo si eso sucede."""),

    (2, "THE PROMISE", "0:45 – 1:30", None,
     """La historia recuerda el Día D como un triunfo. Una historia de determinación aliada venciendo al Muro del Atlántico.

Pero esa historia omite la parte en que casi no sucede.

En este video, vamos a hacer algo que la mayoría de los documentales sobre el Día D se niegan a hacer... vamos a seguir el fracaso. Vamos a rastrear exactamente lo que habría ocurrido, eslabón por eslabón, si los Aliados hubieran sido rechazados al mar el 6 de junio de 1944.

La realidad es esta. Un desembarco fallido en Normandía podría haber cambiado fundamentalmente el tipo de mundo en que vivimos hoy."""),

    (3, "CONTEXTO", "1:30 – 3:30",
     "Animación de mapa: Normandía vs Pas-de-Calais, reserva Panzer",
     """En junio de 1944, la guerra lleva casi cinco años en marcha. Alemania está bajo presión en todos los frentes... pero no está quebrada.

Tres hombres tienen el destino del Día D en sus manos.

Dwight D. Eisenhower. Comandante Supremo. Elegido por su habilidad política para mantener unida una coalición fracturada.

Erwin Rommel. Cree que la invasión debe ser derrotada en las playas mismas... dentro de las primeras 24 horas.

Y Adolf Hitler. Quien controla la reserva Panzer. Tres divisiones blindadas a distancia de ataque de Normandía. Solo Hitler tiene la autoridad para liberarlas. Y en la mañana del 6 de junio... está dormido."""),

    (4, "THE BUILD", "3:30 – 6:00", None,
     """La Operación Fortitude ha convencido al alto mando alemán de que Normandía es una maniobra de distracción. Esto mantiene 19 divisiones congeladas en Calais.

Las bajas americanas en Omaha superan los 2,000 hombres en las primeras dos horas. El General Omar Bradley ordena detener los desembarcos.

A las 11:00 AM, las fuerzas supervivientes en la Playa Omaha comienzan a retirarse hacia el agua. La zona de desembarco tiene una brecha de 30 kilómetros en el centro.

Rommel toma el teléfono para llamar al OKW. Ya no pide los Panzer. Los exige."""),

    (5, "MID-ROLL RE-HOOK", "6:00 – 6:30",
     "Cue musical: cambio a partitura en menor",
     """En un momento, veremos qué ocurre cuando esas divisiones Panzer golpean los flancos aliados expuestos... y seguiremos la cadena de consecuencias hasta 1945.

Quédense con nosotros."""),

    (6, "EL CLÍMAX", "6:30 – 10:00",
     "Narración lenta — deja que cada línea impacte",
     """A las 2:00 PM del 6 de junio, Hitler se despierta. Normandía está rechazando los desembarcos. El Führer está encantado. Libera dos divisiones Panzer.

El 12 de junio, las últimas fuerzas aliadas evacúan Normandía. 28,000 muertos. 40,000 heridos o capturados.

En Moscú, Stalin recibe la noticia con fría furia. Molotov inicia conversaciones con intermediarios alemanes en Estocolmo.

El 6 de agosto de 1945... una ciudad arde. No Hiroshima. Hamburgo."""),

    (7, "AFTERMATH & LEGACY", "10:00 – 12:30",
     "Animación de mapa: Telón de Acero alternativo en la frontera francesa",
     """El bombardeo atómico de Hamburgo termina con la resistencia alemana en tres semanas.

El Ejército Rojo llega a Berlín y continúa hacia el oeste. El Telón de Acero no cae en el Elba. Cae en la frontera francesa.

La Guerra Fría comienza con la Unión Soviética controlando el 70% de la capacidad industrial del continente europeo."""),

    (8, "CLOSING HOOK", "12:30 – 13:30", None,
     """El Día D tuvo éxito gracias al engaño. Al coraje. Pero también... a la suerte.

El margen entre el mundo que obtuvimos... y uno más oscuro... fue, en los momentos críticos, extremadamente delgado.

La próxima semana, entraremos en la Operación Fortitude... y el único agente cuyos informes falsos mantuvieron a 19 divisiones alemanas congeladas en Calais.

Suscríbanse, y les mostraré los documentos."""),
]

for num, title, tc, prod_note, text in parts_dday_es:
    part_header(doc, num, title, tc)
    if prod_note:
        note(doc, prod_note)
    body(doc, text)

doc.add_page_break()

# ══════════════════════════════════════════════
# VIDEO 2 — BARBAROSSA
# ══════════════════════════════════════════════
heading1(doc, "VIDEO 2 — OPERATION BARBAROSSA")
centered(doc, "The Decision That Doomed Nazi Germany", 13, bold=True, color=DARK)
centered(doc, "~1,480 words  |  ~11:22 min  |  Formula: Hidden Truth + Worst Mistake", 9, italic=True, color=GRAY)
doc.add_paragraph()

heading2(doc, "SCRIPT — ENGLISH (AMERICAN)")
divider(doc)

parts_barb_en = [
    (1, "COLD OPEN", "0:00 – 0:45",
     "B-roll: German Panzer columns, dawn light, June 22 1941 archival footage",
     """At 3:15 in the morning on June 22nd, 1941, the ground shook along a front stretching 1,800 miles.

Three million German soldiers. Three thousand tanks. Two thousand aircraft. In a single coordinated strike, the largest military invasion in the history of human warfare had begun.

Adolf Hitler called it Operation Barbarossa. He told his generals it would be over in eight weeks. The Soviet Union, he said, was a rotten structure. You had only to kick in the door... and the whole thing would come crashing down.

He was catastrophically wrong.

And what's remarkable — what history has never fully confronted — is that Hitler knew it. The warnings were there. The intelligence was clear. The math did not work. He invaded anyway."""),

    (2, "THE PROMISE", "0:45 – 1:30", None,
     """Every account of Operation Barbarossa tells you what happened. Three million men crossed the Soviet border. The Wehrmacht advanced faster than any army in history. And then — winter came, and it all fell apart.

That story is true. But it is dangerously incomplete.

In this video, we're going to examine the three decisions — made before a single tank crossed the border — that actually guaranteed Germany's defeat. Decisions rooted not in military miscalculation, but in ideology so extreme it blinded an entire command structure to reality.

Germany did not lose because of the Russian winter. Germany lost because of choices made in Berlin months before the first shot was fired."""),

    (3, "CONTEXT", "1:30 – 3:30",
     "Map animation: German front lines, Soviet territory, strategic resources",
     """By the summer of 1941, Adolf Hitler stands at the peak of his power. France has fallen. Britain has been driven from the continent. Europe belongs to the Third Reich.

And yet Hitler is afraid. Germany imports 74% of its oil. In Hitler's mind, the solution lies East. Ukraine's wheat. The Caucasus oil. The industrial Urals. Conquest of the Soviet Union is not merely a military objective. It is racial and economic destiny.

Field Marshal von Brauchitsch privately believes Barbarossa is a catastrophic mistake — and lacks the courage to say so to Hitler's face. General Franz Halder has wargamed the operation and reached a conclusion he buries in his diary: Germany cannot win a prolonged war against the Soviet Union. He signs the operational orders anyway.

On the other side: 196 million Soviets ruled by Stalin, who has received 84 separate intelligence warnings of the German invasion and dismissed every one. On the morning of June 22nd, Soviet border troops cannot reach their commanders. The phone lines have been cut."""),

    (4, "THE BUILD", "3:30 – 6:00", None,
     """In the first weeks, everything confirms Hitler's prediction. Army Group Centre advances 200 miles in ten days. The Wehrmacht captures more prisoners in six weeks than in all of World War One. Hitler is euphoric.

But three decisions are working quietly against him.

First: instead of concentrating on Moscow, Hitler divides into three simultaneous thrusts. His generals beg him to concentrate. He refuses. No thrust is ever strong enough to deliver a knockout blow.

Second: the Commissar Order. Soviet political officers are to be shot immediately. German occupation runs on systematic starvation and terror. Soviet soldiers who might have surrendered stop surrendering. Every citizen becomes a partisan.

Third: the logistics are built for eight weeks. By October, trucks break down on roads that are barely roads. Rail lines must be re-gauged kilometer by kilometer. Fuel runs short. Winter clothing — never ordered — does not exist. By October 1941, German soldiers are writing home asking their families to send warm socks."""),

    (5, "MID-ROLL RE-HOOK", "6:00 – 6:30",
     "Music cue: tension builds",
     """In a moment, we're going to look at the exact week when German commanders first understood they had entered a war they could not win. And at the single order Hitler gave in December 1941 that sealed the fate of the Third Reich.

Stay with us."""),

    (6, "THE CLIMAX", "6:30 – 10:00",
     "Slow narration — let each line land",
     """On December 2nd, 1941, a German reconnaissance unit reaches Khimki. From there, on a clear day, you can see the spires of the Kremlin. They are turned back the following morning.

Four days after Pearl Harbor, Hitler declares war on the United States. Voluntarily. He is not required to under his treaty with Japan.

On December 5th, Marshal Zhukov launches a Soviet counteroffensive along a 560-mile front. Fresh Siberian divisions smash into exhausted, frostbitten German units that have been fighting without rest for 167 days. The German front shatters.

Hitler fires 35 senior commanders in two months. Then appoints himself Commander-in-Chief of the German Army. A man with no formal military education. A man who has never commanded a regiment in battle.

General Halder writes in his diary on December 19th: "This so-called leadership is characterized by a pathological reaction to momentary impressions and a total lack of understanding of the command structure."

By December 31st, 1941, Germany has suffered 830,000 casualties. Against an enemy Hitler promised would collapse in eight weeks."""),

    (7, "AFTERMATH & LEGACY", "10:00 – 12:30",
     "Map animation: German advance then retreat, 1941–1945",
     """The Eastern Front consumed 80% of all German military casualties. Of 5.3 million German soldiers who died in World War Two, 4.2 million died fighting the Soviet Union. The Soviet Union lost 27 million people — one in seven Soviet citizens.

Germany gained nothing. Not the oil. Not the wheat. Not the Lebensraum.

Historian Richard Evans concludes Barbarossa was "the greatest single military mistake in the history of modern warfare." Not because Germany was weaker — in 1941, Germany was arguably stronger. But because the decision was made on ideological premises with no relationship to military reality."""),

    (8, "CLOSING HOOK", "12:30 – 13:30", None,
     """Operation Barbarossa began with three million soldiers and absolute confidence. It ended with 830,000 casualties before the first winter was over and a war Germany had no mathematical possibility of winning.

The lesson: no military strength compensates for decisions built on ideology instead of reality. The most dangerous moment in any organization is when the person in command stops being able to hear what they don't want to hear.

Next week, we're inside the Soviet response — 1,500 factories moved east of the Urals in ninety days. The logistical achievement that made the Soviet comeback possible.

Subscribe. That story is one you will not find in any mainstream documentary."""),
]

for num, title, tc, prod_note, text in parts_barb_en:
    part_header(doc, num, title, tc)
    if prod_note:
        note(doc, prod_note)
    body(doc, text)

doc.add_page_break()

heading2(doc, "SCRIPT — SPANISH (LATIN AMERICAN)")
divider(doc)

parts_barb_es = [
    (1, "COLD OPEN", "0:00 – 0:45",
     "B-roll: columnas de Panzers alemanes, amanecer del 22 de junio de 1941",
     """A las 3:15 de la madrugada del 22 de junio de 1941, la tierra tembló a lo largo de un frente de 1,800 millas.

Tres millones de soldados alemanes. Tres mil tanques. Dos mil aviones. La invasión militar más grande en la historia de la humanidad había comenzado.

Adolf Hitler la llamó Operación Barbarroja. Le dijo a sus generales que estaría terminada en ocho semanas. La Unión Soviética, decía, era una estructura podrida. Solo había que patear la puerta... y todo se desmoronaría.

Estaba catastróficamente equivocado. Y lo extraordinario es que Hitler lo sabía. Las advertencias estaban ahí. Los números no cuadraban. Invadió de todas formas."""),

    (2, "THE PROMISE", "0:45 – 1:30", None,
     """Cada relato sobre la Operación Barbarroja te cuenta lo que pasó. Pero esa historia está peligrosamente incompleta.

Vamos a examinar las tres decisiones — tomadas antes de que un solo tanque cruzara la frontera — que garantizaron la derrota de Alemania. Decisiones enraizadas en una ideología tan extrema que cegó a toda una estructura de mando ante la realidad.

Alemania no perdió por el invierno ruso. Alemania perdió por decisiones tomadas en Berlín meses antes."""),

    (3, "CONTEXTO", "1:30 – 3:30",
     "Animación de mapa: frentes alemanes, territorio soviético, recursos estratégicos",
     """En el verano de 1941, Hitler está en la cima de su poder. Francia cayó. Gran Bretaña fue expulsada del continente. Pero Hitler tiene miedo. Alemania importa el 74% de su petróleo.

El General Franz Halder ha simulado la operación y llegado a una conclusión que entierra en su diario: Alemania no puede ganar una guerra prolongada contra la Unión Soviética. Firma las órdenes de todas formas.

Al otro lado: 196 millones de soviéticos gobernados por Stalin, quien ha recibido 84 avisos de inteligencia sobre la invasión alemana y los ha descartado todos. En la mañana del 22 de junio, las tropas fronterizas no pueden comunicarse con sus comandantes. Las líneas han sido cortadas."""),

    (4, "THE BUILD", "3:30 – 6:00", None,
     """Tres decisiones actúan silenciosamente en contra de Alemania.

Primera: en lugar de concentrar fuerzas en Moscú, Hitler divide en tres ofensivas simultáneas. Ninguna es suficientemente poderosa para asestar el golpe definitivo.

Segunda: la Orden de los Comisarios. Los prisioneros soviéticos aprenden lo que significa rendirse. Dejan de rendirse. Cada ciudadano se convierte en partisano potencial.

Tercera: la logística está construida para ocho semanas. Para octubre, los camiones se averían. El combustible escasea. La ropa de invierno no existe. Los soldados escriben a casa pidiendo calcetines de lana."""),

    (5, "MID-ROLL RE-HOOK", "6:00 – 6:30",
     "Cue musical: la tensión aumenta",
     """En un momento veremos la semana exacta en que los comandantes alemanes comprendieron que habían entrado en una guerra que no podían ganar. Y la orden de diciembre de 1941 que selló el destino del Tercer Reich.

Quédense con nosotros."""),

    (6, "EL CLÍMAX", "6:30 – 10:00",
     "Narración lenta — deja que cada línea impacte",
     """El 2 de diciembre de 1941, una unidad alemana llega a Khimki. Desde allí, en un día claro, se ven las torres del Kremlin. Son repelidos a la mañana siguiente.

El 5 de diciembre, Zhukov lanza una contraofensiva a lo largo de 560 millas. Divisiones siberianas frescas golpean a unidades alemanas agotadas que llevan 167 días combatiendo.

Hitler destituye a 35 comandantes superiores en dos meses. Luego se nombra a sí mismo Comandante en Jefe del Ejército alemán. Un hombre sin educación militar formal.

Halder escribe el 19 de diciembre: "Este llamado liderazgo se caracteriza por una reacción patológica a las impresiones del momento."

Para el 31 de diciembre: 830,000 bajas alemanas. En seis meses."""),

    (7, "AFTERMATH & LEGACY", "10:00 – 12:30",
     "Animación de mapa: avance alemán y luego retirada",
     """El Frente Oriental consumió el 80% de todas las bajas militares alemanas. 4.2 millones de los 5.3 millones de soldados alemanes muertos combatieron a la Unión Soviética. La URSS perdió 27 millones de personas — uno de cada siete ciudadanos soviéticos.

¿Y qué ganó Alemania? Nada. Ni el petróleo. Ni el trigo. Ni el Lebensraum.

El historiador Richard Evans concluye que Barbarroja fue el error militar individual mas grande en la historia de la guerra moderna."""),

    (8, "CLOSING HOOK", "12:30 – 13:30", None,
     """La Operación Barbarroja comenzó con tres millones de soldados y confianza absoluta. Terminó con 830,000 bajas antes de que acabara el primer invierno.

La lección: ninguna fortaleza militar compensa las decisiones construidas sobre ideología en lugar de realidad.

La próxima semana, entraremos en la respuesta soviética: 1,500 fábricas trasladadas al este de los Urales en noventa días.

Suscríbanse. Esa historia no la encontrarán en ningún documental convencional."""),
]

for num, title, tc, prod_note, text in parts_barb_es:
    part_header(doc, num, title, tc)
    if prod_note:
        note(doc, prod_note)
    body(doc, text)

doc.add_page_break()

# Barbarossa SEO
heading2(doc, "SEO PACKAGE — OPERATION BARBAROSSA")
divider(doc)

tag_block(doc, "OPTIMIZED TITLE", "Operation Barbarossa: The Decision That Doomed Nazi Germany  [58 chars ✓]")
doc.add_paragraph()
heading2(doc, "DESCRIPTION (publish-ready)")
body(doc, """Hitler launched the largest military invasion in history — and sealed Germany's defeat before the first winter was over.

In this documentary, we reveal the three decisions made BEFORE Operation Barbarossa began that made Nazi Germany's defeat inevitable — decisions rooted not in military error, but in ideology that overrode every military reality.

Operation Barbarossa, launched on June 22, 1941, sent 3 million German soldiers across a 1,800-mile front into the Soviet Union. Hitler promised his generals it would be over in eight weeks. What followed was the bloodiest campaign in military history — and the true turning point of World War Two.

What makes this story extraordinary is that Germany's top generals knew the invasion couldn't succeed. General Franz Halder buried his conclusions in a private diary. The Wehrmacht's own logistics were designed for eight weeks — and nothing beyond.

Historians including Richard Evans and David Stahel now argue that Barbarossa was decided not on the battlefield, but in the planning rooms of Berlin — months before a single shot was fired.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHAPTERS:
0:00  The Morning the World Changed
1:30  Why Hitler Was Afraid of Victory
3:15  The Three Men Who Knew It Would Fail
5:00  The Decision That Divided the Army
7:20  The Week Germany Lost the War
9:45  830,000 Dead — And Nothing to Show For It
11:30 The Lesson No Army Has Ever Forgotten
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SOURCES:
• "Barbarossa: Hitler's Invasion of Russia 1941" — David Stahel
• "The Third Reich at War" — Richard J. Evans
• "War Diary 1939–1942" — General Franz Halder (US National Archives)

Subscribe for a new WWII documentary every week — stories history left incomplete.

#WWII #WorldWar2 #MilitaryHistory #OperationBarbarossa #EasternFront""")

doc.add_paragraph()
tag_block(doc, "PRIMARY KEYWORD", "operation barbarossa")
tag_block(doc, "SECONDARY KEYWORDS", "eastern front ww2 · german invasion of russia · hitler military mistakes · why germany lost ww2")
tag_block(doc, "UNIVERSAL TAGS", "world war 2, ww2, wwii, world war ii, ww2 documentary, military history, history documentary, second world war, ww2 history, world war 2 documentary")
tag_block(doc, "TOPIC TAGS", "operation barbarossa, operation barbarossa documentary, hitler invasion russia, german invasion soviet union, eastern front ww2, eastern front documentary, barbarossa 1941, german army ww2, nazi germany ww2, hitler military mistakes")
tag_block(doc, "LONG-TAIL TAGS", "why did germany invade russia ww2, why did operation barbarossa fail, what was operation barbarossa, hitler biggest military mistake, why did germany lose the eastern front, german army eastern front documentary, operation barbarossa explained, why did nazi germany lose ww2, what happened during operation barbarossa, how did the soviet union survive barbarossa")
tag_block(doc, "BEST POST DATE", "Thursday June 19 — captures anniversary spike before June 22 (Barbarossa launch date)")

doc.add_page_break()

# Barbarossa Thumbnail
heading2(doc, "THUMBNAIL BRIEF — OPERATION BARBAROSSA")
divider(doc)
body(doc, """OPTION A — HIGH CTR (Face + Decision)
Background: Aerial photo of Panzer columns advancing — vast open plain, dust horizon
Foreground: Hitler in close-up high-contrast, calculating sideways look — left corner
Color grade: Desaturated near B&W with blood-red vignette on edges
Text overlay: HIS FATAL MISTAKE — Impact white, black stroke, upper right
Mood: Inevitability. The viewer feels there's no going back.

OPTION B — SCALE / MAP
Background: Vintage-style map of USSR with red arrows advancing — 1,800-mile front
Foreground: Number 3,000,000 in massive typography occupying 60% of thumbnail
Color grade: Sepia with Soviet red as accent color
Text overlay: DOOMED FROM DAY ONE
Mood: Incomprehensible scale. The viewer wants to understand the size of the mistake.

OPTION C — SPLIT SCREEN
Left side: German Panzers advancing — summer 1941, warm light, invincible force
Right side: Frozen German soldiers in snow — winter 1941, grey, defeat
Dividing element: Red arrow pointing right with text: 6 MONTHS
Text overlay: WHAT WENT WRONG
Mood: Brutal contrast between expectation and reality.

THUMBNAIL TEXT RANKING:
1. HIS FATAL MISTAKE — direct, single-person responsibility, max CTR
2. DOOMED FROM DAY ONE — implicit counterfactual, immediate curiosity
3. GERMANY'S WORST DECISION — superlative that generates comment debate
4. WHY GERMANY LOST — high organic search, answers a question viewers already have
5. 3 MILLION MEN... FOR NOTHING — number shock + tragic result

CANVA SEARCH TERMS:
• german panzer column 1941 eastern front
• hitler map room planning
• german soldiers winter eastern front 1941""")

doc.add_page_break()

# ══════════════════════════════════════════════
# VIDEO 3 — STALINGRAD
# ══════════════════════════════════════════════
heading1(doc, "VIDEO 3 — BATTLE OF STALINGRAD")
centered(doc, "How 300,000 Germans Were Trapped and Annihilated", 13, bold=True, color=DARK)
centered(doc, "~1,460 words  |  ~11:14 min  |  Formula: Inside View + Number Shock", 9, italic=True, color=GRAY)
doc.add_paragraph()

heading2(doc, "SCRIPT — ENGLISH (AMERICAN)")
divider(doc)

parts_stal = [
    (1, "COLD OPEN", "0:00 – 0:45",
     "B-roll: German soldiers in Stalingrad ruins, snow, February 1943",
     """On February 2nd, 1943, Field Marshal Friedrich Paulus emerged from the basement of a ruined department store in Stalingrad.

He had not seen daylight in weeks. He had not eaten a full meal in months. Around him, what remained of the German 6th Army — once the most powerful fighting force on the Eastern Front — was surrendering in broken groups across a frozen cityscape of rubble and corpses.

91,000 German soldiers were taken prisoner that day. Of those 91,000... fewer than 6,000 would ever see Germany again.

The Battle of Stalingrad lasted 199 days. It consumed 2 million lives. It destroyed the myth of German invincibility.

But the story that history tells about Stalingrad misses the real reason 300,000 German soldiers ended up trapped inside a frozen city with no way out. That reason was a single order. Given by one man. Against the advice of every competent military mind in Germany.

It was given not because of military necessity... but because of pride."""),

    (2, "THE PROMISE", "0:45 – 1:30", None,
     """Stalingrad is the most studied battle of World War Two. And yet the question at its center is rarely asked directly.

Why didn't the Germans break out?

They had the chance. Multiple chances. Their commanders begged for permission. The math was clear. The window was open.

Stalingrad wasn't lost on the battlefield. It was lost in a headquarters 1,200 miles away. And understanding that distinction changes everything about how we read the rest of World War Two."""),

    (3, "CONTEXT", "1:30 – 3:30",
     "Map animation: Summer 1942 German advance, Case Blue, Stalingrad position",
     """By the summer of 1942, Operation Barbarossa has failed to deliver its knockout blow. Hitler launches Case Blue — aimed at the Caucasus oil fields and the Volga River.

Standing in the way is a city on the Volga bend. A city that bears Stalin's name. Hitler does not originally plan to take Stalingrad. But as resistance stiffens, the battle takes on personal meaning for both dictators.

Stalin issues Order 227. Not one step back. Every soldier who retreats without orders faces summary execution.

The man assigned to take the city is General Friedrich Paulus — so loyal to Hitler that his staff privately call him the perfect instrument. He follows orders without question. That loyalty will destroy his army.

Opposing him: General Vasily Chuikov. He develops "hugging the enemy" — keep German forces so close to Soviet lines that the Luftwaffe cannot bomb without hitting their own men. Turn every building into a fortress. Make every room a battle.

By November 1942, the German 6th Army controls 90% of the city. What no one on the German side has noticed... is that the flanks are exposed for 300 miles on each side.

Zhukov has noticed."""),

    (4, "THE BUILD", "3:30 – 6:00", None,
     """On November 19th, 1942, Operation Uranus begins. 1.1 million Soviet soldiers attack the Romanian flanks simultaneously from north and south. The Romanians break in hours. Within four days, the two Soviet pincers meet at Kalach-on-Don.

300,000 German soldiers are encircled.

Paulus requests immediate breakout permission. The window is narrow, but open. Hitler's answer: hold position. Göring has promised the Luftwaffe can deliver 500 tons of supplies per day.

Paulus's logistics officers know the number is impossible. The realistic maximum is 100 tons. The order stands.

Field Marshal von Manstein is given a relief force. By December 19th, his panzers are just 30 miles from the pocket's edge. He sends a coded message to Paulus: break out now. Move toward us.

Paulus requests permission from Hitler to break out.

Hitler refuses."""),

    (5, "MID-ROLL RE-HOOK", "6:00 – 6:30", None,
     """In a moment, we're going to look at the final weeks inside the Stalingrad pocket — what 300,000 men experienced as temperature dropped to minus 30 and food ran out. And at the promotion Hitler gave Paulus in his final hours... and what it was designed to make him do.

Stay with us."""),

    (6, "THE CLIMAX", "6:30 – 10:00",
     "Slow narration pace — let dramatic lines breathe",
     """By January 1943, 6th Army soldiers are surviving on 50 grams of bread per day. Men are amputating frostbitten limbs without anesthesia. The Luftwaffe air bridge has delivered an average of 94 tons per day. One fifth of what Göring promised.

On January 30th, 1943 — the 10th anniversary of Hitler's rise to power — the Führer promotes Friedrich Paulus to Field Marshal.

It is the cruelest promotion in military history.

No German Field Marshal has ever surrendered. The promotion is a message. Paulus is expected to die in Stalingrad. To provide the regime with a heroic death to celebrate on the anniversary of its founding.

Paulus does not comply. On February 2nd, 1943, he surrenders. The first German Field Marshal to be taken prisoner in the war.

Hitler is reportedly speechless with rage. He tells his staff that Paulus had the opportunity for immortality, and chose personal survival instead.

The final tally: 800,000 Axis casualties. 1.1 million Soviet casualties. 91,000 German prisoners — of whom only 6,000 will survive Soviet captivity. The 6th Army has ceased to exist."""),

    (7, "AFTERMATH & LEGACY", "10:00 – 12:30",
     "Map: post-Stalingrad strategic situation, German retreat begins",
     """Joseph Goebbels declared three days of national mourning — the first time Germany publicly acknowledged a defeat. The myth of the invincible German soldier had been shattered in a single announcement.

Strategically, Stalingrad ended Germany's ability to conduct large-scale offensive operations on the Eastern Front. From February 1943 onward, the Wehrmacht would fight defensively — yielding ground, buying time, but never threatening its strategic objectives again.

Historian Antony Beevor writes that Stalingrad "represented the spiritual turning point of the war." Not just for its strategic consequences — but because of what it revealed about the regime that had caused it.

Every soldier who froze to death in January 1943 had been placed there by a command system that prioritized Hitler's prestige over military reality. A system that had fired every general capable of saying the words Hitler most needed to hear: this position cannot be held."""),

    (8, "CLOSING HOOK", "12:30 – 13:30", None,
     """300,000 German soldiers were trapped at Stalingrad not because the Soviet Army was stronger. Not because the German soldier fought poorly. And not because of the Russian winter.

They were trapped because a single man, 1,200 miles away, could not admit he had made a mistake.

The breakout window was open. Manstein was 30 miles away. Paulus had fuel and ammunition and fighting strength.

And Hitler said no.

That one word condemned 294,000 men to death or captivity. It is the most consequential "no" in military history.

Next week: Erwin Rommel and the German generals who understood by late 1943 that the war was lost — and what they chose to do about it.

Subscribe. Because the story of what the German officer corps knew — and when they knew it — is one of the most disturbing chapters of World War Two."""),
]

for num, title, tc, prod_note, text in parts_stal:
    part_header(doc, num, title, tc)
    if prod_note:
        note(doc, prod_note)
    body(doc, text)

doc.add_page_break()

heading2(doc, "SEO PACKAGE — BATTLE OF STALINGRAD")
divider(doc)
tag_block(doc, "OPTIMIZED TITLE", "Battle of Stalingrad: How 300,000 Germans Were Trapped  [54 chars ✓]")
doc.add_paragraph()
body(doc, """DESCRIPTION (publish-ready):

Hitler ordered them to hold. 300,000 German soldiers obeyed. None of them knew it was a death sentence.

In this documentary, we reveal the exact chain of decisions — from Hitler's headquarters to the frozen streets of Stalingrad — that transformed Germany's greatest army into a surrounded, starving, doomed encirclement.

The Battle of Stalingrad lasted 199 days and consumed 2 million lives on both sides. The German 6th Army was encircled by Operation Uranus on November 23rd, 1942. Three separate opportunities to break out were denied by a single order from Hitler's headquarters.

What makes Stalingrad unlike any other battle of World War Two is the collision between military reality and political will. General Paulus requested breakout permission. Field Marshal von Manstein's relief force reached within 30 miles of the pocket. The window was open. Hitler's refusal sealed the fate of 300,000 men.

Historians including Antony Beevor and David Glantz identify Stalingrad as the true strategic turning point of World War Two — not because of its size alone, but because it exposed the fatal flaw at the heart of German command.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHAPTERS:
0:00  The Army That Was Already Doomed
1:45  Stalin's Order: Not One Step Back
3:30  The Trap Closes — Operation Uranus
5:15  The Breakout Window Hitler Refused to Open
7:00  Manstein's Last Chance: 30 Miles Away
8:45  The Promotion That Was a Death Sentence
10:30 91,000 Prisoners — And What Happened to Them

SOURCES:
• "Stalingrad" — Antony Beevor (1998)
• "Armageddon" — Max Hastings
• German Federal Military Archives — 6th Army War Diaries, 1942–43

Subscribe — new WWII documentary every week, going deeper than the history books dare.

#WWII #WorldWar2 #MilitaryHistory #BattleOfStalingrad #EasternFront""")

doc.add_paragraph()
tag_block(doc, "PRIMARY KEYWORD", "battle of stalingrad")
tag_block(doc, "SECONDARY KEYWORDS", "eastern front ww2 · german 6th army · operation uranus · stalingrad encirclement · paulus stalingrad surrender")
tag_block(doc, "TOPIC TAGS", "battle of stalingrad, stalingrad documentary, stalingrad 1942, stalingrad 1943, german 6th army, operation uranus ww2, eastern front stalingrad, paulus stalingrad, stalingrad encirclement, stalingrad turning point")
tag_block(doc, "LONG-TAIL TAGS", "why did germany lose the battle of stalingrad, what happened at stalingrad ww2, how many soldiers died at stalingrad, why didn't the german army break out of stalingrad, battle of stalingrad explained, operation uranus explained ww2, who won the battle of stalingrad, stalingrad ww2 full documentary, what was the significance of stalingrad, german surrender stalingrad 1943")
tag_block(doc, "BEST POST DATE", "Thursday Nov 17 (before Nov 19 Operation Uranus anniversary) OR Jan 31 (before Feb 2 surrender anniversary)")

doc.add_page_break()

# ══════════════════════════════════════════════
# VIDEO 4 — BUNKER
# ══════════════════════════════════════════════
heading1(doc, "VIDEO 4 — INSIDE HITLER'S BUNKER")
centered(doc, "The Last 10 Days of the Third Reich", 13, bold=True, color=DARK)
centered(doc, "~1,510 words  |  ~11:37 min  |  Formula: Inside View + Dark Secret", 9, italic=True, color=GRAY)
doc.add_paragraph()

heading2(doc, "SCRIPT — ENGLISH (AMERICAN)")
divider(doc)

parts_bunker = [
    (1, "COLD OPEN", "0:00 – 0:45",
     "B-roll: burning Berlin, Soviet artillery, bunker entrance archival photos",
     """Fifty feet beneath the burning streets of Berlin, in a concrete bunker that smelled of diesel fuel and fear, the man who had plunged the world into history's deadliest war was waiting to die.

It is April 20th, 1945. Adolf Hitler's 56th birthday.

Outside, Soviet artillery shells are landing less than a mile away. The Red Army — 2.5 million soldiers — has encircled the city. The Reich that Hitler had promised would last a thousand years will survive him by exactly seven days.

In those seven days, inside twelve rooms of reinforced concrete fifteen meters underground, more decisions would be made, more loyalties broken, and more history compressed into a single space than almost anywhere else in the twentieth century.

What happened in the bunker in those final ten days is not the heroic last stand of Nazi mythology. It is something far stranger. And far more human."""),

    (2, "THE PROMISE", "0:45 – 1:30", None,
     """The story of Hitler's last days has been told many times. The movie. The memes. The cultural myth of a raving, broken dictator screaming at maps. That story is not wrong. But it is incomplete.

What the historical record actually shows — drawn from the testimonies of his secretaries, his doctor, his closest aides — is a man of terrifying contradictions. Moments of supernatural calm followed by eruptions of total unreality.

In this video, we're going inside the Führerbunker — room by room, decision by decision, day by day. And we're going to answer the question that every account dances around but rarely confronts directly:

At what point did Hitler know it was over? The answer will surprise you."""),

    (3, "CONTEXT", "1:30 – 3:30",
     "Map animation: Soviet encirclement of Berlin, April 1945",
     """By April 1945, the Third Reich exists mostly on paper.

In the East, Marshal Zhukov's and Marshal Konev's fronts have launched the Berlin Offensive — the largest artillery bombardment in history. 41,600 Soviet guns fired simultaneously on April 16th. The ground shook 200 miles away.

The German forces defending Berlin: boys from the Hitler Youth, old men from the Volksturm, scattered Wehrmacht remnants — perhaps 45,000 soldiers against 2.5 million Red Army troops.

Inside the Führerbunker: Eva Braun, who arrived April 15th and refused to leave. Goebbels with his wife and six children — brought to die with the Reich. Martin Bormann, obsessively documenting every order. Dr. Morell, injecting Hitler with a daily cocktail of vitamins, stimulants, and narcotics.

And the generals. Men who have learned, over years, never to deliver news that contradicts what Hitler wants to believe."""),

    (4, "THE BUILD", "3:30 – 6:00", None,
     """On April 20th, Hitler's birthday, senior Nazi officials arrive to pay their respects — Göring, Himmler, Ribbentrop — many seeing Hitler in person for the last time. Those who see him are shocked. He has aged decades in months. His left hand trembles. His eyes have a glassy, remote quality.

After the reception, most senior officials quietly flee Berlin.

On April 21st, Hitler orders a counterattack. SS General Steiner's army group will strike the Soviet northern flank. Hitler announces it will break the encirclement. His generals exchange silent glances. Steiner's army group barely exists as a coherent unit.

No one says this out loud.

On April 22nd, the situation briefing reveals Steiner's attack has not begun. Will not begin. Cannot begin.

And for the first time — in the testimony of everyone present — Hitler's composure completely breaks. He screams for three hours. He accuses his generals of treason. Then, as suddenly as it began, the storm passes. He sits down. Asks for tea. Begins discussing, in calm detail, the technical specifications of a new anti-aircraft gun."""),

    (5, "MID-ROLL RE-HOOK", "6:00 – 6:30", None,
     """In a moment, we're going inside the final 48 hours — the wedding, the will, the last meal, the decision about the body. And at the one fact about Hitler's death that the Soviet Union concealed for over forty years.

Stay with us."""),

    (6, "THE CLIMAX", "6:30 – 10:00",
     "Slow narration — let each line breathe",
     """On April 28th, Hitler learns that Himmler — the head of the SS, his most loyal servant — has been secretly negotiating surrender terms with the Western Allies. The betrayal is total.

Hitler orders Himmler arrested. Orders the execution of Himmler's liaison officer — Eva Braun's brother-in-law — who is dragged from the bunker and shot in the garden.

That same night, Hitler marries Eva Braun. A small ceremony in the conference room. She begins to sign "Eva B..." then corrects it to "Eva Hitler." They have a small wedding breakfast.

Hitler dictates his political testament. He blames the Jews for the war. He blames his generals for every defeat. He accepts no personal responsibility for anything.

He is still dictating when Soviet forces are fighting in the streets two blocks away.

On April 30th, at approximately 3:30 in the afternoon, Hitler and Eva Braun entered his private study. Those waiting outside heard a single gunshot.

Eva Braun showed no visible wound. She had taken cyanide.

Their bodies were carried into the garden and burned. The Soviet Army was less than 400 meters away.

For years, the Soviet Union claimed Hitler had escaped. In 2018, French forensic scientists gained access to teeth held in Moscow archives since 1945. DNA analysis confirmed they matched Hitler's known dental records.

He had not escaped. He had not survived. In that bunker garden, on the afternoon of April 30th, 1945, the Third Reich effectively ended."""),

    (7, "AFTERMATH & LEGACY", "10:00 – 12:30",
     "Map: post-war Europe, VE Day, May 8 1945",
     """Germany surrendered unconditionally on May 8th, 1945 — eight days after Hitler's death.

What the bunker left behind was not just the end of a regime. It was a case study in the terminal stage of a system built on the cult of a single individual.

In those final ten days, Germany still had armies in the field. It still had functioning ministries. Millions of soldiers prepared to fight and die on orders they received. None of it mattered. Because the system had been so completely centered on one man that when that man descended into unreality — ordering phantom armies, conducting a wedding while shells fell 200 meters away — the entire structure followed him.

The six children of Joseph and Magda Goebbels — whose names all began with H, in honor of Hitler — were killed by their own mother on the night of May 1st. She could not imagine a world for them without National Socialism.

That detail, perhaps more than any other, captures what had been built in Germany between 1933 and 1945."""),

    (8, "CLOSING HOOK", "12:30 – 13:30", None,
     """In ten days inside fifty feet of concrete beneath a burning city, the most destructive political movement of the twentieth century played out its final act.

Not with dignity. Not with clarity. But with phantom armies and a wedding breakfast and a political testament that blamed everyone except the man writing it.

The lesson of the bunker is not about Hitler's madness. It is about the system that made his madness possible. The generals who didn't speak. The officials who fled. The loyal servants who stayed and carried out orders until the last possible moment.

History does not end with one man's decision to pull a trigger in a concrete room. It begins with all the smaller decisions — made by ordinary people, over years — that made that room inevitable.

Next week: the German officers who tried to stop it — the men behind the July 20th plot to assassinate Hitler. Who they were. Why they waited so long. And why, when they finally acted, they failed.

Subscribe. That story changes everything you think you know about the German resistance."""),
]

for num, title, tc, prod_note, text in parts_bunker:
    part_header(doc, num, title, tc)
    if prod_note:
        note(doc, prod_note)
    body(doc, text)

doc.add_page_break()

heading2(doc, "SEO PACKAGE — INSIDE HITLER'S BUNKER")
divider(doc)
tag_block(doc, "OPTIMIZED TITLE", "Inside Hitler's Bunker: The Last 10 Days of the Third Reich  [57 chars ✓]")
doc.add_paragraph()
body(doc, """DESCRIPTION (publish-ready):

Fifty feet underground, while Berlin burned above him, Hitler planned attacks with armies that no longer existed.

Inside Hitler's bunker in the final 10 days of the Third Reich — what the people who were actually there witnessed, and the one fact about Hitler's death that the Soviet Union concealed for over 40 years.

In April 1945, Adolf Hitler retreated to the Führerbunker beneath the Reich Chancellery in Berlin as 2.5 million Soviet soldiers closed in on the city. What followed in those twelve concrete rooms — a wedding, phantom counterattacks, mass betrayal, and a death that sparked decades of conspiracy — is one of history's most documented and least understood final acts.

What separates this account from the myths is the primary source record. Hitler's secretaries Traudl Junge and Christa Schroeder, his pilot Hans Baur, and architect Albert Speer all left detailed testimonies. Together they paint a portrait not of a raving madman, but of something more disturbing: a man of terrifying calm who, until his final hours, believed he had done nothing wrong.

French forensic analysis of dental remains in 2018, using Soviet archives sealed since 1945, finally confirmed what the historical record had long suggested. Hitler died in that bunker on April 30th, 1945.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHAPTERS:
0:00  The Birthday Party Nobody Wanted to Attend
1:30  The Phantom Army That Was Supposed to Save Berlin
3:15  The Moment Hitler's Composure Finally Broke
5:00  Himmler's Betrayal — The Loyalty That Wasn't
7:00  The Wedding Beneath the Rubble
9:00  April 30th — What Actually Happened
10:45 The Secret the Soviet Union Kept for 40 Years

SOURCES:
• "Hitler: 1936–1945 Nemesis" — Ian Kershaw (2000)
• "Until the Final Hour" — Traudl Junge (Hitler's secretary, firsthand account)
• "The Bunker" — James P. O'Donnell (1978, based on 250 firsthand interviews)

Subscribe — every week we go inside the moments history left incomplete.

#WWII #WorldWar2 #MilitaryHistory #HitlersBunker #FallOfBerlin""")

doc.add_paragraph()
tag_block(doc, "PRIMARY KEYWORD", "hitler bunker last days")
tag_block(doc, "SECONDARY KEYWORDS", "führerbunker · fall of berlin 1945 · hitler death ww2 · end of third reich · eva braun bunker")
tag_block(doc, "TOPIC TAGS", "hitler bunker, führerbunker, hitler last days, fall of berlin 1945, berlin 1945, hitler death, third reich collapse, eva braun, berlin ww2, april 1945 berlin")
tag_block(doc, "LONG-TAIL TAGS", "what happened in hitler's bunker, how did hitler die ww2, what were hitler's last days like, führerbunker documentary, what happened in berlin april 1945, did hitler really die in the bunker, soviet union hitler death secret, hitler last words ww2, fall of the third reich documentary, end of nazi germany explained")
tag_block(doc, "BEST POST DATE", "Thursday April 28 — captures the massive search spike before April 30 (Hitler's death anniversary)")

doc.add_page_break()

heading2(doc, "THUMBNAIL BRIEF — INSIDE HITLER'S BUNKER")
divider(doc)
body(doc, """OPTION A — MAX CTR (Face + Tension)
Background: Bunker corridor — bare concrete, yellow emergency lighting, deep shadows
Foreground: Hitler in half-profile, visibly aged 1945 photo, trembling hand visible
Color grade: Near-monochrome grey-green + single red accent on edges
Text overlay: HIS FINAL HOURS — Impact white, black stroke, large, upper left
Mood: Confinement. The viewer feels the weight of the bunker before clicking.

OPTION B — REVELATION / SECRET
Background: Steel bunker door ajar — light escaping through the gap, total darkness around it
Foreground: Red TOP SECRET stamp diagonally across image — partially torn
Color grade: B&W with red on the stamp and the light gap only
Text overlay: WHAT REALLY HAPPENED
Mood: Forbidden access. The viewer feels about to see classified material.

OPTION C — TEMPORAL CONTRAST
Left: Hitler at peak power — Nuremberg 1938, Nazi salute, delirious crowd
Right: Destroyed bunker entrance — Berlin 1945, ruins, silence
Dividing element: 1938 → 1945 in bold white font
Text overlay: HOW IT ENDED
Mood: Inevitable fall. The viewer feels the entire trajectory in 2 seconds.

THUMBNAIL TEXT RANKING:
1. HIS FINAL HOURS — intimacy + inevitability, "his" personalizes it
2. WHAT REALLY HAPPENED — Hidden Truth formula in the thumbnail itself
3. 50 FEET UNDERGROUND — specific + immediate visual, viewer imagines the space
4. BERLIN WAS BURNING — dramatic present tense, creates scene without explaining
5. THEY WERE ALL LYING — betrayal + revelation, high CTR but more sensationalist

TITLE + THUMBNAIL SYNERGY:
✓ Title promises "Inside" — thumbnail visually delivers the interior space. Perfect synergy.
✓ "Last 10 Days" + "HIS FINAL HOURS" = two angles of the same secret, each incomplete without the other.

CANVA SEARCH TERMS:
• führerbunker interior concrete corridor
• hitler 1945 photograph aging
• berlin ruins april 1945 aerial""")

doc.add_page_break()

# ══════════════════════════════════════════════
# QUICK REFERENCE SHEET
# ══════════════════════════════════════════════
heading1(doc, "QUICK REFERENCE — ALL 4 VIDEOS")
divider(doc)

rows = [
    ("VIDEO 1", "What If D-Day Had Failed?",               "Counterfactual",            "what if d-day failed",       "Jun 6 (D-Day anniversary)",     "EN + ES"),
    ("VIDEO 2", "Operation Barbarossa: The Decision...",   "Hidden Truth + Worst Mistake","operation barbarossa",      "Jun 19 (before Jun 22)",        "EN + ES + SEO + Thumb"),
    ("VIDEO 3", "Battle of Stalingrad: How 300,000...",    "Inside View + Number Shock",  "battle of stalingrad",      "Nov 17 OR Jan 31",              "EN + SEO"),
    ("VIDEO 4", "Inside Hitler's Bunker: Last 10 Days",   "Inside View + Dark Secret",   "hitler bunker last days",   "Apr 28 (before Apr 30)",        "EN + SEO + Thumb"),
]

for vid, title, formula, keyword, post_date, assets in rows:
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run(f"{vid}: {title}")
    r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RED
    tag_block(doc, "Formula", formula)
    tag_block(doc, "Primary Keyword", keyword)
    tag_block(doc, "Best Post Date", post_date)
    tag_block(doc, "Assets Included", assets)

doc.add_paragraph()
divider(doc)
doc.add_paragraph()
centered(doc, "PRODUCTION WORKFLOW PER VIDEO", 11, bold=True, color=DARK)
doc.add_paragraph()
body(doc, """1. /wwii-ideas    → Choose topic from pillar bank
2. /wwii-title    → Generate 12 title variations, pick winner
3. /wwii-seo      → Full metadata package (description, tags, chapters)
4. /wwii-script   → Full 8-part voiceover script (EN + ES)
5. /wwii-thumbnail → Detailed thumbnail brief for designer
6. Record voiceover in ElevenLabs (8 blocks per video)
7. Assemble in DaVinci Resolve / CapCut
8. Upload — use SEO package for all metadata fields""")

doc.add_paragraph()
divider(doc)
centered(doc, "WWII Faceless Documentary Channel — Complete Production Package", 9, italic=True, color=LGRAY)
centered(doc, "Generated with Claude Code · claude.ai/code", 8, italic=True, color=LGRAY)

# ── Save
path = "/home/user/ROBOS-TRADING/WWII_Channel_Complete_Package.docx"
doc.save(path)
print(f"Saved: {path}")
