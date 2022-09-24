# MyValuableProfits (MVP)

## Description

Welcome to MyValuableProfits (MVP), a project submitted as part of the 2022 cohort for CS50x, a Harvard University Online Course. MVP is a fully functioning and case-tested stock portfolio website, targetted towards Australian shareholders who would like to track (and convert their money back to AUD) in real time using Yahoo Finance API (Web-scrapper) and Panda Datareader Dataform as the AUD/USD API for exchange rates.

** Important Note: This stock portfolio is only intended to work for ASX / NYSE stocks. All USD currencies are automatically converted to AUD based on the provided date of acquisition (via exchange rate API in the backend). **

![Dashboard](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SS1.png)


## Table of Contents 

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Credits](#credits)
- [License](#license)

## Installation

MVP is a program created with HTML, CSS, and Jinja2 for the frontend and Flask and Python for the backend. Pandas data.database and YFinance web-scrapper have been used to facilitate (forever free) live stock tracking for the ASX and NYSE. A full list of requirements is detailed in requirements.txt which can be found in the main directory of this repository.

###### Yahoo Finance API | https://pypi.org/project/yfinance/ 

###### Pandas DataReader API | https://pandas-datareader.readthedocs.io/en/latest/remote_data.html

## Usage

Upon running the local flask server, a placeholder index.html (WIP) will be found as shown below:

![Index](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSindex.png)

The first step is to register for an account under the register button. The username will be automatically checked against a SQL database in case of an already existing user, in which case an error message will pop up. The password has a four character limit, however all passwords are salted and hashed everytime, and the final hashed password is stored in the database. An additional benefit of this password hashing system is to ensure that even if two different users share the same password, the final salted and hashed password will be different from one another.

![Register](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSregister.png)

The login page is similar to the register page, however it logs the user in. For patreons of MVP that believe choosing a unique username and password is a very difficult task, a test account can be accessed by following the placeholder text in the login and password form.

###### Username : admin
###### Username : admin

![Login](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSlogin.png)

Landing onto the dashboard page is an empty portfolio. To record a stock, input the information about the stock at the bottom of the page under the buy section. Tickers are based off Yahoo Finance. If you are unsure, use the searchbar at the top and enter keywords about your stock; this will redirect you to a yahoo finance search. Please input all currencies in their local currency, and the date of purchase will be used to fetch the AUD/USD exchange rate if the stock is a foreign stock. When all the information is loaded in, press the submit button to update your portfolio. All portfolio information returned is in local ($AUD) currency. Please note: all currency gains/losses from AUD/USD exchange rate are taken care of automatically in the backend.

##### Note: YFinance is used as the live stock price API. Since it is a web-scrapper, optimised load times per stock ~ 10 seconds.

![Screenshot of Buy Form](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSbuy_1.png)

![Screenshot of Dashboard](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSbuy_2.png)

Selling a stock is no different: simply enter the prices at which the stock has been sold for (in local currency) and enter submit. 

![Screenshot of Buy Form](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSsell_1.png)

![Screenshot of Dashboard](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSsell_2.png)

MVP stores all stocks permanently in the portfolio to track exited gains/losses.

## Features

More features are coming soon! Keep an eye on this repository.


## Credits

##### C$50x Finance - the inspiration for this website. [https://cs50.harvard.edu/x/2022/psets/9/finance/]

#### Contributors

##### SunHL [ArigatouGozaimaster] [https://github.com/ArigatouGozaimaster]
##### Eric Chen [tcheric] [https://github.com/tcheric]

#### Online HTML / CSS Tutorials
##### Login / Register HTML CSS - [Online Tutorials YT] [https://www.youtube.com/watch?v=mSAEGEAnyIY]
##### Dashboard HTML CSS - [EGATOR YT] [https://www.youtube.com/watch?v=FaBY9yAUtdg]
##### The Stack Overflow Community for debugging issues (reading old forum posts)


## License

MIT License

Copyright (c) 2022 SunHL, Eric Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.





