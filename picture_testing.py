import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class YandexPictureSearch(unittest.TestCase):
    def setUp(self):
        # В executable_path укажите путь к файлу geckodriver.exe
        self.driver = webdriver.Firefox(
            executable_path=r"D:\Dev\yandex_testing\geckodriver.exe"
        )

    def test_search_in_yandex_ru(self):
        driver = self.driver
        driver.get("http://www.yandex.ru")
        time.sleep(2)
        # Закрывает всплывающее окно об установке Яндекс Браузера
        driver.find_element(by=By.CLASS_NAME, value="modal__close").click()
        assert driver.find_element(
            by=By.XPATH, value="//a[@data-id='images']"
        ), "Ссылка на Яндекс картинки отсутствует."
        driver.find_element(
            by=By.XPATH,
            value="//a[@data-id='images']",
        ).click()
        time.sleep(2)
        new_tab = driver.window_handles[1]
        driver.switch_to.window(f"{new_tab}")
        assert "yandex.ru/images" in driver.current_url, "Неверный сайт."
        time.sleep(1)
        driver.find_element(
            by=By.CSS_SELECTOR,
            value="div.PopularRequestList-Item:nth-child(1)",
        ).click()
        time.sleep(1)
        input = driver.find_element(by=By.NAME, value="text")
        text = input.get_attribute("value")
        assert text is not None, "Текст отсутствует."
        driver.find_element(by=By.CLASS_NAME, value="serp-item__link").click()
        first_picture = driver.find_element(
            by=By.CLASS_NAME, value="MMImage-Origin"
        )
        assert first_picture, "Картинка не открылась."
        time.sleep(1)
        first_picture_src = first_picture.get_attribute("src")
        driver.find_element(by=By.TAG_NAME, value="html").send_keys(
            Keys.ARROW_RIGHT
        )
        time.sleep(1)
        second_picture = driver.find_element(
            by=By.CLASS_NAME, value="MMImage-Origin"
        )
        second_picture_src = second_picture.get_attribute("src")
        assert (
            first_picture_src != second_picture_src
        ), "Картинка не сменилась."
        time.sleep(1)
        driver.find_element(by=By.TAG_NAME, value="html").send_keys(
            Keys.ARROW_LEFT
        )
        first_picture_again = driver.find_element(
            by=By.CLASS_NAME, value="MMImage-Origin"
        )
        first_picture_again_src = first_picture_again.get_attribute("src")
        assert (
            first_picture_src == first_picture_again_src
        ), "Ошибка в переключении картинки."

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
