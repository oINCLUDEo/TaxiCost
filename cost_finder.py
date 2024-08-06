import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service as ChromiumService

from config import url_maxim, url_citimobil
from transliterate import translit
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


def citimobil(actual_address, end_address):
    city = translit(actual_address.split(', ')[0], language_code='ru', reversed=True)
    other_address = actual_address.split(', ')[1]
    other_address2 = end_address.split(', ')[1]
    # TODO Должен быть словарь для исправления некоторых регионов
    if city == "Ul'janovsk":
        city = 'uljanovsk'

    url = url_citimobil + city
    with webdriver.Chrome(service=ChromiumService(ChromeDriverManager().install())) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 5)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Заказать такси')]"))).click()

        # Доступ к shadow-host элементу
        shadow_host = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#myWidget > div')))
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)

        wait_shadow = WebDriverWait(shadow_root, 5)

        # Доступ к текстовым полям внутри shadow-root
        first_address = wait_shadow.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                          'textarea['
                                                                          'placeholder="Введите адрес '
                                                                          'подачи"]')))
        first_address.send_keys(actual_address)

        time.sleep(1)
        wait_shadow.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                      'div > div > div.MuiBox-root.shadows-gmb2ih-root-openMap > '
                                                      'div.os-host.os-host-foreign.os-theme-dark.os-host-resize-disabled'
                                                      '.os-host'
                                                      '-scrollbar-horizontal-hidden.os-host-scrollbar-vertical-hidden'
                                                      '.\.os-theme'
                                                      '-dark.os-host-flexbox.os-host-transition > div.os-padding > div > '
                                                      'div.os-content > div > div.MuiBox-root.shadows-cy4txf-root > div > '
                                                      'div.shadows-98ow2v-wrapper > div > div:nth-child(1) > div > div > '
                                                      'div >'
                                                      'div > div.shadows-1925vua-popperRoot.MuiPopper-root > div > '
                                                      'div.os-padding > div > div.os-content > div > ul > li:nth-child('
                                                      '1)'))).click()

        last_address = wait_shadow.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[placeholder="Введите '
                                                                                          'адрес доставки"]')))
        last_address.send_keys(end_address)
        time.sleep(1)
        wait_shadow.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                      'div > div > div.MuiBox-root.shadows-gmb2ih-root-openMap > '
                                                      'div.os-host.os-host-foreign.os-theme-dark.os-host-resize-disabled'
                                                      '.os-host'
                                                      '-scrollbar-horizontal-hidden.os-host-scrollbar-vertical-hidden'
                                                      '.\.os-theme'
                                                      '-dark.os-host-flexbox.os-host-transition > div.os-padding > div > '
                                                      'div.os-content > div > div.MuiBox-root.shadows-cy4txf-root > div > '
                                                      'div.shadows-98ow2v-wrapper > div > div:nth-child(2) > div > div > '
                                                      'div >'
                                                      'div > div.shadows-1925vua-popperRoot.MuiPopper-root > div > '
                                                      'div.os-padding > div > div > div > ul > li:nth-child(1)'))).click()

        initial_value = wait_shadow.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                          'div > div > div.MuiBox-root.shadows-gmb2ih-root'
                                                                          '-openMap > '
                                                                          'div.os-host.os-host-foreign.os-theme-dark.os'
                                                                          '-host'
                                                                          '-resize-disabled.os-host-scrollbar-horizontal'
                                                                          '-hidden'
                                                                          '.os-host-scrollbar-vertical-hidden.\.os-theme'
                                                                          '-dark.os'
                                                                          '-host-flexbox.os-host-transition > '
                                                                          'div.os-padding >'
                                                                          'div > div.os-content > div > '
                                                                          'div.MuiBox-root.shadows-e9l7sy-container > div '
                                                                          '> div >'
                                                                          'div > div > div > '
                                                                          'div.swiper-slide.swiper-slide-active'
                                                                          '> div > button > div > '
                                                                          'span.MuiTypography-root.MuiTypography-normal'
                                                                          '.shadows'
                                                                          '-11nzmjz-root-priceText'))).text

        a = WebDriverWait(shadow_root, 15).until_not(lambda a: a.find_element(By.CSS_SELECTOR,
                                                                              'div > div > div.MuiBox-root.shadows-gmb2ih'
                                                                              '-root'
                                                                              '-openMap > '
                                                                              'div.os-host.os-host-foreign.os-theme-dark'
                                                                              '.os-host'
                                                                              '-resize-disabled.os-host-scrollbar'
                                                                              '-horizontal-hidden'
                                                                              '.os-host-scrollbar-vertical-hidden.\.os'
                                                                              '-theme-dark.os'
                                                                              '-host-flexbox.os-host-transition > '
                                                                              'div.os-padding >'
                                                                              'div > div.os-content > div > '
                                                                              'div.MuiBox-root.shadows-e9l7sy-container > '
                                                                              'div > div >'
                                                                              'div > div > div > '
                                                                              'div.swiper-slide.swiper-slide-active'
                                                                              '> div > button > div > '
                                                                              'span.MuiTypography-root.MuiTypography'
                                                                              '-normal.shadows'
                                                                              '-11nzmjz-root-priceText').text == initial_value)

        # Получаем стоимость эконом такси
        costs = wait_shadow.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                  'div > div > div.MuiBox-root.shadows-gmb2ih-root'
                                                                  '-openMap > '
                                                                  'div.os-host.os-host-foreign.os-theme-dark.os-host'
                                                                  '-resize-disabled.os-host-scrollbar-horizontal-hidden'
                                                                  '.os-host-scrollbar-vertical-hidden.\.os-theme-dark.os'
                                                                  '-host-flexbox.os-host-transition > div.os-padding > '
                                                                  'div > div.os-content > div > '
                                                                  'div.MuiBox-root.shadows-e9l7sy-container > div > div > '
                                                                  'div > div > div > div.swiper-slide.swiper-slide-active '
                                                                  '> div > button > div > '
                                                                  'span.MuiTypography-root.MuiTypography-normal.shadows'
                                                                  '-11nzmjz-root-priceText')))
        return costs.text


# main('Ульяновск, проспект Академика Филатова', 'Ульяновск, Московское шоссе 108')
