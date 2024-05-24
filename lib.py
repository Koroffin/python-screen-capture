import pygetwindow as gw
import pyautogui

def capture(windowId):
    try:
        # Get the window by its title
        window = gw.getWindowsWithTitle(windowId)[0]
        
        # If the window is not visible, make it visible
        if window.isMinimized:
            window.restore()

        # Bring the window to the front
        window.activate()

        # Get the window's location
        x, y, width, height = window.left, window.top, window.width, window.height

        # Capture the screenshot
        return pyautogui.screenshot(region=(x, y, width, height))

    except IndexError:
        print(f"No window with title '{windowId}' found")

    except Exception as e:
        print(f"An error occurred: {e}")