from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
for section in doc.sections:
    section.top_margin = Inches(1); section.bottom_margin = Inches(1)
    section.left_margin = Inches(1.2); section.right_margin = Inches(1.2)

RED   = RGBColor(0xC0,0x39,0x2B)
DARK  = RGBColor(0x1A,0x1A,0x2E)
GRAY  = RGBColor(0x55,0x55,0x55)
LGRAY = RGBColor(0x99,0x99,0x99)
BLUE  = RGBColor(0x1A,0x52,0x76)

def ctr(doc,text,size=11,bold=False,color=DARK,italic=False):
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(text); r.bold=bold; r.italic=italic
    r.font.size=Pt(size); r.font.color.rgb=color

def h1(doc,text):
    doc.add_paragraph()
    p=doc.add_paragraph(); r=p.add_run(text.upper())
    r.bold=True; r.font.size=Pt(13); r.font.color.rgb=RED
    doc.add_paragraph().add_run("━"*65).font.color.rgb=LGRAY

def h2(doc,text):
    doc.add_paragraph()
    p=doc.add_paragraph(); r=p.add_run(text)
    r.bold=True; r.font.size=Pt(11); r.font.color.rgb=DARK

def ph(doc,n,title,tc):
    doc.add_paragraph()
    p=doc.add_paragraph()
    r=p.add_run(f"PART {n} — {title}  [{tc}]")
    r.bold=True; r.font.size=Pt(10); r.font.color.rgb=RED
    doc.add_paragraph().add_run("─"*55).font.color.rgb=LGRAY

def nt(doc,text):
    p=doc.add_paragraph(); r=p.add_run(f"[{text}]")
    r.italic=True; r.font.size=Pt(8.5); r.font.color.rgb=LGRAY

def vis(doc,text):
    p=doc.add_paragraph(); r=p.add_run(f"VISUAL: {text}")
    r.italic=True; r.font.size=Pt(8.5); r.font.color.rgb=BLUE

def bd(doc,text):
    for line in text.strip().split("\n"):
        p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(2)
        r=p.add_run(line.strip()); r.font.size=Pt(10)

def tb(doc,lbl,val):
    p=doc.add_paragraph()
    r1=p.add_run(f"{lbl}: "); r1.bold=True; r1.font.size=Pt(9.5)
    r2=p.add_run(val); r2.font.size=Pt(9.5); r2.font.color.rgb=GRAY

def div(doc):
    p=doc.add_paragraph()
    p.add_run("═"*65).font.color.rgb=LGRAY

# ══════════════════════════════════════
# DATA — 10 VIDEOS
# ══════════════════════════════════════
videos = [

# ─────────────────────────────────────
# V1: BATTLE OF BRITAIN
# ─────────────────────────────────────
{
"num":1,
"title_en":"Battle of Britain: How 1,000 Pilots Saved Western Civilization",
"title_es":"La Batalla de Inglaterra: Cómo 1,000 Pilotos Salvaron la Civilización",
"chars":"62 ✓","formula":"Underdog + Number Shock",
"keyword":"battle of britain",
"secondary":"raf vs luftwaffe · spitfire · hurricane ww2 · blitz london · operation sea lion",
"post":"Thursday Aug 13 (Adlertag anniversary Aug 13, 1940)",
"hashtags":"#WWII #WorldWar2 #MilitaryHistory #BattleOfBritain #RAF",
"topic_tags":"battle of britain, raf ww2, luftwaffe ww2, spitfire ww2, hurricane fighter ww2, battle of britain documentary, blitz london, operation sea lion, few ww2, winston churchill ww2",
"longtail_tags":"how did britain win the battle of britain, why did germany lose the battle of britain, what was the battle of britain, raf vs luftwaffe ww2, who fought in the battle of britain, battle of britain explained, spitfire vs messerschmitt ww2, why didn't germany invade britain, winston churchill battle of britain, few good men raf ww2",
"sources":"The Most Dangerous Enemy — Stephen Bungay | Finest Hour — Tim Clayton & Phil Craig | The Battle of Britain — James Holland",
"parts_en":[
(1,"COLD OPEN","0:00–0:45",
"B-roll: Spitfires scrambling, contrails across blue sky, burning Heinkel bombers",
"Archival: RAF pilots running to planes, radar operators, Churchhill speech 'finest hour'",
"""In the summer of 1940, Great Britain stood alone.

France had fallen. The Low Countries were occupied. From the English Channel to the borders of the Soviet Union, continental Europe was under Nazi control.

Adolf Hitler gave the order for Operation Sea Lion — the invasion of Britain. All that stood between him and total European domination was 22 miles of water... and approximately 1,000 RAF fighter pilots.

What followed between July and October 1940 was the first major campaign in history fought entirely in the air. The Luftwaffe — 2,600 aircraft, battle-hardened from Spain, Poland, and France — against a Royal Air Force that was outnumbered, outgunned, and losing pilots faster than it could train them.

Churchill called it Britain's finest hour. What it actually was... was Britain's closest-run catastrophe."""),

(2,"THE PROMISE","0:45–1:30",None,None,
"""Every account of the Battle of Britain focuses on the heroism of the Few — the pilots who flew sortie after sortie until they died or were too exhausted to climb back into the cockpit.

That heroism was real. But the battle was won by something else.

In this video, we're going to reveal the three factors that the Luftwaffe never overcame — factors that had nothing to do with courage and everything to do with technology, geography, and one catastrophic German command decision.

Because the truth is: Britain should have lost. The math said so. And understanding why it didn't reveals one of the most underappreciated strategic victories in military history."""),

(3,"CONTEXT","1:30–3:30",
"Map animation: German-occupied Europe, RAF sector stations, radar chain coverage",
"Archival: Dunkirk evacuation aftermath, Churchill in War Cabinet, radar towers",
"""By July 1940, the situation is desperate. The British Expeditionary Force has been evacuated at Dunkirk — saved, but stripped of its equipment. Britain has 25 operational divisions with barely enough rifles to arm them.

Hitler needs air supremacy over the Channel before Sea Lion can launch. He assigns the task to Reichsmarschall Hermann Göring — who promises it will be done in four weeks.

Air Marshal Hugh Dowding commands RAF Fighter Command. He has 650 operational fighters. Against him: 1,000 German bombers and 900 fighters. The odds are two-to-one against.

But Dowding has three assets Göring doesn't fully understand.

First: the Chain Home radar network — 51 stations along the English coast giving Britain advance warning of every German raid. Second: the Sector Control system — a ground-controlled interception network that lets Dowding vector fighters directly onto incoming raids without wasting fuel on patrols. Third: geography. German fighters flying from France have just 20 minutes of combat time over England before fuel forces them to turn back."""),

(4,"THE BUILD","3:30–6:00",
"Map: Luftwaffe attack phases, sector station locations, RAF losses by week",
"Archival: Burning sector stations, pilot interviews (archive), scramble sequences",
"""The Luftwaffe's first phase attacks shipping in the Channel. Britain can absorb these losses.

The second phase — Adlertag, Eagle Day — targets the radar stations and sector airfields. This is the right strategy. By late August, the Luftwaffe is destroying RAF infrastructure faster than it can be repaired. Five of seven sector stations are damaged or destroyed. RAF pilot losses reach 120 per week — against a training pipeline producing 65.

Dowding is running out of pilots. Not planes. Pilots.

The situation is becoming critical when, on August 24th, a German bomber accidentally drops bombs on central London. Churchill orders an immediate retaliation raid on Berlin.

Göring is furious. He promises Hitler that London will be razed.

On September 7th, 1940, the Luftwaffe shifts its targeting from RAF airfields... to London.

It is the worst strategic decision of the entire Battle of Britain. The pressure on Fighter Command is instantly, completely relieved. The sector stations begin to recover. Pilot training catches up to losses.

The Blitz kills 43,000 British civilians. But it saves the Royal Air Force."""),

(5,"MID-ROLL RE-HOOK","6:00–6:30",
"Music: swell of orchestral score, cut to silence",None,
"""In a moment, we're going to look at September 15th, 1940 — the day the Luftwaffe launched its largest single attack on Britain, and the day it became clear the battle was lost for Germany.

And at the number that tells the whole story in one statistic.

Stay with us."""),

(6,"THE CLIMAX","6:30–10:00",
"Archival: September 15 newsreel, Spitfire cockpit footage, burning London docks",
"Map: September 15 raid tracks, RAF interception vectors",
"""September 15th, 1940. Battle of Britain Day.

The Luftwaffe launches 1,120 aircraft in two massive waves. Göring promises Hitler this will be the decisive blow. The RAF, he claims, is down to its last 50 fighters.

Dowding deploys every available squadron — 31 in total. For the first time in the battle, Londoners watching from the streets can see the contrails of hundreds of aircraft weaving across the sky directly overhead.

By the end of the day, Germany has lost 61 aircraft. Britain has lost 31.

More importantly: the Luftwaffe has failed to break through in strength for the third consecutive major attack. The bombing accuracy is falling. Crew morale is deteriorating. Pilots who survive being shot down over England become prisoners. Pilots who survive over France can fly again.

Two days later, Hitler postpones Operation Sea Lion indefinitely. He will never reschedule it.

The official German records show that between July and October 1940, the Luftwaffe lost 1,733 aircraft and 2,662 aircrew killed, missing, or captured.

The RAF lost 1,017 aircraft and 544 pilots killed.

Of the 2,936 aircrew who qualified as 'the Few' by flying at least one operational sortie during the battle, 544 never came home."""),

(7,"AFTERMATH & LEGACY","10:00–12:30",
"Archival: Churchill speech, bombed London rebuilding, RAF memorial footage",
"Map: if Britain had fallen — hypothetical German occupation zones",
"""The Battle of Britain's strategic consequences extended far beyond Britain's survival.

By holding, Britain preserved the only active Allied military front in Western Europe for nearly four years. It provided the base from which the strategic bombing campaign against Germany would eventually be launched. It gave the United States time to rearm and, after Pearl Harbor, a staging ground for the liberation of Europe.

Churchill understood the scale of what had been preserved. His words, spoken at the battle's height, remain among the most precisely observed sentences in military history:

'Never in the field of human conflict was so much owed by so many to so few.'

What Churchill did not say — because he couldn't — was how close the 'so few' had come to not being enough.

By the third week of August 1940, Dowding had calculated that at current attrition rates, Fighter Command had approximately two more weeks of operational capability. If the Luftwaffe had maintained its attacks on the sector stations for fourteen more days, Britain's air defense would have collapsed.

It was Göring's decision to bomb London — not British courage alone — that saved the RAF.

Historian Richard Overy concludes that the Battle of Britain was won as much by German mistakes as by British skill. A conclusion that in no way diminishes the sacrifice of the 544 who died. But that forces us to ask a harder question: how many decisive moments in history are decided not by who fights best... but by who makes the last mistake?"""),

(8,"CLOSING HOOK","12:30–13:30",None,None,
"""In the summer of 1940, 1,000 pilots flew against an air force twice their size, defending a country that had run out of continental allies and had almost run out of time.

They held. Britain held.

Not because the math favored them. The math didn't. Not because the outcome was inevitable. It wasn't. But because a German Reichsmarschall made a decision based on pride instead of strategy — and gave the RAF exactly the two weeks it needed to recover.

The Battle of Britain is not a story about inevitable triumph. It's a story about how close civilizations can come to the edge — and how often what pulls them back is the other side's mistake.

Next week, we're inside the Luftwaffe — the pilots who flew those 1,733 lost aircraft. What they believed. What they were told. And when they understood the battle was unwinnable.

Subscribe. Their story has never been told from their side in this way."""),
],

"parts_es":[
(1,"COLD OPEN","0:00–0:45",
"B-roll: Spitfires despegando, estelas en el cielo azul, bombarderos Heinkel en llamas",
"Archival: pilotos del RAF corriendo hacia sus aviones, discurso de Churchill",
"""En el verano de 1940, Gran Bretaña estaba sola.

Francia había caído. Los Países Bajos estaban ocupados. Desde el Canal de la Mancha hasta las fronteras de la Unión Soviética, Europa continental estaba bajo control nazi.

Adolf Hitler dio la orden para la Operación León Marino — la invasión de Gran Bretaña. Todo lo que se interponía entre él y la dominación total de Europa eran 35 kilómetros de agua... y aproximadamente 1,000 pilotos de la RAF.

Lo que siguió entre julio y octubre de 1940 fue la primera gran campaña de la historia librada íntegramente en el aire. La Luftwaffe — 2,600 aviones, curtida en España, Polonia y Francia — contra una Real Fuerza Aérea superada en número y perdiendo pilotos más rápido de lo que podía entrenarlos.

Churchill lo llamó la hora más gloriosa de Gran Bretaña. Lo que realmente fue... fue la catástrofe más cercana de Gran Bretaña."""),

(2,"THE PROMISE","0:45–1:30",None,None,
"""Cada relato de la Batalla de Inglaterra se centra en el heroísmo de los Pocos — los pilotos que volaron misión tras misión hasta morir o quedar demasiado agotados para subir de nuevo a la cabina.

Ese heroísmo fue real. Pero la batalla se ganó por otra cosa.

En este video, vamos a revelar los tres factores que la Luftwaffe nunca pudo superar — factores que nada tenían que ver con el coraje y todo con la tecnología, la geografía y una catastrófica decisión de mando alemana.

Porque la verdad es: Gran Bretaña debería haber perdido. Los números lo decían. Y entender por qué no lo hizo revela una de las victorias estratégicas más subestimadas de la historia militar."""),

(3,"CONTEXTO","1:30–3:30",
"Mapa: Europa ocupada por Alemania, estaciones del RAF, cobertura de radar",
"Archival: evacuación de Dunkerque, Churchill en el Gabinete de Guerra, torres de radar",
"""Para julio de 1940, la situación es desesperada. El Cuerpo Expedicionario Británico fue evacuado en Dunkerque — salvado, pero despojado de su equipo.

El Mariscal del Aire Dowding manda el Mando de Cazas del RAF. Tiene 650 cazas operativos. En su contra: 1,000 bombarderos alemanes y 900 cazas. Las probabilidades son dos a uno en contra.

Pero Dowding tiene tres activos que Göring no comprende del todo.

Primero: la red de radar Chain Home — 51 estaciones a lo largo de la costa inglesa. Segundo: el sistema de Control de Sector — que permite a Dowding vectorear cazas directamente hacia los ataques sin desperdiciar combustible en patrullas. Tercero: geografía. Los cazas alemanes volando desde Francia tienen solo 20 minutos de tiempo de combate sobre Inglaterra antes de que el combustible los obligue a regresar."""),

(4,"THE BUILD","3:30–6:00",
"Mapa: fases de ataque de la Luftwaffe, ubicaciones de estaciones de sector, bajas del RAF",
"Archival: estaciones de sector en llamas, entrevistas de pilotos de archivo",
"""La segunda fase de la Luftwaffe ataca los aeródromos de sector. Esta es la estrategia correcta. Para finales de agosto, la Luftwaffe destruye infraestructura del RAF más rápido de lo que puede repararse. Cinco de siete estaciones de sector están dañadas o destruidas.

Dowding se está quedando sin pilotos. No sin aviones. Sin pilotos.

El 24 de agosto, un bombardero alemán lanza accidentalmente bombas sobre el centro de Londres. Churchill ordena un ataque de represalia sobre Berlín.

Göring está furioso. Le promete a Hitler que Londres será arrasada.

El 7 de septiembre de 1940, la Luftwaffe cambia sus objetivos de los aeródromos del RAF... a Londres.

Es la peor decisión estratégica de toda la Batalla de Inglaterra. La presión sobre el Mando de Cazas se alivia de inmediato. Las estaciones de sector comienzan a recuperarse.

El Blitz mata a 43,000 civiles británicos. Pero salva a la Real Fuerza Aérea."""),

(5,"MID-ROLL RE-HOOK","6:00–6:30",
"Música: crescendo orquestal, corte al silencio",None,
"""En un momento, vamos a ver el 15 de septiembre de 1940 — el día en que la Luftwaffe lanzó su mayor ataque individual sobre Gran Bretaña, y el día en que quedó claro que la batalla estaba perdida para Alemania.

Quédense con nosotros."""),

(6,"EL CLÍMAX","6:30–10:00",
"Archival: noticiario del 15 de septiembre, metraje de cabina de Spitfire, muelles de Londres ardiendo",
"Mapa: rutas del ataque del 15 de septiembre, vectores de intercepción del RAF",
"""15 de septiembre de 1940. El Día de la Batalla de Inglaterra.

La Luftwaffe lanza 1,120 aviones en dos oleadas masivas. Göring le promete a Hitler que este será el golpe decisivo. El RAF, afirma, está reducido a sus últimos 50 cazas.

Dowding despliega todos los escuadrones disponibles — 31 en total.

Al final del día, Alemania ha perdido 61 aviones. Gran Bretaña ha perdido 31.

Dos días después, Hitler pospone indefinidamente la Operación León Marino. Nunca la reprogramará.

Los registros alemanes oficiales muestran que entre julio y octubre de 1940, la Luftwaffe perdió 1,733 aviones y 2,662 tripulantes muertos, desaparecidos o capturados. El RAF perdió 1,017 aviones y 544 pilotos muertos."""),

(7,"AFTERMATH & LEGACY","10:00–12:30",
"Archival: discurso de Churchill, Londres reconstruyéndose, memorial del RAF",
"Mapa: hipotética ocupación alemana si Gran Bretaña hubiera caído",
"""Las consecuencias estratégicas de la Batalla de Inglaterra se extendieron mucho más allá de la supervivencia de Gran Bretaña.

Churchill comprendió la escala de lo que se había preservado. Sus palabras, pronunciadas en el punto álgido de la batalla, siguen siendo unas de las frases más precisas de la historia militar:

'Nunca en el campo del conflicto humano tantos debieron tanto a tan pocos.'

Lo que Churchill no dijo — porque no podía — era cuán cerca habían estado los 'tan pocos' de no ser suficientes.

El historiador Richard Overy concluye que la Batalla de Inglaterra se ganó tanto por los errores alemanes como por la habilidad británica. Una conclusión que de ninguna manera disminuye el sacrificio de los 544 que murieron."""),

(8,"CLOSING HOOK","12:30–13:30",None,None,
"""En el verano de 1940, 1,000 pilotos volaron contra una fuerza aérea el doble de grande, defendiendo un país que se había quedado sin aliados continentales y casi sin tiempo.

Resistieron. Gran Bretaña resistió.

No porque los números les favorecieran. No lo hacían. Sino porque un Reichsmarschall alemán tomó una decisión basada en el orgullo en lugar de en la estrategia — y le dio al RAF exactamente las dos semanas que necesitaba para recuperarse.

Próxima semana: dentro de la Luftwaffe — los pilotos que volaron esos 1,733 aviones perdidos. Lo que creyeron. Lo que les dijeron. Y cuándo entendieron que la batalla era imposible de ganar.

Suscríbanse."""),
],

"thumb":"""OPTION A — HIGH CTR
Background: Formation of Spitfires in tight V-formation against vivid blue sky, contrails streaming
Foreground: RAF roundel (red-white-blue bullseye) as dominant graphic element, center
Color grade: Saturated blues + warm orange sun — heroic, cinematic
Text overlay: 1,000 vs ALL OF GERMANY — Impact white, black stroke
Mood: Impossible odds. The viewer calculates the mismatch instantly.

OPTION B — FACE + NUMBERS
Background: Close-up of RAF pilot in cockpit, oxygen mask, focused eyes
Foreground: Large number 544 in red — pilots who died — bottom third
Color grade: High contrast, slightly desaturated with red accent
Text overlay: THE FEW
Mood: Intimacy + sacrifice. "The Few" creates immediate recognition for WWII viewers.

OPTION C — DRAMATIC CONTRAST
Left: Dense Luftwaffe bomber formation — hundreds of aircraft, German crosses visible
Right: Lone Spitfire banking into attack — tiny against the mass
Dividing element: VS in bold red
Text overlay: OUTNUMBERED
Mood: Underdog at maximum visual clarity.

THUMBNAIL TEXT RANKING:
1. THE FEW — instant recognition, iconic phrase, emotional weight
2. OUTNUMBERED — visual concept works immediately at thumbnail size
3. 1,000 vs GERMANY — number shock formula, creates scale dissonance
4. BRITAIN'S DARKEST SUMMER — atmospheric, curiosity-gap
5. THEY HELD — simple past tense with massive implication

CANVA SEARCH TERMS: spitfire formation flight ww2 | raf pilot cockpit 1940 | luftwaffe bombers formation england""",

"seo_desc":"""In the summer of 1940, 1,000 RAF pilots stood between Hitler and total European domination. This is the story the history books get wrong.

In this documentary, we reveal the three factors that actually won the Battle of Britain — and why Britain should have lost according to every military calculation.

The Battle of Britain, fought from July to October 1940, was the first major campaign in history decided entirely by air power. RAF Fighter Command, commanded by Air Marshal Hugh Dowding, faced a Luftwaffe twice its size with a dwindling supply of experienced pilots. By late August 1940, Dowding calculated he had approximately two weeks of operational capability remaining.

What saved the RAF was not courage alone — it was a catastrophic German command decision. On September 7th, 1940, Hermann Göring shifted Luftwaffe targeting from RAF sector stations to London. That decision gave Fighter Command exactly the recovery time it needed.

Historian Richard Overy concludes the Battle of Britain was won as much by German mistakes as by British skill — a conclusion that changes how we understand every subsequent battle of World War Two.

CHAPTERS:
0:00 The Summer Britain Stood Alone
1:30 What Dowding Had That Göring Didn't
3:15 Eagle Day — The Right Strategy, Used Wrong
5:00 The Accidental Bomb That Changed Everything
7:00 September 15th — The Day Germany Lost
9:30 544 Dead — The True Cost of Victory
11:00 What Would Have Happened If Britain Had Fallen

SOURCES:
The Most Dangerous Enemy — Stephen Bungay
Finest Hour — Tim Clayton & Phil Craig
The Battle of Britain — James Holland

Subscribe for a new WWII documentary every week.

#WWII #WorldWar2 #MilitaryHistory #BattleOfBritain #RAF""",
},

# ─────────────────────────────────────
# V2: PEARL HARBOR
# ─────────────────────────────────────
{
"num":2,
"title_en":"Pearl Harbor: The 90-Minute Attack That Changed the World",
"title_es":"Pearl Harbor: El Ataque de 90 Minutos Que Cambió el Mundo",
"chars":"58 ✓","formula":"Number Shock + Inside View",
"keyword":"pearl harbor attack",
"secondary":"japanese attack pearl harbor · uss arizona · pacific war start · yamamoto pearl harbor",
"post":"Thursday Dec 4 (before Dec 7 anniversary — biggest WWII traffic day of year)",
"hashtags":"#WWII #WorldWar2 #MilitaryHistory #PearlHarbor #PacificWar",
"topic_tags":"pearl harbor, pearl harbor attack, pearl harbor documentary, december 7 1941, uss arizona, yamamoto pearl harbor, japanese attack pearl harbor, pacific war ww2, pearl harbor explained, pearl harbor 1941",
"longtail_tags":"why did japan attack pearl harbor, what happened at pearl harbor, how many died at pearl harbor, was pearl harbor a surprise attack, pearl harbor full documentary, uss arizona sinking pearl harbor, did america know about pearl harbor, yamamoto pearl harbor quote, why did japan bomb pearl harbor ww2, pearl harbor attack explained",
"sources":"At Dawn We Slept — Gordon Prange | Infamy: Pearl Harbor and Its Aftermath — John Toland | Eagle Against the Sun — Ronald Spector",
"parts_en":[
(1,"COLD OPEN","0:00–0:45",
"B-roll: Pearl Harbor aerial view 1941, battleships at anchor, Sunday morning calm",
"Archival: USS Arizona explosion, smoke over battleship row, sailors running",
"""It is 7:55 on a Sunday morning. December 7th, 1941.

At Pearl Harbor, Hawaii, the US Pacific Fleet lies at anchor in the calm water of the harbor. Sailors are eating breakfast. Officers are sleeping in. Church services are beginning. It is, by every visible measure, a peaceful Sunday morning on an American naval base.

At 7:55, the first Japanese bomb falls.

In the next 90 minutes, Japan will attack with 353 aircraft in two waves. By 9:55, the attack is over. In those 90 minutes, the United States Navy has lost 18 ships, 347 aircraft, and 2,403 Americans.

And the world has changed in a way that will not be undone for decades.

But the story of Pearl Harbor — the story that history has told for 80 years — answers the wrong question. It asks 'what happened?' when the question that actually matters is: why did Japan believe this attack made strategic sense? And why were they catastrophically wrong?"""),

(2,"THE PROMISE","0:45–1:30",None,None,
"""Pearl Harbor is one of the most analyzed events of the 20th century. The books, the films, the conspiracy theories.

And yet the question at its center is almost never asked in full.

Admiral Isoroku Yamamoto — the man who planned the attack, who understood the United States better than any Japanese officer — did not believe Pearl Harbor would win the war. He said so, explicitly, before the attack was launched.

In this video, we're going to go inside Japan's strategic calculation in 1941. We're going to explain exactly what Japan thought Pearl Harbor would achieve, why that calculation was flawed from the start, and how one 90-minute attack created the one outcome Japan's leaders had agreed they must avoid at all costs.

Because Pearl Harbor is not a story about American failure. It is a story about a nation making a rational decision based on a fundamentally wrong assumption about human psychology."""),

(3,"CONTEXT","1:30–3:30",
"Map animation: Japanese empire expansion 1937-1941, US oil embargo, Pacific fleet positions",
"Archival: Japanese army in China, US oil tankers, FDR press conference",
"""By 1941, Japan faces an existential crisis.

Its war in China — begun in 1937 — has consumed resources Japan cannot replace from its own territory. Japan imports 80% of its oil from the United States. In July 1941, after Japan occupies French Indochina, the United States imposes a total oil embargo.

The math is simple and brutal. Japan's military has an 18-month oil reserve. After that: economic collapse, military paralysis, and the humiliating end of the imperial expansion project.

Japan's leadership sees two options.

Accept American demands — withdraw from China, abandon expansion — and accept a status Japan's military finds unthinkable.

Or seize the oil fields of the Dutch East Indies by force, and accept war with the United States.

Admiral Yamamoto argues against war. He has spent time in America. He knows what its industrial capacity means. He tells the Japanese cabinet: 'In the first six to twelve months, I can run wild and win victory upon victory. But if the war continues beyond that, I have no expectation of success.'

He is overruled.

Yamamoto then does something remarkable. He designs the best possible version of the attack he advised against."""),

(4,"THE BUILD","3:30–6:00",
"Map: Japanese carrier fleet route across the Pacific, US radar detection failure",
"Archival: Japanese carrier Akagi flight deck, Zero fighters launching",
"""Operation Z — the Pearl Harbor attack plan — achieves tactical surprise through a combination of factors that historians still debate.

The Japanese strike force takes a northern Pacific route — stormy, rarely traveled — and maintains complete radio silence for 12 days. American intelligence, watching Japanese radio traffic, notes the silence but cannot locate the fleet.

On December 7th, at 7:02 AM, two Army radar operators at Opana Point detect a massive formation of aircraft 137 miles north of Oahu. They report it. The duty officer assumes it is a flight of B-17s expected from the mainland.

He tells them not to worry about it.

At 7:53 AM, Commander Mitsuo Fuchida, leading the first wave, transmits the signal: Tora! Tora! Tora! — confirming complete surprise.

The attack's first 30 minutes are catastrophic for the United States. The battleship USS Arizona is hit by an armor-piercing bomb that detonates her forward ammunition magazine. She sinks in nine minutes. 1,177 of her crew die — most of them still aboard. The Oklahoma capsizes. The West Virginia and California sink at their moorings. Four other battleships are damaged.

In 30 minutes, the entire US Pacific battleship fleet has been neutralized."""),

(5,"MID-ROLL RE-HOOK","6:00–6:30",
"Music: dramatic swell, cut to silence over Pearl Harbor aerial photo",None,
"""In a moment, we're going to look at what Japan's attack missed — the three things that, had they been destroyed on December 7th, 1941, might actually have handed Japan the Pacific War.

And at the decision Yamamoto made that, in the long run, guaranteed America's victory.

Stay with us."""),

(6,"THE CLIMAX","6:30–10:00",
"Archival: USS Enterprise returning to Pearl Harbor, Admiral Kimmel watching smoke, FDR Day of Infamy speech",
"Map: What Japanese aircraft missed — fuel farms, submarine base, repair yards",
"""The Japanese attack achieves its tactical objectives almost completely.

But it misses three things.

First: the aircraft carriers. USS Enterprise, Lexington, and Saratoga are all at sea on December 7th — Enterprise delivering Marine aircraft to Wake Island, Lexington on a similar mission to Midway. The carriers that will decide the Pacific War are untouched.

Second: the fuel farms. Pearl Harbor holds 4.5 million barrels of oil in above-ground storage tanks. The attack ignores them. Had they been destroyed, the US Pacific Fleet would have been unable to operate from Hawaii for months.

Third: the submarine base and repair yards. The dry docks, machine shops, and submarine pens that will allow the United States to repair its damaged fleet and sustain submarine operations remain completely intact.

Yamamoto understands immediately what has and hasn't been achieved. 'I fear we have awakened a sleeping giant,' he reportedly says, 'and filled him with a terrible resolve.'

Whether he actually said these words is disputed. That he believed them is not.

On December 8th, President Roosevelt addresses Congress. The speech lasts seven minutes. It contains 518 words. Congress votes for war against Japan 82-0 in the Senate and 388-1 in the House — the only dissenting vote cast by Montana Representative Jeannette Rankin, a pacifist who had also voted against entering World War One.

Within four days, Hitler declares war on the United States. The conflict becomes global.

Japan has achieved tactical success. It has achieved strategic catastrophe."""),

(7,"AFTERMATH & LEGACY","10:00–12:30",
"Archival: US war production factories, aircraft carriers in Pacific, Midway battle footage",
"Map: Pacific War 1942-1945 US island-hopping strategy",
"""At Pearl Harbor, Japan sank or damaged 18 ships. The United States repaired or raised all but two of them — the Arizona and Oklahoma — and returned them to service.

More significantly: the attack transformed American public opinion overnight. The isolationist movement, which had prevented US entry into the war for two years, ceased to exist on December 8th, 1941.

The industrial capacity Yamamoto had feared — the capacity he had explicitly warned Japan's leaders about — mobilized with a speed and on a scale that remains one of the most extraordinary feats of national organization in history. Between 1941 and 1945, the United States produced 300,000 aircraft, 86,000 tanks, 8,800 naval vessels, and 2.7 million machine guns.

Japan produced a fraction of this.

The six months Yamamoto had predicted proved accurate — and the Battle of Midway in June 1942, six months after Pearl Harbor, marked the moment when Japanese expansion began its irreversible reversal.

Historian Gordon Prange, who spent 37 years researching Pearl Harbor, concluded that the attack was 'the greatest strategic blunder in Japanese history.' Not because it failed tactically, but because it guaranteed the involvement of the one power Japan had agreed it could not afford to fight."""),

(8,"CLOSING HOOK","12:30–13:30",None,None,
"""In 90 minutes on a Sunday morning, Japan achieved one of the most complete tactical surprises in military history.

It also guaranteed its own defeat.

Not because American courage was greater. Not because American strategy was superior. But because Japan's entire strategic calculation rested on a single assumption: that a devastating surprise attack would break American will to fight rather than unify it.

The assumption was wrong. Not debatably wrong. Catastrophically, irreversibly wrong.

Pearl Harbor is the story of what happens when a nation confuses tactical capability with strategic wisdom. When the ability to do something overwhelms the judgment about whether it should be done.

Next week, we're at Midway — June 4th, 1942. The four minutes that reversed everything Japan had built at Pearl Harbor and beyond.

Subscribe. Because Midway is the other half of this story."""),
],
"parts_es":[
(1,"COLD OPEN","0:00–0:45",
"B-roll: Vista aérea de Pearl Harbor 1941, acorazados en el fondeadero, calma del domingo por la mañana",
"Archival: Explosión del USS Arizona, humo sobre Battleship Row, marineros corriendo",
"""Son las 7:55 de un domingo por la mañana. 7 de diciembre de 1941.

En Pearl Harbor, Hawái, la Flota del Pacífico de los EE.UU. está anclada en las aguas tranquilas del puerto. Los marineros desayunan. Los oficiales duermen. Los servicios religiosos están comenzando.

A las 7:55, cae la primera bomba japonesa.

En los siguientes 90 minutos, Japón atacará con 353 aviones en dos oleadas. Para las 9:55, el ataque ha terminado. En esos 90 minutos, la Marina de los Estados Unidos ha perdido 18 barcos, 347 aviones y 2,403 americanos.

Pero la historia de Pearl Harbor responde la pregunta equivocada. Pregunta qué pasó cuando la pregunta que realmente importa es: ¿por qué Japón creyó que este ataque tenía sentido estratégico? ¿Y por qué estaban catastróficamente equivocados?"""),

(2,"THE PROMISE","0:45–1:30",None,None,
"""El Almirante Isoroku Yamamoto — el hombre que planeó el ataque — no creía que Pearl Harbor ganaría la guerra. Lo dijo explícitamente antes de que el ataque se lanzara.

En este video, vamos a entrar en el cálculo estratégico de Japón en 1941. Vamos a explicar exactamente qué pensaba Japón que lograría Pearl Harbor, por qué ese cálculo estaba equivocado desde el principio, y cómo un ataque de 90 minutos creó el único resultado que los líderes de Japón habían acordado que debían evitar a toda costa.

Porque Pearl Harbor no es una historia sobre el fracaso americano. Es una historia sobre una nación que toma una decisión racional basada en una suposición fundamentalmente incorrecta sobre la psicología humana."""),

(3,"CONTEXTO","1:30–3:30",
"Mapa: Expansión del Imperio Japonés 1937-1941, embargo de petróleo de EE.UU., posiciones de la flota del Pacífico",
"Archival: Ejército japonés en China, petroleros de EE.UU., conferencia de prensa de FDR",
"""Para 1941, Japón enfrenta una crisis existencial. Japón importa el 80% de su petróleo de los Estados Unidos. En julio de 1941, después de que Japón ocupa la Indochina francesa, los Estados Unidos imponen un embargo total de petróleo.

Las matemáticas son simples y brutales. Las fuerzas militares de Japón tienen reservas de petróleo para 18 meses. Después: colapso económico y parálisis militar.

El Almirante Yamamoto argumenta en contra de la guerra. Ha pasado tiempo en América. Conoce lo que significa su capacidad industrial. Le dice al gabinete japonés: En los primeros seis a doce meses, puedo correr libremente y ganar victoria tras victoria. Pero si la guerra continúa más allá de eso, no tengo expectativas de éxito.

Es superado en votos. Yamamoto entonces hace algo extraordinario. Diseña la mejor versión posible del ataque que aconsejó no hacer."""),

(4,"THE BUILD","3:30–6:00",
"Mapa: Ruta de la flota de portaaviones japonesa por el Pacífico, fallo del radar de EE.UU.",
"Archival: Cubierta de vuelo del portaaviones Akagi, cazas Zero despegando",
"""El 7 de diciembre, a las 7:02 AM, dos operadores de radar del Ejército detectan una enorme formación de aviones a 220 kilómetros al norte de Oahu. Lo informan. El oficial de guardia asume que es un vuelo de B-17 esperado desde el continente.

Les dice que no se preocupen.

A las 7:53 AM, el comandante Mitsuo Fuchida transmite la señal: Tora! Tora! Tora! — confirmando sorpresa total.

El USS Arizona es alcanzado por una bomba perforante que detona su pañol de municiones de proa. Se hunde en nueve minutos. 1,177 de sus tripulantes mueren. En 30 minutos, toda la flota de acorazados del Pacífico ha sido neutralizada."""),

(5,"MID-ROLL RE-HOOK","6:00–6:30",
"Música: crescendo dramático, corte al silencio",None,
"""En un momento, vamos a ver qué se perdió el ataque de Japón — las tres cosas que, de haber sido destruidas el 7 de diciembre de 1941, podrían haber entregado a Japón la Guerra del Pacífico.

Quédense con nosotros."""),

(6,"EL CLÍMAX","6:30–10:00",
"Archival: USS Enterprise regresando a Pearl Harbor, discurso de FDR 'Día de la Infamia'",
"Mapa: Lo que los aviones japoneses se perdieron — depósitos de combustible, base de submarinos",
"""El ataque japonés logra casi completamente sus objetivos tácticos. Pero se pierde tres cosas.

Primero: los portaaviones. USS Enterprise, Lexington y Saratoga están todos en el mar el 7 de diciembre. Los portaaviones que decidirán la Guerra del Pacífico están intactos.

Segundo: los depósitos de combustible. Pearl Harbor tiene 6.8 millones de litros de petróleo en tanques de almacenamiento a nivel del suelo. El ataque los ignora.

Tercero: la base de submarinos y los astilleros de reparación.

Yamamoto comprende de inmediato lo que se ha y no se ha logrado. Temo que hemos despertado a un gigante dormido, según se dice que afirmó, y lo hemos llenado de una terrible determinación.

El 8 de diciembre, el Presidente Roosevelt se dirige al Congreso. El Congreso vota por la guerra contra Japón 82-0 en el Senado y 388-1 en la Cámara.

Japón ha logrado el éxito táctico. Ha logrado la catástrofe estratégica."""),

(7,"AFTERMATH & LEGACY","10:00–12:30",
"Archival: Fábricas de producción bélica de EE.UU., portaaviones en el Pacífico",
"Mapa: Estrategia de salto de isla en isla en la Guerra del Pacífico 1942-1945",
"""El ataque transformó la opinión pública americana de la noche a la mañana. El movimiento aislacionista dejó de existir el 8 de diciembre de 1941.

Entre 1941 y 1945, los Estados Unidos produjeron 300,000 aviones, 86,000 tanques, 8,800 naves navales y 2.7 millones de ametralladoras.

Japón produjo una fracción de esto.

El historiador Gordon Prange, quien pasó 37 años investigando Pearl Harbor, concluyó que el ataque fue el mayor error estratégico en la historia japonesa. No porque fallara tácticamente, sino porque garantizó la participación de la única potencia que Japón había acordado que no podía permitirse combatir."""),

(8,"CLOSING HOOK","12:30–13:30",None,None,
"""En 90 minutos un domingo por la mañana, Japón logró una de las sorpresas tácticas más completas de la historia militar.

También garantizó su propia derrota.

Porque el cálculo estratégico completo de Japón descansaba en una sola suposición: que un ataque sorpresa devastador rompería la voluntad de lucha de América en lugar de unificarla.

La suposición estaba equivocada. Catastróficamente, irreversiblemente equivocada.

La próxima semana, en Midway — 4 de junio de 1942. Los cuatro minutos que revirtieron todo lo que Japón había construido en Pearl Harbor y más allá.

Suscríbanse."""),
],
"thumb":"""OPTION A — HIGH CTR
Background: USS Arizona explosion — the iconic full-color archival photograph, maximum drama
Foreground: Timestamp 7:55 AM in red digital font, upper left corner
Color grade: Warm sepia with orange fire tones — archival feel but vivid
Text overlay: 90 MINUTES — massive, white Impact font, center bottom
Mood: Countdown. The viewer feels the clock ticking before clicking.

OPTION B — BETRAYAL ANGLE
Background: Japanese Zero fighters in formation over the Pacific — seen from below
Foreground: American flag reflection in calm harbor water — peaceful, about to be shattered
Color grade: Split: calm blue water below, war-orange sky above
Text overlay: THEY NEVER SAW IT COMING
Mood: Vulnerability + shock.

OPTION C — AFTERMATH
Background: Aerial view of Pearl Harbor with ships burning — iconic December 7th photograph
Foreground: Large red number 2,403 — Americans killed
Color grade: Desaturated with red accent on the number
Text overlay: AMERICA'S DARKEST MORNING

THUMBNAIL TEXT RANKING:
1. 90 MINUTES — pure number shock, implies massive consequence from tiny time window
2. THEY NEVER SAW IT COMING — betrayal formula, maximum click impulse
3. AMERICA'S DARKEST MORNING — atmospheric, geographic specificity
4. 2,403 AMERICANS — number shock with human cost
5. THE SLEEPING GIANT — Yamamoto quote reference, recognizable to history viewers

CANVA SEARCH TERMS: uss arizona explosion pearl harbor 1941 | japanese zero fighter pacific | pearl harbor aerial view december 1941""",
"seo_desc":"""In 90 minutes on a Sunday morning, Japan achieved a tactical masterpiece — and guaranteed its own defeat.

In this documentary, we reveal what Japan's attack actually missed, why Admiral Yamamoto opposed the operation before it was launched, and how Pearl Harbor created the exact outcome Japan had agreed it must avoid.

On December 7th, 1941, 353 Japanese aircraft attacked the US Pacific Fleet at Pearl Harbor in two waves. The attack sank or damaged 18 ships, destroyed 347 aircraft, and killed 2,403 Americans. It also failed to destroy the three aircraft carriers that would decide the Pacific War, missed 4.5 million barrels of oil in above-ground storage, and left the repair yards and submarine base completely intact.

What makes Pearl Harbor a uniquely instructive event is that its architect — Admiral Yamamoto — predicted its strategic failure before the first plane took off. His warning to Japan's war cabinet was explicit: America's industrial capacity makes prolonged war unwinnable. The attack itself proved him right within six months.

Historian Gordon Prange, after 37 years of research, called Pearl Harbor the greatest strategic blunder in Japanese history — not because it failed tactically, but because it guaranteed involvement of the one power Japan could not afford to fight.

CHAPTERS:
0:00  Sunday Morning at Pearl Harbor
1:30  Japan's Impossible Calculation
3:15  The Route Nobody Watched — 12 Days of Silence
5:00  7:55 AM — Tora Tora Tora
7:00  What Japan Missed — And Why It Decided Everything
9:30  The Day That Ended American Isolationism
11:00 From Pearl Harbor to Hiroshima: The 1,347-Day Arc

SOURCES:
At Dawn We Slept — Gordon Prange
Infamy: Pearl Harbor and Its Aftermath — John Toland
Eagle Against the Sun — Ronald Spector

Subscribe for a new WWII documentary every week.

#WWII #WorldWar2 #MilitaryHistory #PearlHarbor #PacificWar""",
},

]  # end of videos list (abbreviated — 2 of 10 shown for structure test)

# ══════════════════════════════════════
# COVER
# ══════════════════════════════════════
doc.add_paragraph(); doc.add_paragraph()
ctr(doc,"WWII FACELESS CHANNEL",14,bold=True,color=RED)
ctr(doc,"10-VIDEO PRODUCTION PACKAGE",22,bold=True,color=DARK)
ctr(doc,"Scripts EN + ES · SEO · Thumbnails · Visual Briefs",12,italic=True,color=GRAY)
doc.add_paragraph(); div(doc); doc.add_paragraph()
ctr(doc,"Scripts: 8-part structure · ~1,400 words each · ElevenLabs-ready",10,color=GRAY)
ctr(doc,'Voices: EN "Daniel" / "Antoni"  |  ES "Mateo" / "Sergio"',10,color=GRAY)
ctr(doc,"Settings: Speed 0.93 · Stability 0.75 · Clarity 0.80",10,color=GRAY)
doc.add_paragraph(); div(doc)

video_index = [
    "V01 · Battle of Britain — How 1,000 Pilots Saved Western Civilization",
    "V02 · Pearl Harbor — The 90-Minute Attack That Changed the World",
    "V03 · The Sinking of the Bismarck — Germany's Greatest Naval Disaster",
    "V04 · Rommel's Last Secret — The Desert Fox Who Died for Knowing Too Much",
    "V05 · The Manhattan Project — How America Built the Bomb in 3 Years",
    "V06 · Fall of France — How Europe's Most Powerful Army Collapsed in 6 Weeks",
    "V07 · Battle of Midway — 4 Minutes That Changed the Pacific War",
    "V08 · Iwo Jima — The 36 Days That Broke Two Nations",
    "V09 · The Night Witches — Soviet Women Who Terrified the Luftwaffe",
    "V10 · Operation Mincemeat — The Dead Man Who Changed the War",
]
doc.add_paragraph()
for v in video_index:
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(v); r.font.size=Pt(9.5); r.font.color.rgb=DARK
doc.add_page_break()

# ══════════════════════════════════════
# RENDER VIDEOS
# ══════════════════════════════════════
for vid in videos:
    n   = vid["num"]
    ten = vid["title_en"]
    tes = vid["title_es"]

    # ── ENGLISH SCRIPT
    h1(doc,f"VIDEO {n:02d} — {ten}")
    ctr(doc,f"Formula: {vid['formula']}  |  {vid['chars']}  |  Keyword: {vid['keyword']}",9,italic=True,color=GRAY)
    doc.add_paragraph()
    h2(doc,"SCRIPT — ENGLISH (AMERICAN)")
    div(doc)

    for (pn,ptitle,ptc,pvis_note,parch_note,ptext) in vid["parts_en"]:
        ph(doc,pn,ptitle,ptc)
        if pvis_note:  vis(doc,f"B-ROLL: {pvis_note}")
        if parch_note: vis(doc,f"ARCHIVAL: {parch_note}")
        bd(doc,ptext)

    doc.add_page_break()

    # ── SPANISH SCRIPT
    h2(doc,"SCRIPT — SPANISH (LATIN AMERICAN)")
    div(doc)
    for (pn,ptitle,ptc,pvis_note,parch_note,ptext) in vid["parts_es"]:
        ph(doc,pn,ptitle,ptc)
        if pvis_note:  vis(doc,f"B-ROLL: {pvis_note}")
        if parch_note: vis(doc,f"ARCHIVAL: {parch_note}")
        bd(doc,ptext)

    doc.add_page_break()

    # ── SEO PACKAGE
    h2(doc,f"SEO PACKAGE — VIDEO {n:02d}")
    div(doc)
    tb(doc,"OPTIMIZED TITLE (EN)",ten)
    tb(doc,"OPTIMIZED TITLE (ES)",tes)
    tb(doc,"CHARACTER COUNT",vid["chars"])
    tb(doc,"PRIMARY KEYWORD",vid["keyword"])
    tb(doc,"SECONDARY KEYWORDS",vid["secondary"])
    tb(doc,"HASHTAGS",vid["hashtags"])
    tb(doc,"TOPIC TAGS",vid["topic_tags"])
    tb(doc,"LONG-TAIL TAGS",vid["longtail_tags"])
    tb(doc,"BEST POST DATE",vid["post"])
    tb(doc,"SOURCES",vid["sources"])
    doc.add_paragraph()
    h2(doc,"FULL DESCRIPTION (publish-ready)")
    bd(doc,vid["seo_desc"])
    doc.add_page_break()

    # ── THUMBNAIL BRIEF
    h2(doc,f"THUMBNAIL BRIEF — VIDEO {n:02d}")
    div(doc)
    bd(doc,vid["thumb"])
    doc.add_page_break()

# ── SAVE
path="/home/user/ROBOS-TRADING/WWII_10Videos_Package.docx"
doc.save(path)
print(f"Saved: {path}")
