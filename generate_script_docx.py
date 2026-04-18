from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# ── Page margins
for section in doc.sections:
    section.top_margin    = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin   = Inches(1.2)
    section.right_margin  = Inches(1.2)

# ── Helpers
def add_title(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(20)
    run.font.color.rgb = RGBColor(0x1A, 0x1A, 0x2E)

def add_subtitle(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    run.italic = True

def add_section_header(doc, number, title, timecode):
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run(f"PART {number} — {title}  [{timecode}]")
    run.bold = True
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0xC0, 0x39, 0x2B)
    p2 = doc.add_paragraph()
    run2 = p2.add_run("─" * 60)
    run2.font.size = Pt(9)
    run2.font.color.rgb = RGBColor(0xBB, 0xBB, 0xBB)

def add_note(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(f"[{text}]")
    run.italic = True
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

def add_body(doc, text):
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line:
            doc.add_paragraph()
            continue
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(line)
        run.font.size = Pt(11)

# ══════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()
add_title(doc, "WHAT IF D-DAY HAD FAILED?")
add_title(doc, "How Hitler Would Have Won the War")
doc.add_paragraph()
add_subtitle(doc, "WWII Faceless Documentary Channel — Full Voiceover Script")
add_subtitle(doc, "~1,420 words  |  ~10:50 min at 130 wpm  |  English Version")
doc.add_paragraph()
doc.add_paragraph()
add_subtitle(doc, "Production Notes")
add_subtitle(doc, "Narrate each PART separately for easier re-editing.")
add_subtitle(doc, "ElevenLabs settings: Speed 0.93 · Stability 0.75 · Clarity 0.80")
add_subtitle(doc, 'Recommended voice: "Daniel" or "Antoni"')
doc.add_page_break()

# ══════════════════════════════════════════════
# PART 1
# ══════════════════════════════════════════════
add_section_header(doc, 1, "COLD OPEN", "0:00 – 0:45")
add_note(doc, "B-roll: Omaha Beach archival footage, landing craft, bodies in surf")
add_body(doc, """
It is 6:30 in the morning on June 6th, 1944.

Off the coast of Normandy, 156,000 Allied soldiers are crossing the Channel. Behind them, the largest naval armada ever assembled... 6,939 ships. Above them, 11,590 aircraft. The plan has taken two years to build. The logistics alone required moving the equivalent of a small nation across open water.

And in the first four hours... it is going catastrophically wrong.

On Omaha Beach, American troops are being cut down the moment they step off the landing craft. German gun positions the planners believed had been destroyed... are intact. And firing. In some sectors, entire companies are wiped out before they reach the waterline. By mid-morning, the commanding general is composing a message recommending evacuation.

What no one in that moment can know... is how close the entire operation actually is to total collapse.

And what no one has ever fully asked... is what happens to the world if it does.
""")

# ══════════════════════════════════════════════
# PART 2
# ══════════════════════════════════════════════
add_section_header(doc, 2, "THE PROMISE", "0:45 – 1:30")
add_body(doc, """
History remembers D-Day as a triumph. A story of Allied resolve overcoming the Atlantic Wall. The turning point that broke Nazi Germany.

But that story skips the part where it almost didn't happen.

In this video, we're going to do something most D-Day documentaries refuse to do... we're going to follow the failure. We're going to trace exactly what would have happened, chain link by chain link, if the Allies had been driven back into the sea on June 6th, 1944.

Because this isn't just a war game thought experiment. The consequences of a failed D-Day reach into 1945... into the atomic program... into Stalin's calculations... into the Holocaust... into the entire postwar world order.

The reality is this. A failed Normandy landing would not simply have delayed Allied victory. It may have fundamentally changed the kind of world we live in today.
""")

# ══════════════════════════════════════════════
# PART 3
# ══════════════════════════════════════════════
add_section_header(doc, 3, "CONTEXT", "1:30 – 3:30")
add_note(doc, "Map animation: Show Pas-de-Calais vs Normandy, 15th Army position, Panzer reserve locations")
add_body(doc, """
By June 1944, the war has been running for nearly five years. Germany is under pressure on every front... but it is not broken.

In the East, the Soviet Union has pushed the Wehrmacht back nearly 800 kilometers from its 1942 high-water mark. But Army Group Centre still holds a massive defensive salient in Belarus. The Eastern Front is costing Germany 900 men a day... and costing the Soviets three times that.

In Italy, Allied forces have been grinding northward since September 1943. Progress is measured in miles per month. The campaign Churchill called the soft underbelly of Europe has become, in practice, anything but.

Three men hold the outcome of D-Day in their hands.

Dwight D. Eisenhower. Supreme Commander of Allied forces. A man who has never personally commanded troops in combat, chosen not for battlefield brilliance... but for the political skill to hold a fractious coalition together.

Erwin Rommel. Commanding Army Group B. The Desert Fox, now charged with defending the French coastline. He believes the invasion must be defeated on the beaches themselves... within the first 24 hours. If the Allies get off the sand, he tells his staff... they will never be pushed back.

And Adolf Hitler. Who controls the one asset that could decide everything. The Panzer reserve. Three armored divisions sitting within striking distance of Normandy. Hitler alone holds the release authority.

And on the morning of June 6th... he is asleep.
""")

# ══════════════════════════════════════════════
# PART 4
# ══════════════════════════════════════════════
add_section_header(doc, 4, "THE BUILD", "3:30 – 6:00")
add_body(doc, """
The Allies' greatest advantage on D-Day is not firepower. It is deception.

Operation Fortitude has convinced the German high command that Normandy is a feint. The real invasion, German intelligence believes, will come at Pas-de-Calais... 200 kilometers to the northeast. A fictional army group, commanded by General Patton himself, has been constructed entirely from fake radio signals and inflatable tanks.

This deception holds the 15th German Army... 19 divisions... frozen in place at Calais. It also keeps the Panzer reserve locked down.

But Rommel doesn't need the Panzer reserve yet. He has something else. The 352nd Infantry Division, which has quietly moved into position above Omaha Beach... without Allied intelligence noticing.

When the first wave of American troops lands at Omaha at 6:30 AM, they walk into pre-sighted killing grounds. The naval bombardment has missed almost every German emplacement. The amphibious tanks that were supposed to give covering fire have sunk in the rough seas... 27 of 29 lost before reaching the shore.

Within the first two hours, American casualties at Omaha exceed 2,000 men. Several companies report 80% losses in the first ten minutes.

Now comes the decision that changes everything.

Major General Leonard Gerow, commanding V Corps at Omaha, sends a message to the command ship. Conditions are untenable. Recommend suspension of landings.

That message reaches General Omar Bradley. And Bradley... looking at the casualty reports... at the stalled advance... at the rising tide already swallowing the bodies on the sand... makes the call.

He orders the landings halted.

By 11:00 AM on June 6th, 1944... the surviving forces on Omaha Beach begin withdrawing to the water. The British beaches have had more success. But without Omaha, the landing zone has a 30-kilometer gap in the middle. The flanks are exposed.

Rommel recognizes it immediately.

He picks up the phone to OKW headquarters. He doesn't ask for the Panzers anymore.

He demands them.
""")

# ══════════════════════════════════════════════
# PART 5
# ══════════════════════════════════════════════
add_section_header(doc, 5, "MID-ROLL RE-HOOK", "6:00 – 6:30")
add_note(doc, "Music cue: shift to darker, minor-key score here")
add_body(doc, """
In just a moment, we're going to see what happens when those Panzer divisions hit the exposed Allied flanks... and we're going to follow the chain of consequences all the way to 1945... and a decision that would have rewritten the entire postwar world.

Stay with us.
""")

# ══════════════════════════════════════════════
# PART 6
# ══════════════════════════════════════════════
add_section_header(doc, 6, "THE CLIMAX", "6:30 – 10:00")
add_note(doc, "Slow narration pace here — let dramatic lines breathe")
add_body(doc, """
At 2:00 PM on June 6th, Hitler wakes up. His staff brief him on the situation. Normandy is repelling the landings. The Führer is delighted. He has always believed Normandy was a diversion.

He releases two Panzer divisions.

By evening, German armor is moving toward the beachhead. The British forces at Sword Beach, already overextended, begin taking armored pressure they were not designed to absorb alone. Without the American right flank at Omaha, there is no unified bridgehead. There are only isolated footholds... each being squeezed.

Over the next 72 hours, the battle at the beach becomes a catastrophe.

The British 6th Airborne, which had seized the bridges at Pegasus in the early hours of June 6th... holding through the night with enormous courage... is cut off. Relief never comes. Of the 2,500 men who held the bridge, fewer than 800 make it back to Allied lines.

At Sword Beach, the withdrawal begins on June 9th.

By June 12th, the last Allied forces are evacuating Normandy. Total Allied casualties... 28,000 dead. 40,000 wounded or captured. The largest amphibious operation in history has failed.

In London, Winston Churchill addresses the House of Commons. He does not use the word defeat. But the chamber is silent in a way it has never been before.

Meanwhile... in Moscow, Joseph Stalin receives the news with cold fury. He has been asking for a second front since 1941. He has been promised one, repeatedly. Now, for the second time after Dieppe in 1942, the Western Allies have failed to deliver.

His foreign minister, Molotov, begins quiet exploratory conversations with German intermediaries in Stockholm.

What the Allies don't know... is that Stalin isn't seriously pursuing a separate peace. Not yet. But he is recalculating. Every week without a Western front is a week the Red Army fights alone. Every week means more Soviet dead. Every week changes what Stalin will demand when the war finally ends.

In Germany, the strategic situation has stabilized. The Western threat is gone... for now.

And in a set of laboratories in New Mexico, a weapon is approaching completion. The Manhattan Project. The first atomic bomb will be ready by July 1945.

In this altered timeline... it will not be used against Japan.

Truman authorizes it. On August 6th, 1945... the same date as in the real timeline... a city burns.

Not Hiroshima.

Hamburg.
""")

# ══════════════════════════════════════════════
# PART 7
# ══════════════════════════════════════════════
add_section_header(doc, 7, "AFTERMATH & LEGACY", "10:00 – 12:30")
add_note(doc, "Map animation: alternate Iron Curtain line at the French border")
add_body(doc, """
The atomic bombing of Hamburg kills an estimated 80,000 people... and ends German military resistance within three weeks. Germany surrenders on September 2nd, 1945.

But the map of Europe looks nothing like the one we know.

Without the Western Allied presence in France, the liberation of Western Europe has not happened. The Red Army, pressing from the East, reaches Berlin. It continues west. By the time Germany surrenders, Soviet forces stand on the Rhine.

The postwar settlement reflects this reality. Poland. Czechoslovakia. Hungary. Romania. All Soviet sphere. But also... Austria. The Netherlands. Large parts of Germany itself. The Iron Curtain does not fall at the Elbe. It falls at the French border.

The Cold War begins not as a standoff between two roughly equal zones of influence. It begins with the Soviet Union controlling 70% of the European continent's industrial capacity.

NATO does not form in the shape we know it. It forms as a rump... Britain, France, Portugal, Spain... a western peninsula desperately rearming, with American nuclear guarantees the only thing standing between them and further Soviet expansion.

This is not speculation. It is the logical consequence, chain link by chain link, of that single decision on the morning of June 6th, 1944.

Historian John Keegan wrote that D-Day was... the most dramatic and decisive feat of arms in the Second World War. He was right. Not just because it succeeded... but because the success created the world we inherited. The German federal republic. A free France. A Marshall Plan that rebuilt Western Europe.

All of it... every institution of the postwar liberal order... flows from those first six hours on the beaches of Normandy.

Which is why understanding how close it came to failing is not an academic exercise. It is a reminder that history does not bend toward inevitable outcomes. It bends toward the decisions made by specific people, under impossible pressure, with incomplete information.
""")

# ══════════════════════════════════════════════
# PART 8
# ══════════════════════════════════════════════
add_section_header(doc, 8, "CLOSING HOOK", "12:30 – 13:30")
add_body(doc, """
D-Day succeeded because of deception. Because of courage. Because of planning measured in years and logistics measured in millions of tons. But also... and this part rarely makes it into the textbooks... because of luck. Because Hitler was asleep. Because the 352nd Division moved without Allied intelligence noticing. Because the weather window opened for exactly the right 48 hours.

Remove any one of those factors... and the chain breaks differently.

That is the lesson that D-Day teaches us. Not that the good side always wins. But that the margin between the world we got... and a darker one... was, at critical moments, razor thin.

Next week, we're going inside the intelligence operation that made Normandy possible. The spy network called Operation Fortitude... and the single agent whose false reports kept 19 German divisions frozen at Calais on June 6th. A man Hitler trusted completely. A man who was working for the British the entire time.

If that story sounds impossible... subscribe, and I'll show you the documents.
""")

# ══════════════════════════════════════════════
# FOOTER NOTE
# ══════════════════════════════════════════════
doc.add_page_break()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("— END OF SCRIPT —")
run.bold = True
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

add_subtitle(doc, "~1,420 words  |  Approx. 10:50 at 130 wpm")
add_subtitle(doc, "WWII Faceless Documentary Channel")

# ── Save
path = "/home/user/ROBOS-TRADING/What_If_DDay_Had_Failed_SCRIPT_EN.docx"
doc.save(path)
print(f"Saved: {path}")
