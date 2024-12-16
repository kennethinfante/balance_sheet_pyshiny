# balance_sheet_dash

This is my project in using Shiny for Python to show balance sheet pivot table.

## TODO`
* Arrange month_name by months - ok
* Add conditional checkboxes - ok
* Add apply, reset button - ok
* Show initial balance_sheet - ok
* Add last update marking - ok
* Retain selections when adding new filters - ok
* Spinner - ok
* Format the numbers - ok
* Make the columns to pivot dynamic - ok
* Add totals - ok
* Highlight totals - ok
* Added error checking like for the formula for DAX in PBI - ok
* Add Select All option - need to subclass

## Running

```
shiny run --port 50394 --reload --autoreload-port 50395 app.py
```

## Deployment

```
rsconnect deploy shiny . --name kinfante --title balance_sheet_pyshiny -x "data-raw/tips.csv" "test.py"
```