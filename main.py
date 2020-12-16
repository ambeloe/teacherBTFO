import os
import json
import time
import datetime
import keyboard
import platform
import threading
import subprocess
import urllib.request
# from tkinter import *
import winsound
from zipfile import ZipFile

host = platform.system()
if host == "Windows":
    host_int = 0
elif host == "Darwin":
    host_int = 1
elif host == "Linux":
    host_int = 2
else:
    # unknown host; try to run anyway
    host_int = 3


def clear_console(host_os):
    if host_int == 0:
        os.system("cls")
    elif host_int == 2 or 3:
        os.system("clear")
    else:
        print("could not determine host os to clear screen")


def pip_check():
    output = str(subprocess.check_output("pip"))
    if "pip <command> [options]" in output:
        return True
    else:
        return False


def pip_init():
    subprocess.call("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
    subprocess.call("python get-pip.py --user")
    os.remove("get-pip.py")


def pip_install(package):
    status = subprocess.call("pip install " + package + " --user")
    if status != 0:
        print("error while installing " + package + " using pip.")
        print("please manually install " + package + " for python and try again.")
        raise Exception("pip install error")


if not pip_check():
    pip_init()

try:
    # import selenium
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys
except ModuleNotFoundError:
    pip_install("selenium")
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys

try:
    import keyring
except ModuleNotFoundError:
    pip_install("keyring")
    import keyring

# try:
#     import cv2
# except ModuleNotFoundError:
#     pip_install("opencv-python")
#     import cv2
#
# try:
#     import pytesseract
# except ModuleNotFoundError:
#     pip_install("pytesseract")
#     import pytesseract

clear_console(host_int)
# user_browser = int(input("Which browser do you want to use?\n1) Chrome\n2) Firefox\n3) Safari\n"))

if host_int == 0:
    path = subprocess.check_output("echo %appdata%", shell=True).decode('UTF-8')
    path = path.replace("\\", "/").replace("\r\n", "")
    if not os.path.exists(path + "/teacherBTFO/"):
        os.mkdir(path + "/teacherBTFO/")
    if not os.path.exists(path + "/teacherBTFO/chrome-win/chrome.exe"):
        try:
            os.remove(path + "/teacherBTFO/chrome.zip")
            os.remove(path + "/teacherBTFO/chromedriver.zip")
        except FileNotFoundError:
            pass
        version_json = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2FLAST_CHANGE"))
        chrome_version = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2FLAST_CHANGE"))['metadata'][
            'cr-commit-position-number']
        chrome_generation = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchrome-win.zip"))[
            "generation"]
        latest_chrome = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchrome-win.zip?generation=" + chrome_generation + "&alt=media"
        chromedriver_generation = json.load(urllib.request.urlopen(
            "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchromedriver_win32.zip"))[
            "generation"]
        latest_chromedriver = "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win%2F" + chrome_version + "%2Fchromedriver_win32.zip?generation=" + chromedriver_generation + "&alt=media"
        urllib.request.urlretrieve(latest_chrome, path + "/teacherBTFO/chrome.zip")
        urllib.request.urlretrieve(latest_chromedriver, path + "/teacherBTFO/chromedriver.zip")
        with ZipFile(path + "/teacherBTFO/chrome.zip") as zipf:
            zipf.extractall(path=path + "/teacherBTFO/")
        with ZipFile(path + "/teacherBTFO/chromedriver.zip") as zipf:
            zipf.extractall(path=path + "/teacherBTFO/")
        try:
            os.remove(path + "/teacherBTFO/chrome.zip")
            os.remove(path + "/teacherBTFO/chromedriver.zip")
        except FileNotFoundError:
            pass
elif host_int == 1:
    # placeholder for mac commands
    pass
else:
    # placeholder for linux and other commands
    pass

test = False


def ctime():
    return int(time.time() / 60)


def login(h_u, h_p, d):
    if test:
        return
    d.get(
        "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmeet.google.com%2F&sacu=1&hl=en_US&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    # time.sleep(1)
    for i in range(0, 20):
        try:
            e = d.find_element_by_id("identifierId")
            break
        except:
            time.sleep(0.1)
    e.clear()
    e.send_keys(hcpss_username + "@inst.hcpss.org")

    e = d.find_element_by_xpath("//button[span[text()=\"Next\"]]")
    e.send_keys(Keys.ENTER)

    while True:
        try:
            e = d.find_element_by_id("username")
            break
        except:
            time.sleep(0.02)
    e.send_keys(h_u)
    e = d.find_element_by_id("password")
    e.send_keys(h_p)
    e.send_keys(Keys.ENTER)

def mic_dialog_fuckoff(driver):
    try:
        e = driver.find_element_by_xpath("//div[div/div[text()=\"Allow Meet to use your camera and microphone\"]]/div/div[span/span[text()=\"Dismiss\"]]")
        time.sleep(0.2)
        e.send_keys(Keys.ESCAPE)
    except:
        pass

def join(code, d):
    while True:
        try:
            d.find_element_by_xpath("//*[text()='Use a meeting code']").click()
            time.sleep(0.25)
            break
        except:
            time.sleep(0.05)
    while True:
        try:
            d.find_element_by_xpath("//input[@type='text']").send_keys(code)
            time.sleep(0.1)
            break
        except:
            time.sleep(0.1)
    d.find_element_by_xpath("//span[text()='Continue']").click()


def join_timeout(code, driver, timeout):
    start_time = ctime()
    while ctime() < start_time + timeout:
        join(code, driver)
        time.sleep(1)
        try:
            e = driver.find_element_by_xpath(
                "//div[div/div[text()=\"You\'re not allowed to start a meeting\"] and @style=\"visibility: visible;\"]")
            winsound.Beep(300, 400)
        except:
            break
        time.sleep(29.5)


def meet(username, password, meeting_id, max_len, name, rec):
    boptions = webdriver.ChromeOptions()
    boptions.binary_location = path + "/teacherBTFO/chrome-win/chrome.exe"
    # boptions.headless = True
    boptions.add_argument('--disable-gpu')
    boptions.add_argument("--incognito")
    boptions.add_argument("--app=http://www.gstatic.com/")
    boptions.add_argument("--new-window")
    boptions.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2,
        "profile.default_content_setting_values.media_stream_camera": 2,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2
    })

    driver = webdriver.Chrome(executable_path=path + "/teacherBTFO/chromedriver_win32/chromedriver.exe",
                              options=boptions)
    driver.maximize_window()

    login(hcpss_username, hcpss_password, driver)

    if test:
        # driver.get("https://meet.google.com")
        # while True:
        #     try:
        #         driver.find_element_by_xpath("//div[not(@data-expanded)]/input").send_keys(meeting_id)
        #     except:
        #         time.sleep(0.1)
        # webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
        driver.get(meeting_id)
    else:
        join_timeout(meeting_id, driver, 5)

    # add screenshot code for testing
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    while True:
        try:
            e = driver.find_element_by_xpath("//div[div/div[text()=\"Allow Meet to use your camera and microphone\"]]")
            break
        except:
            try:
                e = driver.find_element_by_xpath("//div[div/div[text()=\"Camera and microphone are blocked\"]]")
                break
            except:
                time.sleep(0.3)
    time.sleep(0.2)
    e.send_keys(Keys.ESCAPE)

    time.sleep(1)
    e = driver.find_element_by_xpath("//div[span/span[text()=\"Join now\"]]")
    e.click()

    def click(x, y):
        el = driver.find_element_by_xpath("//html")
        webdriver.ActionChains(driver).move_to_element(el).move_by_offset(x, y).click()

    def send_msg(msg):
        time.sleep(0.5)
        el = driver.find_element_by_xpath("//div[@data-tooltip=\"Chat with everyone\"]")
        el.send_keys(Keys.SPACE)
        while True:
            try:
                el = driver.find_element_by_xpath("//textarea[@aria-label=\"Send a message to everyone\"]")
                break
            except:
                print("cringe chatbox")
                time.sleep(0.1)
        time.sleep(0.5)
        el.send_keys(msg)
        el.send_keys(Keys.ENTER)
        el = driver.find_element_by_xpath("//i[text()=\"close\"]")
        el.click()

        while True:
            try:
                el = driver.find_element_by_xpath("//div[@data-tooltip=\"Chat with everyone\"]")
                break
            except:
                time.sleep(0.1)

    def toggle_captions(drv):
        try:
            el = drv.find_element_by_xpath("//div[span/span/div/div[contains(text(),\"captions\")]]").click()
        except:
            print("caption toggling failed")

    def set_captions(drv, state):
        try:
            if state:
                el = drv.find_element_by_xpath("//div[span/span/div/div[text()=\"Turn on captions\"]]").click()
            else:
                el = drv.find_element_by_xpath("//div[span/span/div/div[text()=\"Turn off captions\"]]").click()
        except:
            print("failed to set caption state")

    join_time = ctime()
    if rec:
        keyboard.send("F9")
    time.sleep(1)

    # send_msg("present")
    set_captions(driver, True)

    participants = 0
    # wait until people have left
    while True:
        # print("inside main loop")
        time.sleep(1)
        # monstrosity lmao
        t = 0
        e = None
        # try to find for up to 200ms
        while e is None and t < 41:
            try:
                e = driver.find_element_by_xpath(
                    "//div[span/span/div/div/span]/span/span/div/div/span[contains(text(), \"0\") or contains(text(), \"1\") or contains(text(), \"2\") or contains(text(), \"3\") or contains(text(), \"4\") or contains(text(), \"5\") or contains(text(), \"6\") or contains(text(), \"7\") or contains(text(), \"8\") or contains(text(), \"9\")]")
            except:
                try:
                    # might comment it out as it is useful to be able to prevent it from leaving

                    # doesnt work for whatever unholy reason
                    e = driver.find_element_by_xpath("//div[span/div/span]/span/div/span[(contains(text(), \"0\") or contains(text(), \"1\") or contains(text(), \"2\") or contains(text(), \"3\") or contains(text(), \"4\") or contains(text(), \"5\") or contains(text(), \"6\") or contains(text(), \"7\") or contains(text(), \"8\") or contains(text(), \"9\")) and contains(text(), \"(\")]")
                except:
                    pass
            t += 1
            time.sleep(0.05)

        try:
            # print(e.text)
            participants = int(e.text.replace("(", "").replace(")", ""))
        except:
            print("couldn't find participant number")

        clear_console(host_int)
        elapsed = ctime() - join_time
        print("Class: " + name)
        print("Participants: " + str(participants))
        print("Elapsed time: " + str(elapsed))

        # get rid of the USE MIC popup that happens whenever usb devices are plugged or a new window is opened
        mic_dialog_fuckoff(driver)

        # detect if in breakout room
        try:
            e = driver.find_element_by_xpath("//i[text()=\"gmail_rooms\"]")
            breakout = True
        except:
            breakout = False

        # exit logic
        if (participants < 10 and elapsed > 5 and not breakout) or elapsed > max_len:
            break

    # clean up
    # send_msg("bye")
    if rec:
        keyboard.send("F10")
    driver.close()
    # try:
    #     os.remove(path + "/teacherBTFO/peoplecount.png")
    # except FileNotFoundError:
    #     pass


# # meet(hcpss_username, hcpss_password, )
# meet(hcpss_username, hcpss_password, "test", 0, "test")
# while True:
#     pass

schedule = json.load(open(path + "/teacherBTFO/schedule.json"))
hcpss_username = schedule["hcpss_username"]
hcpss_password = schedule["hcpss_password"]


# try:
#     schedule = json.load(open(path + "/teacherBTFO/schedule.json"))
# except FileNotFoundError:
# with open(path + "/teacherBTFO/config.json", "w") as f:
#     f.write(json.dumps({"username": "", "schedule": []}, indent=4))
# schedule = json.load(open(path + "/teacherBTFO/schedule.json"))
# pass


# print(schedule)
# meet(username, password, meeting_id, max_len, name):

def go_to_school(h_u, h_p, meeting):
    tts = datetime.datetime.strptime(meeting["starttime"], "%H:%M")
    tte = tts + datetime.timedelta(minutes=meeting["maxduration"])
    tHour, tMin = tts.hour, tts.minute
    # print(tts + datetime.timedelta(hours=10))
    print(meeting["name"] + " - " + str(tts.time()) + " to " + str(tte.time()))
    while True:
        now = datetime.datetime.now()
        # print(int((tte - now).seconds/60))
        hour, minute = now.hour, now.minute
        ongoing = tts.time() < now.time() < tte.time()
        if tte.time() < now.time():
            break
        # print("hour(" + str(tHour) + ", " + str(hour) + ") minute(" + str(tMin) + ", " + str(minute) + ")")
        # print(minute)
        if (tHour == hour) and (tMin == minute) or ongoing:
            print("starting " + meeting["name"])
            meet(h_u, h_p, meeting["code"], int((tte - now).seconds / 60), meeting["name"], meeting["record"])
            clear_console(host_int)
            print(meeting["name"] + " ended")
            break
        time.sleep(5)


if __name__ == "__main__":
    test = False
    if test:
        meet(hcpss_username, hcpss_password, "test", 10, "test")
    else:
        weekday = datetime.datetime.today().weekday()
        docket = schedule[str(weekday)]
        threads = []
        # start a thread per class
        for meeting in docket:
            threads.append(threading.Thread(target=go_to_school, args=[hcpss_username, hcpss_password, meeting]))
            threads[-1].start()
        # wait for all threads to stop
        for thread in threads:
            thread.join()
        print("done")
