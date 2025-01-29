from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
import pickle
from chromedriver_py import binary_path

# 🔹 Данные для входа (замените на свои)
FOTOR_EMAIL = "zmeirlen@gmail.com"
FOTOR_PASSWORD = "Alihan91alijan!"
COOKIES_FILE_PATH = "fotor_cookies.pkl"

def save_cookies(driver, path):
    """Сохраняет cookies в файл."""
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    print("✅ Cookies сохранены.")

def load_cookies(driver, path):
    """Загружает cookies из файла, если они существуют."""
    if os.path.exists(path):
        with open(path, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("✅ Cookies загружены.")
    else:
        print("⚠ Cookies не найдены. Требуется авторизация.")

def is_logged_in(driver):
    """Проверяет, выполнен ли вход в систему. Если кнопка 'Log in' есть - значит, не вошли."""
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-header-button"))
        )
        print("❌ Cookies устарели или невалидны. Требуется повторная авторизация.")
        return False
    except:
        print("✅ Cookies актуальны, вход выполнен.")
        return True

def login_to_fotor(driver):
    """Автоматически выполняет вход в Fotor, если cookies неактуальны."""
    driver.get("https://www.fotor.com")

    # 🔹 Загружаем cookies и обновляем страницу
    load_cookies(driver, COOKIES_FILE_PATH)
    driver.refresh()
    time.sleep(5)

    # 🔹 Проверяем, актуальны ли cookies
    if is_logged_in(driver):
        return  # Если уже вошли, просто выходим из функции

    # 🔹 Если cookies устарели, выполняем новый вход
    print("🔹 Выполняем повторный вход...")

    try:
        # 🔹 Нажимаем кнопку "Log in"
        login_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "login-header-button"))
        )
        login_button.click()
        print("✅ Кнопка 'Log in' нажата.")
        time.sleep(3)

        # 🔹 Нажимаем "Continue with Email"
        continue_with_email_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'info') and contains(text(), 'Continue with Email')]"))
        )
        continue_with_email_button.click()
        print("✅ Кнопка 'Continue with Email' нажата.")
        time.sleep(3)

        # 🔹 Вводим email
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "emailWayStepInputEmail"))
        )
        email_input.send_keys(FOTOR_EMAIL)
        print(f"✅ Email '{FOTOR_EMAIL}' введен.")

        # 🔹 Нажимаем "Continue"
        continue_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button_reset_css.email_way_bottom_row_next"))
        )
        continue_button.click()
        print("✅ Кнопка 'Continue' нажата.")
        time.sleep(3)

        # 🔹 Вводим пароль
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "emailWayStepInputPassword"))
        )
        password_input.send_keys(FOTOR_PASSWORD)
        print("✅ Пароль введен.")

        # 🔹 Нажимаем кнопку "Log in"
        login_submit_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button_reset_css.email_way_bottom_row_next"))
        )
        login_submit_button.click()
        print("✅ Вход выполнен.")

        time.sleep(10)  # Ждем вход

        # 🔹 Сохраняем cookies после успешного входа
        save_cookies(driver, COOKIES_FILE_PATH)

    except Exception as e:
        print(f"❌ Ошибка при авторизации: {e}")

def swap_faces_and_download(image1_path, image2_path, download_dir):
    """Загружает два изображения, выполняет Face Swap и скачивает результат."""

    # Настройка Chrome
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Настройка для headless-режима (раскомментируйте, если нужен headless)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    # Используем Service для ChromeDriver
    service = Service(binary_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 🔹 Вход в Fotor
        login_to_fotor(driver)

        # 🔹 Переход к Face Swapper
        driver.get("https://www.fotor.com/apps/swapper/")
        print("✅ Открыт Face Swapper")
        time.sleep(5)

        # 🔹 Загрузка первого фото
        upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        upload_input.send_keys(image1_path)
        print("✅ Первое фото загружено.")
        time.sleep(10)

        # 🔹 Нажатие кнопки "+"
        plus_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".swap_target_upload_button__LlgSz"))
        )
        # Используем ActionChains для более надёжного клика
        ActionChains(driver).move_to_element(plus_button).click().perform()
        print("✅ Кнопка '+' нажата.")
        time.sleep(5)

        # 🔹 Загрузка второго фото
        upload_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        upload_input.send_keys(image2_path)
        print("✅ Второе фото загружено.")
        time.sleep(5)

        # 🔹 Сохранение скриншота сразу после загрузки второго фото
        driver.save_screenshot("/app/test_photos/fotor_swapper_debug_after_upload.png")
        print("📸 Скриншот после загрузки второго фото сохранен в /app/test_photos/fotor_swapper_debug_after_upload.png")

        # 🔹 Ожидание появления второго фото на странице
        try:
            # !! ВАЖНО: Замените селектор на тот, который соответствует РЕАЛЬНОМУ элементу на странице
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".layout-swapper-preview-image.second"))
            )
            print("✅ Второе фото появилось на странице.")
        except:
            print("❌ Второе фото не появилось на странице.")
            # Сохраняем HTML-код страницы для анализа
            with open("/app/test_photos/page_source.html", "w") as f:
                f.write(driver.page_source)
            print("❌ HTML-код страницы сохранен в /app/test_photos/page_source.html")
            return None

        # 🔹 Ожидание, пока кнопка "Swap Face Now" станет кликабельной
        swap_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".generate-button_generate_button__LStMd"))
        )

        # 🔹 Дополнительное ожидание
        time.sleep(5)

        # 🔹 Сохранение скриншота перед нажатием кнопки "Swap Face Now"
        driver.save_screenshot("/app/test_photos/fotor_swapper_debug_before_swap.png")
        print("📸 Скриншот перед нажатием Swap Face Now сохранен в /app/test_photos/fotor_swapper_debug_before_swap.png")

        # 🔹 Нажатие кнопки "Swap Face Now"
        swap_button.click()
        print("✅ Начался процесс замены лиц.")

        # 🔹 Ожидание появления окна с кнопкой подтверждения
        message_found = False
        start_time = time.time()
        timeout = 300

        while time.time() - start_time < timeout:
            try:
                message_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".remove-tip_desc__6RIm1"))
                )
                if "We'll keep your generated images for 24 hours!" in message_element.text:
                    print("✅ Сообщение о сохранении изображений появилось.")
                    message_found = True
                    break
            except:
                print("🔄 Ожидание появления сообщения...")
                time.sleep(10)

        if message_found:
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".primary-button_primary_button__-uGVm"))
            )
            confirm_button.click()
            print("✅ Подтверждение выполнено.")
        else:
            print("❌ Сообщение не появилось.")
            return None

        # 🔹 Ожидание загрузки файла
        time.sleep(20)

        # 🔹 Поиск последнего загруженного файла
        files = os.listdir(download_dir)
        paths = [os.path.join(download_dir, basename) for basename in files]
        latest_file = max(paths, key=os.path.getctime)
        print(f"✅ Файл сохранен: {latest_file}")

        return latest_file

    finally:
        driver.quit()

# 🔹 Пример использования
image1 = "/app/test_photos/book_image.jpg"  # Замените на путь к вашему первому изображению
image2 = "/app/test_photos/alihan.png"  # Замените на путь к вашему второму изображению
download_directory = "/app/test_photos"

downloaded_file = swap_faces_and_download(image2, image1, download_directory)
print(f"📥 Загруженный файл: {downloaded_file}")