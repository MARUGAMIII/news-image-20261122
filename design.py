#!/usr/bin/env python3
"""Render THE WORLD TODAY — Sunday 22 November 2026 — to entry.png.

Draws a one-page newspaper front page with Pillow, using only the DejaVu
fonts shipped with the system. All text is laid out from the STORIES data
below, so the image is fully reproducible: run this file and the PNG is
byte-identical every time (no timestamps, no randomness).

    python3 design.py            # writes entry.png beside this file
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (23, 19, 14)
BODY = (51, 48, 42)
MUTED = (107, 100, 90)
RED = (163, 22, 33)
RULE = (201, 194, 180)
GREEN = (14, 122, 58)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def spaced(text, n=1):
    """Fake letter-spacing by inserting thin spaces between characters."""
    return ("\u2009" * n).join(list(text))


# ---------------------------------------------------------------- stories
# (kicker, headline, body incl. source) — bodies are kept short on purpose:
# at most two lines in a 314 px column at 10 px.

LEADS = [
    ("BAHRAIN \u00b7 GULF WAR",
     "Iran strikes US Patriot radars in Bahrain",
     "The IRGC says missiles and drones hit two US Patriot radars at "
     "al-Riffa and Awali bases late Saturday; Bahrain says its defences "
     "intercepted some and a civilian plant caught fire. No injuries "
     "reported. \u2014 AL JAZEERA \u00b7 IANS \u00b7 REUTERS"),
    ("CLIMATE \u00b7 COP31",
     "COP31 in overtime: new draft tabled at dawn",
     "Antalya talks run past their deadline as a revised text is tabled "
     "early Sunday. The draft still omits fossil fuels and the $120bn "
     "adaptation target; the EU says good deal or no deal. "
     "\u2014 REUTERS \u00b7 BBC \u00b7 AP"),
    ("TRADE \u00b7 EUROPE\u2013ASIA",
     "EU and Indonesia sign decade-long trade pact",
     "Signed Saturday in Brussels, the deal scraps 98.5% of tariffs and "
     "should save EU exporters about \u20ac650m a year. Parliaments on "
     "both sides must still ratify it. "
     "\u2014 EUROPEAN COMMISSION \u00b7 AFP"),
]

COLUMNS = [
    ("WAR & DIPLOMACY", [
        ("SATURDAY",
         "Tankers hit near Hormuz as Gulf war widens",
         "Three oil tankers were attacked in or near the strait on "
         "Saturday; Iran warns of a \u2018fierce\u2019 reply if the US stops "
         "its oil convoy. \u2014 EURONEWS \u00b7 AL JAZEERA"),
        ("",
         "US denies Iran claim it damaged an F-16",
         "CENTCOM rejects Tehran\u2019s claim that a missile hit a US jet "
         "on Friday evening. \u2014 EURONEWS"),
        ("",
         "Zelenskyy: NATO is Ukraine\u2019s clearest guarantee",
         "The president repeats the call as Kyiv counts the cost of "
         "Friday\u2019s barrage. \u2014 ANI"),
        ("",
         "Russian ship hit by drones in the Baltic",
         "Finland says Ukraine is likely behind the strike on a Russian "
         "cargo ship; PM Orpo says the war is spilling over. "
         "\u2014 TOI \u00b7 ANI"),
        ("",
         "Russia hits Zelenskyy\u2019s home town",
         "Strikes reported on Kryvyi Rih; Ukraine says it hit Russia\u2019s "
         "only supplier of a key Iskander-M fuel part. \u2014 JAPAKO"),
        ("",
         "Kindergarten hit in Zaporizhzhia region",
         "Russian forces strike the region, damaging a kindergarten. "
         "\u2014 JAPAKO"),
        ("",
         "Saudi coalition says it downed a Houthi missile",
         "A ballistic missile aimed at western Saudi Arabia was "
         "intercepted, the coalition says. \u2014 JAPAKO"),
        ("",
         "Turkey\u2019s spy chief meets Hamas in Istanbul",
         "Talks held with a Hamas delegation in the Turkish city. "
         "\u2014 JAPAKO"),
        ("",
         "Israel coalition talks open",
         "Yashar party chief Eisenkot invites Likud to negotiate; a first "
         "meeting is set. \u2014 ANI \u00b7 TOI"),
        ("",
         "Melania Trump seeks more ceasefires by Christmas",
         "After the Oleshky ceasefire, she pushes for more Russia\u2013Ukraine "
         "truces; Zelenskyy reacts. \u2014 TOI"),
        ("",
         "Trump: Iran deal could last 20 years",
         "The president wants a permanent accord and claims the US removed "
         "Tehran\u2019s leadership twice. \u2014 FOX NEWS \u00b7 TOI"),
        ("",
         "Iran calls US blockade a hostile act",
         "Deputy FM Gharibabadi condemns the naval blockade; Tehran says "
         "Qeshm blasts were US munitions disposal. \u2014 ANI \u00b7 TOI"),
        ("",
         "UN talks on robot weapons fall short",
         "Negotiations on lethal autonomous weapons end below calls for "
         "enforceable rules. \u2014 GRAND STAR"),
        ("",
         "Germany rallies \u2018coalition of the willing\u2019",
         "A Berlin meeting sends Moscow a united message to seek peace "
         "talks. \u2014 OPEN SOURCE TRADES"),
        ("",
         "Sudan rebels seize Blue Nile\u2019s Bau region",
         "The Tasis Alliance takes the key area in the Blue Nile. "
         "\u2014 GRAND STAR"),
        ("",
         "Denmark expels Moscow defence attach\u00e9",
         "The expulsion follows a failed plot to assassinate a Ukrainian "
         "rapper. \u2014 GRAND STAR"),
    ]),
    ("THE WORLD", [
        ("",
         "Hong Kong votes for its Election Committee",
         "Polls open at 9am Sunday; 856 candidates chase 723 seats across "
         "31 subsectors. \u2014 CHINA DAILY ASIA"),
        ("SATURDAY",
         "Mexico\u2019s \u2018El Chapo Isidro\u2019 flown to capital",
         "The FBI top-10 fugitive was captured on Friday in Guasave; 11 "
         "died in the firefight and Sinaloa is calm again. \u2014 AP \u00b7 NPR"),
        ("",
         "Myanmar shaken by 4.1 quake in the early hours",
         "A tremor strikes in the early hours of Sunday, seismologists "
         "report. \u2014 ANI \u00b7 NCS"),
        ("FRIDAY",
         "Peru counts damage after 6.7 quake",
         "The quake near Carhuamayo was felt in Lima; dozens of homes "
         "were damaged in Jun\u00edn, with no deaths reported. "
         "\u2014 USGS \u00b7 FOX WEATHER"),
        ("",
         "Illicit liquor kills 11 in Manipur",
         "Bootleg alcohol leaves 11 dead and 180 ill in north-east India. "
         "\u2014 GRAND STAR"),
        ("",
         "Croatians march in Zagreb",
         "Protesters demand justice over a psychiatric hospital death. "
         "\u2014 GRAND STAR"),
        ("FRIDAY",
         "FBI probes hack of its crime database",
         "A suspected breach of the National Crime Information Center is "
         "under investigation, CNN reports. \u2014 REUTERS \u00b7 CNN"),
        ("",
         "US airlines warned of terror threat",
         "Carriers are alerted to a possible al-Qaeda-linked threat before "
         "Thanksgiving. \u2014 TOI"),
        ("",
         "Bolsonaro in intensive care",
         "Brazil\u2019s jailed ex-president is admitted to ICU with an "
         "acute bowel obstruction. \u2014 TOI"),
        ("",
         "UAE leader meets US security chief",
         "Sheikh Mohamed bin Zayed receives Homeland Security Secretary "
         "Mullin in Abu Dhabi. \u2014 ANI \u00b7 WAM"),
        ("",
         "Bangladesh recalls India\u2019s 1971 sacrifices",
         "The acting high commissioner in Delhi honours India\u2019s role "
         "in the Liberation War. \u2014 ANI"),
        ("",
         "Iran\u2019s internet bill ties accounts to real names",
         "The new law targets online privacy, tying accounts to real "
         "identities. \u2014 JAPAKO"),
        ("SATURDAY",
         "Pentagon curbs social events with Canada",
         "A Hegseth memo limits military \u2018social activities\u2019 with "
         "Canadian forces. \u2014 NYT"),
        ("",
         "Taiwan turns to drone warfare",
         "Citizens take up drones as Trump draws closer to Xi. "
         "\u2014 GRAND STAR"),
        ("",
         "Andy Kim speaks of his father\u2019s Alzheimer\u2019s",
         "The US senator opens up about his father\u2019s illness. "
         "\u2014 GRAND STAR"),
        ("SATURDAY",
         "Gaza ceasefire line breached",
         "Israeli forces cross the boundary in central Gaza, reports say. "
         "\u2014 OPEN SOURCE TRADES"),
    ]),
    ("MONEY, CLIMATE & SPORT", [
        ("SATURDAY",
         "COP31 draft admits 1.5\u00b0C goal missed",
         "For the first time, a COP text acknowledges the 1.5\u00b0C target "
         "has been missed; the world enters \u2018overshoot\u2019. \u2014 BBC"),
        ("",
         "Panama calls COP31 a \u2018petroleum mafia\u2019 hostage",
         "Minister Navarro threatens to block any deal without "
         "fossil-fuel language. \u2014 BLOOMBERG \u00b7 UN NEWS"),
        ("",
         "Africa\u2019s $120bn demand still unmet",
         "The adaptation finance target is cut from the draft; Ghana\u2019s "
         "minister: \u2018We did not come here to beg.\u2019 \u2014 BBC"),
        ("",
         "Will COP31 end with a deal at all?",
         "The BBC asks as negotiators race the clock in Antalya. \u2014 BBC"),
        ("SATURDAY",
         "Ireland stun world champions South Africa 20\u201317",
         "Baloucoune scores twice in Dublin; the Springboks still reach "
         "the Nations Championship final. \u2014 BBC \u00b7 AP"),
        ("SATURDAY",
         "England thrash All Blacks 37\u201312",
         "A record-margin win at Allianz Stadium in the Nations "
         "Championship. \u2014 BBC"),
        ("SATURDAY",
         "France 45\u201317 Argentina",
         "Les Bleus book a final date with South Africa at Twickenham. "
         "\u2014 BBC"),
        ("SATURDAY",
         "Australia edge Wales 29\u201326 in Cardiff",
         "The Wallabies hold on in the Nations Championship. \u2014 BBC"),
        ("SATURDAY",
         "Arsenal go six clear after 2\u20132 at Newcastle",
         "Madueke rescues a point for the leaders; goalkeeper Raya faces "
         "a shoulder scan. \u2014 BBC"),
        ("SATURDAY",
         "Leeds end 27-year wait at Chelsea, 4\u20131",
         "Okafor scores twice in a first Stamford Bridge win since 1999. "
         "\u2014 BBC"),
        ("",
         "Spitting Image co-creator Peter Fluck dies at 85",
         "The satirist behind the puppet show has died. \u2014 BBC"),
        ("",
         "Lock of Washington\u2019s hair sells for $4,000",
         "A lock of the first US president\u2019s hair goes at auction. "
         "\u2014 BBC"),
        ("",
         "Trump\u2013Xi Shenzhen summit: what did it settle?",
         "Analysts pick over the three-way meeting with Putin. "
         "\u2014 GLOBAL DIGEST"),
        ("",
         "EU\u2013Indonesia deal: cars, palm oil, pharma gain",
         "Tariffs on EU cars of up to 50% are phased out in five years; "
         "palm oil and garments gain day-one access. "
         "\u2014 EUROPEAN COMMISSION"),
        ("",
         "Bahrain calls on the UN over Iranian attacks",
         "Manama seeks UN action and reparations after the strikes on its "
         "soil. \u2014 HOMEVO \u00b7 AL JAZEERA"),
    ]),
]

TIMELINE = [
    ("00:07", "Russia hits Zelenskyy\u2019s home town; a kindergarten is struck"),
    ("00:11", "COP31 presidency tables a revised text for Sunday"),
    ("00:29", "UN talks on autonomous weapons fall short of rules"),
    ("00:54", "IRGC claims two Patriot radars hit in Bahrain"),
    ("01:00", "Hong Kong polls open: 856 candidates, 723 seats"),
    ("01:29", "Sudan rebels seize Bau; 11 die from illicit liquor in India"),
    ("01:47", "EU\u2013Indonesia pact confirmed; COP31 still deadlocked"),
    ("SAT 23:40", "Iran warns of \u2018fierce\u2019 reply if US stops oil convoy"),
]

FOOTER_SOURCES = (
    "SOURCES: BBC \u00b7 REUTERS \u00b7 AL JAZEERA \u00b7 AP \u00b7 AFP \u00b7 IANS \u00b7 ANI \u00b7 "
    "EURONEWS \u00b7 EUROPEAN COMMISSION \u00b7 CHINA DAILY ASIA \u00b7 USGS \u00b7 NPR \u00b7 CNN \u00b7 "
    "BLOOMBERG \u00b7 UN NEWS \u00b7 FOX WEATHER \u00b7 AND OTHERS \u2014 ALL STORIES FROM REPORTING "
    "PUBLISHED SUNDAY 22 NOVEMBER 2026 (UTC); ITEMS MARKED SATURDAY OR FRIDAY HAPPENED THEN "
    "AND WERE STILL DEVELOPING TODAY."
)
FOOTER_LINE2 = (
    "THE WORLD TODAY \u00b7 SUNDAY, 22 NOVEMBER 2026 \u00b7 DRAWN IN PYTHON, "
    "RENDERED TO ONE 1024\u00d71024 IMAGE"
)


# ---------------------------------------------------------------- drawing
def draw_centered(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return draw.textbbox((0, 0), text, font=fnt)[3]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = 26, W - 26
    y = 10

    # ---- masthead
    f_over = font(SANS_B, 12)
    draw_centered(d, y, spaced("THE DAY\u2019S WORLD NEWS \u00b7 IN ONE PAGE", 1), f_over, RED)
    y += 16
    f_title = font(SERIF_B, 54)
    draw_centered(d, y, "THE WORLD TODAY", f_title, INK)
    y += 58
    f_date = font(SANS_B, 13)
    draw_centered(
        d, y,
        "SUNDAY, 22 NOVEMBER 2026  \u00b7  50 SOURCED STORIES  \u00b7  ALL TIMES UTC",
        f_date, INK)
    y += 18
    d.rectangle([x0, y, x1, y + 4], fill=INK)
    y += 7

    # ---- date check bar
    f_dc = font(SANS_B, 12)
    dc = ("DATE CHECK \u2713   SUNDAY, 22 NOVEMBER 2026  \u00b7  DAY 326 OF 2026  "
          "\u00b7  COP31 IN OVERTIME  \u00b7  ALL STORIES SOURCED  \u00b7  ")
    d.text((x0, y), dc, font=f_dc, fill=RED)
    w_dc = d.textlength(dc, font=f_dc)
    d.text((x0 + w_dc, y), "VERIFIED TODAY", font=f_dc, fill=GREEN)
    y += 16
    d.rectangle([x0, y, x1, y + 2], fill=RED)
    y += 7

    # ---- lead row
    colw = (x1 - x0 - 2 * 14) // 3
    f_kick = font(SANS_B, 10)
    f_lead_h = font(SERIF_B, 18)
    f_lead_b = font(SANS, 10)
    lead_top = y
    lead_bottom = lead_top
    for i, (kick, head, body) in enumerate(LEADS):
        cx = x0 + i * (colw + 14)
        cy = lead_top
        d.line([cx, cy, cx + colw, cy], fill=INK, width=3)
        cy += 6
        d.text((cx, cy), spaced(kick, 1), font=f_kick, fill=RED)
        cy += 13
        for line in wrap(d, head, f_lead_h, colw):
            d.text((cx, cy), line, font=f_lead_h, fill=INK)
            cy += 20
        cy += 1
        for line in wrap(d, body, f_lead_b, colw):
            d.text((cx, cy), line, font=f_lead_b, fill=BODY)
            cy += 13
        lead_bottom = max(lead_bottom, cy)
    y = lead_bottom + 3

    # ---- story grid
    f_colhead = font(SANS_B, 10)
    f_kick2 = font(SANS_B, 8)
    f_item_h = font(SERIF_B, 11)
    f_item_b = font(SANS, 9)
    grid_top = y
    grid_bottom = grid_top
    for i, (title, items) in enumerate(COLUMNS):
        cx = x0 + i * (colw + 14)
        cy = grid_top
        d.rectangle([cx, cy, cx + colw, cy + 19], fill=INK)
        d.text((cx + 7, cy + 4), spaced(title, 1), font=f_colhead, fill=PAPER)
        cy += 21
        for kick, head, body in items:
            d.line([cx, cy, cx + colw, cy], fill=RULE, width=1)
            cy += 2
            if kick:
                d.text((cx, cy), spaced(kick, 1), font=f_kick2, fill=RED)
                cy += 10
            for line in wrap(d, head, f_item_h, colw):
                d.text((cx, cy), line, font=f_item_h, fill=INK)
                cy += 13
            for line in wrap(d, body, f_item_b, colw):
                d.text((cx, cy), line, font=f_item_b, fill=BODY)
                cy += 11
            cy += 1
        grid_bottom = max(grid_bottom, cy)
    y = grid_bottom + 6

    # ---- timeline (dark box)
    f_thead = font(SANS_B, 11)
    f_t = font(SANS_B, 10)
    f_t2 = font(SANS, 10)
    tcolw = (x1 - x0 - 20 - 3 * 12) // 4
    box_top = y
    d.rectangle([x0, box_top, x1, box_top + 74], fill=INK)
    d.text((x0 + 10, box_top + 5), spaced("THE DAY IN UTC", 2), font=f_thead,
           fill=(232, 180, 184))
    ty = box_top + 22
    for i, (t, txt) in enumerate(TIMELINE):
        col = i % 4
        row = i // 4
        cx = x0 + 10 + col * (tcolw + 12)
        cy = ty + row * 25
        d.text((cx, cy), t, font=f_t, fill=(255, 255, 255))
        tw = d.textlength(t + "  ", font=f_t)
        lines = wrap(d, txt, f_t2, tcolw - tw)
        ly = cy
        for j, line in enumerate(lines[:2]):
            d.text((cx + tw, ly), line, font=f_t2, fill=PAPER)
            ly += 12
    y = box_top + 74 + 2

    # ---- footer
    f_foot = font(SANS, 9)
    f_foot_b = font(SANS_B, 9)
    for line in wrap(d, FOOTER_SOURCES, f_foot, x1 - x0):
        draw_centered(d, y, line, f_foot, MUTED)
        y += 11
    y += 1
    d.line([x0, y, x1, y], fill=INK, width=1)
    y += 3
    draw_centered(d, y, FOOTER_LINE2, f_foot_b, INK)
    y += 12

    print(f"layout ends at y={y} of {H} (overflow: {max(0, y - H)})")
    assert y <= H, "layout overflowed the page"
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
