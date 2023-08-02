#!/bin/bash

#0 1,9 * * * /bin/bash /home/ec2-user/ad-data-analysis/run_report.sh 3
#0 * * * * /bin/bash /home/ec2-user/ad-data-analysis/run_report.sh

# 获取脚本的相对路径
script_relative_path="$0"

# 提取脚本所在的目录部分
script_directory=$(dirname "$script_relative_path")

# shellcheck disable=SC2164
cd $script_directory/script/src

# 获取传入的第一个参数
if [ $# -eq 0 ]; then
    python3 -m analysis.tiktok_report_hourly
    python3 -m analysis.adsense_report
    python3 -m analysis.analytic_report
    python3 -m analysis.tiktok_report
else
    param1=$1
    python3 -m analysis.tiktok_report_hourly $param1
    python3 -m analysis.adsense_report $param1
    python3 -m analysis.analytic_report $param1
    python3 -m analysis.tiktok_report $param1
fi

