import subprocess, time, glob, sys, os

port = 9222
prof = "/home/wazaglo/udacity/work/browser-profile"
os.makedirs(prof, exist_ok=True)
chrome = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-1234/chrome-linux*/chrome")) +
                glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-1234/chrome-linux/chrome")))
chrome = [c for c in chrome if os.path.exists(c)]
if not chrome:
    sys.exit("no chrome")
log = open("/home/wazaglo/udacity/work/chrome.log", "w")
subprocess.Popen(
    [chrome[0], f"--remote-debugging-port={port}", f"--user-data-dir={prof}",
     "--headless=new", "--no-sandbox", "--no-first-run", "--no-default-browser-check",
     "--disable-gpu", "--window-size=1600,900",
     "--accept-lang=en-US,en"],
    stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
time.sleep(2)
print("launched")
