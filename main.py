"""
MIT License

Copyright (c) 2024 PirxcyFinal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Well then, I guess PirxcyProxy is now open source (due to virus accusations).
# If you're gonna skid, i suggest you get some bitches first 😘

import os
from typing import Any
import semver
import survey
import aiohttp
import asyncio
import traceback
import ujson
import crayons
import logging
import winreg
import sys
import aiofiles

import xml.etree.ElementTree as ET


from rich import print_json
from console.utils import set_title # type: ignore
from mitmproxy.tools.dump import DumpMaster
from mitmproxy import http
from mitmproxy.options import Options as mitmoptions
from pypresence import AioPresence


appName = "PirxcyProxy"

logger = logging.getLogger(appName)
logger.setLevel(logging.INFO)
logging.basicConfig(format=f"[{crayons.blue(appName)}] %(message)s") # type: ignore


itemTypeMap = {
  "emote": "AthenaDance",
  "backpack": "AthenaBackpack",
  "outfit": "AthenaCharacter",
  "toy": "AthenaToy",
  "glider": "AthenaGlider",
  "emoji": "AthenaEmoji",
  "pet": "AthenaPetCarrier",
  "spray": "AthenaSpray",
  "music": "AthenaMusicPack",
  "bannertoken": "BannerToken",
  "contrail": "AthenaSkyDiveContrail",
  "wrap": "AthenaItemWrap",
  "loadingscreen": "AthenaLoadingScreen",
  "pickaxe": "AthenaPickaxe",
  "vehicle_wheel": "VehicleCosmetics_Wheel",
  "vehicle_wheel": "VehicleCosmetics_Wheel",
  "vehicle_skin": "VehicleCosmetics_Skin",
  "vehicle_booster": "VehicleCosmetics_Booster",
  "vehicle_body": "VehicleCosmetics_Body",
  "vehicle_drifttrail": "VehicleCosmetics_DrifTrail",
  "vehicle_cosmeticvariant": "CosmeticVariantToken",
  "cosmeticvariant": "none",
  "bundle": "AthenaBundle",
  "battlebus": "AthenaBattleBus",
  "itemaccess": "none",
  "sparks_microphone": "SparksMicrophone",
  "sparks_keyboard": "SparksKeyboard",
  "sparks_bass": "SparksBass",
  "sparks_drum": "SparksDrums",
  "sparks_guitar": "SparksGuitar",
  "sparks_aura": "SparksAura",
  "sparks_song": "SparksSong",
  "building_set": "JunoBuildingSet",
  "building_prop": "JunoBuildingProp",
}

def cls():
  os.system("cls" if os.name == "nt" else "clear")

async def aprint(text: str, delay: float):
  """
  Asynchronously prints each character of the given text with a specified delay between characters.
  (gives it a sexy animation)

  Args:
    text (str): The text to be printed.
    delay (float): The delay in seconds between printing each character.

  Returns:
    None
  """
  for character in text:
    sys.stdout.write(character)
    sys.stdout.flush()
    if character.isalpha():
      await asyncio.sleep(delay)
  sys.stdout.flush()
  return print()

def center(var: str, space: int | None = None):
  if not space:
    space = (
      os.get_terminal_size().columns
      - len(var.splitlines()[int(len(var.splitlines()) / 2)])
    ) // 2
  return "\n".join((" " * int(space)) + var for var in var.splitlines())

def proxy_toggle(enable: bool=True):
  # Open the key where proxy settings are stored
  INTERNET_SETTINGS = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,
    r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings",
    0,
    winreg.KEY_ALL_ACCESS,
  )

  def set_key(name: str, value: str | int):
    try:
      _, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, name)
      winreg.SetValueEx(INTERNET_SETTINGS, name, 0, reg_type, value)
    except FileNotFoundError:
      # If the key does not exist, create it
      winreg.SetValueEx(INTERNET_SETTINGS, name, 0, winreg.REG_SZ, value)

    # Get current proxy enable status

  proxy_enable = winreg.QueryValueEx(INTERNET_SETTINGS, "ProxyEnable")[0]

  if proxy_enable == 0 and enable:
    set_key("ProxyServer", "127.0.0.1:8080")
    set_key("ProxyEnable", 1)
  elif proxy_enable == 1 and not enable:
    set_key("ProxyEnable", 0)
    set_key("ProxyServer", "")

class Addon:
  def __init__(self, server: "MitmproxyServer"):
    self.server = server

  def request(self, flow: http.HTTPFlow) -> None:
    """Handle Requests"""
    try:
      url = flow.request.pretty_url

      if ".blurl" in url:
        logger.info(url)
        flow.request.url = "https://cdnv2.boogiefn.dev/master.blurl"
        logger.info(f".blurl {flow.request.url}")

      if (
        "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/matchmakingservice/ticket/player"
        in flow.request.pretty_url
        and self.server.app.playlist
      ):
        playlistOld, playlistNew = list(self.server.app.playlistId.items())[0]
        flow.request.url = flow.request.url.replace(
          "%3A" + playlistOld, "%3A" + playlistNew
        )
        logger.info(f"Matchmaking: {flow.request.url}")

      if "/client/" in flow.request.url:
        logger.info(f"Client Request: {flow.request.url}")

      if self.server.app.name:
        nameOld, nameNew = list(self.server.app.nameId.items())[0]
        flow.request.url = flow.request.url.replace(nameOld, nameNew)

      if (".png" in url or ".jpg" in url or ".jpeg" in url) and (
        ".epic" in url or ".unreal" in url or ".static" in url
      ):
        logger.info(f"Image: {flow.request.url}")
        flow.request.url = "https://cdnv2.boogiefn.dev/maxresdefault.jpg"

    except:
      pass

  def websocket_message(self, flow: http.HTTPFlow):
    assert flow.websocket is not None
    msg = flow.websocket.messages[-1]
    msg = str(msg)
    msg = msg[1:-1]
    msg = msg

    if "match" in flow.request.pretty_url.lower():
      logger.info("Matchmaking:")
      print_json(msg)

    elif "xmpp" in flow.request.pretty_url.lower():
      if msg.startswith("<presence><status>") and msg.endswith("</presence>"):
        root = ET.fromstring(msg)
        status_element = root.find("status")
        if status_element is None or status_element.text is None: raise TypeError
        json_data = ujson.loads(status_element.text)

        # Change the status
        currentStatus = json_data["Status"]
        json_data["Status"] = (
          f"@ {appName} 🤖"
        )

        new_json_text = ujson.dumps(json_data)
        status_element.text = new_json_text
        new_xml_data = ET.tostring(root)

        flow.websocket.messages[-1].content = new_xml_data
      if self.server.app.config.get("WebSocketLogging", False):
        # XMPP LOG
        logger.info("XMPP:")
        print_json(data=str(flow.websocket.messages[-1])[1:-1])

  def response(self, flow: http.HTTPFlow):
    try:
      url = flow.request.pretty_url

      if (
        "setloadoutshuffleenabled" in url.lower()
        and self.server.app.config.get("EveryCosmetic")
        or url
        == "https://fortnitewaitingroom-public-service-prod.ol.epicgames.com/waitingroom/api/waitingroom"
      ):
        flow.response = http.Response.make(
          204, b"", {"Content-Type": "text/html"}
        )  # Return no body

      if (
        "putbmodularcosmetic" in url.lower()
        or "setloadoutshuffleenabled" in url.lower()
      ):
        # Log when cosmetic has been changed
        logger.info("Cosmetic Change Detected.")

      if  "client/QueryProfile?profileId=athena" in url or "client/QueryProfile?profileId=common_core" in url or "client/ClientQuestLogin?profileId=athena" in url and self.server.app.config.get("EveryCosmetic"):
        text = flow.response.get_text()
        athenaFinal = ujson.loads(text)
        athenaFinal["profileChanges"][0]["profile"]["items"].update(self.server.app.athena)  # Add items to current athena
        flow.response.text = ujson.dumps(athenaFinal)

      if (
        "https://fngw-mcp-gc-livefn.ol.epicgames.com/fortnite/api/game/v2/matchmakingservice/ticket/player"
        in flow.request.pretty_url
        and self.server.app.playlist
      ):
        logger.info("Matchmaking:")
        print_json(flow.response.text)  # Return matchmaking info.

      if "/lightswitch/api/service/bulk/status" in url.lower():
        # Launch Fortnite During Downtimes.
        status = [
          {
            "serviceInstanceId": "fortnite",
            "status": "UP",
            "message": "fortnite is up.",
            "maintenanceUri": None,
            "overrideCatalogIds": ["a7f138b2e51945ffbfdacc1af0541053"],
            "allowedActions": ["PLAY", "DOWNLOAD"],
            "banned": False,
            "launcherInfoDTO": {
              "appName": "Fortnite",
              "catalogItemId": "4fe75bbc5a674f4f9b356b5c90567da5",
              "namespace": "fn",
            },
          }
        ]
        dump = ujson.dumps(status)
        flow.response.text = dump

      if self.server.app.name:
        # Replace Old Name with New Name
        nameOld, nameNew = list(self.server.app.nameId.items())[0]
        if flow.response is not None and flow.response.text is not None:
          flow.response.text = flow.response.text.replace(
            nameOld, nameNew
          )

      if "/lfg/fortnite/tags" in url.lower() and invite:
        self.server.app.config["InviteExploit"]["users"]
        flow.response.text = ujson.dumps({"users": users})
        logger.info(url)

    except Exception as e:
      logger.error(e)


class MitmproxyServer:
  def __init__(self, app: "PirxcyProxy", loop: asyncio.AbstractEventLoop):
    try:
      self.app = app
      self.loop = loop
      self.running = False
      self.task = None
      self.stopped = asyncio.Event()
      self.options = mitmoptions(
        listen_host="127.0.0.1",
        listen_port=8080,
        showhost=False,
      )
      self.m = DumpMaster(
        options=self.options,
        with_dumper=False,
        loop=self.loop,
        with_termlog=False,
      )
      self.m.addons.add(Addon(self)) # type: ignore
    except KeyboardInterrupt:
      pass

  def run_mitmproxy(self):
    self.running = True
    try:
      set_title(f"{appName} (CTRL+C To Close Proxy)")
      # asyncio.create_task(app.updateRPC(state="Running Proxy"))
      logger.info("Proxy Online")
      self.task = asyncio.create_task(self.m.run())
    except KeyboardInterrupt:
      pass

  def start(self):
    self.running = True
    set_title(f"{appName} (CTRL+C To Close Proxy)")
    # asyncio.create_task(app.updateRPC(state="Running Proxy"))
    try:
      self.run_mitmproxy()
      proxy_toggle(True)
      logger.info("Proxy Online")
    except TypeError:
      if self.task:
        self.task.cancel()
      self.task = None
      self.stopped.set()
      return self.stop()

  def stop(self):
    self.running = False
    try:
      self.m.shutdown()
    except AssertionError:
      return "Unable to Close Proxy"

    proxy_toggle(enable=False)
    return True


class PirxcyProxy:
  def __init__(self, loop: asyncio.AbstractEventLoop | None=None, configFile: str = "config.json", client_id: int=1228345213161050232):
    self.loop = loop or asyncio.get_event_loop()
    self.ProxyEnabled = False
    self.configFile = configFile
    self.appauthor = "@pirxcy on Discord"
    self.contributors = ["@kikodev"]
    self.appVersion = semver.Version.parse("2.0.0")
    self.client_id = client_id
    self.mitmproxy_server = MitmproxyServer(app=self, loop=self.loop)

    # Set all configurations to false before reading config
    self.running = False
    self.name = False
    self.nameId = {}
    self.athena = {}
    self.playlist = False
    self.playlistId = {}

    self.config = {}

  async def __async_init__(self):
    """
    Async initializer
    """
    asyncio.create_task(self.connectRPC())

    try:
      async with aiofiles.open(self.configFile) as f:
        self.config = ujson.loads(await f.read())      
    except: 
      pass
    
    if self.config.get("EveryCosmetic"): 
      self.athena = await self.buildAthena()


  async def needsUpdate(self):
    """
    Checks if the application needs to be updated by comparing its version with the latest version available on GitHub.

    This method sends a request to the specified URL to fetch the latest version number of the application.
    If the current version of the application is older than the version obtained from the server, it returns True,
    indicating that an update is needed. Otherwise, it returns False.

    Returns:
      bool: True if an update is needed, False otherwise.

    Raises:
      aiohttp.ClientError: If an error occurs while making the HTTP request.
      ValueError: If the version number retrieved from the server is not a valid float.
    """

    if self.config.get("updateSkip", False):
      return False

    async with aiohttp.ClientSession() as session:
      async with session.get(
        "https://raw.githubusercontent.com/PirxcyFinal/PirxcyProxyFinal/main/VERSION"
      ) as request:
        response = await request.text()
    try:
      self.appVersionServer = semver.Version.parse(response.strip())
    except:
      return False

    return self.appVersion < self.appVersionServer

  async def connectRPC(self):
    try:
      self.RPC = AioPresence(client_id=self.client_id, loop=self.loop)
      await self.RPC.connect()
    except Exception as e:
      logger.error(e)

  async def updateRPC(self, state: str):
    """
    Updates the Rich Presence for PirxcyProxy.

    Parameters:
      state (str): The state to be displayed in the Rich Presence.

    Returns:
      None

    The function updates the Rich Presence for PirxcyProxy, including details
    about the current state, buttons to PirxcyProxy's GitHub repository and
    releases, and images representing the application.

    Example Usage:
      await updateRPC("Playing with PirxcyProxy")
    """
    try:

      await self.RPC.update( # type: ignore
        state=state,
        buttons=[
          {
            "label": appName,
            "url": "https://github.com/PirxcyFinal/PirxcyProxyFinal/",
          }
        ],
        details=f"{appName} v{self.appVersion}",
        large_image=("https://cdnv2.boogiefn.dev/newB.gif"),
        large_text=f"{appName}",
        small_image=(
          "https://upload.wikimedia.org/wikipedia/commons/7/7c/Fortnite_F_lettermark_logo.png"
        ),
        small_text="pirxcy's car will smoke yours, remember that",
      )
    except:
      pass

    return

  def title(self):
    """
      Sets the terminal title and prints a stylized ASCII art title with app information.

    Returns:
      None

    This method sets the terminal title to the app name, then prints a stylized ASCII art title
    with the app name, version, and author centered. The ASCII art title is colored gradually from
    blue to purple. The stylized ASCII art title is printed in the terminal, followed by the app
    name and version centered, and the app author's name centered below.
    """
    set_title(f"{appName}")
    text = """
  ██▓███   ██▓ ██▀███  ▒██   ██▒ ▄████▄▓██   ██▓
  ▓██░  ██▒▓██▒▓██ ▒ ██▒▒▒ █ █ ▒░▒██▀ ▀█ ▒██  ██▒
  ▓██░ ██▓▒▒██▒▓██ ░▄█ ▒░░  █   ░▒▓█  ▄ ▒██ ██░
  ▒██▄█▓▒ ▒░██░▒██▀▀█▄   ░ █ █ ▒ ▒▓▓▄ ▄██▒░ ▐██▓░
  ▒██▒ ░  ░░██░░██▓ ▒██▒▒██▒ ▒██▒▒ ▓███▀ ░░ ██▒▓░
  ▒▓▒░ ░  ░░▓  ░ ▒▓ ░▒▓░▒▒ ░ ░▓ ░░ ░▒ ▒  ░ ██▒▒▒ 
  ░▒ ░    ▒ ░  ░▒ ░ ▒░░░   ░▒ ░  ░  ▒  ▓██ ░▒░ 
  ░░    ▒ ░  ░░   ░  ░  ░  ░     ▒ ▒ ░░  
      ░   ░    ░  ░  ░ ░   ░ ░   
                ░     ░ ░   
  """
    faded = ""
    red = 29
    for line in center(text).splitlines():
      faded += f"\033[38;2;{red};0;220m{line}\033[0m\n"
      if not red == 255:
        red += 15
        if red > 255:
          red = 255
    cls()
    print(faded)
    print(center(f"{appName} v{self.appVersion}"))
    print(center(f"Made by {self.appauthor}"))
    print()

  async def buildAthena(self):
    set_title(f"{appName} Storing Cosmetics")
    asyncio.create_task(self.updateRPC(state="Storing Cosmetics"))

    async with aiohttp.ClientSession() as session:
      async with session.get(
        "https://fortniteapi.io/v2/items/list",
        headers={"Authorization": self.config.get("apiKey")},
      ) as request:
        response = await request.json()

    base = {}
    for item in response["items"]:

      if item.get("styles"): 
        return #add variant support later
      
      templateId = itemTypeMap.get(item["type"]["id"]) + ":" + item["id"]

      itemTemplate = {
          templateId : {
          "templateId": templateId,
          "quantity": 1,
          "attributes": {
            "creation_time": None,
            "archived": False,
            "favorite": True if item["id"].lower().startswith("cid_028") else False,
            "variants": [],
            "item_seen": False,
            "giftFromAccountId": "4735ce9132924caf8a5b17789b40f79c",
          },
        }
      }
      base.update(itemTemplate)
    logger.info(f"Stored {len(response['items'])} cosmetics.")
    self.athena = base
    return base

  def options(self):
    return {
      (
        "Enable Proxy" if not self.ProxyEnabled else "Disable Proxy"
      ): "SET_PROXY_TASK",
      (
        "Configure Custom Display Name"
        if not self.name
        else "Remove Display Name Configuration"
      ): "SET_NAME_TASK",
      (
        "Configure Playlist Swap"
        if not self.playlist
        else "Remove Playlist Configuration"
      ): "SET_PLAYLIST_TASK",
      f"Exit {appName}": "EXIT_TASK",
    }

  async def exec_command(self, option: str):
    options = self.options()
    if option not in options.values():
      return f"Invalid option {option}."
    match option:
      case "SET_PROXY_TASK":
        if self.running:
          return self.mitmproxy_server.stop()

        try:
          self.mitmproxy_server.start()
          await self.mitmproxy_server.stopped.wait()
        except:
          self.running = False
          self.mitmproxy_server.stop()

      case "SET_NAME_TASK":
        self.name = not self.name
        if not self.name:
          self.nameId = {}
          return
        old = input(f"[+] Current Name: ")
        new = input(f"[+] Enter New Display Name to Replace {old}: ")
        self.nameId[old] = new

      case "SET_PLAYLIST_TASK":
        self.playlist = not self.playlist
        if not self.playlist:
          self.playlistId = {}
          return
        new = input(
          f"[+] Enter New Playlist To Overide {self.config.get('Playlist')}: "
        )
        self.playlistId[self.config.get("Playlist", "")] = new
      case "EXIT_TASK":
        cls()
        sys.exit(0)
      case _: pass

  async def checks(self):
    logger.info("Performing Checks... (this shit should be quick)")

    needs_update = await self.needsUpdate()
    if needs_update:
      logger.info(
        f"You're on v{self.appVersion},\nUpdate to v{self.appVersionServer} via Github to continue."
      )
      input()
      sys.exit(1)

  async def main(self):
    cls()
    proxy_toggle(enable=False)
    await self.checks()
    await aprint(
      center(crayons.blue(f"Starting  {appName}...")),
      delay=0.089 # type: ignore
    )

    while True:
      asyncio.create_task(self.updateRPC(state="Main Menu"))
      self.title()

      choices = self.options()
      index: int = survey.routines.select( # type: ignore
        f"Welcome to {appName}\nChoose an option:",
        options=list(choices.keys()),
        focus_mark="➤ ",
        evade_color=survey.colors.basic("magenta"),
      )
      command = list(choices.values())[index]
      self.title()
      try:
        error = await self.exec_command(command)
      except Exception as e:
        error = e

  def run(self):
    return self.main()

  @staticmethod
  async def new():
    cls = PirxcyProxy()
    await cls.__async_init__()
    return cls


if __name__ == "__main__":

  async def main():
    app = await PirxcyProxy.new()
    await app.run()

  asyncio.run(main())
