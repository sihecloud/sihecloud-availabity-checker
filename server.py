import schedule
import time
import requests
import threading
import checker
import os

import datetime
import pytz

def ts_to_date_str(timestamp, format):
    dt = datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Asia/Shanghai'))
    datetime_string = dt.strftime(format)
    return datetime_string


def do_check():
    for item_key in checker.items.keys():
        checker.check_and_log(item_key)





def startWebServer():
    from flask import Flask
    from flask import request, redirect, send_file
    app = Flask(__name__,
                static_url_path='',
                static_folder='static/'
                )

    @app.route('/', methods=['GET'])
    def index():
        return redirect("/index.html", code=302)

    @app.route('/heatmap/by_date/<item_key>', methods=['GET'])
    def get_heat_map_by_date(item_key):
        ts_list = checker.read_log(item_key)
        print(ts_list)
        # reduce into 5min buckets
        ts_list = list(set([x // 300 * 300 for x in ts_list]))
        print(ts_list)
        date_map = {}
        for ts in ts_list:
            date = ts_to_date_str(ts, '%Y-%m-%d')
            if date not in date_map:
                date_map[date] = 0
            date_map[date] += 1
        # assume that check for every 5 minutes.
        return {
            "series": [(date, value / 12 / 24 * 100) for date, value in date_map.items()]
        }

    @app.route('/heatmap/recent/<item_key>', methods=['GET'])
    def get_heat_map_recently(item_key):
        from datetime import datetime, timedelta
        now = datetime.now()
        N_DAYS = 7
        last_week = now - timedelta(days=N_DAYS)

        # 设置时间为0时0分0秒
        begin_date = datetime(last_week.year, last_week.month, last_week.day, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
        threshold_ts = int(begin_date.timestamp())

        days = [
            (now - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(N_DAYS, -1, -1)
        ]
        hours = [f'{x:02d}:00' for x in range(24)]


        ts_list = checker.read_log(item_key)
        # reduce into 5min buckets
        ts_list = list(set([x // 300 * 300 for x in ts_list]))

        ts_list = [ x for x in ts_list if x >= threshold_ts]
        date_hour_map = {}
        for ts in ts_list:
            date_hour = ts_to_date_str(ts, '%Y-%m-%d %H') + ":00"
            if date_hour not in date_hour_map:
                date_hour_map[date_hour] = 0
            date_hour_map[date_hour] += 1

        series = []
        for date_hour, value in date_hour_map.items():
            # assume that check for every 5 minutes.
            pct = value / 12 * 100
            date, hour = date_hour.split(" ")
            series.append((hours.index(hour), days.index(date), pct))

        return {
            "days": days,
            "hours": hours,
            "series": series
        }


    app.run(host='0.0.0.0', port=7000)


if __name__ == '__main__':
    t = threading.Thread(target=startWebServer, args=tuple())
    t.daemon = True
    t.start()

    schedule.every(1).minutes.do(do_check)
    while True:
        schedule.run_pending()
        time.sleep(1)
