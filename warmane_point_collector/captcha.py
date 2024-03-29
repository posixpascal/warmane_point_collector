# A small captcha library which solves captchas either automatically
# or manually using human interactions. The provider of choice is 2captcha.
# other providers are not supported at the moment.
from asyncio import sleep

import requests

from warmane_point_collector.config import config
from warmane_point_collector.logger import logger


class Captcha(object):
    def __init__(self):
        pass

    async def solve_automatically(self, google_recaptcha_key, url):
        form_data = {
            "method": "userrecaptcha",
            "key": config.twocaptcha["api_key"],
            "googlekey": google_recaptcha_key,
            "pageurl": url,
            "json": 1
        }
        logger.info(config.twocaptcha["api_key"])

        # create ticket
        r = requests.post(config.twocaptcha["request_url"], data=form_data)
        request_id = r.json()['request']
        solver_url = config.twocaptcha["solver_url"].format(req_id=request_id)

        recaptcha_counter = 0

        # wait for a human to solve that captcha
        while True:

            # 15s is recommended by docs: https://2captcha.com/2captcha-api#solving_recaptchav2_new
            await sleep(5)

            # check if captcha has been solved
            res = requests.get(solver_url)
            json_response = res.json()

            # check for successful recaptcha token
            if json_response["status"] == 1:
                recaptcha_token = json_response["request"]
                logger.debug(recaptcha_token)
                return recaptcha_token

            recaptcha_counter += 1
            if recaptcha_counter > 10:
                logger.info("Whackness. Captcha provider failed. Going back to human fallback mode :(")
                return False

            if recaptcha_counter > 5:
                logger.info("Still no captcha response...")

    # Checks whether or not the captcha has been solved on the page
    async def is_solved(self, page):
        textarea = await page.querySelector('#g-recaptcha-response')
        textarea = textarea.asElement()
        textarea_value = await textarea.getProperty("value")
        captcha_key = await textarea_value.jsonValue()

        return len(captcha_key) > 0


captcha = Captcha()
