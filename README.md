# Weather application

Weather application is a graphical desktop application for Linux made with the library GTK. The weather data is gathered from [openweathermap](https://openweathermap.org/api) API.
### Features

  - Shows an update weather forecast for one day of New York City.
  - Save history of registered temperatures  in a .csv file
  - Show the history of temperatures in a graph

### Dependencies
- All code is written in Python 3.
- Some code depends on the 'matplotlib' library.


### Description of files
| Filename | Description |
| -------- | ------ |
| README.md | Text file (markdown format) description of the project. |
| main.py | Python file that contains all the developed code |
| venv | Folder that contains a configured Python runtime environment |
| weather_data.csv | Spreadsheet with the gathered data |

### Execution

In order to execute the program it is recommendable to execute the main.py file with the given environment. To do that: 
```sh
$ ./venv/bin/python3 main.py
```
### Todos

 - Add possibility of selecting more cities
 - Add weather status icons (sun,clouds,...)
 - Improve plotting layout
 - Add Night Mode