import time
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


def extractHourAndMinute(inputTime):
    datetime = time.strptime(str(inputTime), '%H:%M')
    return datetime.tm_hour.real, datetime.tm_min.real


def isTimeFormat(inputTime):
    try:
        time.strptime(str(inputTime), '%H:%M')
        return True
    except Exception as e:
        return False


def safeCastBool(val, default=False):
    try:
        return str(val).lower() in ['true', '1', 'y', 'yes']
    except Exception as e:
        return default


def safeCast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def getCurrentDateTime():
    timestamp = int(round(time.time()))
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def fixString(inStr: str):
    filtered_characters = list(s for s in inStr if s.isprintable())
    fixed = ''.join(filtered_characters)
    return fixed.replace("'", "\"")


def notifyUser(color, discordApkiKey, titleMsg=None, descMsg=None):
    webhook = DiscordWebhook(url=discordApkiKey)

    embedColor = color
    if titleMsg is not None and descMsg is None:
        embed = DiscordEmbed(title=titleMsg, color=embedColor)
    elif titleMsg is None and descMsg is not None:
        embed = DiscordEmbed(description=descMsg, color=embedColor)
    elif titleMsg is not None and descMsg is not None:
        embed = DiscordEmbed(title=titleMsg, description=descMsg, color=embedColor)

    webhook.add_embed(embed)

    try:
        webhook.execute()
    except Exception as e:
        print("ERROR: discord Url is not valid - you will still be getting info in the container logs!")