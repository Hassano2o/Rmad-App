cat > main.py << 'EOF'
import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
import subprocess
import os
import json
import time
import threading

# --- CONFIGURATION ---
APP_NAME = "Rmad"
PASS_FILE_NAME = "pass.txt"
DEFAULT_PASS_FILE = "pass.txt"

class LicenseManager:
    def __init__(self):
        self.device_id = self.get_device_id()
        self.license_file = f"{self.device_id}.lic"
        self.load_license()

    def get_device_id(self):
        if platform == "android":
            try:
                import uuid
                return str(uuid.getnode())
            except:
                return "ANDROID_DEFAULT"
        elif platform == "ios":
            return "IOS_DEFAULT"
        else:
            return "PC_DEFAULT"

    def load_license(self):
        if os.path.exists(self.license_file):
            with open(self.license_file, 'r') as f:
                try:
                    data = json.load(f)
                    if time.time() < data.get('expiry', 0):
                        self.is_valid = True
                    else:
                        self.is_valid = False
                except:
                    self.is_valid = False
        else:
            self.is_valid = False

    def save_license(self):
        expiry = time.time() + (365 * 24 * 60 * 60)
        with open(self.license_file, 'w') as f:
            json.dump({'expiry': expiry, 'device': self.device_id}, f)
        self.is_valid = True

class RmadApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.license_mgr = LicenseManager()
        self.passwords = []
        self.current_pass_index = 0
        self.is_scanning = False
        self.is_testing = False
        self.speed = 0.5
        self.file_path = ""
        self.load_pass_file(DEFAULT_PASS_FILE)

    def load_pass_file(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    self.passwords = [line.strip() for line in f if line.strip()]
                self.return_to_main()
                self.show_popup("تم التحميل", f"تم تحميل {len(self.passwords)} باسورد.")
            else:
                self.show_popup("خطأ", "الملف غير موجود")
        except Exception as e:
            self.show_popup("خطأ", str(e))

    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)
        self.root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.title_lbl = Label(text=APP_NAME, font_name='Roboto-Bold', font_size='30sp', color=(0, 0.8, 1, 1))
        self.root.add_widget(self.title_lbl)
        
        self.menu_layout = BoxLayout(orientation='vertical', size_hint_y=0.8)
        self.btn_start = Button(text="بدء الاختبار", size_hint_y=0.2, font_size='20sp', background_color=(0.1, 0.6, 0.1, 1))
        self.btn_start.bind(on_press=self.on_start)
        
        self.btn_load = Button(text="اختيار ملف pass.txt", size_hint_y=0.2, font_size='20sp', background_color=(0.6, 0.6, 0, 1))
        self.btn_load.bind(on_press=self.show_file_picker)
        
        self.lbl_status = Label(text="الحالة: جاهز", font_size='18sp', color=(1, 1, 1, 1))
        
        self.menu_layout.add_widget(self.btn_start)
        self.menu_layout.add_widget(self.btn_load)
        self.menu_layout.add_widget(self.lbl_status)
        
        self.root.add_widget(self.menu_layout)

        self.test_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 0.9))
        self.test_layout.visible = False
        
        self.lbl_network = Label(text="الشبكة: --", font_size='20sp', color=(0.5, 0.5, 1, 1))
        self.lbl_pass = Label(text="الباسورد: --", font_size='20sp', color=(1, 0.5, 0, 1))
        self.lbl_log = Label(text="", halign='center', font_size='16sp')
        
        self.slider_speed = Slider(min=0.1, max=2.0, value=0.5, size_hint=(1, 0.2))
        self.slider_speed.bind(value=self.on_speed_change)
        self.lbl_speed = Label(text="السرعة: متوسطة", size_hint=(1, 0.1))
        
        self.btn_stop = Button(text="إلغاء", size_hint=(1, 0.1), background_color=(0.8, 0.2, 0.2, 1))
        self.btn_stop.bind(on_press=self.stop_testing)
        
        self.test_layout.add_widget(self.lbl_network)
        self.test_layout.add_widget(self.lbl_pass)
        self.test_layout.add_widget(self.lbl_log)
        self.test_layout.add_widget(self.slider_speed)
        self.test_layout.add_widget(self.lbl_speed)
        self.test_layout.add_widget(self.btn_stop)
        
        self.root.add_widget(self.test_layout)
        
        if not self.license_mgr.is_valid:
            self.show_license_popup()

        return self.root

    def show_license_popup(self):
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        lbl = Label(text="لديك 2 محاولات مجانية.\nللنسخة الكاملة تواصل معنا", font_size='20sp', halign='center')
        btn_telegram = Button(text="تواصل تيليجرام", background_color=(0, 0.5, 0.8, 1), size_hint_y=0.3)
        btn_whatsapp = Button(text="تواصل واتساب", background_color=(0.1, 0.6, 0.1, 1), size_hint_y=0.3)
        
        btn_telegram.bind(on_press=lambda x: self.open_url("https://t.me/h1x1o"))
        btn_whatsapp.bind(on_press=lambda x: self.open_url("https://wa.me/9647710016157"))
        
        content.add_widget(lbl)
        content.add_widget(btn_telegram)
        content.add_widget(btn_whatsapp)
        
        p = Popup(title="نسخة Rmad", content=content, size_hint=(0.8, 0.6))
        p.open()

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def show_file_picker(self, *args):
        filechooser = FileChooserListView(filters=['*.txt'])
        btn = Button(text='اختيار', size_hint_y=0.2)
        btn.bind(on_press=lambda x: self.load_selected_file(filechooser.selection))
        
        layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(filechooser)
        layout.add_widget(btn)
        
        p = Popup(title='اختر ملف pass.txt', content=layout, size_hint=(0.9, 0.8))
        p.bind(on_open=lambda x: filechooser.focus = filechooser)
        p.open()

    def load_selected_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.load_pass_file(self.file_path)

    def show_popup(self, title, msg):
        p = Popup(title=title, content=Label(text=msg), size_hint=(0.6, 0.4))
        p.open()

    def on_speed_change(self, instance, value):
        self.speed = value
        self.lbl_speed.text = f"السرعة: {value:.1f} ثانية"

    def on_start(self, instance):
        self.is_scanning = True
        self.lbl_status.text = "جاري البحث عن الشبكات..."
        self.switch_to_test_view()
        
        t = threading.Thread(target=self.scan_and_test)
        t.start()

    def switch_to_test_view(self):
        self.menu_layout.visible = False
        self.test_layout.visible = True

    def return_to_main(self):
        self.menu_layout.visible = True
        self.test_layout.visible = False
        self.is_scanning = False
        self.is_testing = False

    def stop_testing(self, *args):
        self.is_testing = False
        self.return_to_main()

    def scan_and_test(self):
        networks = self.get_wifi_networks()
        if not networks:
            self.show_popup("خطأ", "لا توجد شبكات وايفي")
            self.return_to_main()
            return

        for net in networks:
            if not self.is_scanning:
                break
            
            ssid = net.get('SSID', 'Unknown')
            
            if self.is_connected_to_wifi():
                self.update_log(f"🛑 متصل بشبكة: {ssid}\nيجب فصل الواي فاي!")
                time.sleep(2)
                continue

            self.test_network(ssid)

    def get_wifi_networks(self):
        networks = []
        if platform == "android":
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                WifiManager = autoclass('android.net.wifi.WifiManager')
                
                wm = PythonActivity.mActivity.getSystemService(Context.WIFI_SERVICE)
                info = wm.getConnectionInfo()
                if info:
                    ssid = info.getSSID()
                    if ssid:
                        ssid = ssid.strip('"')
                        networks.append({'SSID': ssid, 'BSSID': info.getBSSID()})
                
                wm.startScan()
                results = wm.getScanResults()
                for i in range(results.size()):
                    res = results.get(i)
                    networks.append({'SSID': res.getSSID().strip('"'), 'BSSID': res.getBSSID()})
            except Exception as e:
                self.update_log(f"Scan Error: {str(e)}")
        else:
            pass
        return networks

    def is_connected_to_wifi(self):
        if platform == "android":
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                WifiManager = autoclass('android.net.wifi.WifiManager')
                wm = PythonActivity.mActivity.getSystemService(Context.WIFI_SERVICE)
                info = wm.getConnectionInfo()
                return info is not None
            except:
                return False
        return False

    def test_network(self, ssid):
        self.is_testing = True
        self.update_log(f"📡 جرب الاتصال بـ: {ssid}")
        
        self.connect_to_wifi(ssid)
        time.sleep(self.speed)
        
        try:
            if platform == "android":
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Context = autoclass('android.content.Context')
                ConnectivityManager = autoclass('android.net.ConnectivityManager')
                cm = PythonActivity.mActivity.getSystemService(Context.CONNECTIVITY_SERVICE)
                network = cm.getActiveNetworkInfo()
                connected = network is not None and network.isConnected()
                
                if connected:
                    self.show_popup("🎉 نجاح!", f"تم الاتصال بـ {ssid} بنجاح!\nالباسورد: {self.passwords[self.current_pass_index]}")
                    self.license_mgr.save_license()
                    self.update_log(f"✅ Found: {self.passwords[self.current_pass_index]} for {ssid}")
                    self.return_to_main()
                    return
                else:
                    self.update_log(f"❌ Failed: {self.passwords[self.current_pass_index]}")
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', '8.8.8.8'], stdout=subprocess.DEVNULL)
                if result.returncode == 0:
                    self.show_popup("🎉 Success!", f"Connected to {ssid}! Password: {self.passwords[self.current_pass_index]}")
                    return
                else:
                    self.update_log(f"❌ Fail: {self.passwords[self.current_pass_index]}")
        except Exception as e:
            self.update_log(f"Error: {str(e)}")

        self.disconnect_wifi()
        self.current_pass_index += 1
        if self.current_pass_index >= len(self.passwords):
            self.show_popup("انتهت القائمة", "انتهت جميع الباسوردات")
            self.return_to_main()
            return

        time.sleep(0.5)

    def connect_to_wifi(self, ssid):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            WifiManager = autoclass('android.net.wifi.WifiManager')
            wm = PythonActivity.mActivity.getSystemService(Context.WIFI_SERVICE)
            
            wm.setWifiEnabled(False)
            time.sleep(1)
            wm.setWifiEnabled(True)
        except Exception as e:
            self.update_log(f"Connect Error: {str(e)}")

    def disconnect_wifi(self):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            WifiManager = autoclass('android.net.wifi.WifiManager')
            wm = PythonActivity.mActivity.getSystemService(Context.WIFI_SERVICE)
            wm.setWifiEnabled(False)
            time.sleep(1)
            wm.setWifiEnabled(True)
        except:
            pass

    def update_log(self, msg):
        Clock.schedule_once(lambda dt: self.lbl_log.text = msg)

if __name__ == '__main__':
    RmadApp().run()
EOF
