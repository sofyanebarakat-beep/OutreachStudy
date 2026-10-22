# Elementor page data for outreachstudy.eu

Snapshots of the Elementor layout (`_elementor_data` post meta) for pages edited
through the WordPress MCP connection, plus the scripts that produced them.

## Pages changed on 2026-10-22

| Page | ID | What changed |
|---|---|---|
| Home | 4500 | Single-slide carousel replaced with a responsive two-column hero, focused H1 and CTAs, trust cues and support badge; "How it works" (4 steps); programme cards fixed (correct apply link, MBA name, Business description) plus a Professional English Programme card; FAQ (6 questions); final call-to-action band; unused theme demo slides removed |
| Our Programs | 7595 | Lovable programme-search iframe removed and replaced with two responsive native Elementor programme cards; H1, intro, real FAQ and consultation CTA included |
| Contact | 77 | Real address, phone, email, hours and social links; the broken Contact Form 7 shortcode replaced with contact options |
| About Us | 71 | Theme demo content replaced with real company content |

Main action on the site: **Book a Free Consultation** goes to the Contact page;
**Apply Now** on programme cards goes to https://apply.outreachstudy.eu/.

## Restoring a page

1. Open the `*-before.json` file and send its JSON (as one string) as the
   `_elementor_data` meta of that page.
2. Delete the page's `_elementor_element_cache` meta, otherwise Elementor keeps
   showing the cached version.
3. Clear the LiteSpeed page cache.

There is no `before` file for About Us and Our Programs: About was entirely
theme demo content, and Our Programs only lost the demo FAQ widget.

## Still to do

These need access the WordPress MCP connection does not have (the header and
footer are theme templates outside the REST API):

- Header (template 4649): old address "230, Seaspeed Triq Ninu Cremona, Paola";
  the "Apply now" button links to `apply.outreachstudy.eu/admin`.
- Footer (template 3133): email link goes to `info@company.com`; no phone or
  address; "#" links; copyright year 2025.
- Mobile menu: address "Paola, Malta".
- Floating WhatsApp button: needs the WhatsApp number.
- Convert large PNG images to WebP.
- Testimonials section: needs real student quotes and permission to publish.
- Programme cards: duration, start dates and prices for each programme.
