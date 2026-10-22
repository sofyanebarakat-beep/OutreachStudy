import json, sys, importlib.util
spec = importlib.util.spec_from_file_location("bh", sys.argv[1]); bh = importlib.util.module_from_spec(spec)
# reuse the section helpers from the homepage builder without running it
src = open(sys.argv[1]).read().split("d = json.load")[0]; exec(src, bh.__dict__)
section, inner, w, heading, button = bh.section, bh.inner, bh.w, bh.heading, bh.button


def programme_card(i, label, title, description, facts, url, featured=False):
    card = inner(i, [
        w(i + "a", "heading", title=label.upper(), header_size="h6", title_color="#442DFA",
          typography_typography="custom", typography_font_size={"unit": "px", "size": 12, "sizes": []},
          typography_font_weight="700", typography_letter_spacing={"unit": "px", "size": 1.2, "sizes": []}),
        w(i + "b", "heading", title=title, header_size="h2", title_color="#13211F",
          typography_typography="custom", typography_font_size={"unit": "px", "size": 30, "sizes": []},
          typography_font_size_mobile={"unit": "px", "size": 26, "sizes": []}, typography_font_weight="700"),
        w(i + "c", "text-editor", editor=f"<p>{description}</p>", text_color="#52605D",
          typography_typography="custom", typography_font_size={"unit": "px", "size": 16, "sizes": []},
          typography_line_height={"unit": "em", "size": 1.65, "sizes": []}),
        w(i + "d", "icon-list", icon_color="#28A77A", text_color="#263936", space_between={"unit": "px", "size": 14, "sizes": []},
          icon_list=[{"text": fact, "selected_icon": {"value": "fas fa-check-circle", "library": "fa-solid"}, "_id": i + str(n)} for n, fact in enumerate(facts)]),
        button(i + "e", "View Programme" if featured else "Apply Now", url, icon="fas fa-arrow-right", align="left"),
    ], width={"unit": "%", "size": 48.5, "sizes": []}, width_mobile={"unit": "%", "size": 100, "sizes": []},
       background_background="classic", background_color="#FFFFFF", border_border="solid",
       border_width={"unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": True},
       border_color="#E5E8E7", border_radius={"unit": "px", "top": "22", "right": "22", "bottom": "22", "left": "22", "isLinked": True},
       padding={"unit": "px", "top": "38", "right": "38", "bottom": "38", "left": "38", "isLinked": True},
       padding_mobile={"unit": "px", "top": "28", "right": "24", "bottom": "28", "left": "24", "isLinked": False},
       box_shadow_box_shadow={"horizontal": 0, "vertical": 16, "blur": 45, "spread": -24, "color": "rgba(19,33,31,0.28)"})
    return card

intro = section("pg10001", [inner("pg10002", [
    w("pg10003", "heading", title="Study in Malta: Programmes and Schools", header_size="h1", align="center", title_color="#162726"),
    w("pg10004", "text-editor", align="center", editor=
      "<p>Choose from our two English programmes, then book a free consultation. We help you understand the course, prepare your application and plan your next step.</p>"),
], width={"unit": "%", "size": 80, "sizes": []}, width_mobile={"unit": "%", "size": 100, "sizes": []}, align_self="center")], top=60, bottom=30)

programmes = section("pg15001", [
    inner("pg15002", [
        programme_card("pg1510", "Study in Malta", "Professional English Programme in Malta",
          "Build professional English skills while studying full-time in Malta with an EU-recognised qualification.",
          ["12 months full-time", "MQF Level 4 · 48 ECTS", "Residence permit and part-time work rights", "Launch price €3,950 (standard €4,950)"],
          "https://outreachstudy.eu/study-english-in-malta/", featured=True),
        programme_card("pg1520", "Study online", "Intensive English Programme — 10 Weeks",
          "Improve your English through a structured online programme designed around consistent, teacher-led practice.",
          ["10-week intensive programme", "3 hours daily, Monday to Friday", "Evening classes", "Certified English teachers"],
          bh.CONSULTATION),
    ], flex_direction="row", flex_wrap="wrap", flex_justify_content="space-between", flex_gap={"column": "28", "row": "28", "isLinked": False, "unit": "px"},
       content_width="boxed", boxed_width={"unit": "px", "size": 1160, "sizes": []}),
], bg="#F7F5EF", top=55, bottom=80)

FAQ = [
    ("Is Malta a good destination for international students?",
     "Yes. English is an official language in Malta, schools offer EU-recognised qualifications, and students enjoy a safe, multicultural Mediterranean lifestyle."),
    ("Do I need a visa to study in Malta?",
     "Students from the EU do not need a visa. Most students from outside the EU need a student visa and a residence permit for courses longer than 90 days. Requirements depend on your nationality and your course, and we help you prepare your application."),
    ("How much does it cost to study in Malta?",
     "It depends on the school and programme. For example, our 12-month Professional English Programme has a launch price of €3,950. See our <a href=\"https://outreachstudy.eu/studying-in-malta-on-a-budget-a-guide-to-affordability-in-malta/\">guide to the cost of studying in Malta</a> for living costs."),
    ("What are the entry requirements?",
     "They depend on the programme level. Read our <a href=\"https://outreachstudy.eu/study-in-malta-requirements/\">guide to study in Malta requirements</a>, or book a free consultation and we check your documents with you."),
]
faq = section("pg20001", [
    inner("pg20002", [heading("pg20003", "FAQ", "Frequently Asked Questions About Studying in Malta")]),
    inner("pg20004", [w("pg20005", "accordion", tabs=[{"tab_title": q, "tab_content": f"<p>{a}</p>", "_id": f"pgq{n:04d}"} for n, (q, a) in enumerate(FAQ)])],
          width={"unit": "%", "size": 80, "sizes": []}, width_mobile={"unit": "%", "size": 100, "sizes": []}, align_self="center"),
    inner("pg20006", [button("pg20007", "Book a Free Consultation", bh.CONTACT)]),
], bg="#F2F4F7")

print(json.dumps([intro, programmes, faq], ensure_ascii=False, separators=(",", ":")))
