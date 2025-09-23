import pytest
import allure  # Импорт Allure для репортинга
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.feature("Login Functionality")  # Группировка тестов по функционалу
@allure.severity(allure.severity_level.CRITICAL)  # Уровень важности теста
@allure.title("Successful Login Test")  # Название теста в отчёте
@allure.description("Тест проверяет успешный вход с правильными учетными данными на сайт the-internet.herokuapp.com")  # Описание
def test_successful_login(driver):
    with allure.step("Открыть страницу логина"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Заполнить форму логина правильными данными"):
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys("tomsmith")

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("SuperSecretPassword!")

    with allure.step("Нажать кнопку входа"):
        submit_button = driver.find_element(By.TAG_NAME, "button")
        submit_button.click()

    with allure.step("Проверить успешную авторизацию"):
        success_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )
        assert "You logged into a secure area!" in success_element.text, "Сообщение об успехе не найдено"
        assert "secure" in driver.current_url, "URL не содержит 'secure'"

@allure.feature("Login Functionality")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Unsuccessful Login Test")
@allure.description("Тест проверяет неудачную попытку входа с неправильными учетными данными на сайт the-internet.herokuapp.com")
def test_unsuccessful_login(driver):
    with allure.step("Открыть страницу логина"):
        driver.get("https://the-internet.herokuapp.com/login")

    with allure.step("Заполнить форму логина неправильными данными"):
        username_input = driver.find_element(By.ID, "username")
        username_input.clear()
        username_input.send_keys("invalid_user")

        password_input = driver.find_element(By.ID, "password")
        password_input.clear()
        password_input.send_keys("wrong_password")

    with allure.step("Нажать кнопку входа"):
        submit_button = driver.find_element(By.TAG_NAME, "button")
        submit_button.click()

    with allure.step("Проверить сообщение об ошибке"):
        error_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )
        assert "Your username is invalid!" in error_element.text, "Сообщение об ошибке не найдено"
