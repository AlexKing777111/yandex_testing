import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class YandexSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(
            executable_path=r"D:\Dev\yandex_testing\geckodriver.exe"
        )

    def test_search_in_yandex_ru(self):
        driver = self.driver
        driver.get("http://www.yandex.ru")
        assert driver.find_element(
            by=By.CSS_SELECTOR, value="#text"
        ), "Поле поиска не найдено"
        search = driver.find_element(by=By.CSS_SELECTOR, value="#text")
        search.send_keys("тензор")
        time.sleep(1)
        assert driver.find_element(
            by=By.CLASS_NAME, value="mini-suggest__popup-content"
        ), "Таблица с подсказками suggest отсутствует."
        search.send_keys(Keys.RETURN)
        time.sleep(3)
        assert driver.find_element(
            by=By.XPATH, value="//ul[@id='search-result']"
        ), "Таблица результатов поиска отсутствует."
        driver.find_element(
            by=By.PARTIAL_LINK_TEXT,
            value="tensor",
        ).click()
        time.sleep(1)
        new_tab = driver.window_handles[1]
        driver.switch_to.window(f"{new_tab}")
        assert "tensor.ru" in driver.current_url, "Неверный сайт."

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
