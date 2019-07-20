# 🦡 warmane_point_collector

A python3 bot which collects daily login points from [warmane.com](https://www.warmane.com). It supports multiple
accounts, can run chrome in headless mode and solve recaptchas automatically in the background.

Please make sure that you've signed into the game at least once the day you're running this.
 
## 💻 Install

Install using docker or [Pipenv](https://docs.pipenv.org/en/latest/)

### 🐍 Via pipenv

```bash
# Clone the repository & cd into it
pipenv install
```

You can also install this bot as a library using  `pipenv install warmane_point_collector`. 

## 🐳 Via docker

Build the image once.

```
# Clone the repository & cd into it
docker build -t warmane_point_collector .
```

then run it using:

```
# Clone the repository & cd into it
docker run -t warmane_point_collector
```

## 🚀 Usage

```bash
pipenv run python3 warmane.py
# or
pipenv shell
python3 warmane.py
```

## 🔩 Config

Rename the provided `config.ini.sample` to `config.ini` and edit it in place.

```toml
[bot]
# Whether or not to solve captchas using 2captcha.com — Account required
use_2captcha = 0

[endpoint]
# Warmane website configs
endpoint_url = https://www.warmane.com
login_url = %(endpoint_url)s/account/login
collect_points_url = %(endpoint_url)s/account

[2captcha]
# 2captcha configuration
api_key = YOUR_2CAPTCHA_API_KEY

# You can override 2captcha endpoints here.
request_url = http://2captcha.com/in.php
solver_url = http://2captcha.com/res.php?key=%(api_key)s&action=get&id={req_id}&json=1

[chrome]
# Whether or not to run chrome in headless mode (e.g. without a window)
headless = 1
# if testing is 1 this will slowdown each chrome action by 10 seconds.
testing = 0
# set the chrome path.
# do note that pyppeteer bundles chromium but I had troubles with that.
# You can change main.py and remove the "executablePath" setting from the launch() call.
# Then pyppeteer will use the bundled chromium instead.
path = YOUR CHROME PATH

[selectors]
# for website navigational purposes
username_field = [name='userID']
password_field = [name='userPW']
submit_btn = .wm-ui-position-abottom [type='submit']
recaptcha_iframe = #loginWidget iframe[role='presentation']

my_current_points = body table .myCoins
my_current_coins = body table .myPoints
collect_points_btn = a[data-click='collectpoints']

[account_one]
# your warmane accounts
username = YOUR_USERNAME
password = YOUR_PASSWORD

# you can add as many accounts as you want as long as you prefix each section with account_.
# see below:
#[account_two]
#username = ""
#password = ""
#
#[account_XXXXXXXXXXXXXXXXXXXXXX]
#username = ""
#password = ""

#[account_any]
#username = ""
#password = ""
```

## 👀 Recaptcha Bypass

To bypass the recaptcha you have to add a [2captcha.com](https://2captcha.com) API key in the config file.

## 🤓 Solve Recaptcha manually

If you do not want to use 2captcha.com you can also manually solve the captchas.
The bot will automatically fill in all credentials and will wait for you to solve the captcha.
Once you solve the captcha the bot will continue and collect your points.

Do note that manual captcha solving is only possible then running the bot in non-headless mode.
Set `headless = 0` in your `config.ini` file.



## 📋 License

```
MIT License

Copyright (c) [2019] [Pascal Raszyk]

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
```
