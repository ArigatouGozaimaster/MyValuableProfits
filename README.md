# MyValuableProfits (MVP)


## Introduction

Welcome to MyValuableProfits (MVP), a project created as my final project for CS50x 2022, a free and online Harvard/EdX course. MVP is a fully functioning and user-tested stock portfolio website, targeted towards Australian shareholders who would like to track (and convert their money back to AUD) in real time. This program uses the Yahoo Finance API (Web-scrapper) and Panda Datareader Dataform as the AUD/USD API for exchange rates. Although the load times are on the slower end (due to Yahoo Finance), this project was not geared for speed but rather functionality (although loading times have been optimised!). I hope you enjoy browsing through my project as much as I had fun creating it! This was C$50.

** Important Note: This stock portfolio is only intended to work for ASX / NYSE stocks. All USD currencies are automatically converted to AUD based on the provided date of acquisition (via exchange rate API in the backend). **

![Dashboard](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SS1.png)


## Table of Contents 

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Credits](#credits)
- [License](#license)


## Installation

MVP is a program created with HTML, CSS, and Jinja2 for the frontend and Flask and Python for the backend. Pandas data.database and YFinance web-scrapper have been used to facilitate (forever free) live stock tracking on both the ASX and NYSE. A variety of different APIs have been tested for this program such as IEX, however YFinance was chosen as the unlimited and free web scrapping API. A full list of requirements can be found detailed under requirements.txt, located in the main repository. 

###### Yahoo Finance API | https://pypi.org/project/yfinance/ 

###### Pandas DataReader API | https://pandas-datareader.readthedocs.io/en/latest/remote_data.html


## Usage

Upon running the local flask server, a placeholder (WIP) index.html will be found as shown below:

![Index](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSindex.png)

The register page is a fully functioning registration page for the user to create an account. This works by checking the user's inputted username against the backend SQL database implemented in sqlite3, and will either continue on to create a user's account or return an error message if a duplicate account name is detected. For security, each user's passwords will be hashed and salted meaning the SQL database will not store the original plaintext password. 
The Secret Key has been referenced from another python file to demonstrate that Secret Keys should never be accessible, however for this program it has been kept as part of the main directory to ensure a functioning program.

![Registration Error](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSregister_error.png)

![Register](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSregister.png)

The login page follows the same logic and returns an error if a matching account cannot be found in the SQL database as well as returning errors on mismatched account information. For a sample account to see the program without creating an account, the following username/password combination have been provided as shown below.

###### Username : admin
###### Username : admin

![Login Error](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSlogin_error.png)

![Login](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSlogin.png)

Landing onto the dashboard page is an empty portfolio. To record a stock, input the information about the stock at the bottom of the page under the buy section. Tickers are based off Yahoo Finance: if a user is unsure, they can enter any string into the searchbar and this will redirect the user to yahoo finance search with the results of the inputted search query.

When recording a stock acquisition/sell, all costs must be added in by the stock's local currency. This is necessary as the backend AUD/USD exchange rate automatically converts the costs to an accurate number based on the date of purchase provided. As an example, when recording Apple stocks, costs/profits should be inputted as USD meanwhile when purchasing an Australian stock such as VTS.AX, prices should be recorded in AUD (in which case no currency exchange will occur). All currency exchange calculations are automatically done in the backend of the program under app.py.

##### Note: YFinance is used as the live stock price API. Since it is a web-scrapper, optimised load times per stock ~ 10-20 seconds.
##### YFinance was chosen as the API with accessibility in mind, not speed optimisation.

![Screenshot of Buy Form](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSbuy_1.png)

![Screenshot of Dashboard](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSbuy_2.png)

Selling a stock is no different: simply enter the prices at which the stock has been sold for (in local currency) and enter submit. 

![Screenshot of Buy Form](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSsell_1.png)

![Screenshot of Dashboard](https://github.com/ArigatouGozaimaster/MyValuableProfits/blob/main/static/images/SSsell_2.png)

MVP stores all stocks permanently in the portfolio to track exited gains/losses.

## Features

More features are coming soon! Keep an eye on this repository.

Planned Features include:
- Stock purchase history
- Additional stock support in other regions of the world
- Loading Screen (for long API wait-time)
- Permanently delete stocks from dashboard
- Change username and/or password

## Credits

##### C$50x Finance - the inspiration for this website. [https://cs50.harvard.edu/x/2022/psets/9/finance/]

#### Contributors

##### Hongliang Sun [ArigatouGozaimaster] [https://github.com/ArigatouGozaimaster]
##### Eric Chen [tcheric] [https://github.com/tcheric]

HTML and CSS stylisation guides were utilised for the aesthetic design of the program.

#### Online HTML / CSS Tutorials
##### Login / Register HTML CSS - [Online Tutorials YT] [https://www.youtube.com/watch?v=mSAEGEAnyIY]
##### Dashboard HTML CSS - [EGATOR YT] [https://www.youtube.com/watch?v=FaBY9yAUtdg]
##### The Stack Overflow Community for debugging issues (reading old forum posts)


## License

MIT License

Copyright (c) 2022 Hongliang Sun, Eric Chen

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
