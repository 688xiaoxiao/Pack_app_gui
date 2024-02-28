import logging
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logger_config import configure_logger  # 导入日志配置函数

# 配置日志
configure_logger()

class Base:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.first_tr_loc = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div[3]/table/tbody/tr[1]/td[1]')
        self.copy_loc = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div[3]/table/tbody/tr[1]/td[6]/span')
        self.sure_loc = (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[3]/div/div[3]/button[2]')
    
    def click_copy(self, app_build_url: str, if_copy=True):
        """点击复制进行构建
        
        app_build_url in [ANDROID_BUILD_URL, IOS_BUILD_URL]
        """
        try:
            self.get_site(app_build_url)
            # time.sleep(1)                 # raise TimeoutException(message, screen, stacktrace)
            self.filter_operator()
            first_tr_ele = self.wait.until(EC.visibility_of_element_located(self.first_tr_loc))
            # 点击复制
            if if_copy:
                time.sleep(0.5)
                first_tr_ele.find_element(*self.copy_loc).click()
                self.wait.until(EC.element_to_be_clickable(self.sure_loc)).click()
                # 打印构建结果
                build_result = self.get_build_result()
                
                # 记录日志
                logger = logging.getLogger(__name__)
                logger.info(f"Build result: {build_result}")
        except:
            # 记录异常日志
            logger = logging.getLogger(__name__)
            logger.exception("An error occurred in click_copy method")
