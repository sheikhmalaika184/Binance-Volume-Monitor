import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.chrome.options import Options
from telethon import TelegramClient, sync

DRIVER_PATH = '/Users/malaikasheikh/python/chromedriver'
# starting a browser 
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
options = Options()
options.add_argument("--window-size=1920,1200")
options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

# TELEGRAM SIGNAL
api_id = 123456
api_hash = ''
client = TelegramClient('session_name', api_id, api_hash).start()

def send_signal(msg):
  me = client.get_me()
  client.send_message(me, msg)


def make_request(url):
    driver.get(url)
    time.sleep(5)
    table_tag = driver.find_element(By.XPATH, '//*[@id="pinger"]/thead')
    table_rows = driver.find_elements(By.XPATH, '//*[@id="pinger"]/tr')
    previous_rows  = len(table_rows)
    for r in table_rows:
        total_th = r.find_elements(By.XPATH, '//th')
        coin = r.text.replace("\n"," ")
        coin_info = coin.split(" ")
        ping = int(coin_info[1])
        net_vol = float(coin_info[3].replace("%",""))
        print(coin_info)
        print("ping: ", ping)
        print("Net Volume: ", net_vol)
        if((ping ==  1 and net_vol > 4) or (ping ==  1 and net_vol < -4)):
            send_signal(coin)
    print("")
    #finding followers button 
    while(True):
      #finding followers button 
      print("Running")
      time.sleep(15)
      table_tag = driver.find_element(By.XPATH, '//*[@id="pinger"]/thead')
      table_rows = driver.find_elements(By.XPATH, '//*[@id="pinger"]/tr')

      print("length: ", len(table_rows))
      if(len(table_rows) > previous_rows):
        for r in range( 0, len(table_rows) - previous_rows):
          coin = table_rows[r].text.replace("\n"," ")
          coin_info = coin.split(" ")
          ping = int(coin_info[1])
          net_vol = float(coin_info[3].replace("%",""))
          if((ping ==  1 and net_vol > 4) or (ping ==  1 and net_vol < -4)):
            send_signal(coin)
          print(coin_info)
          print("ping: ", ping)
          print("Net Volume: ", net_vol)
        previous_rows = len(table_rows)
      print("")


make_request('https://agile-cliffs-23967.herokuapp.com/')