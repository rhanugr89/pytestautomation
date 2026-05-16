from selenium import  webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class LoginPage:
    def __init__(self,driver):
        self.driver =driver
        self.wait = WebDriverWait(self.driver,20)

    enter_userEmail = (By.CSS_SELECTOR,"#userEmail")
    enter_password = (By.CSS_SELECTOR,"#userPassword")



    def login_to_the_application(self,username,password):
        email =  self.wait.until(EC.visibility_of_element_located(self.enter_userEmail))
        email.send_keys(username)
        password_field = self.wait.until(EC.visibility_of_element_located(self.enter_userEmail))
        password_field.send_keys(password)




