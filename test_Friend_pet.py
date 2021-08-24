import pytest
from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Когда помещаю инициализацию драйвера в фикстуру выдает ошибку не пойму почему.
pytest.driver = webdriver.Chrome('C:/Program Files/Dr/chromedriver.exe')

@pytest.fixture(autouse=True)
def testing():
   # неявное ожидание (ожидание элементов 3 сек)
   pytest.driver.implicitly_wait(3)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   # неявное ожидание (опрашивать структуру документа на наличие элемента с id email)
   email = pytest.driver.find_element_by_id("email")
   yield
   pytest.driver.quit()

# проверка карточек питомцев
def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys(valid_email)
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

imagesS = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
namesS = pytest.driver.find_elements_by_css_selector('.card-deck .card-body .card-title')
descriptionsS = pytest.driver.find_elements_by_css_selector('.card-deck .card-body .card-text')

# проверка
for i in range(len(namesS)):
   assert imagesS[i].get_attribute('src') != ''
   assert namesS[i].text != ''
   assert descriptionsS[i].text != ''
   assert ', ' in descriptionsS[i]
   parts = descriptionsS[i].text.split(", ")
   assert len(parts[0]) > 0
   assert len(parts[1]) > 0

# проверка таблицы питомцев
def test_table_my_pets():
   # Явное ожидание
   element = WebDriverWait(pytest.driver, 5).until(
      EC.presence_of_element_located((By.ID, "email"))
   )
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys(valid_email)
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # переходим на страницу со списком питомцев пользователя
   pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()
   # получаем количество питомцев из статистики
   count_of_my_pets = pytest.driver.find_element_by_css_selector('div.\\.col-sm-4.left').text.split()
   # получаем количество строк из таблицы Все мои питомцы
   all_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr')
   # получаем количество питомцев с фото
   images = pytest.driver.find_elements_by_tag_name('img')
   value_of_my_pets = pytest.driver.find_elements_by_xpath('//tbody/tr/td')  # получаем данные из таблицы
   names = value_of_my_pets[::4]  # извлекаем имена
   breed = value_of_my_pets[1:-1:4]  # извлекаем породу
   age = value_of_my_pets[2:-1:4]  # извлекаем возраст

   # Присутствуют все питомцы
   for i in range(len(all_my_pets)):
      assert len(all_my_pets) is int(count_of_my_pets[(2)])

   # у половины питомцев есть фото,
   for i in range(len(all_my_pets)):
      assert len(images) / len(all_my_pets) > 0, 5

   # У всех питомцев есть имя, возраст и порода,
   for i in range(len(value_of_my_pets)):
      assert value_of_my_pets[i].text != ''

   # У всех питомцев разные имена,
   for i in range(len(names)):
      assert len(names) is len(set(names))




