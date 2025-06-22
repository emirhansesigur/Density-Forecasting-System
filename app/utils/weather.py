import requests

def get_weather_for_datetime_daily(latitude, longitude, dt, timezone="Europe/Istanbul"):
    """
    Belirtilen tarih ve saat için sıcaklık, nem ve yağış değerlerini döndürür.
    dt: datetime.datetime nesnesi
    """

    # Sadece tarih kısmını al (örnek: "2025-06-23")
    date_str = dt.date().isoformat()

    HOURLY_PARAMS = [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation"
    ]
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly={','.join(HOURLY_PARAMS)}"
        f"&start_date={date_str}"
        f"&end_date={date_str}"
        f"&timezone={timezone.replace('/', '%2F')}"
    )

    response = requests.get(url)
    data = response.json()


    # Tüm saatlik verileri döndür
    return data



def get_weather_for_date_hourly(latitude, longitude, dt, timezone="Europe/Istanbul"):
    """
    Belirtilen tarih ve saat için sıcaklık, nem ve yağış değerlerini döndürür.
    dt: datetime.datetime nesnesi
    """
    HOURLY_PARAMS = [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation"
    ]
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly={','.join(HOURLY_PARAMS)}"
        #f"&forecast_days=7"
        f"&timezone={timezone.replace('/', '%2F')}"
    )
    response = requests.get(url)
    data = response.json()


    # Saatlik verileri al
    times = data['hourly']['time']
    temperatures = data['hourly']['temperature_2m']
    humidities = data['hourly']['relative_humidity_2m']
    precipitations = data['hourly']['precipitation']
    # dt'yi ISO formatına çevir (örn: "2025-07-01T12:00")
    dt_str = dt.strftime("%Y-%m-%dT%H:00")
    if dt_str in times:
        idx = times.index(dt_str)
        temperature = temperatures[idx]
        humidity = humidities[idx]
        precipitation = precipitations[idx]
        print(f"Weather for {dt_str}: {temperature}°C, {humidity}%, {precipitation}mm")
        return {
            "temperature": temperature,
            "humidity": humidity,
            "precipitation": precipitation
        }
    else:
        raise ValueError(f"{dt_str} için hava durumu verisi bulunamadı.")
