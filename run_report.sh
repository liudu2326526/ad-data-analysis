#!/bin/bash

# shellcheck disable=SC2164
cd script/src

# 获取传入的第一个参数
if [ $# -eq 0 ]; then
    python3 -m analysis.adsense_report
    python3 -m analysis.tiktok_report_hourly
    python3 -m analysis.tiktok_report
else
    param1=$1
    python3 -m analysis.tiktok_report_hourly $param1
    python3 -m analysis.adsense_report $param1
    python3 -m analysis.analytic_report $param1
    python3 -m analysis.tiktok_report $param1
fi

