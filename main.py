import flet as ft 
import requests
from googletrans import Translator


from config import Weather_API

def translate_text(text, target_language='ru'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text 

def main(page: ft.Page):
    page.title = "Погодная программа"
    page.theme_mode = 'dark' # light
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_data = ft.TextField(width = 400, label = "Введите город")
    weather_data = ft.Text("")
    weather_img = ft.Image(src = "./image.png", width = 100, height = 100)

    
    
    def get_info(e):
        if len(user_data.value) < 2:
            return 

        API = Weather_API
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={user_data.value}&appid={API}&units=metric"
        try:
            res = requests.get(URL).json()
            temp = res['main']['temp']
            temp_max = res['main']["temp_max"]
            temp_min = res["main"]["temp_min"]
            isWeather = res["weather"][0]["description"]
            isWeatherRU = translate_text(text = isWeather)

            iconWeather = res["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{iconWeather}.png"
            with open("image.png", "wb") as f:
                icon = requests.get(icon_url)
                f.write(icon.content)
            

            weather_data.value = f"""
                Погода: {isWeatherRU}
                Температура: {temp} °C
                Макс. Температура: {temp_max} °C
                Мин. Температура: {temp_min} °C
            """
            page.update()
           
        except:
            weather_data.value = "К сожилению Мы не знаем токого города"

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.SUNNY, on_click = change_theme),
                ft.Text("Погодная программа")
            ],
            alignment = ft.MainAxisAlignment.CENTER
        ),
        ft.Row([user_data], alignment = ft.MainAxisAlignment.CENTER),
        ft.Row([weather_data, weather_img], alignment = ft.MainAxisAlignment.CENTER),
        ft.Row([ft.ElevatedButton(text = "Получить", on_click = get_info)], alignment = ft.MainAxisAlignment.CENTER),
        
    )

if __name__ == "__main__":
    ft.app(target = main) #view = ft.AppView.WEB_BROWSER