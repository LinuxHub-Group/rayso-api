#      <one line to give the program's name and a brief idea of what it does.>
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
import os
import platform
import unittest
import threading

from browser import new_web_driver

# from browser import new_remote_web_driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class RaySo:
    def __init__(self):
        # self.webdriver = new_web_driver(http_proxy="127.0.0.1:7890")
        self.webdriver = new_web_driver()
        self.lock = threading.Lock()

    def connect(self):
        self.lock.acquire()
        # self.webdriver.get("https://ray.so/")
        #
        # self.webdriver = new_remote_web_driver('http://127.0.0.1:5566/wd/hub')
        self.webdriver.get("https://rayso-proxy.coolrc.workers.dev")  # 反代地址

        # 隐藏拖动控制 和 工具栏
        self.webdriver.execute_script(
            """
        let elem = document.querySelector(".drag-control-points")
        elem.style.display='none';

        elem = document.querySelector("section.controls")
        elem.style.display='none';

        elem = document.querySelector(".CodeMirror-vscrollbar")
        elem.style.overflow="-moz-hidden-unscrollable"

        elem = document.querySelector(".title")
        elem.textContent=""
        elem.style.color="#aaaaaa"

        """
        )
        self.lock.release()

    def capture(self, content, font="Fira code", padding=26, title="", size=1):
        self.lock.acquire()
        self.set_content(content)
        self.set_font(font)
        self.set_padding(padding)
        self.set_title(title)
        self.set_size(size)

        box = self.webdriver.find_element_by_xpath('//*[@id="frame"]')
        self.lock.release()
        return box.screenshot_as_base64

    def set_content(self, content: str):
        lock = threading.Lock()
        lock.acquire()
        """
        填入内容
        """
        ActionChains(self.webdriver).send_keys("r").perform()  # 随机更换主题

        textarea = self.webdriver.find_element_by_css_selector(
            ".CodeMirror > div > textarea"
        )
        textarea.send_keys(Keys.CONTROL + "a")
        textarea.send_keys(Keys.BACKSPACE)
        textarea.send_keys(content)
        textarea.send_keys(Keys.ESCAPE)
        lock.release()

    def set_font(self, font: str):
        lock = threading.Lock()
        lock.acquire()
        """
        修改代码块字体
        """
        self.webdriver.execute_script(
            f"""
        let elem = document.getElementsByClassName("CodeMirror-code");
        elem[0].style.fontFamily = "{font}";
        """
        )
        lock.release()

    def set_padding(self, padding: int):
        lock = threading.Lock()
        lock.acquire()
        """
        修改图片padding

        :param padding: int, 单位px
        """

        self.webdriver.execute_script(
            f"""
        let elem = document.querySelector("#frame")
        elem.style.padding="{padding}px"
        """
        )
        lock.release()

    def set_title(self, title: str):
        lock = threading.Lock()
        lock.acquire()
        """
        设置代码块标题
        """

        self.webdriver.execute_script(
            f"""
        let elem = document.querySelector(".title")
        elem.textContent="{title}"
        """
        )
        lock.release()

    def set_size(self, size: float):
        lock = threading.Lock()
        lock.acquire()
        """
        缩放图片

        :param size: 图片缩放倍数，1-2
        """
        if size < 1 or size > 2:
            size = 1

        self.webdriver.execute_script(
            f"""
        let elem = document.querySelector("#frame")
        elem.style.scale = {size}
        """
        )
        lock.release()

    # def __del__(self):
    #     self.quit()

    def quit(self):
        try:
            self.webdriver.quit()
        except Exception as e:
            print(e)


class TestRaySo(unittest.TestCase):
    def test_capture(self):
        rayso = RaySo()
        rayso.connect()
        base64 = rayso.capture("let a = 5")
        # print(base64)
        self.assertTrue(len(base64) > 1000)

    def test_del(self):
        RaySo()
        sys = platform.system()
        if sys != "Windows":
            command = "taskkill /F /T /IM "
            command = command + "firefox.exe"
            os.system(command)  # nosec
        else:
            command = "pkill gecko && pkill firefox"
            os.system(command)  # nosec
