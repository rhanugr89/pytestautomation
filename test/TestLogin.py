import pdb
import time
from traceback import print_tb

import pytest
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v140.service_worker import set_force_update_on_page_load
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup")
class TestLogin:

    def test_login_with_valid_credentials(self):
        enter_user_email = (By.CSS_SELECTOR, "#userEmail")
        enter_password =  (By.CSS_SELECTOR, "#userPassword")
        product_to_buy = "ADIDAS ORIGINAL"
        wait = WebDriverWait(self.driver,10)
        email = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#userEmail")))
        email.send_keys("hanamantaste@gmail.com")
        password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#userPassword")))
        password_field.send_keys("Raghapur@1989")
        self.driver.find_element(By.CSS_SELECTOR,"#login").click()
        products = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,".card-body")))
        for product in products:
            product_text = product.find_element(By.CSS_SELECTOR,"b").text
            # print(product_text)
            if product_text.__eq__(product_to_buy):
                product.find_element(By.CSS_SELECTOR,"button .fa-shopping-cart").click()
                toast_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".toast-message"))).text.strip()
                assert toast_message=="Product Added To Cart"
                break
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"[routerlink='/dashboard/cart']"))).click()
        except ElementClickInterceptedException as e:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[routerlink='/dashboard/cart']"))).click()
        check_out_page = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".wrap.cf")))
        self.driver.find_element(By.XPATH,"//button[text()='Checkout']").click()
        enter_country = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"[placeholder='Select Country']")))
        enter_country.send_keys("Ind")
        select_county  = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,".ta-results button span ")))

        for country in select_county:
            # print(country.text)
            if country.text.strip()=="India":
                country.click()
                break
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        place_order_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"a.action__submit")))
        place_order_button.click()
        order_placed = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".toast-title"))).text.strip()
        assert order_placed=="Order Placed Successfully"
        thank_you_for_the_order =self.driver.find_element(By.CSS_SELECTOR,".hero-primary").text.strip()
        assert thank_you_for_the_order=="THANKYOU FOR THE ORDER."
        order_id1 = self.driver.find_element(By.CSS_SELECTOR,"label.ng-star-inserted").text.strip()
        order_id = order_id1.replace("|", "").strip()

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> : ",order_id)
        click_on_order = self.driver.find_elements(By.CSS_SELECTOR,"[routerlink='/dashboard/myorders']")
        click_on_order[1].click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,".table.table-bordered")))
        table_rows = self.driver.find_elements(By.CSS_SELECTOR,"tbody tr")
        for row in table_rows:
            order = row.find_element(By.CSS_SELECTOR,"th").text.strip()
            print("order===============================",order)
            if order in order_id:
                row.find_element(By.CSS_SELECTOR,"button.btn.btn-primary").click()
                break
        history = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.col-text.-main"))).text.strip()
        expected_id = history.replace("|", "").strip()
        assert order_id == expected_id, f"Expected and Actual is not matching with {order_id} and actual {expected_id}"
        print("history --------------------------------",history)
        # thanks_text = self.driver.find_element(By.CSS_SELECTOR,"[class='hero-primary']").text.strip()      
        # expected_text = "Thankyou for the order.".capitalize()
        # assert thanks_text == expected_text
        product_title = self.driver.find_element(By.CSS_SELECTOR,"div.title").text.strip()
        print("Product Title>>",product_title)
        assert  product_to_buy == product_title
        print("ALL DONE")
        # pdb.set_trace()
        



