import json,sys
d=json.loads(open(sys.argv[1]).read())
form_col=d[0]['elements'][0]['elements'][0]
info=d[0]['elements'][0]['elements'][1]['elements'][0]['settings']
d[0]['elements'].insert(0,{"id":"ct00000","elType":"widget","widgetType":"html","elements":[],"settings":{"html":"<script>(function(){function f(){document.querySelectorAll('a[href^=\\\"https://apply.outreachstudy.eu\\\"]').forEach(function(a){a.href='https://consultation.outreachstudy.eu/';});}if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',f);}else{f();}new MutationObserver(f).observe(document.documentElement,{childList:true,subtree:true});})();</script>"}})
# Contact Form 7 is not installed, so the form widget printed a raw shortcode: replace it with real contact options
form_col['elements']=[{"id":"a1c0f01","elType":"widget","widgetType":"text-editor","elements":[],"settings":{"editor":
"<h2>Talk to Outreach Study</h2>"
"<p>Want to study in Malta? Our team gives free advice on programmes, applications, student visas and accommodation. Contact us by phone or email, or start your application online.</p>"
"<p>After you contact us, we review your study goals and explain the most relevant next step. Schools make admission decisions, and Maltese authorities make visa and residence decisions.</p>"
"<ul>"
"<li><strong>Phone:</strong> <a href=\"tel:+35677200984\">+356 7720 0984</a></li>"
"<li><strong>Email:</strong> <a href=\"mailto:study@outreachrecruitment.net\">study@outreachrecruitment.net</a></li>"
"<li><strong>Book online:</strong> <a href=\"https://consultation.outreachstudy.eu/\">Free consultation</a></li>"
"</ul>"
"<p>Follow us: <a href=\"https://www.facebook.com/profile.php?id=61582445649555\" target=\"_blank\" rel=\"noopener\">Facebook</a> · "
"<a href=\"https://www.instagram.com/outreachstudy\" target=\"_blank\" rel=\"noopener\">Instagram</a> · "
"<a href=\"https://www.tiktok.com/@outreachstudy\" target=\"_blank\" rel=\"noopener\">TikTok</a></p>"}}]
info['section_description']="Visit our office in L-Iklin, Malta, or contact us by phone or email for free study advice."
L=info['contact_info_list']
L[0].update(contact_info_phone="+356 7720 0984",contact_info_phone_url="+35677200984",contact_info_email="study@outreachrecruitment.net")
L[1].update(contact_info_address="Triq Ninu Cremona, L-Iklin PLA 1576, Malta")
L[2].update(contact_info_office_time_one="Monday - Friday: 9:00 - 17:00",contact_info_office_time_two="Saturday & Sunday: Closed")
print(json.dumps(d,ensure_ascii=False,separators=(',',':')))
