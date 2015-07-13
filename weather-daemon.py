#!/usr/bin/python
import time
import pymysql
import datetime
import urllib2
import progressbar
import threading
import json

def fetch_city_weather_report(url):
    retry_count = 0
    while retry_count < 4:
        try:
            call = urllib2.urlopen(url)
            response = call.read()
            update_city_dict(json.loads(response))
            break
        except:
            retry_count += 1
            time.sleep(retry_count*10)
    else:
        print "problem in url: ", url
    return

def sort_the_list_from_the_website_by_countries(item):
    item = item.split('\n')
    for i, line in enumerate(item):
        item[i] = line.split('\t')
    del item[len(item)-1]
    del item[0]
    item = sorted(item, key=lambda x: x[4])
    return item

def check_and_insert_countries(data):
    db = pymysql.connect(host="localhost", user="root", passwd="renton872")
    curs = db.cursor()
    for line in data:
        curs.execute("SELECT country_name FROM weather.countries where country_name = %s", (line[4]))
        result1 = curs.fetchall()
        if not result1:
            curs.execute("insert into weather.countries (country_name) values (%s)", (line[4]))
    db.close()

def update_city_dict(response):
    global cities_dict
    global finish_count
    global update_list
    global error_count
    global total_time
    try:
        cities_dict[response['sys']['country']][response['name']]['weather']['temperature'] = response['main']['temp']
        cities_dict[response['sys']['country']][response['name']]['weather']['humidity'] = response['main']['humidity']
        cities_dict[response['sys']['country']][response['name']]['weather']['clouds'] = response['clouds']['all']
        cities_dict[response['sys']['country']][response['name']]['weather']['wind_speed'] = response['wind']['speed']
        cities_dict[response['sys']['country']][response['name']]['weather']['wind_deg'] = response['wind']['deg']
        cities_dict[response['sys']['country']][response['name']]['weather']['max_temp'] = response['main']['temp_max']
        cities_dict[response['sys']['country']][response['name']]['weather']['min_temp'] = response['main']['temp_min']
        cities_dict[response['sys']['country']][response['name']]['weather']['pressure'] = response['main']['pressure']
        cities_dict[response['sys']['country']][response['name']]['end_time'] = time.clock()
        run_time = cities_dict[response['sys']['country']][response['name']]['end_time'] - cities_dict[response['sys']['country']][response['name']]['start_time']
        finish_count += 1
        total_time += run_time
        update_list.append((response['sys']['country'], response['name']))
    except:
        error_count += 1

def get_the_list_of_cities_and_ids_from_the_website():
    print "Fetching the list of cities from the web"
    call = urllib2.urlopen("http://openweathermap.org/help/city_list.txt")
    return call.read()

def create_cities_dict(city_list):
    global city_count
    global place_holder
    global cities
    cities = {}
    for line in city_list:
        if line[4] not in cities:
            cities[line[4]] = {}
        cities[line[4]][line[1]] = {'url' : "http://api.openweathermap.org/data/2.5/weather?id=%s" % line[0], 'id' : line[0], 'country' : line[4], 'name' : line[1], 'weather' : {}}
    return cities

def update_city_in_db(city, curs):
    try:
        curs.execute("SELECT country_id FROM weather.countries where country_name = %s", (city['country']))
        result = curs.fetchall()
        curs.execute("select city_name, country_id from weather.cities where (city_name = %s and country_id = %s)", (city['name'], result))
        city_check = curs.fetchall()
        if not city_check:
            curs.execute(
                "insert into weather.cities (city_name, country_id, data_key, temperature, humidity, clouds, wind_speed, wind_deg, max_temp, min_temp, pressure) "
                "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)",
                (city['name'], result, city['id'], city['weather']['temperature'], city['weather']['humidity'], city['weather']['clouds'], city['weather']['wind_speed'], city['weather']['wind_deg'], city['weather']['max_temp'], city['weather']['min_temp'], city['weather']['pressure'])
            )
        else:
            curs.execute(
                "update weather.cities "
                "set temperature = %s, humidity = %s, clouds = %s, wind_speed = %s, wind_deg = %s, max_temp = %s, min_temp = %s, pressure = %s "
                "where (city_name = %s and country_id = %s) ",
                (city['weather']['temperature'], city['weather']['humidity'], city['weather']['clouds'], city['weather']['wind_speed'], city['weather']['wind_deg'], city['weather']['max_temp'], city['weather']['min_temp'], city['weather']['pressure'], city['name'], result)
            )
        current_time = datetime.datetime.now()
        curs.execute(
            "update weather.cities "
            "set last_update = %s "
            "where(city_name = %s and country_id = %s) ",
            (current_time, city['name'], result)
        )
    except:
        print "failed to write to db, city:", city['name'], 'city id:', city['id']

def write_some_of_the_cities_to_db(ready_list, curs, partial_city_dict):
    try:
        for item in ready_list:
            update_city_in_db(partial_city_dict[item[0]][item[1]], curs)
        return ready_list
    except:
        print "Failed to update bunch"

def eta(city_count, total_time):
    global cities_updated_today
    global error_count
    avg_time = total_time / float(city_count - cities_updated_today)
    time_left = (74071.0 - city_count - error_count)*avg_time
    return str(datetime.timedelta(seconds=int(time_left)))

def estimate_complete_percentage(city_count, total):
    perc = city_count*100/total
    return str(perc)

def send_requests_and_update_to_db(data_list):
    global finish_count
    global cities_dict
    global update_list
    global error_count
    global total_time
    global cities_updated_today
    error_count = 0
    place_holder = 0
    city_count = 0
    finish_count = 0
    total_time = 0.0
    update_list = []
    cities_updated_today = 0
    db = pymysql.connect(host="localhost", user="root", passwd="renton872")
    curs = db.cursor()
    thread_list = [""]*20
    print "Starting to update\n"
    time.sleep(0.1)
    update_time_counter = time.clock()
    try:
        widgets = ['db update progress: ', progressbar.FormatLabel(''),'%', ' ', progressbar.Bar(marker=progressbar.RotatingMarker()),
           ' ', 'time left: ', progressbar.FormatLabel('')]
        pbar = progressbar.ProgressBar(widgets=widgets, maxval=74071).start()
        while city_count < len(data_list):
            temp_list = [""]*20
            for i,item in enumerate(thread_list):
                if item == "" or not item.is_alive():
                    city_count += 1
                    curs.execute("SELECT country_id FROM weather.countries where country_name = %s", (data_list[city_count -1][4]))
                    result = curs.fetchall()
                    curs.execute("select last_update from weather.cities where (city_name = %s and country_id = %s)", (data_list[city_count -1][1], result))
                    city_last_update = curs.fetchall()
                    try:
                        if city_last_update and (datetime.datetime.now() - datetime.datetime.strptime(city_last_update[0][0], "%Y-%m-%d %H:%M:%S.%f")).total_seconds() < 3600:
                            cities_updated_today += 1
                            finish_count += 1
                        else:
                            cities_dict[data_list[city_count -1][4]][data_list[city_count -1][1]]['start_time'] = time.clock()
                            new_thread = threading.Thread(target= fetch_city_weather_report, args=(cities_dict[data_list[city_count -1][4]][data_list[city_count -1][1]]['url'],))
                            new_thread.start()
                            temp_list[i-1] = new_thread
                    except:
                        cities_dict[data_list[city_count -1][4]][data_list[city_count -1][1]]['start_time'] = time.clock()
                        new_thread = threading.Thread(target= fetch_city_weather_report, args=(cities_dict[data_list[city_count -1][4]][data_list[city_count -1][1]]['url'],))
                        new_thread.start()
                        temp_list[i-1] = new_thread
                else:
                    temp_list[i-1] = item
            thread_list = temp_list
            if len(update_list) > 100:
                cities_to_remove = write_some_of_the_cities_to_db(update_list, curs, cities_dict)
                db.commit()
                update_list = filter(lambda x:x not in cities_to_remove, update_list)
            if time.clock() - update_time_counter > 2:
                widgets[1] = progressbar.FormatLabel(('%s' %estimate_complete_percentage(city_count, len(data_list))).format(city_count))
                widgets[7] = progressbar.FormatLabel(('%s' %eta(city_count, total_time)).format(city_count))
                pbar.update(city_count)
                update_time_counter = time.clock()
            time.sleep(0.5)
        if update_list:
            for item in update_list:
                update_city_in_db(cities_dict[item[0]][item[1]], curs)
            update_list = []
    except:
        print "error :("
    finally:
        print "\n"
        if cities_updated_today == len(data_list):
            print "Update done, all cities are up to date"
        else:
            print "Update stopped, out of", len(data_list), "cities:"
            print "updated cities:", finish_count - cities_updated_today, "cities up to date:", cities_updated_today, "cities that failed to update:", error_count
        db.commit()
        db.close()

def main():
    global finish_count
    global cities_dict
    global update_list
    global error_count
    global total_time
    global cities_updated_today
    running = True
    raw_data = get_the_list_of_cities_and_ids_from_the_website()
    data = sort_the_list_from_the_website_by_countries(raw_data)
    cities_dict = create_cities_dict(data)
    check_and_insert_countries(data)
    send_requests_and_update_to_db(data)


main()





