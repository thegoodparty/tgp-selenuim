from selenium import webdriver
import time
import psutil
import json
import requests
from pyvirtualdisplay import Display

def getDriver():
    options = webdriver.ChromeOptions()
    # options.headless = True

    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')        
    options.add_argument("--shm-size=2g")
    display = Display(visible=0, size=(800, 600))
    display.start()
    # driver = webdriver.Chrome('./chromedriver.exe', options=options)
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
    
    # driver = webdriver.Chrome(options=options)

    # driver = webdriver.Chrome(options=options)
    return driver

def kill_children(proc):
    for sub_proc in proc.children(True):
        sub_proc.kill()
    proc.kill()


def kill_idle_process():
    # names = ['Xvfb', 'chromedriver', 'chromedriver.ex']
    names = ['Xvfb']

    for proc in psutil.process_iter():
        """ current time in seconds """
        current_time = time.time()

        try:
            pinfo = proc.as_dict(
                attrs=['pid', 'ppid', 'name', 'create_time', 'username', 'cwd'])
            #print(pinfo['name'])
            """ if orphan process """
            # if pinfo['username'] == 'www-data' and pinfo['name'] in names:
            if pinfo['name'] in names:
                kill_children(proc)

        except psutil.NoSuchProcess:
            pass
domains = [
    {
        'backend': 'https://api.goodparty.org/api/v1/new-candidates',
        'frontend': 'https://goodparty.org/share-image/{}'
    },
    {
        'backend': 'https://api-dev.goodparty.org/api/v1/new-candidates',
        'frontend': 'https://dev.goodparty.org/share-image/{}'
    },
]
for domain in domains:
    res = requests.get(domain['backend'])
    # print(res.text)
    candidates = json.loads(res.text)['candidates']
    for key in candidates:
        # print(key, candidates[key])
        for candidate in candidates[key]:
            print(candidate['id'])
            driver = getDriver()
            driver.get(domain['frontend'].format(candidate['id']))
            time.sleep(10)
            print(driver.page_source)
            driver.quit()
            kill_idle_process()
