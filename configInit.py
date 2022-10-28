import sys
from dataclasses import dataclass
from os import path

from environs import Env

import util
import yaml


@dataclass
class ConfSchedule:
    message: str
    month: str
    day: str
    hour: int
    minute: int
    dayOfWeek: str


@dataclass
class ConfTime:
    message: str
    hour: int
    minute: int


@dataclass
class FortniteSchedule:
    message: str
    weekType: str
    hour: int
    minute: int
    dayOfWeek: str


@dataclass
class Config:
    tz: str
    discordApiKey: str
    cron: list[ConfSchedule]
    lastDayOfMonthSchedule: list[ConfTime]
    fortnight: FortniteSchedule


conf = Config(None, None, list(), list(), None)


def extractCronTimeArray(item):
    cronSchedule = ConfSchedule(None, None, None, None, None, None)
    for croneKey, cronVal in item.items():
        if croneKey == "message":
            if cronVal != "<INPUT YOUR REMINDER HERE>":
                cronSchedule.message = cronVal
            else:
                errMsg = "ERROR: Cron Reminder message is not setup! Put your CRON reminder message!"
                print(f"{errMsg} Now exiting!")
                sys.exit()
        if croneKey == "month":
            if str(cronVal).isdigit() or cronVal == "*":
                monthInt = util.safeCast(cronVal, int, "*")
                cronSchedule.month = monthInt
            else:
                errMsg = "ERROR: Month time format is not valid! Please use a number!"
                print(f"{errMsg} Now exiting!")
                sys.exit()

        if croneKey == "time":
            if util.isTimeFormat(cronVal):
                hour, minute = util.extractHourAndMinute(cronVal)
                cronSchedule.hour = hour
                cronSchedule.minute = minute
            else:
                errMsg = "ERROR: Weekly time format is not valid! Please use HH:mm format! Don't forget to wrap the time in quotes in the yaml file"
                print(f"{errMsg} Now exiting!")
                sys.exit()

        if croneKey == "day":
            if str(cronVal).isdigit() or cronVal == "*":
                dayInt = util.safeCast(cronVal, int, "*")
                cronSchedule.day = dayInt
            else:
                errMsg = "ERROR: Day format is not valid! Please use a number!"
                print(f"{errMsg} Now exiting!")
                sys.exit()

        if croneKey == "day_of_week":
            if cronVal in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"] or cronVal == "*":
                cronSchedule.dayOfWeek = cronVal
            else:
                errMsg = "ERROR: Cron schedule's day_of_week is not set properly - Please use MON, TUE, WED, THU, FRI, SAT or SUN to specify the day."
                print(f"{errMsg} Now exiting!")
                sys.exit()

    return cronSchedule


def extractLastDayOfMonthArray(item):
    lastDaySchedule = ConfTime(None, None, None)
    for lastDayKey, lastDayVal in item.items():
        if lastDayKey == "message":
            if lastDayVal != "<INPUT YOUR REMINDER HERE>":
                lastDaySchedule.message = lastDayVal
            else:
                errMsg = "ERROR: Last Day Of Month Reminder message format is not setup! Put your reminder message!"
                print(f"{errMsg} Now exiting!")
                sys.exit()
        if lastDayKey == "time":
            if util.isTimeFormat(lastDayVal):
                hour, minute = util.extractHourAndMinute(lastDayVal)
                lastDaySchedule.hour = hour
                lastDaySchedule.minute = minute
            else:
                errMsg = "ERROR: Last Day Of Month time format is not valid! Please use HH:mm format! Don't forget to wrap the time in double quotes in the yaml file"
                print(f"{errMsg} Now exiting!")
                sys.exit()

    return lastDaySchedule


def printSetConfig():
    resultStr = "The following config params were set:\n"
    resultStr += f"- discord_api_key = {conf.discordApiKey}\n"

    resultStr += f"Backup Schedule:\n"
    if conf.cron is not None:
        for idx, item in enumerate(conf.cron):
            resultStr += f"\t---- cron {idx + 1} ----\n"
            resultStr += f"\t- cron.message = {item.message}\n"
            resultStr += f"\t- cron.month = {item.month}\n"
            resultStr += f"\t- cron.day = {item.day}\n"
            resultStr += f"\t- cron.hour = {item.hour}\n"
            resultStr += f"\t- cron.minute = {item.minute}\n"
            resultStr += f"\t- cron.dayOfWeek = {item.dayOfWeek}\n"
            resultStr += "\n\n"

    if conf.lastDayOfMonthSchedule is not None:
        for idx, item in enumerate(conf.lastDayOfMonthSchedule):
            resultStr += f"\t---- last_day_of_month {idx + 1} ----\n"
            resultStr += f"\t- last_day_of_month.message = {item.message}\n"
            resultStr += f"\t- last_day_of_month.hour = {item.hour}\n"
            resultStr += f"\t- last_day_of_month.minute = {item.minute}\n"
            resultStr += "\n\n"

    if conf.fortnight is not None:
        resultStr += f"\t---- fortnight ----\n"
        resultStr += f"\t- fortnight.message = {conf.fortnight.message}\n"
        resultStr += f"\t- fortnight.week_type = {conf.fortnight.weekType}\n"
        resultStr += f"\t- fortnight.hour = {conf.fortnight.hour}\n"
        resultStr += f"\t- fortnight.minute = {conf.fortnight.minute}\n"
        resultStr += f"\t- fortnight.dayOfWeek = {conf.fortnight.dayOfWeek}\n"
        resultStr += "\n\n"

    resultStr += "\n\nNOTE: DON'T FORGET THAT IF YOU MAKE ANY CHANGE TO THE YAML FILE - YOU WILL NEED TO RESTART THIS CONTAINER!!"
    print(resultStr)


def initConfig():
    try:
        if path.exists('/yaml/config.yml'):
            with open('/yaml/config.yml') as f:
                docs = yaml.load_all(f, Loader=yaml.FullLoader)

                for doc in docs:
                    for k, v in doc.items():
                        if k == "general_settings" and v is not None:
                            for generalKey, generalVal in v.items():
                                if generalKey == "discord_api_key" and generalVal != "<INSERT YOUR DISCORD WEBHOOK API KEY>":
                                    conf.discordApiKey = generalVal

                        # cron Schedule
                        if k == "reminder_schedule" and v is not None:
                            for reminderScheduleKey, reminderScheduleVal in v.items():
                                if reminderScheduleKey == "cron" and reminderScheduleVal is not None:
                                    for cronItem in reminderScheduleVal:
                                        conf.cron.append(extractCronTimeArray(cronItem))

                                if reminderScheduleKey == "last_day_of_month" and reminderScheduleVal is not None:
                                    for lastDayItem in reminderScheduleVal:
                                        conf.lastDayOfMonthSchedule.append(extractLastDayOfMonthArray(lastDayItem))

                        if k == "fortnight_schedule" and v is not None:
                            fortniteSchedule = FortniteSchedule(None, None, None, None, None)
                            for fortnightItem, reminderScheduleVal in v.items():
                                if fortnightItem == "message":
                                    if reminderScheduleVal != "<INPUT YOUR REMINDER HERE>":
                                        fortniteSchedule.message = reminderScheduleVal
                                    else:
                                        errMsg = "ERROR: Fortnight reminder message is not setup! Put your reminder message!"
                                        print(f"{errMsg} Now exiting!")
                                        sys.exit()

                                if fortnightItem == "week_type":
                                    if reminderScheduleVal.lower() in ['even','odd']:
                                        fortniteSchedule.weekType = reminderScheduleVal
                                    else:
                                        errMsg = "ERROR: Fortnight Week Type is not set properly! Please use EVEN or ODD values"
                                        print(f"{errMsg} Now exiting!")
                                        sys.exit()

                                if fortnightItem == "time":
                                    if util.isTimeFormat(reminderScheduleVal):
                                        hour, minute = util.extractHourAndMinute(reminderScheduleVal)
                                        fortniteSchedule.hour = hour
                                        fortniteSchedule.minute = minute
                                    else:
                                        errMsg = "ERROR: Fortnight time format is not valid! Please use HH:mm format! Don't forget to wrap the time in double quotes in the yaml file"
                                        print(f"{errMsg} Now exiting!")
                                        sys.exit()

                                if fortnightItem == "day_of_week":
                                    if reminderScheduleVal in ["MON", "TUE", "WED", "THU", "FRI", "SAT",
                                                               "SUN"] or reminderScheduleVal == "*":
                                        fortniteSchedule.dayOfWeek = reminderScheduleVal
                                    else:
                                        errMsg = "ERROR: Fortnight schedule's day_of_week is not set properly - Please use MON, TUE, WED, THU, FRI, SAT or SUN to specify the day."
                                        print(f"{errMsg} Now exiting!")
                                        sys.exit()

                                conf.fortnight = fortniteSchedule

            env = Env()
            try:
                conf.tz = env('TZ')
            except Exception as e:
                errMsg = "ERROR: Timezone is not set in the docker run command/compose. You need to have it set in order for the sync to be executed on time."
                print(f"{errMsg} Now exiting!")
                sys.exit()

            printSetConfig()
            return conf

        else:
            errMsg = "ERROR: config.yml file not found (please bind the volume that contains the config.yml file)"
            print(f"{errMsg} - now exiting!")
            sys.exit()

    except Exception as e:
        errMsg = "ERROR: config.yml file is not a valid yml file"
        print(f"{errMsg} - now exiting!", e)
        sys.exit()
