# TODO: Fix status, make prettier

import os
import sys
import time
from flask import Response
import webbrowser
from threading import Timer

from flask import Flask
from flask import request
import anki_vector
import json
from anki_vector import audio
from anki_vector.connection import ControlPriorityLevel
from anki_vector.util import degrees

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

app = Flask(__name__, static_url_path='/static')

args = anki_vector.util.parse_command_args()

serialnumber = "00e20145"


@app.route('/api/say')
def say_text():
    text = request.args.get('text')

    if not text:
        return "text required"

    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text(text)

    return "executed"


@app.route('/api/volume/<level>', methods=['POST'])
def set_volume(level):
    if int(level) < 0 or int(level) > 4:
        return "level should be from 0 to 4"

    levels = {
        0: audio.RobotVolumeLevel.LOW,
        1: audio.RobotVolumeLevel.MEDIUM_LOW,
        2: audio.RobotVolumeLevel.MEDIUM,
        3: audio.RobotVolumeLevel.MEDIUM_HIGH,
        4: audio.RobotVolumeLevel.HIGH,
    }

    lavels_labels = {
        0: "low",
        1: "medium low",
        2: "medium",
        3: "medium high",
        4: "high",
    }

    pic_labels = {
        0: "low",
        1: "mediumlow",
        2: "medium",
        3: "mediumhigh",
        4: "high",
    }

    with anki_vector.Robot(args.serial) as robot:
        robot.audio.set_master_volume(levels[int(level)])
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "volumefacepics", pic_labels[int(level)] + ".jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        robot.behavior.say_text("Volume set to " + lavels_labels[int(level)])
        time.sleep(duration_s)

    return "Volume set to " + lavels_labels[int(level)]


@app.route('/api/battery')
def get_battery_state():
    with anki_vector.Robot(args.serial, behavior_control_level=None) as robot:
        print("Connecting to a cube...")
        # robot.world.connect_cube()
        battery_state = robot.get_battery_state()
        if battery_state:
            response = {}

            response['robot'] = {
                'volts': battery_state.battery_volts,
                'level': battery_state.battery_level,
                'is_charging': battery_state.is_charging,
                'is_on_charger_platform': battery_state.is_on_charger_platform,
                'suggested_charger_sec': battery_state.suggested_charger_sec,
            }
            # response['cube'] = {
            #     'volts': battery_state.cube_battery.battery_volts,
            #     'level': battery_state.cube_battery.level,
            #     'time_since_last_reading_sec': battery_state.cube_battery.time_since_last_reading_sec,
            #     'factory_id': battery_state.cube_battery.factory_id,
            # }

    return Response((json.dumps(response)), mimetype='application/json')


@app.route('/api/behavior/drive_on_charger')
def behavior_drive_on_charger():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.drive_on_charger()

    return "executed"

@app.route('/')
def main_page():
    return """
<html>
  <head>
  </head>
<style>
.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  padding: 12px 16px;
  z-index: 1;
}

.dropdown:hover .dropdown-content {
  display: block;
}
</style>
<body>
<h1>Vector API</h1>
<hr>
<h2>Status</h2>
<div id="root"></div>
<button onclick="getVicstatus()">Get Status</button>
<button onClick="window.location.reload();">Clear (refresh page)</button>
<hr>
<h2>Set Volume</h2>
<div class="dropdown">
  <button class="dropbtn">Hover Over This</button>
  <div class="dropdown-content">
  <ul>
<li><form method="post" action="/api/volume/0" target="hiddenFrame">
  <button type="submit">Low</button>
</form></li>
<li><form method="post" action="/api/volume/1" target="hiddenFrame">
  <button type="submit">Medium Low</button>
</form></li>
<li><form method="post" action="/api/volume/2" target="hiddenFrame">
  <button type="submit">Medium</button>
</form></li>
<li><form method="post" action="/api/volume/3" target="hiddenFrame">
  <button type="submit">Medium High</button>
</form></li>
<li><form method="post" action="/api/volume/4" target="hiddenFrame"> 
  <button type="submit">High</button>
</form></li>
  </ul>
  </div>
</div>
<hr>
<h2>Set Locale</h2>
<div class="dropdown">
  <button class="dropbtn">Hover Over This</button>
  <div class="dropdown-content">
  <ul>
<li><form method="post" action="/api/locale/enUS" target="hiddenFrame"> 
  <button type="submit">English (US)</button>
</form></li>
<li><form method="post" action="/api/locale/deDE" target="hiddenFrame"> 
  <button type="submit">German</button>
</form></li>
<li><form method="post" action="/api/locale/frFR" target="hiddenFrame"> 
  <button type="submit">French</button>
</form></li>
<li><form method="post" action="/api/locale/jaJP" target="hiddenFrame"> 
  <button type="submit">Japanese</button>
</form></li>
  </ul>
  </div>
</div>
<hr>
<h2>Set Button</h2>
<form method="post" action="/api/settings/button/alexa" target="hiddenFrame"> 
  <button type="submit">Alexa</button>
</form>
<form method="post" action="/api/settings/button/heyvector" target="hiddenFrame">
  <input type="hidden"/> 
  <button type="submit">Hey Vector</button>
</form>
<hr>
<h2>Set Temp</h2>
<form method="post" action="/api/settings/temp/f" target="hiddenFrame">
  <button type="submit">Fahrenheit</button>
</form>
<form method="post" action="/api/settings/temp/c" target="hiddenFrame">
  <button type="submit">Celcius</button>
</form>
<hr>
<h2>Set Units</h2>
<form method="post" action="/api/settings/units/metric" target="hiddenFrame"> 
  <button type="submit">Metric</button>
</form>
<form method="post" action="/api/settings/units/imperial" target="hiddenFrame"> 
  <button type="submit">Imperial</button>
</form>
<hr>
<h2>Set Time</h2>
<form method="post" action="/api/settings/time/24" target="hiddenFrame"> 
  <button type="submit">24 Hour</button>
</form>
<form method="post" action="/api/settings/time/12" target="hiddenFrame"> 
  <button type="submit">12 Hour</button>
</form>
<hr>
<h2>Set Location</h2>
<form method="POST" action="/api/settings/location" target="hiddenFrame">
    <input name="text">
    <input type="submit" placeholder="Put text here">
    <small>Location (ex. San Francisco, California, United States of America)</small>
</form>
<form method="POST" action="/api/settings/timezone" target="hiddenFrame">
    <input name="text">
    <input type="submit" placeholder="Put text here">
    <small>Time Zone (ex. America/Los_Angeles)</small>
</form>
<hr>
</h2>
<h2>Set Eye Color</h2>

<div class="dropdown">
  <button class="dropbtn">Hover Over This</button>
  <div class="dropdown-content">
  <ul>
<li><form method="post" action="/api/settings/eyecolor/0" target="hiddenFrame"> 
  <button type="submit">Teal</button>
</form></li>
<li><form method="post" action="/api/settings/eyecolor/1" target="hiddenFrame"> 
  <button type="submit">Orange</button>
</form></li>
<li><form method="post" action="/api/settings/eyecolor/2" target="hiddenFrame"> 
  <button type="submit">Yellow</button>
</form></li>
<li><form method="post" action="/api/settings/eyecolor/3" target="hiddenFrame"> 
  <button type="submit">Lime Green</button>
</form></li>
<li><form method="post" action="/api/settings/eyecolor/4" target="hiddenFrame"> 
  <button type="submit">Azure Blue</button>
</form></li>
<li><form method="post" action="/api/settings/eyecolor/5" target="hiddenFrame"> 
  <button type="submit">Purple</button>
</form></li>
<li><form method="post" action="/api/settings/eyecolor/6" target="hiddenFrame"> 
  <button type="submit">Matrix Green/White</button>
</form></li>
  </ul>
  </div>
</div>
<hr>
<h2>TTS</h2>
<form method="POST" action="/api/say/" target="hiddenFrame">
    <input name="text">
    <input type="submit" placeholder="Put text here">
</form>
<hr>
<h2>Actions</h2>
<form method="POST" action="/api/intents/explore_start" target="hiddenFrame">
  <button type="submit">Explore Start</button>
</form>
<form method="POST" action="/api/intents/listen_beat" target="hiddenFrame">
  <button type="submit">Listen for Beat</button>
</form>
<form method="POST" action="/api/intents/sleep" target="hiddenFrame">
  <button type="submit">Go to Sleep</button>
</form>
<form method="POST" action="/api/intents/goodnight" target="hiddenFrame">
  <button type="submit">Goodnight</button>
</form>
<hr>
<h2>BlackJack</h2>
<form method="POST" action="/api/intents/play_blackjack" target="hiddenFrame">
  <button type="submit">Play Blackjack</button>
</form>
<form method="POST" action="/api/intents/blackjack_hit" target="hiddenFrame">
  <button type="submit">Hit</button>
</form>
<form method="POST" action="/api/intents/blackjack_stand" target="hiddenFrame">
  <button type="submit">Stand</button>
</form>
<form method="POST" action="/api/intents/blackjack_playagain" target="hiddenFrame">
  <button type="submit">Play Again</button>
</form>
<form method="POST" action="/api/intents/negative" target="hiddenFrame">
  <button type="submit">Don't Play Again</button>
</form>
<hr>
<h2>All App Intents</h2>
<div class="dropdown">
  <button class="dropbtn">Hover Over This</button>
  <div class="dropdown-content">
<!--Listing Manually.-->
  <ul>
<li><form method="post" action="/api/intents/signout_alexa" target="hiddenFrame"> 
  <button type="submit">Signout Alexa</button>
</form></li>
<li><form method="post" action="/api/intents/signin_alexa" target="hiddenFrame"> 
  <button type="submit">Signin Alexa</button>
</form></li>
<li><form method="post" action="/api/intents/do_trick" target="hiddenFrame"> 
  <button type="submit">Do Trick</button>
</form></li>
<li><form method="post" action="/api/intents/play_game" target="hiddenFrame"> 
  <button type="submit">Play Game</button>
</form></li>
<li><form method="post" action="/api/intents/play_blackjack" target="hiddenFrame"> 
  <button type="submit">Play BlackJack</button>
</form></li>
<li><form method="post" action="/api/intents/fistbump" target="hiddenFrame"> 
  <button type="submit">Fistbump</button>
</form></li>
<li><form method="post" action="/api/intents/pickup_cube" target="hiddenFrame"> 
  <button type="submit">Pickup Cube</button>
</form></li>
<li><form method="post" action="/api/intents/pop_a_wheelie" target="hiddenFrame"> 
  <button type="submit">Pop A Wheelie</button>
</form></li>
<li><form method="post" action="/api/intents/roll_cube" target="hiddenFrame"> 
  <button type="submit">Roll Cube</button>
</form></li>
<li><form method="post" action="/api/intents/be_quiet" target="hiddenFrame"> 
  <button type="submit">Be Quiet</button>
</form></li>
<li><form method="post" action="/api/intents/shutup" target="hiddenFrame"> 
  <button type="submit">Shut Up</button>
</form></li>
<li><form method="post" action="/api/intents/come_here" target="hiddenFrame"> 
  <button type="submit">Come Here</button>
</form></li>
<li><form method="post" action="/api/intents/listen_beat" target="hiddenFrame"> 
  <button type="submit">Listen Beat</button>
</form></li>
<li><form method="post" action="/api/intents/affirmative" target="hiddenFrame"> 
  <button type="submit">Affirmative</button>
</form></li>
<li><form method="post" action="/api/intents/negative" target="hiddenFrame"> 
  <button type="submit">Negative</button>
</form></li>
<li><form method="post" action="/api/intents/praise" target="hiddenFrame"> 
  <button type="submit">Praise</button>
</form></li>
<li><form method="post" action="/api/intents/apology" target="hiddenFrame"> 
  <button type="submit">Apology</button>
</form></li>
<li><form method="post" action="/api/intents/scold" target="hiddenFrame"> 
  <button type="submit">Scold</button>
</form></li>
<li><form method="post" action="/api/intents/love" target="hiddenFrame"> 
  <button type="submit">Love</button>
</form></li>
<li><form method="post" action="/api/intents/abuse" target="hiddenFrame"> 
  <button type="submit">Abuse</button>
</form></li>
<li><form method="post" action="/api/intents/goodbye" target="hiddenFrame"> 
  <button type="submit">Goodbye</button>
</form></li>
<li><form method="post" action="/api/intents/good_morning" target="hiddenFrame"> 
  <button type="submit">Good Morning</button>
</form></li>
<li><form method="post" action="/api/intents/goodnight" target="hiddenFrame"> 
  <button type="submit">Goodnight</button>
</form></li>
<li><form method="post" action="/api/intents/check_timer" target="hiddenFrame"> 
  <button type="submit">Check Timer</button>
</form></li>
<li><form method="post" action="/api/intents/show_time" target="hiddenFrame"> 
  <button type="submit">Show Time</button>
</form></li>
<li><form method="post" action="/api/intents/take_photo" target="hiddenFrame"> 
  <button type="submit">Take Photo</button>
</form></li>
<li><form method="post" action="/api/intents/go_home" target="hiddenFrame"> 
  <button type="submit">Go Home</button>
</form></li>
<li><form method="post" action="/api/intents/sleep" target="hiddenFrame"> 
  <button type="submit">Sleep</button>
</form></li>
<li><form method="post" action="/api/intents/explore_start" target="hiddenFrame"> 
  <button type="submit">Explore Start</button>
</form></li>
<li><form method="post" action="/api/intents/knowledge_question" target="hiddenFrame"> 
  <button type="submit">KG Question</button>
</form></li>
<li><form method="post" action="/api/intents/knowledge_unknown" target="hiddenFrame"> 
  <button type="submit">KG Unknown</button>
</form></li>
<li><form method="post" action="/api/intents/blackjack_hit" target="hiddenFrame"> 
  <button type="submit">Blackjack Hit</button>
</form></li>
<li><form method="post" action="/api/intents/blackjack_stand" target="hiddenFrame"> 
  <button type="submit">Blackjack Stand</button>
</form></li>
<li><form method="post" action="/api/intents/blackjack_playagain" target="hiddenFrame"> 
  <button type="submit">Play Again</button>
</form></li>
<li><form method="post" action="/api/intents/look_at_me" target="hiddenFrame"> 
  <button type="submit">Look At Me</button>
</form></li>
<li><form method="post" action="/api/intents/find_cube" target="hiddenFrame"> 
  <button type="submit">Find Cube</button>
</form></li>
<li><form method="post" action="/api/intents/what_is_name" target="hiddenFrame"> 
  <button type="submit">What Is Name</button>
</form></li>
<li><form method="post" action="/api/intents/volume_up" target="hiddenFrame"> 
  <button type="submit">Volume Up</button>
</form></li>
<li><form method="post" action="/api/intents/volume_down" target="hiddenFrame"> 
  <button type="submit">Volume Down</button>
</form></li>
<li><form method="post" action="/api/intents/move_backwards" target="hiddenFrame"> 
  <button type="submit">Move Backwards</button>
</form></li>
<li><form method="post" action="/api/intents/turn_left" target="hiddenFrame"> 
  <button type="submit">Turn Left</button>
</form></li>
<li><form method="post" action="/api/intents/turn_right" target="hiddenFrame"> 
  <button type="submit">Turn Right</button>
</form></li>
<li><form method="post" action="/api/intents/turn_around" target="hiddenFrame"> 
  <button type="submit">Turn Around</button>
</form></li>
<li><form method="post" action="/api/intents/happy_new_year" target="hiddenFrame"> 
  <button type="submit">Happy New Year</button>
</form></li>
<li><form method="post" action="/api/intents/happy_holidays" target="hiddenFrame"> 
  <button type="submit">Happy Holidays</button>
</form></li>
<li><form method="post" action="/api/intents/robot_age" target="hiddenFrame"> 
  <button type="submit">Robot Age</button>
</form></li>
<li><form method="post" action="/api/intents/eye_color" target="hiddenFrame"> 
  <button type="submit">Eye Color</button>
</form></li>
  </ul>
  </div>
</div>
<hr>
<h2>Intents with Param (needs SDK mods)</h2>
<form method="POST" action="/api/meetvictor/" target="hiddenFrame">
    <input name="text">
    <input type="submit" placeholder="Put text here">
    <small>Meet Victor (name)</small>
</form>
<hr>
</body>
</html>

   <script>
var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}
   </script>
   <script>
function getVicstatus() {
   const app = document.getElementById('root')
   
   var client = new HttpClient();
client.get('/api/fancy/status', function(response) {

          var data = JSON.parse(response)

          const h3 = document.createElement('h3')
          h3.textContent = data.status

          app.appendChild(h3)
});
}
   </script>

<iframe name="hiddenFrame" width="0" height="0" border="0" style="display: none;"></iframe>
"""

    return "executed"

@app.route('/api/say/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    if not processed_text:
        return "text required"

    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text(processed_text)

    return "executed"


@app.route('/api/locale/frFR', methods=['POST'])
def locale_french():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='fr_FR')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "localefacepics", "fr_FR.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/locale/jaJP', methods=['POST'])
def locale_japanese():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='ja_JP')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "localefacepics", "ja_JP.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"


@app.route('/api/locale/deDE', methods=['POST'])
def locale_german():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='de_DE')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "localefacepics", "de_DE.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/locale/enUS', methods=['POST'])
def locale_englishus():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='en_US')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "localefacepics", "en_US.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/action/goodnight', methods=['POST'])
def action_goodnight():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.drive_on_charger()
        
    with anki_vector.Robot(behavior_control_level=None) as robot:
        robot.behavior.app_intent(intent='intent_system_sleep')
        
    return "executed"


@app.route('/api/intents/<intentt>', methods=['POST'])
def intent_specific(intentt):
    with anki_vector.Robot(args.serial, behavior_control_level=None) as robot:
        robot.behavior.app_intent(intent=intentt)
    return "executed"

@app.route('/api/settings/button/alexa', methods=['POST'])
def button_alexa():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'button_wakeword':1})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "alexab.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/button/heyvector', methods=['POST'])
def button_vector():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'button_wakeword':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "heyvectorb.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/temp/c', methods=['POST'])
def temp_celcius():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'temp_is_fahrenheit':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "tempc.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/temp/f', methods=['POST'])
def temp_fahrenheit():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'temp_is_fahrenheit':1})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "tempf.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/eyecolor/0', methods=['POST'])
def set_eye_color_0():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'eye_color':0})
    return "executed"

@app.route('/api/settings/eyecolor/1', methods=['POST'])
def set_eye_color_1():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'eye_color':1})
    return "executed"

@app.route('/api/settings/eyecolor/2', methods=['POST'])
def set_eye_color_2():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'eye_color':2})
    return "executed"

@app.route('/api/settings/eyecolor/3', methods=['POST'])
def set_eye_color_3():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'eye_color':3})
    return "executed"

@app.route('/api/settings/eyecolor/4', methods=['POST'])
def set_eye_color_4():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'eye_color':4})
    return "executed"

@app.route('/api/settings/eyecolor/5', methods=['POST'])
def set_eye_color_5():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'eye_color':5})
    return "executed"

@app.route('/api/settings/eyecolor/6', methods=['POST'])
def set_eye_color_6():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'eye_color':6})
    return "executed"

@app.route('/api/settings/units/metric', methods=['POST'])
def unit_metric():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'dist_is_metric':1})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "metric.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/units/imperial', methods=['POST'])
def unit_imperial():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'dist_is_metric':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "imperial.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/location', methods=['POST'])
def location_string():
    text = request.form['text']
    if not text:
        return "text required"
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'default_location':str(text)})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "location.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/timezone', methods=['POST'])
def time_zone():
    text = request.form['text']
    if not text:
        return "text required"
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'time_zone':str(text)})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "timezone.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/time/24', methods=['POST'])
def time_24():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'clock_24_hour':1})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "24hour.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/time/12', methods=['POST'])
def time_12():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'clock_24_hour':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "settingsfacepics", "12hour.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 3.0
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/meetvictor', methods=['POST'])
def intent_meetvictor():
    text = request.form['text']
    if not text:
        return "text required"
    
    with anki_vector.Robot(args.serial, behavior_control_level=None) as robot:
        robot.behavior.app_intent('meet_victor', text)
    return "executed"


@app.route('/api/animation/list')
def animation_list():
    with anki_vector.AsyncRobot(args.serial, behavior_control_level=None) as robot:
        anim_request = robot.anim.load_animation_list()
        anim_request.result()
        anim_names = robot.anim.anim_list
    return str(json.dumps(anim_names))


# @TODO should be post
@app.route('/api/animation/<animation_id>')
def animation_play(animation_id):
    with anki_vector.Robot(args.serial) as robot:
        robot.anim.play_animation(animation_id)
    return "executed"


@app.route('/api/animation-trigger/list')
def animation_trigger_list():
    with anki_vector.AsyncRobot(args.serial, behavior_control_level=None) as robot:
        anim_trigger_request = robot.anim.load_animation_trigger_list()
        anim_trigger_request.result()
        anim_trigger_names = robot.anim.anim_trigger_list
    return Response((json.dumps(anim_trigger_names)), mimetype='application/json')


# @TODO should be post
@app.route('/api/animation-trigger/<animation_id>')
def animation_trigger_play(animation_id):
    with anki_vector.Robot(args.serial) as robot:
        robot.anim.play_animation_trigger(animation_id)
    return "executed"


@app.route('/api/status/')
def get_status():
    current_states = []

    with anki_vector.Robot(args.serial, behavior_control_level=None) as robot:

        if robot.status.is_on_charger: current_states.append("is_on_charger")
        if robot.status.are_motors_moving: current_states.append("are_motors_moving")
        if robot.status.are_wheels_moving: current_states.append("are_wheels_moving")
        if robot.status.is_animating: current_states.append("is_animating")
        if robot.status.is_being_held: current_states.append("is_being_held")
        if robot.status.is_button_pressed: current_states.append("is_button_pressed")
        if robot.status.is_carrying_block: current_states.append("is_carrying_block")
        if robot.status.is_charging: current_states.append("is_charging")
        if robot.status.is_cliff_detected: current_states.append("is_cliff_detected")
        if robot.status.is_docking_to_marker: current_states.append("is_docking_to_marker")
        if robot.status.is_falling: current_states.append("is_falling")
        if robot.status.is_head_in_pos: current_states.append("is_head_in_pos")
        if robot.status.is_in_calm_power_mode: current_states.append("is_in_calm_power_mode")
        if robot.status.is_lift_in_pos: current_states.append("is_lift_in_pos")
        if robot.status.is_pathing: current_states.append("is_pathing")
        if robot.status.is_picked_up: current_states.append("is_picked_up")
        if robot.status.is_robot_moving: current_states.append("is_robot_moving")
    return Response((json.dumps(current_states)), mimetype='application/json')


@app.route('/api/fancy/gitlab-build-finished')
def fancy_gitlab_build_success():
    robot = anki_vector.Robot(args.serial)
    robot.connect()

    robot.anim.play_animation_trigger("ReactToTriggerWordOffChargerFrontLeft")
    robot.screen.set_screen_to_color(anki_vector.color.Color(rgb=[50, 119, 168]), duration_sec=6.0)
    robot.behavior.say_text("Gitlab build finished, check your app.")
    robot.disconnect()
    return "executed"


@app.route('/api/fancy/status')
def fancy_status():
    response = {}
    robot = anki_vector.Robot(args.serial, behavior_control_level=None)
    robot.connect()

    if robot.status.is_charging:
        response['status'] = 'Charging'
    if robot.status.is_robot_moving and robot.status.are_wheels_moving:
        response['status'] = 'Exploring'
    if robot.status.is_on_charger \
            and robot.status.is_head_in_pos \
            and robot.status.is_in_calm_power_mode \
            and robot.status.is_lift_in_pos:
        response['status'] = 'Sleeping'
    if robot.status.is_on_charger \
            and robot.status.is_animating \
            and robot.status.is_charging \
            and robot.status.is_head_in_pos \
            and robot.status.is_lift_in_pos:
        response['status'] = 'Charging/Observing'
    if robot.status.is_animating \
            and robot.status.is_head_in_pos \
            and robot.status.is_lift_in_pos:
        response['status'] = 'Observing off Charger'
    if robot.status.is_on_charger \
            and robot.status.is_animating \
            and robot.status.is_head_in_pos \
            and robot.status.is_lift_in_pos:
        response['status'] = 'Observing on Charger'
    if robot.status.is_animating \
            and robot.status.is_head_in_pos \
            and robot.status.is_lift_in_pos \
            and robot.status.is_robot_moving:
        response['status'] = 'Exploring'
    if robot.status.are_motors_moving \
            and robot.status.is_robot_moving:
        response['status'] = 'Exploring'
    if robot.status.is_animating \
            and robot.status.is_cliff_detected \
            and robot.status.is_head_in_pos \
            and robot.status.is_in_calm_power_mode \
            and robot.status.is_lift_in_pos:
        response['status'] = 'Stuck on edge'

    robot.disconnect()

    return Response(json.dumps(response), mimetype='application/json')

def open_browser():
      webbrowser.open_new('http://localhost:5000/')


if __name__ == '__main__':
    Timer(0, open_browser).start();
    app.run(debug=False, host='0.0.0.0')
