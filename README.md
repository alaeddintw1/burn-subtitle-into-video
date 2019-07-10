السلام عليكم

هذا سكريبت بسيط مكتوب بلغه بايثون3
يمكنك من وضع الترجمه او النص للكلام الموجود بالفيديو
بطريقه ان يكون وكانه من صور الفيديو, اي انه يصبح كصوره من ضمن الفيديو وليس بطريقه السابتيتلsubtitle

طريقته بسيطه, قم بوضع ملف بايثون المكتوب  هنا+ ملف الفونت +ملف الفيديو +ملف السابتيتل
قم بعمب الامر التالي:
>python3 HardCodeSrt_v1.py
وسف ينتج لك 3 ملفات وهي الملف النهائي الذي فيه السابتيتل مطبوع على الفيديو
وملف فيديو مع سابتيتل بدون صوت
وملف نص عادي فيه فقط النصوص بدون الفرمته الموجوده بملف السابتيتل
طبعا كلها تساعد في عمليه الدبلجه الصوتويه للفيديوهات.

ارجو ان يكون ذو فائده لمن يبحث عن هكذا برنامج وان يكون مجاني وفعال بالنسبه للغه العربيه

والسلام ختام
alaeddintw1@gmail.com

# burn-subtitle-into-video
Python3 script tool for burning .srt subtitle file to a video.

you only need to place the sahel.ttf (true type font) inside 
same folder + video file + .srt (subtitle file).

Output will be 3 files:
1>hardcoded subtitle to mp4 file.
2>silent video file without subtitles.
3>Text file contains only subtitle texts without srt formatting.

just run as following:
>python3 HardCodeSrt_v1.py

it will ask for video file name + srt file name (must be inside same running this script folder).

Hope it help someone....as i was in a need for such a tool and didnt found free and working tool.

Plz execuse my programming coding mess as i was in a hurry and its not commercial ;).

Sincere Rgds.
Alaeddintw1@gmail.com


