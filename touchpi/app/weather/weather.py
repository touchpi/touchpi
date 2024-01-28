from touchpi.appbase.app import App, log
from PySimpleGUI import Push, VPush, Sizer, HorizontalSeparator, VerticalSeparator, Column, Text, Button, Image


class Weather(App):
    def __init__(self):
        super().__init__()
        self.actual_temp = "0 °C°"
        self.actual_icon = "50n.png"
        self.forecast_list = []
        self.forecast_index = 0
        self.forecast_time = "Today"
        self.forecast_temp = "0 °C°"
        self.forecast_icon = "50n.png"
        self.forecast_text = "Unknown"
        self.forecast_list.append({'time': self.forecast_time,
                                   'temp': self.forecast_temp,
                                   'icon': self.forecast_icon,
                                   'text': self.forecast_text,
                                   })

    @staticmethod
    def layout():
        left_layout = [[Push(), Text('Actual', font='Any 14'), Push()]]
        left_layout += [[HorizontalSeparator(pad=10)]]
        left_layout += [[Push(), Text('0°C', font='Any 24', key='weather_ActualTemp'), Push()]]
        left_layout += [[Push(), Image(App.get_app_folder() + 'icons/50n.png', key='weather_ActualIcon'), Push()]]
        left_layout += [[Sizer(0, 96)]]

        right_layout = [[Push(), Text('Tomorrow 18:00', font='Any 14', key='weather_ForecastTime'), Push()]]
        right_layout += [[HorizontalSeparator(pad=10)]]
        right_layout += [[Push(), Text('0°C', font='Any 24', key='weather_ForecastTemp'), Push()]]
        right_layout += [[Push(), Image(App.get_app_folder() + 'icons/50n.png', key='weather_ForecastIcon'), Push()]]
        right_layout += [[Push(), Text('thunderstorm with heavy drizzle', size=(15, 2), font='Any 12',
                                       expand_y=True, auto_size_text=True, key='weather_ForecastText'), Push()]]
        right_layout += [[Sizer(0, 10)]]
        right_layout += [[Push(),
                          Button('-6', pad=0, disabled=True, key="weather_ForecastMinus"),
                          Sizer(30, 0),
                          Button('+6', pad=0, disabled=True, key="weather_ForecastPlus"),
                          Push()]]

        layout = [[VPush()]]
        layout += [[Push(),
                    Column(left_layout, key='weather_ScreenLeft'),
                    Sizer(0, 300), VerticalSeparator(pad=20),
                    Column(right_layout, key='weather_ScreenRight'),
                    Push()]]
        layout += [[VPush()]]
        log.debug("WeatherApp layout initialised.")
        return layout

    def set_forecast_to_start(self):
        self.forecast_index = 0
        self.forecast_time = self.forecast_list[0]['time']
        self.forecast_temp = self.forecast_list[0]['temp']
        self.forecast_icon = self.forecast_list[0]['icon']
        self.forecast_text = self.forecast_list[0]['text']
        self.window['weather_ForecastPlus'].update(disabled=False)
        self.window['weather_ForecastMinus'].update(disabled=True)

    def set_forecast_plus(self):
        if self.forecast_index < 8:
            self.forecast_index = self.forecast_index + 1
            self.forecast_time = self.forecast_list[self.forecast_index]['time']
            self.forecast_temp = self.forecast_list[self.forecast_index]['temp']
            self.forecast_icon = self.forecast_list[self.forecast_index]['icon']
            self.forecast_text = self.forecast_list[self.forecast_index]['text']
            if self.forecast_index == 8:
                return "LIST_END"
            else:
                return "LIST_BETWEEN"
        else:
            return "LIST_END"

    def set_forecast_minus(self):
        if self.forecast_index > 0:
            self.forecast_index = self.forecast_index - 1
            self.forecast_time = self.forecast_list[self.forecast_index]['time']
            self.forecast_temp = self.forecast_list[self.forecast_index]['temp']
            self.forecast_icon = self.forecast_list[self.forecast_index]['icon']
            self.forecast_text = self.forecast_list[self.forecast_index]['text']
            if self.forecast_index == 0:
                return "LIST_START"
            else:
                return "LIST_BETWEEN"
        else:
            return "LIST_START"

    def show_values(self):
        self.window['weather_ActualTemp'].update(self.actual_temp)
        self.window['weather_ActualIcon'].update(App.get_app_folder() + "icons/" + self.actual_icon)
        self.window['weather_ForecastTime'].update(self.forecast_time)
        self.window['weather_ForecastTemp'].update(self.forecast_temp)
        self.window['weather_ForecastIcon'].update(App.get_app_folder() + "icons/" + self.forecast_icon)
        self.window['weather_ForecastText'].update(self.forecast_text)

    def update(self, event, values):
        if event == 'openweather_data':
            data = self.get_event_value(event, values)
            self.actual_temp = data["actual_temp"]
            self.actual_icon = data["actual_icon"]
            self.forecast_list = data["forecast_list"]
            self.set_forecast_to_start()
            self.show_values()
        elif event == 'weather_ForecastPlus':
            if self.set_forecast_plus() == "LIST_END":
                self.window['weather_ForecastPlus'].update(disabled=True)
            else:
                self.window['weather_ForecastMinus'].update(disabled=False)
            self.show_values()
        elif event == 'weather_ForecastMinus':
            if self.set_forecast_minus() == "LIST_START":
                self.window['weather_ForecastMinus'].update(disabled=True)
            else:
                self.window['weather_ForecastPlus'].update(disabled=False)
            self.show_values()


if __name__ == '__main__':
    app = Weather()
    app.run()
