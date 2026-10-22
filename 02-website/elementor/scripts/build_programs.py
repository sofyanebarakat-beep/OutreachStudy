import json, sys, importlib.util
spec = importlib.util.spec_from_file_location("bh", sys.argv[1]); bh = importlib.util.module_from_spec(spec)
# reuse the section helpers from the homepage builder without running it
src = open(sys.argv[1]).read().split("d = json.load")[0]; exec(src, bh.__dict__)
section, inner, w, heading, button = bh.section, bh.inner, bh.w, bh.heading, bh.button

iframe = {"id": "fc9f68d", "elType": "container", "settings": {"flex_direction": "column", "content_width": "full"}, "elements": [
    {"id": "d9f72d9", "elType": "widget", "widgetType": "html", "elements": [], "settings": {"html":
        "<iframe src=\"https://global-pathways-finder.lovable.app/search\" title=\"Search study programmes in Malta\" style=\"width:100%; height:100vh; border:none;\" loading=\"lazy\"></iframe>"}}],
    "isInner": False}

intro = section("pg10001", [inner("pg10002", [
    w("pg10003", "heading", title="Study in Malta: Programmes and Schools", header_size="h1", align="center", title_color="#162726"),
    w("pg10004", "text-editor", align="center", editor=
      "<p>Search English courses, foundation degrees, bachelor's and master's programmes at schools in Malta. "
      "Filter by subject and level, then book a free consultation and we help you apply.</p>"),
], width={"unit": "%", "size": 80, "sizes": []}, width_mobile={"unit": "%", "size": 100, "sizes": []}, align_self="center")], top=60, bottom=30)

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

print(json.dumps([intro, iframe, faq], ensure_ascii=False, separators=(",", ":")))
