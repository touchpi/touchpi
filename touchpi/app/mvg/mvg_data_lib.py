from touchpi.appbase.app import log, settings
from requests import get
from datetime import datetime


def get_url_data(request):
    r = get(request)
    log.debug("URL Response: " + str(r) + " of request: " + str(request))
    return r


def get_rawdata():
    departure1_raw_data = ""
    departure2_raw_data = ""
    try:
        departure1_raw_data = get_url_data(settings.mvg_public_transport_url1)
        departure2_raw_data = get_url_data(settings.mvg_public_transport_url2)
    except Exception as err:
        log.error("Error in URL request: " + str(err) + " " + str(type(err)))
        if type(departure1_raw_data) is not str:
            log.error("Response 1: " + str(departure1_raw_data.content))
        else:
            log.error("Response 1: " + str(departure1_raw_data))
        if type(departure2_raw_data) is not str:
            log.error("Response 2: " + str(departure2_raw_data.content))
        else:
            log.error("Response 2: " + str(departure2_raw_data))
        raise ValueError("URL request failed")
    else:
        return departure1_raw_data, departure2_raw_data


def convert_rawdata(data):
    try:
        d1 = data[0].json()
        d2 = data[1].json()

        # departure times of first part of public transportation
        log.debug("Origin data of first transport  " + str(d1))
        d1 = [d for d in d1 if d['destination'] in settings.mvg_possible_destination1]
        d1 = [d for d in d1 if d['cancelled'] in [False]]
        del d1[5:]
        log.debug("Filtered data of first transport: " + str(d1))

        # departure times of second part of public transportation
        log.debug("Origin data of second transport : " + str(d2))
        d2 = [d for d in d2 if d['destination'] in settings.mvg_possible_destination2]
        d2 = [d for d in d2 if d['cancelled'] in [False]]
        del d2[5:]
        log.debug("Filtered data of second transport: " + str(d2))

        departures = [[], []]
        for d in d1:
            minutes = round(
                (datetime.fromtimestamp(d['realtimeDepartureTime'] / 1000) - datetime.now()).total_seconds() / 60)
            departures[0].append(minutes)
        for d in d2:
            minutes = round(
                (datetime.fromtimestamp(d['realtimeDepartureTime'] / 1000) - datetime.now()).total_seconds() / 60)
            departures[1].append(minutes)
        log.info("Departure times to come in minutes: " + str(departures))
    except Exception as err:
        log.error("Error in converting rawdata: " + str(err) + " " + str(type(err)))
        raise ValueError("Converting data failed")
    else:
        return departures
