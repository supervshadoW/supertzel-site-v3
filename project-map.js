/* מפת הפרויקט: the customer picks a kind of space from pictures, ticks what he wants, numbers light up on the picture,
   and leaves a phone number to receive the full map. Mounts into #pm-mount (data-door="balcony" | "garden").
   Submit goes through window.stzSendLead (lead.js) so the Google Ads conversion and the lead e-mail/WhatsApp work as for every other form.
   On localhost, or with ?pmdry=1, nothing is sent. */
(function () {
  'use strict';
  var IMG = '/img/fast/';
  var WA = '972559958231';
  // general ranges per component at a typical size (market research Nov 2026, upper side, incl. installation): deliberately broad and rounded, shown only as one total
  var EST = { floor: [8000, 15000], deck: [10000, 15000], glass: [15000, 25000], plants: [2000, 6000], grass: [4000, 8000], perg: [20000, 35000], shade: [20000, 35000], build: [25000, 35000], fence: [8000, 15000], garden: [5000, 10000], rail: [6000, 15000], lat: [6000, 12000], light: [2000, 6000], kit: [20000, 30000], green: [5000, 12000] };
  function fmtN(n) { return n.toLocaleString('he-IL'); }

  var STAGES = [
    { t: 'רק מתחילים לחשוב', n: 'מתחילים משאלות פשוטות: איך אתם חיים במקום ומה חשוב לכם שיישאר פתוח.' },
    { t: 'יש תוכנית, עדיין בלי ביצוע', n: 'בודקים את התוכנית מול המציאות בשטח ומתאימים אותה לביצוע.' },
    { t: 'יש הצעות ואני משווה', n: 'מביאים את ההצעות לפגישה ועוברים יחד על מה שכלול בכל אחת.' }
  ];

  var DATA = {
    balcony: {
      q0: 'איזו מרפסת דומה לשלכם?', hint0: 'בחירה אחת. התמונה מתחלפת בהתאם.', q2: 'מה תרצו במרפסת?',
      empty: 'בחרו מה תרצו במרפסת, והמספרים יופיעו כאן.', pick: 'בחרו קודם איזו מרפסת דומה לשלכם',
      types: [
        { name: 'מרפסת בפרופיל שחור', sub: 'אלומיניום שחור וסגירת זכוכית', pic: IMG + 'gallery/glass-1.webp', ar: '1400/651', tag: 'הדמיה', alt: 'הדמיה של מרפסת בסגירת זכוכית בפרופיל אלומיניום שחור, עם עציצים וספה',
          comps: [
            { k: 'floor', t: 'דק או ריצוף', cat: 'ריצוף, דקים וחיפויים', o: 1, x: '46%', y: '88%', d: 'הבסיס של המרפסת, בגבהים שמתואמים מראש.' },
            { k: 'glass', t: 'סגירת מרפסת זכוכית', cat: 'סגירות מרפסת ומערכות הזזה', o: 2, x: '62%', y: '30%', d: 'בפרופיל אלומיניום שחור, נמדדת במדויק לפי המרפסת.' },
            { k: 'plants', t: 'צמחייה ועציצים', cat: 'גינה ופיתוח נוף', o: 3, x: '89%', y: '42%', d: 'הנגיעה החיה של המרפסת, שמשלימה את הקו.' }
          ] },
        { name: 'פנטהאוז פנורמי', sub: 'זכוכית פנורמית ופרגולה חשמלית', pic: IMG + 'hero/hero-panoramic-balcony.webp', ar: '1800/837', tag: 'פרויקט שבוצע', alt: 'פנטהאוז בסגירת זכוכית פנורמית עם פרגולה חשמלית',
          comps: [
            { k: 'floor', t: 'דק או ריצוף', cat: 'ריצוף, דקים וחיפויים', o: 1, x: '74%', y: '88%', d: 'הבסיס של המרפסת, בגבהים שמתואמים מראש.' },
            { k: 'grass', t: 'דשא סינטטי', cat: 'גינה ופיתוח נוף', o: 2, x: '84%', y: '66%', d: 'הנגיעה הירוקה של המרפסת, על בסיס שמתואם מראש.' },
            { k: 'perg', t: 'פרגולה חשמלית', cat: 'קירוי והצללה', o: 3, x: '50%', y: '9%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת מרפסת זכוכית פנורמית', cat: 'סגירות מרפסת ומערכות הזזה', o: 4, x: '32%', y: '45%', d: 'נמדדת במדויק אחרי שהגבהים והקירוי סגורים.' }
          ] },
        { name: 'מרפסת דק ונוף', sub: 'דק ופרגולה בגמר עץ', pic: IMG + 'gallery/project-deck-view.webp', ar: '1400/692', tag: 'פרויקט שבוצע', alt: 'מרפסת גדולה עם דק ופרגולה בגמר עץ',
          comps: [
            { k: 'deck', t: 'דק', cat: 'ריצוף, דקים וחיפויים', o: 1, x: '45%', y: '86%', d: 'הבסיס של המרפסת, בגבהים שמתואמים מראש.' },
            { k: 'rail', t: 'מעקה אלומיניום', cat: 'גידור ותיחום', o: 2, x: '60%', y: '49%', d: 'מותאם למרפסת ולנוף, בכפוף לדרישות הבטיחות החלות בפרויקט.' },
            { k: 'perg', t: 'פרגולה בגמר עץ', cat: 'קירוי והצללה', o: 3, x: '48%', y: '13%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'light', t: 'תאורה משולבת', cat: 'גינה ופיתוח נוף', o: 4, x: '68%', y: '12%', d: 'הנגיעה האחרונה, שמחברת את הכול.' }
          ] },
        { name: 'מרפסת בדירת נופש', sub: 'דק עץ ומעקה זכוכית לנוף הכנרת', pic: IMG + 'gallery/project-lake-terrace.webp', ar: '1400/654', tag: 'פרויקט שבוצע', alt: 'מרפסת של דירת נופש בכנרת עם דק עץ ומעקה זכוכית',
          comps: [
            { k: 'deck', t: 'דק עץ', cat: 'ריצוף, דקים וחיפויים', o: 1, x: '40%', y: '62%', d: 'הבסיס של המרפסת, בגבהים שמתואמים מראש.' },
            { k: 'rail', t: 'מעקה זכוכית', cat: 'גידור ותיחום', o: 2, x: '78%', y: '38%', d: 'מותאם למרפסת ולנוף, בכפוף לדרישות הבטיחות החלות בפרויקט.' }
          ] },
        { name: 'מרפסת בסגנון ביתי', sub: 'עץ טבעי ורשת עץ, אווירה חמה', pic: IMG + 'gallery/project-wood-lattice-balcony.webp', ar: '1600/747', tag: 'פרויקט שבוצע', alt: 'מרפסת עם פרגולת עץ, רשת עץ ומעקה זכוכית',
          comps: [
            { k: 'floor', t: 'ריצוף', cat: 'ריצוף, דקים וחיפויים', o: 1, x: '50%', y: '88%', d: 'הבסיס של המרפסת, בגבהים שמתואמים מראש.' },
            { k: 'rail', t: 'מעקה זכוכית', cat: 'גידור ותיחום', o: 2, x: '58%', y: '57%', d: 'מותאם למרפסת ולנוף, בכפוף לדרישות הבטיחות החלות בפרויקט.' },
            { k: 'perg', t: 'פרגולת עץ', cat: 'קירוי והצללה', o: 3, x: '50%', y: '9%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'lat', t: 'רשת עץ לפרטיות', cat: 'סגירות מרפסת ומערכות הזזה', o: 4, x: '18%', y: '45%', d: 'מסכי צד שנותנים פרטיות ומשאירים את האור.' }
          ] },
        { name: 'פרגולה בגוון שמנת', sub: 'אלומיניום בצורת L על מרפסת גדולה', pic: IMG + 'gallery/pergola-1.webp', ar: '1400/654', tag: 'פרויקט שבוצע', alt: 'פרגולת אלומיניום גדולה בגוון שמנת בצורת L על מרפסת גדולה',
          comps: [
            { k: 'floor', t: 'ריצוף', cat: 'ריצוף, דקים וחיפויים', o: 1, x: '18%', y: '90%', d: 'הבסיס של המרפסת, בגבהים שמתואמים מראש.' },
            { k: 'rail', t: 'מעקה זכוכית', cat: 'גידור ותיחום', o: 2, x: '45%', y: '84%', d: 'מותאם למרפסת ולנוף, בכפוף לדרישות הבטיחות החלות בפרויקט.' },
            { k: 'perg', t: 'פרגולת אלומיניום בגוון שמנת', cat: 'קירוי והצללה', o: 3, x: '42%', y: '22%', d: 'פרופילי הצללה בגוון בהיר, בצורת L שעוטפת את פינת המרפסת.' }
          ] },
        { other: true, name: 'משהו אחר', sub: 'ספרו לנו מה בראש שלכם', pic: IMG + 'hero/hero-glass-balcony.webp', ar: '1800/837', tag: '', alt: 'מרפסת', comps: [] }
      ]
    },
    garden: {
      q0: '', hint0: '', q2: 'מה תרצו בגינה?',
      empty: 'בחרו מה תרצו בגינה, והמספרים יופיעו כאן.', pick: '',
      types: [
        { name: 'גינה ובית פרטי', sub: 'פרגולה, מטבח חוץ ודק', pic: IMG + 'w/envelope-pergola-deck.webp', ar: '1024/559', tag: 'הדמיה', alt: 'הדמיה של גינה עם פרגולה, מטבח חוץ ודק',
          comps: [
            { k: 'deck', t: 'דק וריצוף', cat: 'ריצוף, דקים וחיפויים', o: 1, x: '44%', y: '91%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'perg', t: 'פרגולה אלומיניום', cat: 'קירוי והצללה', o: 2, x: '52%', y: '20%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 3, x: '17%', y: '74%', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'green', t: 'גינון ותאורה', cat: 'גינה ופיתוח נוף', o: 4, x: '90%', y: '83%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] }
      ]
    },
    envelope: {
      q0: 'איזה סגנון מעטפת הכי קרוב לכם?', hint0: 'בחירה אחת. ההדמיה מתחלפת בהתאם.', q2: 'מה תרצו במעטפת?',
      empty: 'בחרו מה תרצו במעטפת, והמספרים יופיעו כאן.', pick: 'בחרו קודם איזה סגנון קרוב לכם', pickTxt: 'בחרו איזה סגנון מעטפת קרוב לכם, וההדמיה תתחלף.',
      types: [
        { name: 'ים-תיכוני ופתוח', sub: 'פרגולה לבנה, זכוכית ומטבח חוץ', pic: IMG + 'w/envelope-pergola-deck.webp', ar: '1024/559', tag: 'הדמיה', alt: 'הדמיה של פרגולה לבנה, סגירות זכוכית, מטבח חוץ, דק וגינה',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '52%', y: '20%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '55%', y: '60%', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '', y: '', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '17%', y: '74%', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '', y: '', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '44%', y: '91%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '90%', y: '83%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] },
        { name: 'אבן ואפור', sub: 'פרגולה אפורה, קיר אבן וגדר', pic: IMG + 'w/envelope-grey-stone-dining.webp', ar: '1792/1008', tag: 'הדמיה', alt: 'הדמיה של פרגולת אלומיניום אפורה, קיר אבן, מטבח חוץ, דק, גדר ושער וגינה',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '62%', y: '20%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '78%', y: '52%', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '', y: '', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '58%', y: '56%', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '14%', y: '58%', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '50%', y: '78%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '10%', y: '84%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] },
        { name: 'חם, אבן ועץ', sub: 'פרגולה כהה, מטבח ובר', pic: IMG + 'w/envelope-stone-bar.webp', ar: '1792/1008', tag: 'הדמיה', alt: 'הדמיה של פרגולה כהה, מטבח חוץ ובר, גדר, דק ופיתוח גינה באבן',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '64%', y: '22%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '', y: '', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '', y: '', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '40%', y: '55%', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '82%', y: '44%', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '60%', y: '77%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '33%', y: '88%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] },
        { name: 'לבן ומינימליסטי', sub: 'פרגולה לבנה עם תאורה', pic: IMG + 'w/envelope-white-kitchen.webp', ar: '1920/1072', tag: 'הדמיה', alt: 'הדמיה של פרגולה לבנה עם תאורה, מטבח חוץ ובר, אדניות וסגירת זכוכית',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '55%', y: '17%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '86%', y: '52%', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '', y: '', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '33%', y: '62%', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '', y: '', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '55%', y: '86%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '49%', y: '52%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] },
        { name: 'כפרי מודרני', sub: 'פרגולת עץ ודק עץ', pic: IMG + 'w/envelope-modern-village.webp', ar: '1792/1008', tag: 'הדמיה', alt: 'הדמיה של פרגולת עץ, דק עץ, אדניות וגינה בסגנון כפרי מודרני',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '50%', y: '14%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '', y: '', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '', y: '', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '', y: '', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '', y: '', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '52%', y: '85%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '84%', y: '70%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] },
        { name: 'לבן קלאסי', sub: 'פרגולה, מטבח, גדר ושער', pic: IMG + 'w/envelope-white-gate.webp', ar: '1600/874', tag: 'הדמיה', alt: 'הדמיה של פרגולה לבנה עם צמחייה מטפסת, מטבח חוץ, גדר ושער, דק וגינה',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '50%', y: '20%', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '', y: '', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '', y: '', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '20%', y: '62%', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '56%', y: '52%', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '55%', y: '90%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '82%', y: '76%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] },
        { name: 'בנייה קלה בגינה', sub: 'חדר עבודה או אירוח', pic: IMG + 'w/envelope-light-build-office.webp', ar: '1600/874', tag: 'הדמיה', alt: 'הדמיה של חדר בבנייה קלה בגוון שחור עם חזית זכוכית, דק וגינה',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '', y: '', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '', y: '', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '58%', y: '48%', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '', y: '', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '', y: '', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '46%', y: '86%', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '14%', y: '74%', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] },
        { name: 'עסקים ומוסדות', noEst: true, sub: 'חדר שמש מזכוכית לבית קפה', pic: IMG + 'w/envelope-business-cafe.webp', ar: '1280/720', tag: 'הדמיה', alt: 'הדמיה של חדר שמש מזכוכית ומסגרת פלדה לבית קפה, עם קירוי זכוכית וחזית שקופה',
          comps: [
            { k: 'shade', t: 'פרגולה והצללה', cat: 'קירוי והצללה', o: 1, x: '', y: '', d: 'מותאמת לכיווני השמש ולקו של הבית.' },
            { k: 'glass', t: 'סגירת זכוכית', cat: 'סגירות זכוכית', o: 2, x: '55%', y: '12%', d: 'קו נקי שמחבר בין הבית לנוף.' },
            { k: 'build', t: 'בנייה קלה או חדר שמש', cat: 'בנייה קלה ותוספות', o: 3, x: '14%', y: '50%', d: 'תוספת שמתכננים מול הבית הקיים.' },
            { k: 'kit', t: 'מטבח חוץ', cat: 'מטבחי חוץ ונגרות', o: 4, x: '', y: '', d: 'הכנות מתואמות מראש מול בעלי מקצוע מוסמכים, ככל שנדרש.' },
            { k: 'fence', t: 'גדר ושער', cat: 'גידור ושערים', o: 5, x: '', y: '', d: 'בגוון ובקו אחד עם הבית.' },
            { k: 'deck', t: 'דק, ריצוף וחיפוי', cat: 'ריצוף, דקים וחיפויים', o: 6, x: '', y: '', d: 'הבסיס של המרחב, בגבהים שמתואמים מראש.' },
            { k: 'garden', t: 'גינה ופיתוח נוף', cat: 'גינה ופיתוח נוף', o: 7, x: '', y: '', d: 'הנגיעות האחרונות, שמחברות את הכול.' }
          ] }
      ]
    }
  };

  var tries = 0;
  function boot() {
    var mount = document.getElementById('pm-mount');
    if (mount && !mount.__pmReady) {
      // the page framework can replace the mounted node (listeners are lost on a clone): an expando marks only the node we really wired
      mount.__pmReady = true;
      init(mount);
    }
    if (tries++ < 60) setTimeout(boot, 500);
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function track(name, p) { try { if (window.stzTrack) window.stzTrack(name, p || {}); } catch (e) {} }

  function init(mount) {
    var dd = mount.getAttribute('data-door'), door = (dd === 'garden' || dd === 'envelope') ? dd : 'balcony';
    var CFG = DATA[door], TYPES = CFG.types, MULTI = TYPES.length > 1, OFF = MULTI ? 0 : 1, TOTAL = MULTI ? 4 : 3;
    var DRY = /^(localhost|127\.0\.0\.1)$/.test(location.hostname) || /[?&]pmdry=1/.test(location.search);
    var st = { step: OFF, type: MULTI ? null : 0, on: {}, stage: null, hot: null, sent: false, note: '' };
    var COMP = [], pins = [];

    mount.innerHTML =
      '<div class="pm-stage"><div class="pm-viz"><div class="pm-pic"><img alt="" decoding="async"><div class="pm-empty"></div><span class="pm-tag"></span></div><div class="pm-legend"></div></div><div class="pm-panel"></div></div>';
    var pic = mount.querySelector('.pm-pic'), img = pic.querySelector('img'), empty = mount.querySelector('.pm-empty'), tag = mount.querySelector('.pm-tag'), legend = mount.querySelector('.pm-legend'), panel = mount.querySelector('.pm-panel');

    function setPicture(T) { img.src = T.pic; img.alt = T.alt; pic.style.aspectRatio = T.ar; tag.textContent = T.tag; }
    function applyType(i) {
      var T = TYPES[i]; setPicture(T);
      pins.forEach(function (b) { b.remove(); }); pins = [];
      COMP = T.comps; st.on = {}; st.hot = null;
      COMP.forEach(function (c) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'pm-pin'; b.style.left = c.x; b.style.top = c.y; b.innerHTML = '<b></b>'; if (!c.x) b.style.display = 'none';
        b.onclick = function () { st.hot = (st.hot === c.k ? null : c.k); sync(); if (st.step === 3) { var li = panel.querySelector('.pm-list li[data-k="' + c.k + '"]'); if (li && li.scrollIntoView) li.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); } };
        pic.appendChild(b); pins.push(b);
      });
    }
    if (!MULTI) applyType(0); else setPicture(TYPES[0]);
    empty.textContent = MULTI ? (CFG.pickTxt || 'בחרו איזו מרפסת דומה לשלכם, והתמונה תתחלף.') : CFG.empty;

    function picked() { return COMP.filter(function (c) { return st.on[c.k]; }).sort(function (a, b) { return a.o - b.o; }); }
    function estimate() {
      var lo = 0, hi = 0, p = picked();
      if (TYPES[st.type] && TYPES[st.type].noEst) return null;
      p.forEach(function (c) { var r = EST[c.k]; if (r) { lo += r[0]; hi += r[1]; } });
      if (!lo) return null;
      return { lo: Math.floor(lo / 5000) * 5000, hi: Math.ceil(hi / 5000) * 5000 };
    }
    function nSuppliers() { var p = picked(); return Math.max(2, p.length + ((st.on.perg || st.on.kit) ? 1 : 0)); }
    function summary() {
      var p = picked();
      return 'מפת פרויקט | סגנון: ' + TYPES[st.type].name + ' | רכיבים: ' + p.map(function (c, i) { return (i + 1) + ') ' + c.t; }).join(', ') +
        ' | שלב: ' + STAGES[st.stage].t + ' | ספקים משוער: ' + nSuppliers() + (estimate() ? ' | הערכה שהוצגה: ' + fmtN(estimate().lo) + ' עד ' + fmtN(estimate().hi) + ' ש"ח' : '') + (st.note.trim() ? ' | הערה: ' + st.note.trim() : '');
    }
    function sync() {
      var p = picked();
      COMP.forEach(function (c, i) {
        var idx = p.indexOf(c);
        pins[i].classList.toggle('on', idx > -1);
        pins[i].classList.toggle('hot', st.hot === c.k);
        pins[i].firstChild.textContent = idx > -1 ? (idx + 1) : '';
        pins[i].setAttribute('aria-label', idx > -1 ? ((idx + 1) + ' ' + c.t) : c.t);
      });
      empty.textContent = st.type === null ? (CFG.pickTxt || 'בחרו איזו מרפסת דומה לשלכם, והתמונה תתחלף.') : CFG.empty;
      empty.style.opacity = (p.length || st.step > 1) ? 0 : 1;
      legend.innerHTML = p.length ? p.map(function (c, i) { return '<span><em>' + (i + 1) + '</em>' + esc(c.t) + '</span>'; }).join('') : '<span style="opacity:.7">' + (st.type === null ? esc(CFG.pick) : 'עוד לא נבחר רכיב') + '</span>';
      [].forEach.call(panel.querySelectorAll('.pm-chip[data-k]'), function (ch) {
        var c = COMP.filter(function (x) { return x.k === ch.getAttribute('data-k'); })[0], idx = p.indexOf(c);
        ch.setAttribute('aria-pressed', idx > -1); ch.querySelector('.pm-num').textContent = idx > -1 ? idx + 1 : '';
      });
      [].forEach.call(panel.querySelectorAll('.pm-list li'), function (li) { li.classList.toggle('hot', li.getAttribute('data-k') === st.hot); });
    }

    function prog() { var s = ''; for (var i = 0; i < TOTAL; i++) s += '<span class="' + (i <= st.step - OFF ? 'on' : '') + '"></span>'; return '<div class="pm-prog">' + s + '</div>'; }
    function simpleChips(arr, sel) { return '<div class="pm-chips">' + arr.map(function (a, i) { return '<button type="button" class="pm-chip" data-i="' + i + '" aria-pressed="' + (sel === i) + '">' + esc(a) + '</button>'; }).join('') + '</div>'; }
    function typeCards() { return '<div class="pm-tcards">' + TYPES.map(function (T, i) { return '<button type="button" class="pm-tcard' + (T.other ? ' pm-other' : '') + '" data-ty="' + i + '" aria-pressed="' + (st.type === i) + '">' + (T.other ? '' : '<img src="' + T.pic + '" alt="" loading="lazy" decoding="async">') + '<span><b>' + esc(T.name) + '</b><small>' + esc(T.sub || '') + '</small></span></button>'; }).join('') + '</div>'; }

    function fullPlan() {
      var p = picked();
      return '<div class="pm-steps"><span>פגישה ומדידה</span><span>תכנון יישומי</span><span>ביצוע</span><span>מסירה</span></div>' +
        '<div class="pm-note">' + esc(STAGES[st.stage].n) + '</div>' +
        (st.note.trim() ? '<div class="pm-note"><b>מה שחשוב לכם:</b> ' + esc(st.note.trim()) + '</div>' : '') +
        '<ol class="pm-list">' + p.map(function (c, i) { return '<li data-k="' + c.k + '"><span class="n">' + (i + 1) + '</span><div><span class="cl">' + esc(c.cat) + '</span><b>' + esc(c.t) + '</b><span class="d">' + esc(c.d) + '</span></div></li>'; }).join('') + '</ol>';
    }

    function render() {
      var h = prog(), p = picked();
      if (st.step === 0) {
        h += '<p class="pm-q">' + esc(CFG.q0) + '</p><p class="pm-hint">' + esc(CFG.hint0) + '</p>' + typeCards() +
          '<div class="pm-nav"><span></span><button type="button" class="pm-btn" id="pm-next"' + (st.type === null ? ' disabled' : '') + '>המשך ←</button></div>';
      } else if (st.step === 1) {
        var other = !!TYPES[st.type].other;
        h += '<p class="pm-q">' + esc(other ? 'מה בראש שלכם?' : CFG.q2) + '</p><p class="pm-hint">' + (other ? 'כתבו לנו בקצרה, ונתאים את המפה.' : 'אפשר לבחור כמה. המספרים נדלקים על התמונה לפי סדר הבנייה.') + '</p>' +
          (COMP.length ? '<div class="pm-chips">' + COMP.map(function (c) { return '<button type="button" class="pm-chip" data-k="' + c.k + '" aria-pressed="false"><span class="pm-num"></span><span class="pm-tx"><span>' + esc(c.t) + '</span><span class="pm-cat">' + esc(c.cat) + '</span></span></button>'; }).join('') + '</div>' : '') +
          '<label class="pm-lbl" for="pm-note-in">' + (other ? 'מה תרצו?' : 'משהו אחר שחשוב לכם? (לא חובה)') + '</label>' +
          '<textarea id="pm-note-in" class="pm-note-in" rows="2" placeholder="למשל: סוג חומר, גוון, רעיון שראיתם">' + esc(st.note) + '</textarea>' +
          '<div class="pm-nav">' + (MULTI ? '<button type="button" class="pm-back" id="pm-back">→ חזרה</button>' : '<span></span>') + '<button type="button" class="pm-btn" id="pm-next"' + ((p.length || st.note.trim()) ? '' : ' disabled') + '>המשך ←</button></div>';
      } else if (st.step === 2) {
        h += '<p class="pm-q">איפה אתם עכשיו?</p><p class="pm-hint">בחירה אחת</p>' + simpleChips(STAGES.map(function (s) { return s.t; }), st.stage) +
          '<div class="pm-nav"><button type="button" class="pm-back" id="pm-back">→ חזרה</button><button type="button" class="pm-btn" id="pm-next"' + (st.stage === null ? ' disabled' : '') + '>הצגת המפה ←</button></div>';
      } else {
        var n = nSuppliers(), T = TYPES[st.type];
        h += '<p class="pm-q">' + (T.other ? 'הבקשה שלכם מוכנה' : 'המפה שלכם מוכנה: ' + esc(T.name) + ', ' + p.length + ' רכיבים') + '</p>' +
          (T.other && !p.length ? '' : '<div class="pm-sup"><span class="n">' + n + '</span><div><b>בפרויקט כזה עובדים בערך ' + n + ' ספקים.</b><span class="s">אצלכם: תוכנית אחת ונקודת קשר אחת, מדידה אחת והובלה אחת. כשהפרויקט מנוהל במקום אחד יש פוטנציאל לחיסכון בעלויות לעומת הזמנה נפרדת מכל ספק, בהתאם לפרויקט ולהצעה בכתב. <a href="#' + (document.getElementById('one') ? 'one' : 'why') + '">מה זה נותן לכם ←</a></span></div></div>');
        var E = estimate();
        if (!E && TYPES[st.type].noEst) h += '<div class="pm-note">פרויקטים עסקיים ומוסדיים מתומחרים לפי מדידה והיקף. נחזור אליכם עם הצעה.</div>';
        if (E) h += '<div class="pm-price"><span class="pm-price-l">הערכה כללית לפרויקט כזה</span><b class="pm-price-n">בערך ' + esc(fmtN(E.lo)) + ' עד ' + esc(fmtN(E.hi)) + ' ש"ח</b>' +
          '<span class="pm-price-s">טווח כללי, בגודל טיפוסי לכל רכיב ועם התקנה. הגודל, החומרים והגימור משנים אותו, והמחיר נקבע רק אחרי מדידה בשטח, בהצעה מפורטת בכתב.' + (E.lo < 40000 ? ' פרויקטים שלמים אצלנו מתחילים בדרך כלל בכ-40,000 ש"ח.' : '') + '</span></div>';
        if (!st.sent) {
          h += '<p class="pm-hint">השאירו מספר טלפון ונשלח לכם את המפה המלאה: סדר בנייה, שלבים ומה מתואם עם מה. נחזור אליכם לשיחה קצרה.</p>' +
            '<form class="pm-form" id="pm-form" novalidate><input name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="טלפון" aria-label="טלפון" required><input name="name" type="text" autocomplete="name" placeholder="שם (לא חובה)" aria-label="שם"><button type="submit" class="pm-btn" id="pm-send">שלחו לי את המפה ←</button></form>' +
            '<p class="pm-err" id="pm-err" role="alert"></p>' +
            '<p class="pm-fine">השארת פרטים מהווה הסכמה ליצירת קשר לצורך טיפול בפנייה זו בלבד. <a href="/legal#terms">תנאי השימוש</a> · <a href="/legal#privacy">מדיניות הפרטיות</a></p>' +
            '<div class="pm-nav"><button type="button" class="pm-back" id="pm-back">→ לשינוי הבחירות</button><span></span></div>';
        } else {
          h += '<div class="pm-ok"><h3>המפה בדרך אליכם.</h3><p>נחזור אליכם לשיחה קצרה. קודם מקשיבים, אחר כך מציעים.</p>' +
            '<a class="pm-btn wa" target="_blank" rel="noopener" href="https://wa.me/' + WA + '?text=' + encodeURIComponent('היי, בניתי מפת פרויקט באתר. ' + summary()) + '">לשלוח לנו גם בוואטסאפ ←</a></div>' + fullPlan();
        }
      }
      panel.innerHTML = h;
      [].forEach.call(panel.querySelectorAll('.pm-tcard'), function (b) { b.onclick = function () { st.type = +b.getAttribute('data-ty'); applyType(st.type); track('pm_style', { style: TYPES[st.type].name }); sync(); render(); }; });
      [].forEach.call(panel.querySelectorAll('.pm-chip'), function (b) {
        b.onclick = function () {
          if (b.getAttribute('data-k')) { var k = b.getAttribute('data-k'); st.on[k] = !st.on[k]; sync(); var nx = document.getElementById('pm-next'); if (nx) nx.disabled = !(picked().length || st.note.trim()); return; }
          st.stage = +b.getAttribute('data-i'); render();
        };
      });
      [].forEach.call(panel.querySelectorAll('.pm-list li'), function (li) { li.onclick = function () { st.hot = (st.hot === li.getAttribute('data-k') ? null : li.getAttribute('data-k')); sync(); }; });
      var ni = document.getElementById('pm-note-in'); if (ni) ni.oninput = function () { st.note = ni.value; var n2 = document.getElementById('pm-next'); if (n2) n2.disabled = !(picked().length || st.note.trim()); };
      var nx = document.getElementById('pm-next'); if (nx) nx.onclick = function () { st.step++; track('pm_step', { step: st.step }); render(); };
      var bk = document.getElementById('pm-back'); if (bk) bk.onclick = function () { st.sent = false; st.step = st.step === 3 ? 1 : st.step - 1; render(); };
      var fm = document.getElementById('pm-form'); if (fm) fm.onsubmit = submit;
      sync();
    }

    function submit(ev) {
      ev.preventDefault();
      var f = ev.target, phone = String(f.phone.value || '').replace(/[^\d+]/g, ''), name = String(f.name.value || '').trim(), err = document.getElementById('pm-err'), btn = document.getElementById('pm-send');
      var digits = phone.replace(/^\+972/, '0').replace(/^972/, '0');
      if (!/^0\d{8,9}$/.test(digits)) { err.textContent = 'נא להזין מספר טלפון תקין, למשל 0501234567.'; f.phone.focus(); return; }
      err.textContent = ''; btn.disabled = true; btn.textContent = 'שולחים...';
      var done = function () { st.sent = true; track('pm_lead', { style: TYPES[st.type].name }); render(); var ok = panel.querySelector('.pm-ok'); if (ok && ok.scrollIntoView) ok.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); };
      if (DRY || !window.stzSendLead) { if (window.console) console.log('[project-map] dry run, not sent:', summary(), digits, name); done(); return; }
      window.stzSendLead({ name: name, phone: digits, solution: TYPES[st.type].name, message: summary(), source: door + '_map' }).then(done).catch(function () {
        btn.disabled = false; btn.textContent = 'שלחו לי את המפה ←';
        err.textContent = 'לא הצלחנו לשלוח כרגע. אפשר גם להתקשר: 055-310-0154.';
      });
    }

    render();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
