# לידים ממודעות → גיליון → Google Ads (בלי תלות בעוגיות)

## למה
ההמרות ב-Google Ads עמדו על 0 למרות לידים אמיתיים. הסיבה העיקרית בצד האתר: כל עוד גולש לא לחץ "קבל הכל" בבאנר,
`analytics.js` רץ עם `ads_data_redaction`, ומזהה הקליק (gclid) לא מגיע לגוגל עם ההמרה. הזרימה כאן מודדת לידים ממודעות בלי עוגיות.

## מה האתר עושה (analytics.js, `adClick` / `adLead` / `adRow`)
- מי שהגיע ממודעה (gclid / wbraid / gbraid בכתובת, נשמר ב-sessionStorage `stz-click`):
  - **וואטסאפ:** נוספת להודעה שורה `מס' פנייה: 123456`, ושורה אחת לכל מספר נשלחת ל-webhook (`kind=וואטסאפ`).
  - **טופס:** אחרי שליחה מוצלחת (`stzTrack('generate_lead')`) נשלחת שורה (`kind=טופס`).
- השדות שנשלחים (POST, form-urlencoded, sendBeacon): `kind, lead, page, gclid, wbraid, gbraid, utm`.
- מי שלא הגיע ממודעה: שום שינוי.
- הכתובת: `LEAD_HOOK` בראש `analytics.js`.

## הגיליון
[לידים מוואטסאפ ממודעות גוגל](https://docs.google.com/spreadsheets/d/1jJ3ciSMmGgTDNjYipbi1-wXaa5gU5eMlrclVdt3qcGA/edit)
(נוצר בדרייב של anastasiyaminov@gmail.com, משותף לעריכה עם supervshadow@gmail.com).
- לשונית `לידים` (Make כותב, ערכים RAW): A זמן · B מס' פנייה · C איכות (טוב / לא רלוונטי, לא חובה) · D עמוד (+ kind) ·
  E gclid · F שם ההמרה (`ליד ממודעה`) · G זמן ההמרה (`YYYY-MM-DD HH:mm:ss`, Asia/Jerusalem) · H wbraid · I gbraid · J utm.
- לשונית `העלאה לגוגל`: שורת `Parameters:TimeZone=Asia/Jerusalem` + כותרות. **הנוסחה ב-A3 עוד לא סופית**: צריך לכתוב אותה
  דרך Sheets עצמו (Make, Update a Cell, USER_ENTERED), כי נוסחה מ-xlsx לא נבדקה:
  `=IFERROR(FILTER('לידים'!E2:G,'לידים'!E2:E<>"",'לידים'!C2:C<>"לא רלוונטי"),)`

## Make (חשבון supervshadow@gmail.com, team 2129528)
- webhook: `לידים ממודעות (וואטסאפ וטופס)` (id 3935096) = `LEAD_HOOK`.
- Credential request (Google Sheets + Google Ads, שניהם supervshadow): `21ada348-e54e-43d4-8847-ac0b3b9e24ac`.
- תרחיש 1 (מיידי): webhook → filter (`lead` = 6 ספרות או `kind=טופס`, ויש gclid/wbraid/gbraid) → Google Sheets Add a Row (RAW).
- תרחיש 2 (יומי): Google Ads API דרך `google-ads-conversions:makeAnApiCall`:
  - פעם אחת: לבדוק `customer.auto_tagging_enabled`, פעולות ההמרה (סטטוס, primary/secondary, סוג), ו-final URLs של המודעות.
  - פעם אחת: ליצור פעולת המרה `ליד ממודעה` מסוג UPLOAD_CLICKS, ערך 3 ILS, ספירה One.
  - כל יום: לשורות עם gclid שלא סומנו "לא רלוונטי" → `uploadClickConversions` (כפילויות נדחות אצל גוגל).
- חבילה חינמית: 1,000 פעולות בחודש, 2 תרחישים פעילים. שורה = 2 פעולות.
- שאריות בחשבון IL PROJECTS (לא בשימוש, אפשר למחוק ידנית): webhook 3933364 ושתי בקשות חיבור שלא אושרו.
