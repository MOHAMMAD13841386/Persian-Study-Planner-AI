# main.py - برنامه اصلی کامل
import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
import json
import os
from datetime import datetime
import numpy as np

Window.size = (360, 640)

# ==================== هوش مصنوعی ====================
class PersianStudyAI:
    def __init__(self):
        self.data_file = "study_data.json"
        self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {
                    "exams": [],
                    "subjects": [
                        {"name": "ریاضی", "hours": 0, "last_score": 0},
                        {"name": "فیزیک", "hours": 0, "last_score": 0},
                        {"name": "شیمی", "hours": 0, "last_score": 0},
                        {"name": "ادبیات", "hours": 0, "last_score": 0}
                    ],
                    "goals": [],
                    "study_sessions": []
                }
        except:
            self.data = {"exams": [], "subjects": [], "goals": []}
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_exam(self, subject, score, total=20):
        exam = {
            "id": len(self.data["exams"]) + 1,
            "subject": subject,
            "score": score,
            "total": total,
            "percentage": (score/total) * 100,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "type": "آزمون"
        }
        self.data["exams"].append(exam)
        self.save_data()
        
        # بروزرسانی درس
        for sub in self.data["subjects"]:
            if sub["name"] == subject:
                sub["last_score"] = score
                break
        
        return exam
    
    def analyze_performance(self):
        if not self.data["exams"]:
            return {"error": "هیچ آزمونی ثبت نشده است"}
        
        percentages = [e["percentage"] for e in self.data["exams"]]
        avg = np.mean(percentages)
        
        # تحلیل دروس
        subject_stats = {}
        for subject in set([e["subject"] for e in self.data["exams"]]):
            sub_scores = [e["percentage"] for e in self.data["exams"] if e["subject"] == subject]
            subject_stats[subject] = {
                "میانگین": round(np.mean(sub_scores), 1),
                "تعداد": len(sub_scores),
                "وضعیت": self._get_score_status(np.mean(sub_scores))
            }
        
        return {
            "تحلیل کلی": {
                "میانگین کل": f"{round(avg, 1)}%",
                "وضعیت": self._get_score_status(avg),
                "تعداد آزمون‌ها": len(percentages),
                "بهترین نمره": f"{round(max(percentages), 1)}%",
                "ضعیف‌ترین نمره": f"{round(min(percentages), 1)}%"
            },
            "تحلیل دروس": subject_stats,
            "توصیه‌ها": self._generate_recommendations(avg, subject_stats)
        }
    
    def _get_score_status(self, score):
        if score >= 85: return "عالی 🏆"
        elif score >= 70: return "خوب 👍"
        elif score >= 50: return "متوسط 📊"
        else: return "نیاز به تلاش ⚠️"
    
    def _generate_recommendations(self, avg_score, subject_stats):
        recommendations = []
        
        if avg_score < 60:
            recommendations.append("✅ روزی ۲ ساعت مطالعه مفید داشته باشید")
            recommendations.append("✅ روی مفاهیم پایه تمرکز کنید")
        
        # تشخیص دروس ضعیف
        weak_subjects = [sub for sub, stats in subject_stats.items() 
                        if stats["میانگین"] < 60]
        
        if weak_subjects:
            recommendations.append(f"🔴 روی این دروس بیشتر کار کنید: {', '.join(weak_subjects)}")
        
        # توصیه عمومی
        recommendations.append("⏱️ از تکنیک پومودورو استفاده کنید (۹۰ دقیقه مطالعه، ۲۰ دقیقه استراحت)")
        recommendations.append("📅 برنامه هفتگی منظم داشته باشید")
        
        return recommendations

# ==================== اپلیکیشن ====================
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai = PersianStudyAI()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # پس‌زمینه
        with layout.canvas.before:
            Color(0.95, 0.95, 0.98, 1)
            Rectangle(pos=layout.pos, size=layout.size)
        
        # عنوان
        title = Label(
            text='🧠 برنامه‌ریز درسی فارسی\nبا هوش مصنوعی پیشرفته',
            font_size=24,
            bold=True,
            color=(0.1, 0.1, 0.2, 1),
            size_hint=(1, 0.15),
            halign='center'
        )
        title.bind(size=title.setter('text_size'))
        layout.add_widget(title)
        
        # کارت آمار
        stats_card = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.2),
            padding=10
        )
        with stats_card.canvas.before:
            Color(0.2, 0.6, 0.9, 0.2)
            Rectangle(pos=stats_card.pos, size=stats_card.size)
        
        self.stats_label = Label(
            text='🎯 آماده برای شروع\nاولین آزمون خود را ثبت کنید',
            font_size=16,
            color=(0.2, 0.2, 0.4, 1),
            halign='center'
        )
        self.stats_label.bind(size=self.stats_label.setter('text_size'))
        stats_card.add_widget(self.stats_label)
        layout.add_widget(stats_card)
        
        # دکمه‌های اصلی
        buttons = [
            ("📝 ثبت آزمون جدید", (0.2, 0.6, 0.9, 1), self.add_exam),
            ("📊 تحلیل هوشمند", (0.9, 0.5, 0.2, 1), self.show_analysis),
            ("⏱️ پومودورو ۹۰/۲۰", (0.3, 0.7, 0.3, 1), self.start_pomodoro),
            ("📅 برنامه هفتگی", (0.7, 0.3, 0.7, 1), self.show_schedule),
            ("🎯 تعیین هدف", (0.2, 0.5, 0.8, 1), self.set_goal),
            ("📚 منابع آموزشی", (0.8, 0.4, 0.2, 1), self.show_resources)
        ]
        
        for text, color, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.12),
                background_color=color,
                background_normal='',
                color=(1, 1, 1, 1),
                font_size=15,
                bold=True
            )
            btn.bind(on_press=callback)
            layout.add_widget(btn)
        
        self.add_widget(layout)
        Clock.schedule_once(self.update_stats, 0.5)
    
    def update_stats(self, dt):
        """بروزرسانی آمار"""
        analysis = self.ai.analyze_performance()
        if "error" not in analysis:
            stats = analysis["تحلیل کلی"]
            self.stats_label.text = f'📊 آمار کلی\nمیانگین: {stats["میانگین کل"]}\nوضعیت: {stats["وضعیت"]}\nتعداد آزمون‌ها: {stats["تعداد آزمون‌ها"]}'
    
    def add_exam(self, instance):
        """افزودن آزمون"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # انتخاب درس
        subjects = ["ریاضی", "فیزیک", "شیمی", "ادبیات", "زبان انگلیسی", "دینی"]
        
        subject_label = Label(text="انتخاب درس:", font_size=16)
        content.add_widget(subject_label)
        
        self.subject_input = TextInput(
            hint_text="نام درس",
            size_hint=(1, 0.2)
        )
        content.add_widget(self.subject_input)
        
        # نمره
        score_label = Label(text="نمره کسب شده (از 20):", font_size=16)
        content.add_widget(score_label)
        
        self.score_input = TextInput(
            hint_text="مثال: 16",
            size_hint=(1, 0.2),
            input_filter='int'
        )
        content.add_widget(self.score_input)
        
        # دکمه‌ها
        btn_layout = BoxLayout(spacing=10, size_hint=(1, 0.3))
        
        cancel_btn = Button(text="لغو")
        save_btn = Button(text="ذخیره", background_color=(0.3, 0.7, 0.3, 1))
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(save_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(
            title="ثبت آزمون جدید",
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        cancel_btn.bind(on_press=popup.dismiss)
        save_btn.bind(on_press=self.save_exam)
        
        self.current_popup = popup
        popup.open()
    
    def save_exam(self, instance):
        """ذخیره آزمون"""
        subject = self.subject_input.text.strip()
        try:
            score = float(self.score_input.text)
        except:
            score = 0
        
        if subject and 0 <= score <= 20:
            self.ai.add_exam(subject, score)
            self.current_popup.dismiss()
            self.update_stats(0)
            self.show_message("موفقیت", f"آزمون {subject} با نمره {score} ثبت شد!")
        else:
            self.show_message("خطا", "لطفاً اطلاعات را صحیح وارد کنید")
    
    def show_analysis(self, instance):
        """نمایش تحلیل"""
        analysis = self.ai.analyze_performance()
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        if "error" in analysis:
            content.add_widget(Label(text=analysis["error"], font_size=16))
        else:
            # تحلیل کلی
            general = analysis["تحلیل کلی"]
            general_text = f"""📊 تحلیل کلی:
میانگین: {general['میانگین کل']}
وضعیت: {general['وضعیت']}
تعداد آزمون‌ها: {general['تعداد آزمون‌ها']}
بهترین نمره: {general['بهترین نمره']}
ضعیف‌ترین نمره: {general['ضعیف‌ترین نمره']}
"""
            content.add_widget(Label(text=general_text, font_size=14))
            
            # توصیه‌ها
            if "توصیه‌ها" in analysis:
                recommendations = "\n".join(analysis["توصیه‌ها"])
                content.add_widget(Label(text=f"\n💡 توصیه‌ها:\n{recommendations}", font_size=12))
        
        close_btn = Button(text="بستن", size_hint=(1, 0.2))
        popup = Popup(
            title="تحلیل هوشمند",
            content=content,
            size_hint=(0.9, 0.7)
        )
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
    
    def start_pomodoro(self, instance):
        """شروع پومودورو"""
        self.show_message("پومودورو", "⏱️ تایمر ۹۰ دقیقه‌ای شروع شد!\n\n۹۰ دقیقه مطالعه 📚\n۲۰ دقیقه استراحت ☕")
    
    def show_schedule(self, instance):
        """نمایش برنامه هفتگی"""
        schedule = """📅 برنامه هفتگی پیشنهادی:

شنبه: ریاضی (۲ ساعت)
یکشنبه: فیزیک (۱.۵ ساعت)
دوشنبه: شیمی (۲ ساعت)
سه‌شنبه: ادبیات (۱ ساعت)
چهارشنبه: مرور دروس
پنجشنبه: آزمون آزمایشی
جمعه: استراحت و برنامه‌ریزی
"""
        self.show_message("برنامه هفتگی", schedule)
    
    def set_goal(self, instance):
        """تعیین هدف"""
        self.show_message("تعیین هدف", "🎯 هدف این هفته: ۱۵ ساعت مطالعه\n🎯 هدف این ماه: افزایش ۱۰٪ میانگین نمرات")
    
    def show_resources(self, instance):
        """نمایش منابع آموزشی"""
        resources = """📚 منابع آموزشی مفید:

• کانال‌های یوتیوب:
  - ریاضی: ریاضیات مهدوی
  - فیزیک: فیزیکفا
  - شیمی: شیمی کنکور

• وبسایت‌ها:
  - مکتب‌خونه (maktabkhooneh.org)
  - فرادرس (faradars.org)
  - درسینه (darsineh.com)
"""
        self.show_message("منابع آموزشی", resources)
    
    def show_message(self, title, message):
        """نمایش پیام ساده"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, font_size=14))
        
        btn = Button(text="متوجه شدم", size_hint=(1, 0.2))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.5))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()

class PersianStudyPlannerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        return sm

# اجرای برنامه
if __name__ == '__main__':
    PersianStudyPlannerApp().run()
