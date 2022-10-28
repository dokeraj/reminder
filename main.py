import calendar
from datetime import datetime
import configInit
import util

from apscheduler.schedulers.background import BlockingScheduler

# Creates a default Background Scheduler
sched = BlockingScheduler()


def mainFortnight(msg, weekType, discordApiKey):
    my_date = datetime.today()
    year, week_num, day_of_week = my_date.isocalendar()

    # check to see if the weekType is 'even' or 'odd'
    if weekType.lower() == 'even' and week_num % 2 == 0:
        startMainProcess(msg, discordApiKey)

    elif weekType.lower() == 'odd' and week_num % 2 != 0:
        startMainProcess(msg, discordApiKey)
    else:
        print(
            f"\n\nINFO - Fortnight notification will not be pushed. Reason: The config file has been set to '{weekType}' week type and now we're in week number {week_num}.\n")


def mainLastDayOfMonth(msg, discordApiKey):
    # check to see if it is in fact the last day of the month - and if so, then allow the schedule to take place
    today = datetime.today()
    curDay = today.day
    daysInCurMonth = calendar.monthrange(today.year, today.month)[1]

    if daysInCurMonth == curDay:
        startMainProcess(msg, discordApiKey)


def startMainProcess(msg, discordApiKey):
    print(f"\n\nPosting reminder now..\n {msg}")
    util.notifyUser(2903955, discordApiKey, None, msg)


def main():
    print(f"STARTING reminder SCRIPT!")

    config = configInit.initConfig()
    scheduler = BlockingScheduler({'apscheduler.timezone': config.tz})

    for cronJob in config.cron:
        scheduler.add_job(startMainProcess, args=(cronJob.message, config.discordApiKey), trigger='cron',
                          minute=cronJob.minute,
                          hour=cronJob.hour, day=cronJob.day, month=cronJob.month,
                          day_of_week=cronJob.dayOfWeek)

    for lastDayJob in config.lastDayOfMonthSchedule:
        scheduler.add_job(mainLastDayOfMonth, args=(lastDayJob.message, config.discordApiKey), trigger='cron',
                          minute=lastDayJob.minute,
                          hour=lastDayJob.hour, day='*', month='*',
                          day_of_week='*')

    if config.fortnight is not None:
        scheduler.add_job(mainFortnight,
                          args=(config.fortnight.message, config.fortnight.weekType, config.discordApiKey),
                          trigger='cron',
                          minute=config.fortnight.minute,
                          hour=config.fortnight.hour, day='*', month='*',
                          day_of_week=config.fortnight.dayOfWeek)

    print("\nAll setup - now waiting for the time to come to show the reminder!")
    scheduler.start()


main()
