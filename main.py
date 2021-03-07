# Coded by #RedEye#6555
# "TOS: The developer of this software is not responsible for any damages caused by this software. The software was developed only for educational purposes."
import ctypes
import uuid
from io import BytesIO
from threading import Thread

import certifi
import pycurl
import requests
from colorama import init

init()

# Colors
WHITE = "\033[1;37;40m"
RED = "\033[1;31;40m"
GREEN = "\033[1;32;40m"


# Pycurl Req
def http_request(url, headers, data=None):
    curl = pycurl.Curl()
    response = BytesIO()

    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.ENCODING, "")
    curl.setopt(pycurl.WRITEDATA, response)
    curl.setopt(pycurl.HTTPHEADER, headers)
    curl.setopt(pycurl.CAINFO, certifi.where())

    if data:
        curl.setopt(pycurl.POST, True)
        curl.setopt(pycurl.POSTFIELDS, data)

    try:
        curl.perform()
    except:
        pass
    finally:
        curl.close()

    return response.getvalue().decode("utf-8")


class Instagram:
    def __init__(self):
        super(Instagram, self).__init__()
        self.attempts = 0
        self.running = True
        self.claimed = False
        self.target = ''

        self.url = 'https://i.instagram.com/api/v1'
        self.user_agent = 'Instagram 11.0.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)'
        self.guid = str(uuid.uuid1())
        self.device_id = 'android-{}'.format(self.guid)

    #   Login to instagram (Sessionid)
    def login(self, session):
        self.session = requests.Session()
        self.sessionID = session

        self.session.headers.update({
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            'User-Agent': self.user_agent,
            'X-IG-Capabilities': '3brTvw==',
            'Cookie': "sessionid={}".format(session),
            'X-IG-Connection-Type': 'WIFI'
        })

        self.loginResponse = self.session.get(self.url + '/accounts/current_user/?edit=true')
        lr = self.loginResponse.json()

        if self.loginResponse.status_code == 200:
            self.username = lr['user']['username']
            self.email = lr['user']['email']
            self.full_name = lr['user']['full_name']
            print("\nSuccessfully logged in as: {}\n".format(self.username))
            return True
        else:
            print(lr)
            print('An unknown login error occurred. ^')
            return False
        # End of login

    # Change username
    def change_username(self):
        response = http_request("https://i.instagram.com/api/v1/accounts/set_username/", [
            "Accept: */*",
            "Accept-Language: en-US",
            "User-Agent: Instagram 11.0.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)",
            "Cookie: sessionid=" + self.sessionID
        ], "username=%s" % self.target)
        if not response:
            return False
        if "isn't" in response:
            self.attempts += 1
        # Check if username claimed
        elif "\"status\":\"ok\"" in response:
            self.claimed = True
            self.running = False
            return True
        return False


# Threader
class Thread(Thread):
    def __init__(self, instagram):
        super(Thread, self).__init__()
        self.instagram = instagram

    def run(self):
        while self.instagram.running:
            try:
                if self.instagram.change_username():
                    self.instagram.claimed = True
                    self.instagram.running = False
                else:
                    self.instagram.attempts += 1
            except:
                continue


def main():
    print(
        "Welcome \n"
        "TOS: The developer of this software is not responsible for any damages caused by this software. The software was developed only for educational purposes. \n"
    )
    while True:
        try:
            instagram = Instagram()
            # Session ID > Acc
            session = input("Session : ")
            if not instagram.login(session):
                continue
            # End of login

            # Set Target Username
            instagram.target = input("Target: ").strip().lower()

            print('')

            # Threads
            threads = int(input("Threads: "))

            # MessageBox to Start Swapping
            ctypes.windll.user32.MessageBoxW(0, f"Your Target is @{instagram.target}", "#RedEye | #Test :", 1)
            for _ in range(threads * 10):
                thread = Thread(instagram)
                thread.setDaemon(True)
                thread.start()

            # Running
            while instagram.running and not instagram.claimed:
                print("Swapping: {}@{} {}| Attempts: {:,}".format(RED, instagram.target, WHITE, instagram.attempts),
                      end="\r", flush=True)

            # Print if username claimed successfully
            if instagram.claimed:
                print("\n\n{}Claimed Successfully: {}@{}\n".format(GREEN, RED, instagram.target))
                input('Press enter to exit...')
                exit()

        # Close
        except Exception as e:
            print('{}Unknown error: '.format(RED) + str(e))
            input('Press enter to exit...')
            exit()


if __name__ == '__main__':
    main()
