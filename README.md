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

## Deployment

```
rsconnect deploy shiny . --name kinfante --title balance_sheet_pyshiny -x "data-raw/tips.csv" "test.py"
```