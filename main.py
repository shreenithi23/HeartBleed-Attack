import subprocess
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyLayout(FloatLayout):  # Use FloatLayout for full control over positioning
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

        # Create a button to start the attack
        self.start_button = Button(text="Start Attack", size_hint=(None, None), size=(200, 50))
        self.start_button.bind(on_press=self.start_attack)

        # Center the button in the FloatLayout
        self.start_button.pos_hint = {'center_x': 0.5, 'center_y': 0.4}  # Adjust Y position to center it
        self.add_widget(self.start_button)

        # Add a label with custom text for HeartBleed Attack
        self.center_label = Label(text="HeartBleed Attack", font_size='24sp', color=(1, 1, 1, 1),
                                  size_hint=(None, None))  # Let label autosize to fit text
        self.center_label.size = self.center_label.texture_size  # Adjust size to fit the text
        self.center_label.pos_hint = {'center_x': 0.5, 'center_y': 0.6}  # Position above the button
        self.add_widget(self.center_label)


    def start_attack(self, instance):
        # Replace these commands with the actual commands you want to run
        command1 = "python server.py"  # Command for the server
        command2 = "python client.py"   # Command for the client

        # Open the commands in separate Command Prompt windows
        subprocess.Popen(['start', 'cmd', '/k', command1], shell=True)
        subprocess.Popen(['start', 'cmd', '/k', command2], shell=True)

class TheLab(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    TheLab().run()