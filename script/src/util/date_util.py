#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import re
import time
import calendar
from dateutil.relativedelta import relativedelta


def yesterday():
  return someday(1)


def today():
  return someday(0)


def tomorrow():
  return someday(-1)


def someday(days_ago):
  return (datetime.datetime.utcnow() - datetime.timedelta(days_ago)).strftime(
      "%Y-%m-%d")


def someday_from_day(day, days_ago):
  target_day = datetime.datetime.strptime(day, "%Y-%m-%d")
  return (target_day - datetime.timedelta(days_ago)).strftime("%Y-%m-%d")


def get_year_month_day(day):
  target_day = datetime.datetime.strptime(day, "%Y-%m-%d")
  return target_day.year, target_day.month, target_day.day


def chuange_format(day, format="%Y%m%d"):
  target_day = datetime.datetime.strptime(day, "%Y-%m-%d")
  return target_day.strftime(format)
