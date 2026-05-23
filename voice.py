import speech_recognition as sr
import pyautogui

def move_up(distance=20):
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x, current_y - distance)

def move_down(distance=20):
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x, current_y + distance)

def move_left(distance=20):
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x - distance, current_y)

def move_right(distance=20):
    current_x, current_y = pyautogui.position()
    pyautogui.moveTo(current_x + distance, current_y)

def click_left():
    pyautogui.click(button='left')

def click_right():
    pyautogui.click(button='right')

recognizer = sr.Recognizer()
microphone = sr.Microphone()

command_functions = {
    "move up": move_up,
    "move down": move_down,
    "move left": move_left,
    "move right": move_right,
    "click left": click_left,
    "click right": click_right
}

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

while True:
    print("Listening for commands...")
    result = recognize_speech_from_mic(recognizer, microphone)

    if result["transcription"]:
        command = result["transcription"].lower()
        print(f"Recognized command: {command}")

        # Extract distance if present
        distance = 20  # Default distance

        if "move" in command:
            distance_words = ['ten', 'twenty', 'thirty']
            for word in distance_words:
                if word in command:
                    distance = int(word)
                    break

        if command in command_functions:
            command_functions[command](distance)
        else:
            print("Unknown command")
    elif result["error"]:
        print(f"Error: {result['error']}")
