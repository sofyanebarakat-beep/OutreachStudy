import json, sys

APPLY = "https://apply.outreachstudy.eu/"
CONTACT = "https://outreachstudy.eu/contact/"
PHONE_TEL = "+35677200984"
PHONE = "+356 7720 0984"
BLUE = "#442dfa"  # theme colour 1 (edcare_theme_color_1)

pad = lambda t, b: {"unit": "px", "top": str(t), "right": "12", "bottom": str(b), "left": "12", "isLinked": False}


def section(i, els, bg=None, top=120, bottom=120):
    s = {"flex_direction": "column", "padding": pad(top, bottom), "padding_tablet": pad(80, 80), "padding_mobile": pad(70, 70)}
    if bg:
        s.update(background_background="classic", background_color=bg)
    return {"id": i, "elType": "container", "settings": s, "elements": els, "isInner": False}


def inner(i, els, **s):
    return {"id": i, "elType": "container", "settings": dict(content_width="full", **s), "elements": els, "isInner": True}


def w(i, t, **s):
    return {"id": i, "elType": "widget", "widgetType": t, "settings": s, "elements": []}


def heading(i, sub, title, align="center"):
    return w(i, "edcare_heading", section_subheading_icon={"value": "fas fa-bolt", "library": "fa-solid"},
             section_subheading=sub, section_title=title, section_text_align=align)


def link(url):
    return {"url": url, "is_external": "", "nofollow": "", "custom_attributes": ""}


def button(i, text, url, primary=True, icon=None, align="center"):
    s = dict(text=text, link=link(url), align=align, size="md", border_radius={"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True})
    if primary:
        s.update(background_color=BLUE, button_text_color="#FFFFFF")
    else:
        s.update(background_color="#FFFFFF", button_text_color=BLUE, border_border="solid",
                 border_width={"unit": "px", "top": "2", "right": "2", "bottom": "2", "left": "2", "isLinked": True}, border_color=BLUE)
    if icon:
        s.update(selected_icon={"value": icon, "library": "fa-solid"}, icon_indent={"unit": "px", "size": 8, "sizes": []})
    return w(i, "button", **s)


def walk(els):
    for e in els:
        yield e
        yield from walk(e.get("elements", []))


d = json.load(open(sys.argv[1]))
by_id = {e["id"]: e for e in walk(d)}

# 1. Hero: fix typos, clearer promise, correct links (the old links pointed to apply.outreachstudy.eu/admin and the empty Course page)
hero = by_id["cc7f902"]["settings"]["slider_list"][0]
hero.update(
    slider_subheading="Discover study opportunities in Malta",
    slider_title_one="Study in Malta with",
    slider_title_two=" expert help from ",
    slider_title_three="Outreach Study",
    slider_description="English courses, diplomas and degrees in Malta, with support for<br> your application, student visa and residence permit, from your<br> first question to your first day in class.",
    slider_button_text="Book a Free Consultation",
    slider_button_link=link(CONTACT),
    slider_button_text_two="Browse Study Options",
    slider_button_link_type_two="2",
    slider_button_page_link_two="7595",
)
hero["slider_image"]["alt"] = "Valletta skyline and Grand Harbour, Malta"
hero.pop("slider_button_page_link", None)

# 2. Course cards: fix copy and point "Apply Now" at the application form instead of its admin area
cards = by_id["6997472"]["settings"]["slider_list"]
for c in cards:
    c["slider_title"] = c["slider_title"].strip()
    c["slider_description"] = c["slider_description"].strip()
    c["slider_button_link"] = {"url": APPLY, "is_external": "", "nofollow": "", "custom_attributes": ""}
    for f in c["feature_list"]:
        f["feature_text"] = f["feature_text"].strip()
health, it, business, english = cards
health["feature_list"][0]["feature_text"] = "BSc (Hons) Health, Social Care and Wellbeing (Bachelor's)"
health["feature_list"][1]["feature_text"] = "Master of Public Health (Master's)"
it["feature_list"][0]["feature_text"] = "Foundation Degree in Information Technology and Study Skills"
it["feature_list"][1]["feature_text"] = "BSc (Hons) Computer Science and Information Technology (Bachelor's)"
it["feature_list"][2]["feature_text"] = "MSc Information Technology Management (Master's)"
business["slider_description"] = "Prepares you for a career in leadership, management and entrepreneurship through its Business and Management programs."
business["feature_list"][0]["feature_text"] = "Foundation Degree in Business Management and Study Skills"
business["feature_list"][1]["feature_text"] = "Master of Business Administration (MBA)"
english["slider_title"] = "Learn English in 10 Weeks (Online)"
health["service_slider_image"]["alt"] = "Two students studying together on a laptop in a library"
it["service_slider_image"]["alt"] = "Students studying together on a laptop in a café"
business["service_slider_image"]["alt"] = "Students and teacher joining hands in a study group"
# Professional English Programme: facts as published on /study-english-in-malta/
cards.insert(0, {
    "_id": "pe2026a",
    "slider_title": "Professional English Programme in Malta",
    "slider_description": "A full-time English programme in Malta with an EU qualification, a residence permit and the right to work part-time.",
    "slider_button_text": "View Programme",
    "slider_button_link": link("https://outreachstudy.eu/study-english-in-malta/"),
    "feature_list": [
        {"feature_icon": {"value": "fas fa-check", "library": "fa-solid"}, "feature_text": "12 months full-time, MQF Level 4, 48 ECTS", "_id": "pe2026b"},
        {"feature_icon": {"value": "fas fa-check", "library": "fa-solid"}, "feature_text": "Residence permit and part-time work rights", "_id": "pe2026c"},
        {"feature_icon": {"value": "fas fa-check", "library": "fa-solid"}, "feature_text": "Launch price €3,950 (standard €4,950)", "_id": "pe2026d"},
    ],
    "activeItemIndex": 1,
    "service_slider_image": {"url": "https://outreachstudy.eu/wp-content/uploads/2025/02/offer-img.png", "id": 4508, "size": "", "alt": "International students studying together outdoors in Malta", "source": "library"},
})
by_id["a96a953"]["settings"].update(section_subheading="Programmes", section_title="Find Your Programme in Malta")

# 3. About block: button label + link
by_id["42cc0a9"]["settings"].update(button_text="About Outreach Study")

# 4. New sections
trust = section("hs10001", [inner("hs10002", [
    w("hs10003", "heading", title="Study in Malta: English Courses, Diplomas and Degrees with Visa Support", header_size="h1",
      align="center", title_color="#162726", typography_typography="custom", typography_font_size={"unit": "px", "size": 32, "sizes": []},
      typography_font_size_mobile={"unit": "px", "size": 24, "sizes": []}, typography_font_weight="600"),
    w("hs10004", "icon-list", view="inline", icon_align="center", space_between={"unit": "px", "size": 28, "sizes": []},
      icon_color=BLUE, text_color="#3A3D3E", icon_list=[
          {"text": "EU-recognised qualifications", "selected_icon": {"value": "fas fa-graduation-cap", "library": "fa-solid"}, "_id": "hs1000a"},
          {"text": "Student visa and residence permit support", "selected_icon": {"value": "fas fa-passport", "library": "fa-solid"}, "_id": "hs1000b"},
          {"text": "Free consultation", "selected_icon": {"value": "fas fa-comments", "library": "fa-solid"}, "_id": "hs1000c"},
      ]),
])], bg="#F2F4F7", top=40, bottom=40)


def step(i, n, icon, title, text):
    return inner("c" + i, [w(i, "icon-box", selected_icon={"value": icon, "library": "fa-solid"}, view="stacked",
                                primary_color=BLUE, title_text=f"{n}. {title}", description_text=text, title_size="h3")])


how = section("hs20001", [
    inner("hs20002", [heading("hs20003", "How It Works", "Your Path to Studying in Malta in 4 Steps")]),
    inner("hs20004", [
        step("hs20005", 1, "fas fa-comments", "Free Consultation", "Tell us your goals, budget and background. We answer your questions and explain your options."),
        step("hs20006", 2, "fas fa-graduation-cap", "Choose Your Programme", "We help you compare English courses, diplomas and degrees and pick the right school."),
        step("hs20007", 3, "fas fa-passport", "Application and Visa", "We help you prepare your documents, apply to your school and get ready for your visa and residence permit."),
        step("hs20008", 4, "fas fa-plane-arrival", "Arrive in Malta", "We share practical advice on accommodation, living costs and settling into student life."),
    ], flex_direction="row", flex_wrap_tablet="wrap"),
    inner("hs20009", [button("hs2000a", "Book a Free Consultation", CONTACT)]),
])

FAQ = [
    ("Do I need a visa to study in Malta?",
     "Students from the EU do not need a visa. Most students from outside the EU need a student visa and a residence permit for courses longer than 90 days. Requirements depend on your nationality and your course, and we help you prepare your application."),
    ("Can I work while studying in Malta?",
     "Yes. Non-EU students with a valid student residence permit can usually work up to 20 hours per week. Read our <a href=\"https://outreachstudy.eu/work-while-studying-in-malta/\">guide to working while studying in Malta</a> for the rules and job types."),
    ("How much does it cost to study in Malta?",
     "It depends on the programme and school. For example, our 12-month Professional English Programme has a launch price of €3,950. See our <a href=\"https://outreachstudy.eu/studying-in-malta-on-a-budget-a-guide-to-affordability-in-malta/\">guide to the cost of studying in Malta</a> for living costs."),
    ("What level of English do I need?",
     "English courses accept all levels. Diplomas and degrees usually ask for proof of English, such as an IELTS score or an equivalent test. We tell you the exact level your chosen programme needs."),
    ("Can I stay in Malta after I graduate?",
     "Eligible graduates can apply for a 9-month post-study visa extension to look for work in Malta and gain international experience."),
    ("How does Outreach Study help me?",
     "We give you a free consultation, help you choose a programme and school, support your application, visa and residence permit, and give practical advice for your arrival in Malta."),
]
faq = section("hs30001", [
    inner("hs30002", [heading("hs30003", "FAQ", "Questions About Studying in Malta")]),
    inner("hs30004", [w("hs30005", "accordion", tabs=[{"tab_title": q, "tab_content": f"<p>{a}</p>", "_id": f"hsq{n:04d}"} for n, (q, a) in enumerate(FAQ)])],
          width={"unit": "%", "size": 80, "sizes": []}, width_mobile={"unit": "%", "size": 100, "sizes": []}, align_self="center"),
], bg="#F2F4F7")

cta = section("hs40001", [inner("hs40002", [
    w("hs40003", "heading", title="Ready to Study in Malta?", header_size="h2", align="center", title_color="#FFFFFF"),
    w("hs40004", "text-editor", align="center", text_color="#FFFFFF",
      editor="<p>Book a free consultation with our team in Malta. We answer your questions and help you choose the right programme.</p>"),
    inner("hs40005", [
        button("hs40006", "Book a Free Consultation", CONTACT, primary=False),
        w("hs40007", "button", text=f"Call {PHONE}", link=link(f"tel:{PHONE_TEL}"), align="center", size="md",
          background_color="rgba(0,0,0,0)", button_text_color="#FFFFFF", border_border="solid",
          border_width={"unit": "px", "top": "2", "right": "2", "bottom": "2", "left": "2", "isLinked": True}, border_color="#FFFFFF",
          border_radius={"unit": "px", "top": "8", "right": "8", "bottom": "8", "left": "8", "isLinked": True},
          selected_icon={"value": "fas fa-phone-alt", "library": "fa-solid"}, icon_indent={"unit": "px", "size": 8, "sizes": []}),
    ], flex_direction="row", flex_justify_content="center", flex_wrap="wrap", flex_gap={"column": "16", "row": "16", "isLinked": True, "unit": "px", "size": 16}),
])], bg=BLUE, top=80, bottom=80)

order = [c["id"] for c in d]
d.insert(order.index("90bc247") + 1, trust)
# "How it works" after the About block, before the programme cards
d.insert([c["id"] for c in d].index("bfba620"), how)
# drop the empty placeholder container
d = [c for c in d if c["id"] != "ad88a93"]
# FAQ before the blog, CTA band last (directly above the footer)
d.insert([c["id"] for c in d].index("3443e7c"), faq)
d.append(cta)

print(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
