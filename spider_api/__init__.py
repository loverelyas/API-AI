import requests
import os
from dotenv import load_dotenv
try:
    import telebot
except ImportError:
    raise ImportError("لم يتم العثور على مكتبة pyTelegramBotAPI. يرجى تثبيتها باستخدام: pip install pyTelegramBotAPI")

load_dotenv()


# قراءة المتغيرات من GitHub Secrets
BOTTOKEN = os.getenv('BOTTOKEN')  # التوكن الخاص ببوت Telegram
ADMINID = os.getenv('ADMINID')  # معرف الدردشة الخاص بالإدمن
APIURL = os.getenv('APIURL')  # رابط API

# التحقق من أن المتغيرات موجودة

if not BOTTOKEN or not ADMINID or not APIURL:
    raise ValueError("يجب تعيين المتغيرات في ملف .env أو GitHub Secrets.")


# إنشاء كائن البوت
admin_bot = telebot.TeleBot(BOTTOKEN)

def WormGPT(text):
    """
    دالة لإرسال نص إلى API واستقبال الرد، وإرسال الطلب والرد إلى الإدمن.

    :param text: النص المراد إرساله.
    :return: الرد من API مع تنسيق مخصص.
    """
    # التحقق من أن النص غير فارغ
    if not text:
        return {"response": "You must enter text. You have not entered text."}

    try:
        # إرسال الطلب إلى API
        response = requests.get(f'{APIURL}?msg={text}')
        response.raise_for_status()  # التحقق من وجود أخطاء في الطلب

        # استخراج الرد من API
        result = response.json().get("response", "No response found in API reply.")

        # تنسيق الرد
        formatted_response = f"""
{result}

┏━━⚇
┃━┃ t.me/spider_XR7
┗━━━━━━━━
        """

        # إرسال الطلب والرد إلى الإدمن
        message_to_admin = f"""
📩 *طلب جديد من المستخدم:*
{text}

📤 *الرد من API:*
{formatted_response}
        """
        admin_bot.send_message(ADMINID, message_to_admin, parse_mode="Markdown")

        return {"response": formatted_response}

    except requests.exceptions.RequestException as e:
        # في حالة حدوث خطأ في الاتصال
        error_message = f"An error occurred while connecting to the API: {e}"
        admin_bot.send_message(ADMINID, error_message, parse_mode="Markdown")
        return {"response": error_message}
    except KeyError:
        # في حالة عدم وجود مفتاح "response" في الرد
        error_message = "The API response format is invalid."
        admin_bot.send_message(ADMINID, error_message, parse_mode="Markdown")
        return {"response": error_message}
    except Exception as e:
        # في حالة حدوث أي خطأ غير متوقع
        error_message = f"An unexpected error occurred: {e}"
        admin_bot.send_message(ADMINID, error_message, parse_mode="Markdown")
        return {"response": error_message}

# مثال استخدام
if __name__ == "__main__":
    # نص المستخدم (يمكن استبداله بمدخلات المستخدم الفعلية)
    user_text = "مرحبًا، كيف حالك؟"

    # الحصول على الرد من API
    response = WormGPT(user_text)

    # طباعة الرد (يمكن استبداله بإرسال الرد إلى المستخدم)
    print(response["response"])
