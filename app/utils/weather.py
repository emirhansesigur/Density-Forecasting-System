import requests


def get_weather_for_datetime_daily(latitude, longitude, dt, timezone="Europe/Istanbul"):
    """
    Belirtilen tarih ve saat için sıcaklık, nem ve yağış değerlerini döndürür.
    dt: datetime.datetime nesnesi
    
    Raises:
        ConnectionError: İnternet bağlantısı yoksa
        Timeout: İstek zaman aşımına uğrarsa
        RequestException: Diğer HTTP hataları için
        ValueError: API'dan geçersiz veri gelirse
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

    
    try:
        # Timeout ekleyerek isteğin çok uzun sürmesini engelle
        response = requests.get(url, timeout=10)
        
        # HTTP hata kodlarını kontrol et
        response.raise_for_status()
        
        # JSON parse etmeye çalış
        data = response.json()
        
        # API'dan beklenen verilerin gelip gelmediğini kontrol et
        if 'hourly' not in data:
            raise ValueError("API'dan beklenen veri formatı alınamadı")
            
        return data
        

    except ValueError as e:
        if "JSON" in str(e):
            raise ValueError("API'dan geçersiz JSON verisi alındı")
        else:
            raise e




def getWeatherForDateHourly(latitude, longitude, dt, timezone="Europe/Istanbul"):
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
