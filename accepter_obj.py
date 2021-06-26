from pyautogui import *
import pyautogui
import win32api
import win32con
import pandas as pd
import pydirectinput

class Accepter:
    def __init__(self, path):
        self.bans = []
        self.picks = []
        self.items = []
        self.path = path #path to PersistedSettings.json
        self.miniMapScale = self.getMiniMapScale()
        self.miniMapSize = self.getMiniMapSize()
        self.leagueLeftCorner = (0,0)
        self.window_width = 0
        self.Accepting = 0
        self.picking = 0
        self.banning = 0
        self.picked = 0
        self.gameStarted = 0
        self.gameStarting = 0

    def defineAfterStartButton(self):
        s = pyautogui.screenshot()
        self.gameStarted = self.hasGameStarted(s)
        self.gameStarting = self.isGameStarting(s)
        self.leagueLeftCorner = self.findLeftCorner(s.crop((0,0,500,500)))
        if self.leagueLeftCorner != "League not opened":
            s = pyautogui.screenshot()
            print(self.leagueLeftCorner)
            self.window_width = 1600
            self.Accepting = self.toAccept(s)
            self.picking = self.isPicking(s)
            self.banning = self.isBanning(s)
            try:
                self.picked = self.isPicked(s)
            except:
                print("errors dunno why")
            print("a")

    def getMiniMapScale(self):
        leagueSettings = pd.read_json(self.path)
        miniMapScale = float(leagueSettings['files'][0]['sections'][5]['settings'][29]['value'])/3
        return miniMapScale

    def getMiniMapSize(self):
        return (209 + 209 * self.miniMapScale, 210 + 210 * self.miniMapScale)

    def findLeftCorner(self, s = pyautogui.screenshot()):
        color = (30, 40, 45)
        for x in range(s.width):
            for y in range(s.height):
                if s.getpixel((x, y)) == color:
                    return x, y
        return "League not opened"


    def isPicked(self, s = pyautogui.screenshot()):
        if s.getpixel((self.leagueLeftCorner[0] + 1050, self.leagueLeftCorner[1] + 850)) == (204, 189, 144):
            return True
        return False

    def isBanning(self, s = pyautogui.screenshot()):
        if s.getpixel((self.leagueLeftCorner[0] + 760, self.leagueLeftCorner[1] + 40)) == (240, 215, 199):
            return True
        return False

    def isPicking(self, s = pyautogui.screenshot()):
        x = self.leagueLeftCorner[0] + 760
        y = self.leagueLeftCorner[1] + 40
        if s.getpixel((x, y)) == (223, 228, 208):
            return True
        return False

    def isGameStarting(self, s = pyautogui.screenshot()):
        if s.getpixel((30,20)) == (24,88,65):
            return True
        return False

    def hasGameStarted(self, s = pyautogui.screenshot()):
        x, y = 1770, 15
        color = (207, 183, 108)
        if s.getpixel((x, y)) == color:
            return True
        return False

    def toAccept(self, s=""):
        s = pyautogui.screenshot()
        if s.getpixel((self.leagueLeftCorner[0]+1389,self.leagueLeftCorner[1]+185)) == (10,193,220):
            return True
        return False

    def click(self, x, y):
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def rightClick(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

    def confirm(self):
        self.click(self.leagueLeftCorner[0] + 800, self.leagueLeftCorner[1] + 750)

    def searchChamp(self, champ): #presses search button and searchs for champion
        self.click(self.leagueLeftCorner[0] + 1000, self.leagueLeftCorner[1] + 130)  # click search button
        self.click(self.leagueLeftCorner[0] + 1000, self.leagueLeftCorner[1] + 130)  # click search button
        pyautogui.typewrite(champ)

    def selectSearched(self):
        self.click(self.leagueLeftCorner[0] + 480, self.leagueLeftCorner[1] + 200)
        sleep(0.1)
        self.click(self.leagueLeftCorner[0] + 480, self.leagueLeftCorner[1] + 200)


    ################################ FUNCTIONALITY ################################

    def findMatch(self): # if can start match
        while True:
            if self.window_width == 1600:
                # PRESS FIND MATCH
                s = pyautogui.screenshot()
                x = self.leagueLeftCorner[0] + 769
                y = self.leagueLeftCorner[1] + 870
                if s.getpixel((x, y)) == (3, 108, 133):
                    self.click(x, y)
                    break
        self.Accepting = True
        self.acceptMatch()

    def acceptMatch(self): # accept when window pops up
        x = self.leagueLeftCorner[0] + 769
        y = self.leagueLeftCorner[1] + 870
        while not pyautogui.screenshot().getpixel((x, y)) == (3, 108, 133):
            self.Accepting = self.toAccept()
            print(self.Accepting)
            # ACCEPT MATCH WHEN READY
            s = pyautogui.screenshot()
            x = self.leagueLeftCorner[0] + 800
            y = self.leagueLeftCorner[1] + 700
            if s.getpixel((x, y)) == (153, 187, 187): #IF ACCEPT WINDOW POPS UP
                self.click(x, y)
                sleep(5)
                self.startRunning()
        else:
            self.findMatch()
    def Declare(self): # declare champion
        s = pyautogui.screenshot()
        x = self.leagueLeftCorner[0] + 570
        y = self.leagueLeftCorner[1] + 40
        while s.getpixel((x, y)) == (240, 230, 210):
            if self.window_width == 1600:
                # DECLARE CHAMPION
                self.searchChamp(self.picks[0])
                sleep(1)
                self.selectSearched()
                sleep(20)
                self.banChamp()
        else:
            self.acceptMatch()
    def banChamp(self):
        s = pyautogui.screenshot()
        x = self.leagueLeftCorner[0] + 760
        y = self.leagueLeftCorner[1] + 40
        while s.getpixel((x, y)) == (240, 215, 199):
            # DECLARE CHAMPION
            for ban in self.bans[:5]:
                self.searchChamp(ban)
                sleep(0.3)
                self.selectSearched()
                sleep(0.3)
                self.confirm()
            sleep(5)
            self.pickChamp()
        else:
            self.acceptMatch()

    def pickChamp(self):
        x = self.leagueLeftCorner[0] + 760
        y = self.leagueLeftCorner[1] + 40
        while True:
            s = pyautogui.screenshot()
            if s.getpixel((x, y)) == (223, 228, 208):
                while s.getpixel((x, y)) == (223, 228, 208):
                    for pick in self.picks:
                        self.searchChamp(pick)
                        sleep(0.3)
                        self.selectSearched()
                        sleep(0.2)
                        self.confirm()
                        if self.isPicked(): #if champ is picked break loop
                            self.Picked = True
                            break
                    print("start of sleep")
                    sleep(3)
                    self.purchaseItems()
                else:
                    self.acceptMatch()

    def purchaseItems(self):
        print("starts purchase")
        while not pyautogui.screenshot().getpixel((1770, 15)) == (207, 183, 108):
            print("runs while loop")
            sleep(1)
        else:
            print("runs else")
            self.gameStarted = True
        sleep(1)
        waitingForStart = True
        print("clicking")
        self.click(200,200)
        sleep(0.5)
        self.click(200, 200)   # make league main window
        print("pressing keyboard")
        pydirectinput.keyDown("p")  # open shop
        while waitingForStart:
            sleep(0.5)
            color = (156, 154, 140)
            s = pyautogui.screenshot()
            for y in range(s.height):
                if not waitingForStart:
                    break
                for x in range(s.width):
                    if s.getpixel((x, y)) == color:
                        search_x = x
                        search_y = y
                        waitingForStart = False
                        break
        if not waitingForStart:
            for item in self.items:
                self.click(search_x + 30, search_y)
                sleep(1)
                pyautogui.typewrite(item)
                sleep(1)
                pydirectinput.rightClick(search_x + 40, search_y + 70)
                pydirectinput.rightClick(search_x + 40, search_y + 70)
                pydirectinput.rightClick(search_x + 40, search_y + 70)
                self.click(search_x + 40, search_y + 70)
                self.click(search_x + 40, search_y + 70)
                self.click(search_x + 40, search_y + 70)
                sleep(2)
            pydirectinput.press("ESC")
            sleep(5)
        self.walkToLane()

    def walkToLane(self):
        if self.miniMapScale > 0.5:
            self.click(int(1920 - (self.miniMapSize[0] + 100 * self.miniMapScale) / 2),
                  int(1080 - (self.miniMapSize[1] - 100 * self.miniMapScale) / 2))
            pydirectinput.rightClick()
            pyautogui.rightClick()
            self.rightClick()
            pydirectinput.rightClick()
            pyautogui.rightClick()
            sleep(6000)
        else:
            self.click(int(1920 - (self.miniMapSize[0] + 40 + 100 * self.miniMapScale) / 2),
                  int(1080 - (self.miniMapSize[1] - 40 - 100 * self.miniMapScale) / 2))
            pydirectinput.rightClick()
            pyautogui.rightClick()
            self.rightClick()
            pydirectinput.rightClick()
            pyautogui.rightClick()
            sleep(6000)


    def startRunning(self):
        if self.Accepting:
            print("accepting")
            self.acceptMatch()
        elif self.banning:
            print("banning")
            self.banChamp()
        elif self.picking:
            print("picking")
            self.pickChamp()
        elif self.picked:
            print("picked")
            self.purchaseItems()
        elif self.gameStarting:
            print("gamestarting")
            self.purchaseItems()
        elif self.gameStarted:
            self.purchaseItems()
        else:
            print("looping again")
            self.defineAfterStartButton()
            self.startRunning()
