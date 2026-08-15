import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
import subprocess
import os
import json
import time
import socket
import threading
import platform as py_platform

# --- CONFIGURATION ---
APP_NAME = "Rmad Pro"
PASS_FILE_NAME = "pass.txt"

# رابط تحديث التطبيق (يمكنك تغييره لاحقاً)
APP_VERSION = "1.0"
UPDATE_URL = "https://github.com/Hassano20/Rmad-App/releases"

class LicenseManager:
    def __init__(self):
        self.device_id = self.get_device_id()
        self.license_file = f"{self.device_id}.lic"
        self.uses = 0
        self.load_license()

    def get_device_id(self):
        # استخدام MAC Address للجهاز ليكون أكثر دقة
        if platform == "android":
            try:
                import uuid
                return str(uuid.getnode())
            except:
                return "ANDROID_DEFAULT"
        return py_platform.node()

    def load_license(self):
        # بيانات الاشتراك الافتراضية
        self.limit_uses = 2
        self.is_valid = True # للتطوير
        self.is_pro = False # افتراضياً مجاني

        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
                    self.uses = data.get('uses', 0)
                    self.is_pro = data.get('is_pro', False)
            except:
                pass

    def save_license(self):
        with open(self.license_file, 'w') as f:
            json.dump({'uses': self.uses, 'is_pro': self.is_pro, 'device': self.device_id}, f)
        self.is_pro = True

    def check_usage(self):
        if not self.is_pro:
            self.uses += 1
            self.save_license()
            if self.uses > self.limit_uses:
                return False
        return True

class WifiToolApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.license_mgr = LicenseManager()
        self.passwords = []
        self.current_pass_index = 0
        self.is_scanning = False
        self.speed = 0.5
        self.file_path = ""
        self.current_ip = "0.0.0.0"
        self.current_ssid = "Unknown"
        
        # Load default passwords
        self.load_pass_file(PASS_FILE_NAME)

    def build(self):
        Window.clearcolor = (0.08, 0.1, 0.15, 1) # Dark Blue Theme
        self.root = BoxLayout(orientation='vertical')
        
        # Create Tabbed Panel
        self.tabbed_panel = TabbedPanel(orientation='ltr')
        
        # Tab 1: Main Hacking Tool
        self.tab_hack = TabbedPanelHeader(text="تخمين وايفي")
        self.tab_hack_content = self.create_hack_tab()
        self.tabbed_panel.add_widget(self.tab_hack)
        self.tabbed_panel.add_widget(self.tab_hack_content)
        
        # Tab 2: Network Scanner
        self.tab_scan = TabbedPanelHeader(text="فحص الشبكة")
        self.tab_scan_content = self.create_scan_tab()
        self.tabbed_panel.add_widget(self.tab_scan)
        self.tabbed_panel.add_widget(self.tab_scan_content)

        self.root.add_widget(self.tabbed_panel)
        
        # Check License & Version
        if not self.license_mgr.is_pro and self.license_mgr.uses >= self.license_mgr.limit_uses:
            self.show_license_popup()
        
        # Check for updates (Mockup)
        Clock.schedule_once(self.check_updates, 2)

        return self.root

    def create_hack_tab(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.lbl_status = Label(text="الحالة: جاهز", font_size='20sp', color=(0.8, 0.8, 0.8, 1), size_hint_y=0.1)
        self.btn_start = Button(text="بدء التخمين", size_hint_y=0.15, font_size='20sp', background_color=(0, 0.7, 0.2, 1))
        self.btn_start.bind(on_press=self.on_start_hacking)
        
        self.btn_load = Button(text="اختيار ملف pass.txt", size_hint_y=0.1, background_color=(0.7, 0.7, 0, 1))
        self.btn_load.bind(on_press=self.show_file_picker)
        
        self.lbl_log = Label(text="سجل العمليات...", halign='center', valign='middle', font_size='14sp')
        
        self.slider_speed = Slider(min=0.1, max=3.0, value=0.5)
        self.slider_speed.bind(value=self.on_speed_change)
        
        self.btn_stop = Button(text="إلغاء", size_hint_y=0.1, background_color=(0.8, 0.2, 0.2, 1))
        self.btn_stop.bind(on_press=self.stop_hacking)
        
        layout.add_widget(self.lbl_status)
        layout.add_widget(self.btn_start)
        layout.add_widget(self.btn_load)
        layout.add_widget(self.lbl_log)
        layout.add_widget(Label(text="السرعة:", size_hint_y=0.05))
        layout.add_widget(self.slider_speed)
        layout.add_widget(self.btn_stop)
        
        return layout

    def create_scan_tab(self):
        # ScrollView for all info
        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', size_hint=(1, None), spacing=10, padding=10)
        layout.bind(minimum_height=self.setter('height'), minimum_width=self.setter('width'))
        
        # Info Cards
        items = [
            ("عنوان IP الخاص بك", "0.0.0.0"),
            ("اسم الشبكة (SSID)", "Unknown"),
            ("قناة الواي فاي (Channel)", "N/A"),
            ("سرعة الإنترنت", "N/A"),
            ("عدد الأجهزة المتصلة", "N/A"),
            ("معدل الخسارة (Packet Loss)", "0%"),
            ("Ping (Ping)", "0ms"),
        ]
        
        self.lbl_info_labels = []
        for title, val in items:
            lbl_title = Label(text=title, font_size='16sp', color=(0, 0.8, 1, 1), size_hint_y=0.1)
            lbl_val = Label(text=val, font_size='20sp', color=(1, 1, 1, 1), size_hint_y=0.1)
            layout.add_widget(lbl_title)
            layout.add_widget(lbl_val)
            self.lbl_info_labels.append((lbl_title, lbl_val))

        self.btn_refresh = Button(text="تحديث البيانات", size_hint_y=0.1, background_color=(0.1, 0.4, 0.8, 1))
        self.btn_refresh.bind(on_press=self.refresh_network_data)
        layout.add_widget(self.btn_refresh)
        
        # Router Buttons
        router_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        btn_192 = Button(text="192.168.1.1", background_color=(0.6, 0, 0, 1))
        btn_10 = Button(text="192.168.0.1", background_color=(0, 0.6, 0, 1))
        btn_1 = Button(text="192.168.1.254", background_color=(0.6, 0.6, 0, 1))
        
        router_layout.add_widget(btn_192)
        router_layout.add_widget(btn_10)
        router_layout.add_widget(btn_1)
        layout.add_widget(router_layout)
        
        scroll.add_widget(layout)
        return scroll

    def show_file_picker(self, *args):
        # File picker logic (simplified for brevity, use standard Kivy FileChooser)
        from kivy.uix.filechooser import FileChooserListView
        filechooser = FileChooserListView(filters=['*.txt'])
        btn = Button(text='تأكيد', size_hint_y=0.2)
        btn.bind(on_press=lambda x: self.load_selected_file(filechooser.selection))
        
        p = Popup(title='اختر ملف', content=FileChooserListView(), size_hint=(0.9, 0.8))
        p.content.add_widget(btn)
        p.open()

    def load_selected_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.load_pass_file(self.file_path)

    def load_pass_file(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.passwords = [line.strip() for line in f if line.strip()]
                self.show_popup("تم", f"تم تحميل {len(self.passwords)} باسورد.")
            else:
                self.show_popup("خطأ", "الملف غير موجود")
        except Exception as e:
            self.show_popup("خطأ", str(e))

    def show_popup(self, title, msg):
        p = Popup(title=title, content=Label(text=msg), size_hint=(0.6, 0.4))
        p.open()

    def show_license_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        lbl = Label(text="لديك 2 استخدام مجاني.\nاشترك الآن!", halign='center', font_size='20sp')
        btn = Button(text="تواصل معنا", size_hint_y=0.2)
        content.add_widget(lbl)
        content.add_widget(btn)
        p = Popup(title="Rmad Pro", content=content, size_hint=(0.7, 0.5))
        p.open()

    def on_speed_change(self, instance, value):
        self.speed = value

    def on_start_hacking(self, instance):
        self.is_scanning = True
        self.current_pass_index = 0
        self.lbl_status.text = "جاري البحث عن الشبكات..."
        self.start_hacking_thread()

    def stop_hacking(self, *args):
        self.is_scanning = False

    def start_hacking_thread(self):
        t = threading.Thread(target=self.hack_loop)
        t.start()

    def hack_loop(self):
        # Get Networks
        networks = self.get_wifi_networks()
        if not networks:
            self.update_log("لم يتم العثور على شبكات")
            return

        for net in networks:
            if not self.is_scanning: break
            ssid = net.get('SSID', 'Unknown')
            self.update_log(f"فحص: {ssid}")
            
            # Check Connection
            if self.is_connected_to_wifi():
                self.update_log("🛑 متصل بشبكة أخرى! يرجى الفصل.")
                time.sleep(2)
                continue

            # Try Password
            self.attempt_connection(ssid)

    def attempt_connection(self, ssid):
        if not self.license_mgr.check_usage():
            self.update_log("انتهت المحاولات المجانية!")
            self.show_license_popup()
            return

        self.update_log(f"جرب: {self.passwords[self.current_pass_index]}")
        
        # Logic to connect and check
        # (Implementation of jnius connection logic goes here)
        # If success:
        # self.show_popup("Success", f"Password: {self.passwords[self.current_pass_index]}")
        # self.license_mgr.save_license()
        
        time.sleep(self.speed)
        self.current_pass_index += 1
        if self.current_pass_index >= len(self.passwords):
            self.update_log("انتهت القائمة.")
            self.is_scanning = False

    def update_log(self, msg):
        Clock.schedule_once(lambda dt: self.lbl_log.text = msg)

    def get_wifi_networks(self):
        # (Standard Kivy jnius implementation)
        return []

    def is_connected_to_wifi(self):
        # (Standard Kivy jnius implementation)
        return False

    def refresh_network_data(self):
        self.update_ip()
        self.update_ping()

    def update_ip(self):
        try:
            # Get public IP
            ip = socket.gethostbyname(socket.gethostname())
            # Note: socket.gethostname usually gets local IP. For public IP, use requests.get('https://api.ipify.org')
            self.current_ip = ip
            self.lbl_info_labels[0][1].text = self.current_ip
        except:
            pass

    def update_ping(self):
        # Simple ping test
        pass

    def check_updates(self, dt):
        # Simple version check
        pass

if __name__ == '__main__':
    WifiToolApp().run()
