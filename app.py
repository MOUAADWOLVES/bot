# app.py - ملف البوت المعدل للعمل على Netlify
import os
import logging
import json
import time
from flask import Flask, render_template_string, request, jsonify
import requests

# إعدادات التطبيق
app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8390149006:AAFSy4v-lir3S_GrGBFKXNoVy9sR_jgn23g")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# حالة البوت
bot_status = "نشط"
bot_start_time = time.time()

# صفحة HTML الرئيسية
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>بوت ⌯𝗠𝗢𝗨𝗔𝗔𝗗 - حالة التشغيل</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            padding: 30px;
            margin-top: 30px;
        }
        header {
            text-align: center;
            padding: 20px 0;
            color: white;
            background: rgba(0,0,0,0.7);
            border-radius: 10px;
            margin-bottom: 30px;
        }
        h1 {
            color: #764ba2;
            text-align: center;
        }
        .status {
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
        }
        .online {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .offline {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .btn {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 12px 25px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            margin: 10px 5px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }
        .btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        .bot-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid #e9ecef;
        }
        .feature:hover {
            transform: translateY(-5px);
        }
        footer {
            text-align: center;
            padding: 30px 0;
            color: #6c757d;
            margin-top: 40px;
            border-top: 1px solid #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 style="color: white;">بوت ⌯𝗠𝗢𝗨𝗔𝗔𝗗</h1>
            <p>نظام إدارة وعرض حالة البوت على Netlify</p>
        </header>
        
        <div class="status {{ status_class }}">
            {{ status_message }}
        </div>
        
        <div style="text-align: center;">
            <a href="https://t.me/Kfkfkhjjfkbot" class="btn">إضافة إلى المجموعة</a>
            <a href="https://t.me/UPDATE_GATTOUZ" class="btn">قناة التحديثات</a>
            <a href="https://t.me/MBl_py" class="btn">اتصل بالمطور</a>
        </div>
        
        <div class="bot-info">
            <h2>معلومات البوت</h2>
            <p><strong>اسم البوت:</strong> ⌯𝗠𝗢𝗨𝗔𝗔𝗗</p>
            <p><strong>المطور:</strong> MAYKEL (@MBl_py)</p>
            <p><strong>حالة البوت:</strong> {{ bot_status }}</p>
            <p><strong>وقت التشغيل:</strong> {{ uptime }}</p>
            <p><strong>الإصدار:</strong> 2.0 (معدل للعمل على Netlify)</p>
        </div>
        
        <h2>ميزات البوت</h2>
        <div class="features">
            <div class="feature">
                <h3>🔐 نظام الحماية</h3>
                <p>قفل وفتح أنواع متعددة من المحتوى</p>
            </div>
            <div class="feature">
                <h3>💰 نظام الاقتصاد</h3>
                <p>فلوس، وظائف، وتحويل الأموال</p>
            </div>
            <div class="feature">
                <h3>🎮 ألعاب الترفيه</h3>
                <p>أوامر تسلية تفاعلية</p>
            </div>
            <div class="feature">
                <h3>📊 الإحصائيات</h3>
                <p>توب الفلوس والحرامية</p>
            </div>
        </div>
        
        <div class="bot-info">
            <h2>كيفية الاستخدام</h2>
            <p>1. أضف البوت إلى مجموعتك على Telegram</p>
            <p>2. امنح البوت صلاحية المشرف</p>
            <p>3. استخدم الأمر /settings لرؤية جميع الأوامر</p>
            <p>4. استخدم الأوامر المختلفة للإدارة والترفيه</p>
        </div>
        
        <footer>
            <p>تم التطوير بواسطة MAYKEL | @MBl_py</p>
            <p>⌯𝗠𝗢𝗨𝗔𝗔𝗗 Bot - جميع الحقوق محفوظة © 2024</p>
        </footer>
    </div>
</body>
</html>
"""

# ملفات التخزين
ADMINS_FILE = "admins.json"
GROUP_SETTINGS_FILE = "group_settings.json"
GROUP_ROLES_FILE = "group_roles.json"
USER_DATA_FILE = "user_data.json"
CODES_FILE = "codes.json"
DEVELOPER_DATA_FILE = "developer.json"
USER_PHOTOS_FILE = "user_photos.json"

# تحميل البيانات
def load_data(filename, default={}):
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تحميل جميع البيانات
admins_data = load_data(ADMINS_FILE, {"owner": 5545019702, "admins": [5545019702]})
group_settings = load_data(GROUP_SETTINGS_FILE)
group_roles = load_data(GROUP_ROLES_FILE)
user_data = load_data(USER_DATA_FILE)
codes_data = load_data(CODES_FILE)
developer_data = load_data(DEVELOPER_DATA_FILE, {"photo_id": None, "photo_url": None})
user_photos = load_data(USER_PHOTOS_FILE)

# وظائف المساعدة
def is_owner(user_id):
    return admins_data.get("owner") == user_id

def is_admin(user_id):
    return user_id in admins_data.get("admins", []) or is_owner(user_id)

def get_user_data(user_id):
    user_id_str = str(user_id)
    if user_id_str not in user_data:
        user_data[user_id_str] = {
            "money": 1000,
            "job": None,
            "last_salary": None,
            "married_to": None,
            "last_daily": None,
            "bank_account": None,
            "messages_count": 0,
            "rob_count": 0,
            "rob_success": 0,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        save_data(USER_DATA_FILE, user_data)
    return user_data[user_id_str]

def update_user_data(user_id, data):
    user_id_str = str(user_id)
    user_data[user_id_str] = data
    save_data(USER_DATA_FILE, user_data)

# وظائف Telegram API
def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    
    if parse_mode:
        payload["parse_mode"] = parse_mode
        
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

def answer_callback_query(callback_query_id, text):
    url = f"{TELEGRAM_API_URL}/answerCallbackQuery"
    payload = {
        "callback_query_id": callback_query_id,
        "text": text
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error answering callback query: {e}")
        return None

# معالجة webhook من Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = request.get_json()
        
        # معالجة الرسائل
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            text = message.get('text', '')
            
            # معالجة الأمر /start
            if text in ['/start', '/help']:
                welcome_text = f"""*▶️ | مرحباً بك في بوت ⌯𝗠𝗢𝗨𝗔𝗔𝗗*\n\n
*◈ | للبحث عن فيديو:*
`يوت` + كلمة البحث

*◈ | مثال:* `يوت أغنية جميلة`

*◈ | البوت يدعم المجموعات أيضاً*"""
                
                markup = {
                    "inline_keyboard": [[
                        {"text": "اضفني في مجموعتك ✅", "url": "https://t.me/Kfkfkhjjfkbot?startgroup=true"}
                    ]]
                }
                
                send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")
            
            # معالجة الأمر /settings
            elif text == '/settings':
                settings_text = """
🛡️ أوامر الحماية:

قفل/فتح الملصقات
قفل/فتح الصور
قفل/فتح الفيديو
قفل/فتح الدردشة
قفل/فتح الصوتيات
قفل/فتح الملفات
قفل/فتح إعادة توجيه
قفل/فتح التاق
قفل/فتح العربية
قفل/فتح الإنجليزية
قفل/فتح الموسيقى
قفل/فتح المعرفات
قفل/فتح جهات الاتصال
قفل/فتح الألعاب
قفل/فتح الروابط
قفل/فتح البوتات
قفل/فتح إشعارات الدخول
قفل/فتح قران كريم

👥 أوامر الإدارة:
كتم/حظر/فك كتم/فك حظر (بالرد)
رفع/تنزيل مشرف/مميز (بالرد)

💰 أوامر الاقتصاد:
انشاء حساب بنكي
حسابي
فلوسي
راتب
عمل
روح [المبلغ] (بالرد)
مهر (بالرد)
كود [الكود]

🎮 أوامر الترفيه:
ثث، كتاب، نرد، زوجني، احبك، بوسة، تفاصيل، هينه
                """
                send_message(chat_id, settings_text)
            
            # معالجة أوامر الاقتصاد
            elif text in ['انشاء حساب بنكي', 'حسابي', 'فلوسي', 'راتب']:
                user_info = get_user_data(user_id)
                response_text = ""
                
                if text == 'انشاء حساب بنكي':
                    if not user_info.get('bank_account'):
                        user_info['bank_account'] = True
                        update_user_data(user_id, user_info)
                        response_text = "✅ تم إنشاء حسابك البنكي بنجاح!"
                    else:
                        response_text = "⚠️ لديك حساب بنكي بالفعل!"
                
                elif text == 'حسابي':
                    response_text = f"💼 معلومات حسابك:\n\n"
                    response_text += f"💰 الرصيد: {user_info.get('money', 0)} $\n"
                    response_text += f"👔 الوظيفة: {user_info.get('job', 'لا يوجد')}\n"
                    response_text += f"💍 الحالة الاجتماعية: {'متزوج' if user_info.get('married_to') else 'أعزب'}\n"
                    response_text += f"🏦 الحساب البنكي: {'مفعل' if user_info.get('bank_account') else 'غير مفعل'}"
                
                elif text == 'فلوسي':
                    response_text = f"💰 رصيدك: {user_info.get('money', 0)} $"
                
                elif text == 'راتب':
                    if user_info.get('job'):
                        # منح راتب عشوائي بين 1000 و 5000
                        salary = 1000  # يمكن تعديل هذا حسب الوظيفة
                        user_info['money'] = user_info.get('money', 0) + salary
                        update_user_data(user_id, user_info)
                        response_text = f"💰 تم استلام راتبك: {salary} $\n💼 رصيدك الحالي: {user_info['money']} $"
                    else:
                        response_text = "❌ ليس لديك وظيفة لاستلام الراتب!"
                
                send_message(chat_id, response_text)
        
        # معالجة استفسارات callback
        elif 'callback_query' in update:
            callback_query = update['callback_query']
            callback_data = callback_query['data']
            callback_id = callback_query['id']
            
            if callback_data.startswith('check_sub_'):
                user_id = int(callback_data.split('_')[-1])
                # هنا يجب إضافة التحقق الفعلي من الاشتراك في القناة
                answer_callback_query(callback_id, "✅ تم التحقق من الاشتراك، يمكنك استخدام البوت الآن!")
            
        return jsonify({'status': 'ok'})
    return 'OK'

# إعداد webhook
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    webhook_url = f"https://{request.host}/webhook"
    url = f"{TELEGRAM_API_URL}/setWebhook?url={webhook_url}"
    
    try:
        response = requests.get(url)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)})

# الصفحة الرئيسية
@app.route('/')
def home():
    # حساب وقت التشغيل
    uptime_seconds = time.time() - bot_start_time
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))
    
    # تحديد حالة البوت
    status_class = "online" if bot_status == "نشط" else "offline"
    status_message = "✅ البوت يعمل بشكل طبيعي" if bot_status == "نشط" else "❌ البوت غير نشط حاليًا"
    
    return render_template_string(HTML_TEMPLATE, 
                                status_class=status_class,
                                status_message=status_message,
                                bot_status=bot_status,
                                uptime=uptime_str)

if __name__ == '__main__':
    # هذا السطر غير ضروري على Netlify ولكن يبقى للتشغيل المحلي
    app.run(host='0.0.0.0', port=5000)