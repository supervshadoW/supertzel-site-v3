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
- לשונית `העלאה לגוגל`: שורת `Parameters:TimeZone=Asia/Jerusalem` + כותרות, וב-A3 (נכתב דרך Sheets, נבדק עם שורת בדיקה שנמחקה):
  `=IFERROR(FILTER('לידים'!E2:G,'לידים'!E2:E<>"",'לידים'!C2:C<>"לא רלוונטי"),)`

## Make (חשבון supervshadow@gmail.com, team 2129528)
- webhook: `לידים ממודעות (וואטסאפ וטופס)` (id 3935096) = `LEAD_HOOK`.
- Credential request (Google Sheets + Google Ads, שניהם supervshadow): `21ada348-e54e-43d4-8847-ac0b3b9e24ac`.
- תרחיש 1 `לידים ממודעות → גיליון` (id 8054590, פעיל, נבדק מקצה לקצה): webhook → filter (`lead` = 6 ספרות או `kind=טופס`, ויש gclid/wbraid/gbraid) → Google Sheets Add a Row (RAW, OVERWRITE), חיבור 12115761.
- תרחיש 2 `העלאת לידים איכותיים ל-Google Ads (אוטומטי)` (id 8210876, פעיל, כל יום 10:00), Google Ads API v23 דרך `google-ads-conversions:makeAnApiCall` (חיבור 12120100), router עם 3 מסלולים (שגיאה במסלול דוח לא עוצרת את ההעלאה):
  - דוח ביצועים → רשומה `daily_perf` ב-data store 225022: קמפיין לפי יום (7 ימים), המרות לפי פעולה, מונחי חיפוש לפי יום + מילת המפתח שהפעילה אותם.
  - בדיקת הגדרות → רשומה `daily_setup`: מילים שליליות (קמפיין, קבוצות, רשימות משותפות ושיוכן), מילות מפתח וסטטוס, היסטוריית שינויים 14 יום (מי / Google Recommendations), נכסים שנוצרו אוטומטית.
  - העלאה: שורות שסומנו `טוב` בלשונית `לידים` → `uploadClickConversions` לפעולה `customers/6267135003/conversionActions/7875926566`, ואז הסימון הופך ל-`טוב · הועלה`. מסנן מדלג על תוצאה ריקה.
- תרחיש 8056925 (אבחון, לא פעיל) ו-8204249 (לא פעיל): כלים חד-פעמיים. בחבילה החינמית אפשר רק 2 תרחישים פעילים.
- חבילה חינמית: 1,000 פעולות בחודש, 2 תרחישים פעילים. שורה = 2 פעולות. התרחיש היומי: כ-21 פעולות ביום (כ-650 בחודש).
- שאריות בחשבון IL PROJECTS (לא בשימוש, אפשר למחוק ידנית): webhook 3933364 ושתי בקשות חיבור שלא אושרו.
