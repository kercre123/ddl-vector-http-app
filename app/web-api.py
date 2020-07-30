# TODO: Fix status, make prettier

import os
import sys
import time
import webbrowser
from threading import Timer
from flask import Flask, request, Response, render_template
import anki_vector
import json
from anki_vector import audio
from anki_vector.connection import ControlPriorityLevel
from anki_vector.util import degrees

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")

app = Flask(__name__, static_url_path='', static_folder='resources/webstuff/static', template_folder='resources/webstuff/templates')

args = anki_vector.util.parse_command_args()


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
        image_path = os.path.join(current_directory, "resources", "volumefacepics", pic_labels[int(level)] + ".jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        robot.behavior.say_text("Volume set to " + lavels_labels[int(level)])
        time.sleep(duration_s)

    return "Volume set to " + lavels_labels[int(level)]

# soon to be used
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


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/api/say', methods=['POST'])
def say_text_post():
    text = request.form['text']
    processed_text = text.upper()
    if not processed_text:
        return "text required"

    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text(processed_text)

    return "executed"

@app.route('/api/extras/chatterbot', methods=['POST'])
def chatterbot():
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer
    chatbot = ChatBot("Vector")
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train(
        "chatterbot.corpus.english"
    )
    text = request.form['text']
    processed_text = text.upper()
    if not processed_text:
        return "text required"

    chatter_response = chatbot.get_response(processed_text)

    parsed_response = f'"{chatter_response}"'

    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.say_text(parsed_response)

    return 'executed'

@app.route('/api/locale/frFR', methods=['POST'])
def locale_french():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='fr_FR')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "localefacepics", "fr_FR.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/locale/jaJP', methods=['POST'])
def locale_japanese():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='ja_JP')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "localefacepics", "ja_JP.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"


@app.route('/api/locale/deDE', methods=['POST'])
def locale_german():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='de_DE')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "localefacepics", "de_DE.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/locale/enUS', methods=['POST'])
def locale_englishus():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.change_locale(locale='en_US')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "localefacepics", "en_US.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/intents/<intent>', methods=['POST'])
def intent_specific(intent):
    with anki_vector.Robot(args.serial, behavior_control_level=None) as robot:
        robot.behavior.app_intent(intent=intent)
    return "executed"

@app.route('/api/extras/get_image')
def request_image():
    with anki_vector.Robot(args.serial) as robot:
        robot.camera.init_camera_feed()
        image = robot.camera.latest_image
        image.raw_image.save("resources/webstuff/static/image/vectorimg.png", "PNG")
    return "executed"

@app.route('/api/settings/button/alexa', methods=['POST'])
def button_alexa():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'button_wakeword':1})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "alexab.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/button/heyvector', methods=['POST'])
def button_vector():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'button_wakeword':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "heyvectorb.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/temp/c', methods=['POST'])
def temp_celcius():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'temp_is_fahrenheit':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "tempc.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/temp/f', methods=['POST'])
def temp_fahrenheit():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'temp_is_fahrenheit':1})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "tempf.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
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
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "metric.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/units/imperial', methods=['POST'])
def unit_imperial():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'dist_is_metric':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "imperial.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
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
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "location.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
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
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "timezone.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/time/24', methods=['POST'])
def time_24():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'clock_24_hour':1})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "24hour.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
        robot.screen.set_screen_with_image_data(screen_data, duration_s)
        time.sleep(duration_s)
    return "executed"

@app.route('/api/settings/time/12', methods=['POST'])
def time_12():
    with anki_vector.Robot(args.serial) as robot:
        robot.behavior.update_settings(settings={'clock_24_hour':0})
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, "resources", "settingsfacepics", "12hour.jpg")
        image_file = Image.open(image_path)
        screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
        duration_s = 1.5
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

# used for debugging
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
