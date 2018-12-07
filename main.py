import gi
import urllib.request, json
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib
import matplotlib
matplotlib.use('agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3 as NavigationToolbar
from matplotlib import pyplot as plt
from datetime import datetime
import time
import csv

tempCurrent = 0
tempMin = 0
tempMax = 0
pressure = 0
humidity = 0
loop = 0
historyList = []
historyIndexes = []

def getData():
    with urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?id=5128581&appid=8685bce726629e5232653689c92586bf") as url:
        data = json.loads(url.read().decode())

        global tempCurrent
        global tempMin
        global tempMax
        global pressure
        global humidity

        tempCurrent = round(data['main']['temp'] - 273.15, 2)
        tempMin = round(data['main']['temp_min'] - 273.15, 2)
        tempMax = round(data['main']['temp_max'] - 273.15, 2)
        pressure = (data['main']['pressure'])
        humidity = (data['main']['humidity'])

        writeHistoryToFile(tempCurrent)

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Weather in NYC")

        Gtk.Window.set_default_size(self,200,-1)

        grid = Gtk.Grid()
        self.add(grid)

        titleLabel = Gtk.Label()
        titleLabel.set_markup("<big>THE WEATHER IN NYC\n</big>")

        global tempCurrentLabel
        global tempMinLabel
        global tempMaxLabel
        global pressureLabel
        global humidityLabel

        tempCurrentLabel = Gtk.Label('Current temperature: ' + str(tempCurrent) + ' ºC\n')
        tempMinLabel = Gtk.Label('Min temperature: ' + str(tempMin) + ' ºC\n')
        tempMaxLabel = Gtk.Label('Max temperature: ' + str(tempMax) + ' ºC\n')
        pressureLabel = Gtk.Label('Pressure: ' + str(pressure) + 'hpa\n')
        humidityLabel = Gtk.Label('Humidity: ' + str(humidity) + '%\n')

        historyButton = Gtk.Button.new_with_label("Historical")
        historyButton.connect("clicked", self.on_history_button_clicked)

        grid.add(titleLabel)
        grid.attach(tempCurrentLabel, 0, 1, 1, 1)
        grid.attach(tempMinLabel, 0, 2, 1, 1)
        grid.attach(tempMaxLabel, 0, 3, 1, 1)
        grid.attach(pressureLabel, 0, 4, 1, 1)
        grid.attach(humidityLabel, 0, 5, 1, 1)
        grid.attach(historyButton, 0, 6, 1, 1)

        self.timeout_id = GLib.timeout_add(2000, self.on_timeout, None)

    def on_history_button_clicked(self, button):
        historyWindow = HistoryWindow()
        historyWindow.show_all()


    def on_timeout(self, user_data):

        getData()

        tempCurrentLabel.set_text('Current temperature: ' + str(tempCurrent) + ' ºC\n')
        tempMinLabel.set_text('Min temperature: ' + str(tempMin) + ' ºC\n')
        tempMaxLabel.set_text('Max temperature: ' + str(tempMax) + ' ºC\n')
        pressureLabel.set_text('Pressure: ' + str(pressure) + 'hpa\n')
        humidityLabel.set_text('Humidity: ' + str(humidity) + '%\n')

        historyList.append(tempCurrent)

        historyIndexes.append(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

        return True

class HistoryWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Weather in NYC")

        Gtk.Window.set_default_size(self,500, 500)
        Gtk.Window.set_title(self,'Historical weather data')

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        Gtk.Window.add(self,box)

        fig = Figure(figsize=(5, 5), dpi=80)
        ax = fig.add_subplot(111)

        values = historyList
        indexes = historyIndexes
        ax.xaxis.set_major_locator(plt.MaxNLocator(15))

        ax.plot(indexes, values, color='blue')

        fig.autofmt_xdate()

        canvas = FigureCanvas(fig)
        box.pack_start(canvas, True, True, 0)
        toolbar = NavigationToolbar(canvas, self)
        box.pack_start(toolbar, False, True, 0)

def writeHistoryToFile(currentTemp):
    with open('weather_data.csv', mode='a') as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        date = (datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

        employee_writer.writerow([date,currentTemp])


def retrieveHistory():
    with open('weather_data.csv', mode='r') as csvfile:
        plot = csv.reader(csvfile, delimiter=',')
        for row in plot:
            historyIndexes.append(row[0])
            historyList.append(row[1])

retrieveHistory()
getData()
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()