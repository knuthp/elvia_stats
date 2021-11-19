![unittest](https://github.com/knuthp/elvia_stats/workflows/unittest/badge.svg)

## Power Consumption Statistics for Norwegian Elvia
Main focus is the new model for pricing power line rent (Nettleie). Norway will from 2022-01-01 have a new price model for line rental that is based on several factors in addition to consumption.

* Time of day (Night/Day)
* Time of year (Summer/Winter)
* Maximum consumption for one hour

With less than 1.5 months left we Elvia has not published the new price model. However, we utilize pilot models they have tried for some customers.

Elvia also has an API to get historic consumption per hour. Access can be optained by generating an access token on Elvia Web pages. For demonstration I use my house's values.

__For a demo see:__

[elvia-stats](https://elvia-stats.herokuapp.com/) on Heroku (Takes a small time to load if sleeping)


## Technology
* Python 3.9 - Programming language
* Streamlit - Dasboard
* Jupyter Lab - For data exploration
* Heroku - deployment