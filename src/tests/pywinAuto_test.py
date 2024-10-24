from pywinauto import Application, Desktop
import pyautogui
import sys, os
import time

def main():
    # Replace this with the exact window title of your application
    app_title = 'Microsoft Dynamics NAV (SrvRDS-CB.bila.local)'

    # Connect to the application
    try:
        app = Application(backend='uia').connect(title=app_title)
        print(f"Connected to application: {app_title}")
    except Exception as e:
        print(f"Could not connect to application: {e}")
        return

    # Access the main window
    try:
        main_window = app.window(title=app_title)
        main_window.wait('visible', timeout=10)
        print("Main window is ready.")
    except Exception as e:
        print(f"Could not access main window: {e}")
        return
    parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_folder = os.path.join(os.path.dirname(parent_folder), 'images')
    # try and click the sager button
    try:
        sager_img = os.path.join(image_folder, 'Sager_knap_normal.png')
        button_location = pyautogui.locateCenterOnScreen(sager_img, confidence=0.95)
        if button_location:
            print("Button location found:", button_location)
            pyautogui.click(button_location)
            pyautogui.click(button_location)
            print("Sager button clicked.")
        else:
            print("Sager button not found.")
        multikladet_img = os.path.join(image_folder, 'multiklade_knap_normal.png')
        button_location = pyautogui.locateCenterOnScreen(multikladet_img, confidence=0.95)
        if button_location:
            print("Button location found:", button_location)
            pyautogui.click(button_location)
            pyautogui.click(button_location)
            print("Multikladet button clicked.")
        else:
            print("Multikladet button not found.")
        time.sleep(1)
        empty_space_img = os.path.join(image_folder, 'empty_space.png')
        button_location = pyautogui.locateCenterOnScreen(empty_space_img, confidence=0.95)
        if button_location:
            print("Button location found:", button_location)
            pyautogui.click(button_location)
            pyautogui.click(button_location)
            print("Empty space clicked.")
        else:
            print("Empty space not found.")
    except Exception as e:
        print(f"Could not click sager button: {e}")
        return

if __name__ == "__main__":

    # Print possible windows
    print("Windows detected with UIA backend:")
    windows = Desktop(backend='uia').windows()
    for w in windows:
        print(w.window_text())


    main()
