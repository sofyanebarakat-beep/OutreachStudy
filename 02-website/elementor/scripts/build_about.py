import json
pad={"unit":"px","top":"120","right":"12","bottom":"120","left":"12","isLinked":False}
padt={"unit":"px","top":"80","right":"12","bottom":"80","left":"12","isLinked":False}
padm={"unit":"px","top":"70","right":"12","bottom":"70","left":"12","isLinked":False}
def box(i,els,**s): return {"id":i,"elType":"container","settings":dict(s),"elements":els,"isInner":False}
def inner(i,els,**s): return {"id":i,"elType":"container","settings":dict(content_width="full",**s),"elements":els,"isInner":True}
def w(i,t,**s): return {"id":i,"elType":"widget","widgetType":t,"settings":s,"elements":[]}
def heading(i,sub,title,align="left"): return w(i,"edcare_heading",section_subheading_icon={"value":"fas fa-bolt","library":"fa-solid"},section_subheading=sub,section_title=title,section_text_align=align)
def iconbox(i,icon,title,desc): return inner("c"+i,[w(i,"icon-box",selected_icon={"value":icon,"library":"fa-solid"},title_text=title,description_text=desc,title_size="h3")])
SOC=('<a href="https://www.facebook.com/profile.php?id=61582445649555" target="_blank" rel="noopener">Facebook</a> · '
     '<a href="https://www.instagram.com/outreachstudy" target="_blank" rel="noopener">Instagram</a> · '
     '<a href="https://www.tiktok.com/@outreachstudy" target="_blank" rel="noopener">TikTok</a>')
d=[
 box("ab10001",[inner("ab10002",[
   inner("ab10003",[w("ab10004","image",image={"id":4508,"url":"https://outreachstudy.eu/wp-content/uploads/2025/02/offer-img.png","alt":"International students studying together outdoors in Malta","source":"library"},image_size="full")],width={"unit":"%","size":45},width_tablet={"unit":"%","size":100,"sizes":[]}),
   inner("ab10005",[
     heading("ab10006","About Outreach Study","Helping International Students Study in Malta"),
     w("ab10007","text-editor",editor=
       "<p>Outreach Study helps international students who want to study in Malta and Europe. We guide you from your first question to your first day in class: choosing the right programme, preparing your application, and getting support with your student visa and residence permit.</p>"
       "<p>Malta is an English-speaking EU country with a Mediterranean climate, internationally recognised qualifications and lower living costs than many other European study destinations. Our team in Malta knows the local schools, the application process and student life on the island, so you can plan your studies with confidence.</p>"),
     w("ab10008","button",text="Start Your Application",link={"url":"https://apply.outreachstudy.eu/","is_external":"","nofollow":"","custom_attributes":""}),
   ],width={"unit":"%","size":55},width_tablet={"unit":"%","size":100,"sizes":[]},padding={"unit":"px","top":"0","right":"0","bottom":"0","left":"40","isLinked":False},padding_tablet={"unit":"px","top":"30","right":"0","bottom":"0","left":"0","isLinked":False}),
 ],flex_direction="row",flex_align_items="center",flex_wrap_tablet="wrap")],flex_direction="column",padding=pad,padding_tablet=padt,padding_mobile=padm),
 box("ab20001",[
   inner("ab20002",[heading("ab20003","What We Do","How Outreach Study Helps You","center")]),
   inner("ab20004",[
     iconbox("ab20005","fas fa-graduation-cap","Choose the Right Programme","We help you compare English courses, diplomas and degree programmes in Malta and pick the one that fits your goals and budget."),
     iconbox("ab20006","fas fa-passport","Application & Visa Support","We help you prepare your documents, apply to your school and get ready for your student visa and residence permit application."),
     iconbox("ab20007","fas fa-plane-arrival","Arrival & Student Life","We share practical advice on accommodation, living costs, working while you study and settling into life in Malta."),
   ],flex_direction="row",flex_wrap_tablet="wrap"),
 ],flex_direction="column",background_background="classic",background_color="#F2F4F7",padding=pad,padding_tablet=padt,padding_mobile=padm),
 box("ab30001",[inner("ab30002",[
   heading("ab30003","Contact Us","Talk to Our Team in Malta","center"),
   w("ab30004","text-editor",align="center",editor=
     "<p><strong>Address:</strong> Triq Ninu Cremona, L-Iklin PLA 1576, Malta<br>"
     "<strong>Phone:</strong> <a href=\"tel:+35677200984\">+356 7720 0984</a><br>"
     "<strong>Email:</strong> <a href=\"mailto:study@outreachrecruitment.net\">study@outreachrecruitment.net</a></p>"
     "<p>Follow us: "+SOC+"</p>"),
   w("ab30005","button",text="Contact Us",align="center",link={"url":"https://outreachstudy.eu/contact/","is_external":"","nofollow":"","custom_attributes":""}),
 ])],flex_direction="column",padding=pad,padding_tablet=padt,padding_mobile=padm),
]
print(json.dumps(d,ensure_ascii=False,separators=(',',':')))
