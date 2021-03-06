#      create a browser
#      Copyright (C) <2021>  <coolrc>
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


def new_web_driver(
    http_proxy=None, socks5_proxy=None, socks_username=None, socks_password=None
) -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")  # 允许root下使用
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless")  #
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("window-size=2560,1440")
    # TODO: chrome proxy
    # if http_proxy is not None:
    #     webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
    #         "httpProxy": http_proxy,
    #         "sslProxy": http_proxy,
    #         "proxyType": "MANUAL",
    #     }
    #     return webdriver.Chrome(options=chrome_options)
    # if socks5_proxy is not None:
    #     webdriver.DesiredCapabilities.FIREFOX["proxy"] = {
    #         "socks_proxy": socks5_proxy,
    #         "socksUsername": socks_username,
    #         "socksPassword": socks_password,
    #         "proxyType": "MANUAL",
    #     }
    #     return webdriver.Firefox(options=ffoptions)
    return webdriver.Chrome(options=chrome_options)


def new_remote_web_driver(url: str):
    driver = webdriver.Remote(
        command_executor=url, desired_capabilities=DesiredCapabilities.CHROME
    )  # firefox有bug，辣鸡mozilla
    return driver
