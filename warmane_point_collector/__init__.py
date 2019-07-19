# built-ins
import asyncio

# vendors
from asyncio import sleep
from urllib.parse import urlparse, parse_qs

from pyppeteer import launch

from warmane_point_collector.captcha import captcha
from warmane_point_collector.config import config
from warmane_point_collector.logger import logger


def patch_pyppeteer():
    import pyppeteer.connection
    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method


async def main():
    # pyppeteer is broken and disconnects the chrome session after 20s.
    # @see https://github.com/miyakogi/pyppeteer/pull/160
    # @see https://github.com/miyakogi/pyppeteer/issues/62
    patch_pyppeteer()

    headless_mode = config.chrome['headless'] == '1'
    testing_mode = config.chrome['testing'] == '1'

    logger.info("Starting warmane bot")

    if headless_mode:
        logger.info("In headless mode")

    slowdown = 0
    if testing_mode:
        slowdown = 10

    browser = await launch(
        {'executablePath': config.chrome["path"], 'headless': headless_mode, 'slowmo': slowdown, 'timeout': 1})

    for account in config.accounts:
        logger.info("Using account: {}".format(account["username"]))

        page = await browser.newPage()

        # GET /
        logger.info("Visiting {}".format(config.endpoint["endpoint_url"]))
        await page.goto(config.endpoint["endpoint_url"])

        # GET Login URL
        logger.info("Visiting {}".format(config.endpoint["login_url"]))
        await page.goto(config.endpoint["login_url"])

        # Form Input
        logger.info("Filling in credentials...")
        await page.type(config.selectors["username_field"], account["username"])
        await page.type(config.selectors["password_field"], account["password"])

        # Captcha hustle
        logger.info("Solving recaptcha...")
        use_2captcha = config.bot["use_2captcha"] == '1'

        is_solved = False
        captcha_token = ""

        # Solve automatically by using the 2captcha api
        if use_2captcha:
            # Get iframe url
            recaptcha_iframe = await page.querySelector(config.selectors['recaptcha_iframe'])
            recaptcha_iframe_url = (await (await recaptcha_iframe.asElement().getProperty("src")).jsonValue())

            # Extract site key
            recaptcha_url = urlparse(recaptcha_iframe_url)
            recaptcha_sitekey = parse_qs(recaptcha_url.query)['k'][0]
            captcha_token = await captcha.solve_automatically(recaptcha_sitekey, config.endpoint["login_url"])
            is_solved = True

        # wait for human to solve the captcha
        while not is_solved:
            print("Waiting for captcha to be solved...")
            is_solved = await captcha.is_solved(page)
            # Get iframe url
            recaptcha_iframe = await page.querySelector("#g-recaptcha-response")
            captcha_token = (await (await recaptcha_iframe.asElement().getProperty("value")).jsonValue())
            captcha_token = captcha_token

        logger.info("Captcha was solved.")

        logger.info("Logging in...")
        # perform login in JS as recaptcha would detect it otherwise
        # this uses jQuery as it's already loaded on warmane and comes in handy
        await page.evaluate("""
            () => {
                $.ajax({
                    method: 'POST',
                    action: `%(endpoint)s`,
                    data: {
                        return: "",
                        userID: document.querySelector(`%(username_field)s`).value,
                        userPW: document.querySelector(`%(password_field)s`).value,
                        'g-recaptcha-response': `%(captcha)s`
                    },
                    success: (res) => {
                    }
                });
            }
        """ % ({
            "endpoint": config.endpoint["login_url"],
            "username_field": config.selectors["username_field"],
            "password_field": config.selectors["password_field"],
            "captcha": captcha_token
        }))

        logger.info("Logged in") # we're in. :)

        await page.goto(config.endpoint['collect_points_url'])
        await page.waitForSelector(config.selectors["collect_points_btn"])

        logger.info("Getting points")
        await page.click(config.selectors["collect_points_btn"])

        logger.info("Done.")
        await page.close()
        # collect the points through API
        # POST /account/
        #request = requests.post(config.endpoint["collect_points_url"], data={"collectpoints": True}).json()
        #if "messages" in request and "error" in request["messages"]:
        #    logger.error(";".join(request["messages"]["error"]))


