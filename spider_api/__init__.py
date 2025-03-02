import requests
import subprocess
import sys
from pkg_resources import parse_version

def check_for_updates():
    """
    دالة للتحقق من وجود إصدارات أحدث من المكتبة.
    """
    package_name = "spider-api"  # استبدل this باسم المكتبة الخاص بك
    try:
        # الحصول على الإصدار المثبت حاليًا
        installed_version = subprocess.check_output([sys.executable, "-m", "pip", "show", package_name])
        installed_version = installed_version.decode("utf-8").split("\n")[1].split(": ")[1]

        # الحصول على الإصدار الأحدث من PyPI
        latest_version = subprocess.check_output([sys.executable, "-m", "pip", "index", "versions", package_name])
        latest_version = latest_version.decode("utf-8").split("\n")[0].split(": ")[1]

        # مقارنة الإصدارات
        if parse_version(latest_version) > parse_version(installed_version):
            print(f"🔄 يوجد إصدار أحدث ({latest_version}). جاري التحديث...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
            print(f"✅ تم تحديث {package_name} إلى الإصدار {latest_version}.")
        else:
            print(f"ℹ️ أنت تستخدم أحدث إصدار من {package_name} ({installed_version}).")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء التحقق من التحديثات: {e}")

def WormGPT(text):
    """
    دالة لإرسال نص إلى API واستقبال الرد.

    :param text: النص المراد إرساله.
    :return: الرد من API مع تنسيق مخصص.
    """
    # التحقق من التحديثات عند كل استخدام
    check_for_updates()

    # التحقق من أن النص غير فارغ
    if not text:
        return {"response": "You must enter text. You have not entered text."}

    try:
        # إرسال الطلب إلى API
        response = requests.get(f'https://api-production-8dd7.up.railway.app/api?msg={text}')
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
        return {"response": formatted_response}

    except requests.exceptions.RequestException as e:
        # في حالة حدوث خطأ في الاتصال
        return {"response": f"An error occurred while connecting to the API: {e}"}
    except KeyError:
        # في حالة عدم وجود مفتاح "response" في الرد
        return {"response": "The API response format is invalid."}
    except Exception as e:
        # في حالة حدوث أي خطأ غير متوقع
        return {"response": f"An unexpected error occurred: {e}"}
