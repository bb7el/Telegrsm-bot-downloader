import telebot
from telebot import types
import requests
import json

# التوكن الخاص بالبوت
token = "7270813649:AAGdAMMe1DPXlLOEIPq_L3NaHCzmdhEpquI"
bot = telebot.TeleBot(token)

# تخزين الرسائل المتعلقة بالفيديوهات
sent_video_messages = {}

# تعيين الأوامر
bot.set_my_commands([
    telebot.types.BotCommand("/start", "🤖 تشغيل البوت"),
    telebot.types.BotCommand("/help", "🆘 تعليمات")
])

# التعامل مع أمر start
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, '''
مرحبًا بك في بوتنا الفريد والمختص في تحميل الفيديوهات من تيكتوك وإنستغرام! 🎥✨

📌 هل تبحث عن طريقة سهلة وسريعة لحفظ مقاطع الفيديو المفضلة لديك من تيكتوك وإنستغرام؟ لا تبحث بعيدًا، فقد وصلت إلى المكان المثالي! نحن هنا لنقدم لك تجربة مميزة وخدمة احترافية تضيف لمسة من الفخامة إلى تجربتك اليومية.

🔍 فقط أرسل لنا رابط الفيديو الذي ترغب بتحميله، وسنقوم بالباقي! استمتع بحفظ ومشاركة لحظاتك المفضلة بكل سهولة وسرعة.

🌟 نعدك بأن نقدم لك خدمة موثوقة وآمنة تحافظ على جودة الفيديوهات العالية لتستمتع بمشاهدتها في أي وقت وأي مكان.

إذا كنت مستعدًا للبدء، فقط ابدأ بمشاركة الروابط معنا الآن! 📲

نحن هنا لخدمتك! 🤝
    ''')



# إرسال رسالة ترحيب تلقائيًا عند بدء المحادثة
@bot.message_handler(func=lambda message: True, content_types=['new_chat_members'])
def on_user_joined(message):
    bot.send_message(message.chat.id, '''
مرحبًا بك في بوتنا الفريد والمختص في تحميل الفيديوهات من تيكتوك وإنستغرام! 🎥✨

📌 هل تبحث عن طريقة سهلة وسريعة لحفظ مقاطع الفيديو المفضلة لديك من تيكتوك وإنستغرام؟ لا تبحث بعيدًا، فقد وصلت إلى المكان المثالي! نحن هنا لنقدم لك تجربة مميزة وخدمة احترافية تضيف لمسة من الفخامة إلى تجربتك اليومية.

🔍 فقط أرسل لنا رابط الفيديو الذي ترغب بتحميله، وسنقوم بالباقي! استمتع بحفظ ومشاركة لحظاتك المفضلة بكل سهولة وسرعة.

🌟 نعدك بأن نقدم لك خدمة موثوقة وآمنة تحافظ على جودة الفيديوهات العالية لتستمتع بمشاهدتها في أي وقت وأي مكان.

إذا كنت مستعدًا للبدء، فقط ابدأ بمشاركة الروابط معنا الآن! 📲

نحن هنا لخدمتك! 🤝
    ''')




# التعامل مع أمر help
@bot.message_handler(commands=["help"])
def help_message(message):
    bot.reply_to(message, """
    📜 <b>تعليمات استخدام البوت:</b>
    1. أرسل رابط فيديو من تيك توك أو إنستغرام لتحميله. 🎥
    2. سأقوم بمعالجة الرابط وإرسال الفيديو مع التفاصيل. 💾
    3. بعد الانتهاء، يمكنك إرسال رابط آخر لتحميل فيديو جديد. 🔄
    """, parse_mode="HTML")

# التعامل مع الرسائل النصية
@bot.message_handler(content_types=['text'])
def handle_message(message):
    url = message.text.strip()

    if "tiktok.com" in url:
        handle_tiktok_video(message, url)
    elif "instagram.com" in url:
        handle_instagram_video(message, url)
    else:
        bot.reply_to(message, '❌ الرابط غير معروف. يرجى إرسال رابط تيك توك أو إنستغرام.')

def handle_tiktok_video(message, url):
    try:
        msgg = bot.send_message(message.chat.id, "*📥 جاري التحميل...*", parse_mode="Markdown")
        response = requests.get(f'https://tikwm.com/api/?url={url}')
        data = response.json()

        print(json.dumps(data, indent=2))  # تحسين طباعة الاستجابة للتحقق من البيانات

        if 'data' in data:
            video_data = data['data']
            music_url = video_data.get('music')
            region = video_data.get('region')
            title = video_data.get('title')
            video_url = video_data.get('play')
            avatar_url = video_data.get('author', {}).get('avatar')
            music_info = video_data.get('music_info', {})
            name = music_info.get('author')
            duration = video_data.get('duration')
            share_count = video_data.get('share_count')
            comment_count = video_data.get('comment_count')
            play_count = video_data.get('play_count')
            likes = video_data.get('digg_count')

            # حذف رسالة التحميل
            bot.delete_message(chat_id=message.chat.id, message_id=msgg.message_id)

            # إرسال صورة الملف الشخصي
            bot.send_photo(message.chat.id, avatar_url, caption=f"""
            *🌟 تفاصيل الحساب:*
            - **🧑 اسم الحساب:** {name}
            - **🌍 دولة الحساب:** {region}

            *🎥 تفاصيل الفيديو:*
            - **👁️ عدد المشاهدات:** {play_count}
            - **👍 عدد الإعجابات:** {likes}
            - **💬 عدد التعليقات:** {comment_count}
            - **🔄 عدد المشاركات:** {share_count}
            - **⏳ طول الفيديو:** {duration}
            """, parse_mode="Markdown")

            # إرسال الفيديو
            bot.send_video(message.chat.id, video_url, caption=f"*📹 عنوان الفيديو:* {title}", parse_mode="Markdown")

            if music_url:
                # تحميل وارسال ملف الصوت
                audio_response = requests.get(music_url)
                audio_file_path = "/tmp/audio.mp3"
                with open(audio_file_path, 'wb') as f:
                    f.write(audio_response.content)
                bot.send_audio(message.chat.id, open(audio_file_path, 'rb'), title="🎵 TikTok Audio")
            else:
                bot.reply_to(message, "🔍 لم يتم العثور على رابط الصوت.")

            # رسالة بعد الانتهاء من إرسال الفيديو والصوت
            bot.reply_to(message, "🎉 تم إرسال الفيديو بنجاح! أرسل لي رابطاً آخر لتحميل فيديو جديد.")

            # أزرار تفاعلية
            keyboard = types.InlineKeyboardMarkup()
            button = types.InlineKeyboardButton(text="🔄 أرسل رابط آخر", callback_data="send_another")
            keyboard.add(button)
            bot.send_message(message.chat.id, "📩 هل لديك رابط آخر لتحميله؟", reply_markup=keyboard)

        else:
            bot.reply_to(message, "❌ لم يتم العثور على بيانات الفيديو. يرجى التحقق من الرابط وإعادة المحاولة.")

    except Exception as e:
        bot.delete_message(chat_id=message.chat.id, message_id=msgg.message_id)
        bot.reply_to(message, f'💥 حدث خطأ: {str(e)}. يرجى المحاولة مرة أخرى.')

def handle_instagram_video(message, url):
    try:
        # إرسال رسالة "جاري التحميل..."
        msgg = bot.send_message(message.chat.id, "*📥 جاري تحميل الفيديو...*", parse_mode="Markdown")

        # إرسال طلب لتحميل الفيديو من إنستغرام
        json_data = {'url': url}
        response = requests.post('https://insta.savetube.me/downloadPostVideo', json=json_data).json()
        video_url = response['post_video_url']

        # حذف رسالة "جاري التحميل..."
        bot.delete_message(chat_id=message.chat.id, message_id=msgg.message_id)

        # إرسال الفيديو مباشرةً
        bot.send_video(message.chat.id, video_url, caption="📽️ فيديو إنستغرام تم تحميله بنجاح! 🎉", parse_mode="Markdown")
    except Exception as e:
        bot.delete_message(chat_id=message.chat.id, message_id=msgg.message_id)
        bot.reply_to(message, '❌ الرابط غير صحيح أو حدث خطأ أثناء المعالجة.')

# التعامل مع أزرار الاستجابة
@bot.callback_query_handler(func=lambda call: call.data == 'vid')
def handle_callback(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.reply_to(call.message, "🎉 تم إرسال الفيديو بنجاح!")

@bot.callback_query_handler(func=lambda call: call.data == "send_another")
def handle_another(call):
    bot.send_message(call.message.chat.id, "✅ تم استلام طلبك! أرسل لي رابط الفيديو الذي ترغب في تحميله.")

print('Bot is running...')
bot.infinity_polling()
