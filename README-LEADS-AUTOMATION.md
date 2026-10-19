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

## מה נשאר (Make)
ההחלטה: הכול תחת **supervshadow@gmail.com** (סופר צל), גם חשבון ה-Make.
1. לחבר את ה-connector של Make ב-Claude לחשבון ה-Make של supervshadow (claude.ai/customize/connectors), ולפתוח סשן חדש.
2. ב-Make של supervshadow: webhook חדש (gateway-webhook) → לעדכן `LEAD_HOOK` ב-`analytics.js` (ולהעלות את `?v=`).
3. Credential request אחד: `google-sheets` + `google-ads-conversions` (שניהם supervshadow).
4. תרחיש 1 (מיידי): webhook → filter (`lead` = 6 ספרות או `kind=טופס`, ויש gclid/wbraid/gbraid) → Google Sheets Add a Row (RAW).
5. תרחיש 2 (יומי): Google Ads API דרך `google-ads-conversions:makeAnApiCall`:
   - פעם אחת: לבדוק `customer.auto_tagging_enabled`, פעולות ההמרה (סטטוס, primary/secondary, סוג), ו-final URLs של המודעות.
   - פעם אחת: ליצור פעולת המרה `ליד ממודעה` מסוג UPLOAD_CLICKS, ערך 3 ILS, ספירה One.
   - כל יום: לשורות עם gclid שלא סומנו "לא רלוונטי" ולא הועלו → `uploadClickConversions` (כפילויות נדחות אצל גוגל).
6. למחוק את ה-webhook הזמני בחשבון IL PROJECTS (id 3933364) ואת בקשות החיבור שלא אושרו שם.
7. חבילה חינמית: 1,000 פעולות בחודש, 2 תרחישים פעילים. שורה = 2 פעולות.
