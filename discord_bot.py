import discord
from discord.ext import commands
import requests
import urllib.parse
import datetime
from settings import MySettings

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

settings = MySettings()


async def get_edt_datas(v_date):
    session = requests.Session()

    url = (
        "https://ws-edt-igs.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=G&Tel="
        + settings.username
        + "&date="
        + v_date
        + "&hashURL="
    )

    payload = {}
    headers = {
        "authority": "ws-edt-igs.wigorservices.net",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "fr",
        "sec-ch-ua": '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62",
    }

    response = session.request("GET", url, headers=headers, data=payload)

    executionToken = (
        response.text.replace('execution" value="', "µ").split("µ")[1].split('"')[0]
    )

    url = (
        "https://cas-p.wigorservices.net/cas/login?service=https%3A%2F%2Fws-edt-igs.wigorservices.net%2FWebPsDyn.aspx%3Faction%3DposEDTLMS%26serverID%3DG%26Tel%3D"
        + settings.username
        + "%26date%3D"
        + urllib.parse.quote(v_date)
        + "%26hashURL%3D"
    )

    payload = (
        "username="
        + settings.username
        + "&password="
        + urllib.parse.quote(settings.password)
        + "&execution="
        + urllib.parse.quote(executionToken)
        + "&_eventId=submit&geolocation="
    )
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "fr",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://cas-p.wigorservices.net",
        "Referer": "https://cas-p.wigorservices.net/cas/login",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62",
        "sec-ch-ua": '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    with open("dom.html", "w") as f:

        response = session.request("POST", url, headers=headers, data=payload)
        f.write(response.text)

    print("DOM successfully downloaded")

    date = v_date.split("/")
    week = datetime.date(int(date[2]), int(date[0]), int(date[1])).isocalendar().week

    with open("dom.html", "r") as f:
        with open("data.csv", "w") as d:
            for line in f.readlines():
                if 'class="TCase"' in line:
                    try:
                        eDate = "n/a"
                        match (line.split("left:"))[1].split("%")[0]:
                            case "103.1200":
                                eDate = str(
                                    datetime.date.fromisocalendar(
                                        int(date[2]), week, 1
                                    ).strftime("%d/%m/%Y")
                                )
                            case "122.5200":
                                eDate = str(
                                    datetime.date.fromisocalendar(
                                        int(date[2]), week, 2
                                    ).strftime("%d/%m/%Y")
                                )
                            case "141.9200":
                                eDate = str(
                                    datetime.date.fromisocalendar(
                                        int(date[2]), week, 3
                                    ).strftime("%d/%m/%Y")
                                )
                            case "161.3200":
                                eDate = str(
                                    datetime.date.fromisocalendar(
                                        int(date[2]), week, 4
                                    ).strftime("%d/%m/%Y")
                                )
                            case "180.7200":
                                eDate = str(
                                    datetime.date.fromisocalendar(
                                        int(date[2]), week, 5
                                    ).strftime("%d/%m/%Y")
                                )
                        # print(eDate)
                        line = (line.split("</span>"))[1].split("</table>")[0]
                        line = (
                            line.replace("<br/>", ",")
                            .replace("</td>", ",")
                            .replace("</tr>", ",")
                            .replace("<td>", ",")
                            .replace("<tr>", ",")
                            .replace('<td class="TChdeb">', ",")
                            .replace('<td class="TCSalle">', ",")
                        )
                        line = eDate + "," + line
                        final = ""
                        for i in range(len(line)):
                            try:
                                if line[i] == "," and line[i - 1] == ",":
                                    pass
                                else:
                                    final += line[i]
                            except:
                                pass

                        d.write(final[:-1] + "\n")
                    except:
                        pass


@client.event
async def on_ready():
    print("Bot's ready")
    print("-+-+-+-+-+-")


@client.command()
async def edt(ctx, arg=""):
    print("Getting datas")
    await get_edt_datas(
        datetime.date.strftime(arg, "%d/%m/%Y").strftime("%m/%d/%Y")
        if arg != ""
        else datetime.date.today().strftime("%m/%d/%Y")
    )
    date = ""
    with open("data.csv", "r") as data:
        print("Data treatment")
        for line in data.readlines():
            values = line[:-1].split(",")
            if arg == "" or arg == values[0]:

                if date != values[0]:
                    if date != "":
                        await ctx.send(embed=embed)
                    date = values[0]
                    title = "Emploi du temps " + date
                    embed = discord.Embed(title=title)
                value = values[3] + "\n" + values[4] + "\n" + values[1]
                embed.add_field(name=values[2], value=value, inline=False)

        try:
            await ctx.send(embed=embed)
        except:
            pass
    print("Done")


client.run(settings.token)
