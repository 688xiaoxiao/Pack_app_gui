from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
from cfg import *


class Base:

    def __init__(self, driver):
        self.d = driver
        self.d.implicitly_wait(8)
        self.wait = WebDriverWait(driver, 8)
        self.d.maximize_window()
        self.login_by_email()


    username_loc = (By.XPATH, '//input[@name="userName"]')
    passwd_loc = (By.XPATH, '//input[@name="password"]')
    privacy_checkbox_loc = (By.XPATH, '//span[@class="el-checkbox__inner"]')
    login_btn_loc = (By.XPATH, '//button[@type="button"][1]')
    

    # 确定 按钮
    sure_loc = (By.XPATH, '//*[contains(text(), "确定")]')
    # alert
    alert_loc = (By.XPATH, '//*[@class="zk-message__content"]')

    # 操作人
    operator_loc = (By.XPATH, '//*[@placeholder="操作人"]')
    # 搜索
    search_btn_loc = (By.XPATH, '//*[contains(text(),"搜索")]')
    # 列表第一行 
    first_tr_loc = (By.XPATH, '//*[@id="zk-table"]/div[1]/div[2]/div[2]/table/tbody/tr[1]')
    # 状态
    status_loc = (By.XPATH, './td[5]/div[2]//span/span')
    # 复制
    copy_loc = (By.XPATH, './/*[contains(text(), "复制")]')
    # 详情
    detail_loc =   (By.XPATH, './/*[contains(text(), "详情")]')

    # 应用名称
    app_name_loc = (By.XPATH, '//*[contains(text(),"应用名称")]/following-sibling::div')
    # 应用类型
    app_type_loc = (By.XPATH, '//*[contains(text(),"应用类型")]/following-sibling::div')
    # 版本号
    app_version_loc = (By.XPATH, '//*[contains(text(),"版本号")]/following-sibling::div')
    # 包类型
    apk_type_loc = (By.XPATH, '//*[contains(text(), "包类型")]/following-sibling::div')
    # 环境
    apk_environment_loc = (By.XPATH, '//*[contains(text(), "环境")]/following-sibling::div')
    # 完成时间
    update_time_loc = (By.XPATH, '//*[contains(text(), "更新时间")]/following-sibling::div')
    # 构建备注
    remark_loc = (By.XPATH, '//*[contains(text(), "备注")]/following-sibling::div')
    # 构建时间
    build_time_loc = (By.XPATH, '//*[contains(text(), "构建时间")]/following-sibling::div')
    
    apk_name = (By.XPATH, '//*[starts-with(text(), " app-")]')

    exernal_img_qr_code_loc = (By.XPATH, '//*[contains(text(), "外网下载地址")]/../../..')
    check_larger_img = (By.XPATH, './/i')
    larger_img = (By.XPATH, '//body//*[@loading-background="transparent"]/img')


    def scroll_ele_into_view(self, webelement):
        """使元素处于正中"""
        self.d.execute_script("arguments[0].scrollIntoView({block:'center',inline:'center'})", webelement)
        time.sleep(0.2)


    def get_site(self, url):  
        """访问网址, 并等待1.5秒"""  
        self.d.get(url)
        time.sleep(1.5)


    def check_if_internal_work(self):
        """检查是否为内网"""
        pass


    def type_account(self):
        """输入账号"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.username_loc)).send_keys(ACCOUNT)
        except:
            traceback.print_exc() 
        
        
    def type_passwd(self):
        """输入密码"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.passwd_loc)).send_keys(PASSWD)
        except:
            traceback.print_exc()  
        
        
    def click_privacy(self):
        """点击隐私协议"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.privacy_checkbox_loc)).click() 
        except:
            traceback.print_exc()  
        
    
    def click_login_btn(self):
        """点击login按钮"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.login_btn_loc)).click()
            time.sleep(2.5)
        except:
            traceback.print_exc()
        
    
    def check_on_appserve_page(self):
        """判断是否在appServe页面"""
        while True:
            if "https://appff.zeekrlife.com/#/appServe" in self.d.current_url:
                time.sleep(1.5)  
                break


    def login_by_email(self):
        """通过邮件登录"""
        self.get_site(LOGIN_URL)
        self.type_account()
        self.type_passwd()
        # self.click_privacy()
        self.click_login_btn()
        self.check_on_appserve_page()
        

    def click_new_build(self):
        """点击新构建按钮"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.new_build_loc)).click()
        except:
            traceback.print_exc()
          

    def click_sure(self):
        """点击确定"""
        try:
            self.wait.until(EC.element_to_be_clickable(self.sure_loc)).click()
        except:
            traceback.print_exc()  
        
        
    def get_build_result(self):
        """打印构建结果"""
        try:
            # alert_info = self.wait.until(EC.visibility_of_element_located(self.alert_loc)).text.strip()
            alert_ele = self.wait.until(EC.visibility_of_element_located(self.alert_loc))
            time.sleep(0.3)
            alert_info = alert_ele.text.strip()
            print(f"创建结果 ========> ：{alert_info}")
        except:
            print("none") 


    def filter_operator(self):
        """过滤操作人"""
        self.wait.until(EC.visibility_of_element_located(self.operator_loc)).send_keys(OPERATOR)            
        self.wait.until(EC.visibility_of_element_located(self.search_btn_loc)).click()
        time.sleep(0.5)


    def click_copy(self, app_build_url:str, if_copy=True):
        """点击复制 进行构建
        
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
                self.get_build_result()
        except:
            traceback.print_exc()
    

    def get_apk_info(self):
        """拿到app相关信息，如应用名称，应用类型，版本号，包类型，环境，完成时间"""
        app_name = self.wait.until(EC.visibility_of_element_located(self.app_name_loc)).text.strip()
        app_type = self.wait.until(EC.visibility_of_element_located(self.app_type_loc)).text.strip()
        app_version = self.wait.until(EC.visibility_of_element_located(self.app_version_loc)).text.strip()
        apk_type = self.wait.until(EC.visibility_of_element_located(self.apk_type_loc)).text.strip()
        apk_environment = self.wait.until(EC.visibility_of_element_located(self.apk_environment_loc)).text.strip()
        update_time = self.wait.until(EC.visibility_of_element_located(self.update_time_loc)).text.strip()
        remark = self.wait.until(EC.presence_of_element_located(self.remark_loc)).text.strip()
        return app_name, app_type, app_version, apk_type, apk_environment, update_time, remark
    

    def get_1st_status_value(self):
        """拿到第一行状态值"""
        self.d.refresh()   # 分发平台有bug, 成功后得再刷新下页面，否则appname拿不到 # 这里刷新后，还应继续筛选操作人
        time.sleep(2)
        self.filter_operator()
        first_tr_ele = self.wait.until(EC.visibility_of_element_located(self.first_tr_loc))
        status_value = first_tr_ele.find_element(*self.status_loc).text.strip()

        return status_value, first_tr_ele


    def get_build_detail_info(self):
        """拿到构建详情"""
        first_tr_ele = self.get_1st_status_value()[1]
        detail_btn = first_tr_ele.find_element(*self.detail_loc)
        detail_btn.click()
        time.sleep(2.5)
        app_name, app_type, app_version, apk_type, apk_environment, update_time, remark = self.get_apk_info()
        print(app_name, app_type, app_version, apk_type, apk_environment, update_time, remark)

        return app_name, app_type, app_version, apk_type, apk_environment, update_time, remark


    def save_qr_code(self, appid):
        """保存 外网下载地址二维码
        app_type in ["Android", "IOS"]
        
        return build_result"""
        try:
            # if appid:
            #     self.get_site(APP_BUILD_BASE_URL+ appid)
            # else:
            #     return ["请选择应用"]*7
            if not appid:
                return ["请选择应用"]*7
            
            while True:
                status_value = self.get_1st_status_value()[0]

                if status_value == "成功":        
                    app_name, app_type, app_version, apk_type, apk_environment, update_time, remark = self.get_build_detail_info()                         
                    # apk_name = self.wait.until(EC.visibility_of_element_located(self.apk_name)).text.strip()  # 之前展示apkname，现在不展示了
                    exernal_img_qr_code = self.wait.until(EC.visibility_of_element_located(self.exernal_img_qr_code_loc))
                    # 移动到QR code
                    ActionChains(self.d).move_to_element(exernal_img_qr_code).perform()
                    # QR code 中间的 i
                    exernal_img_qr_code.find_element(*self.check_larger_img).click()

                    large_img = self.wait.until(EC.visibility_of_element_located(self.larger_img))
                    time.sleep(2)
                    # qr_code_img
                    if app_type == "Android":
                        large_img.screenshot(f"./qr_code_img/Android.png")
                    else:
                        large_img.screenshot(f"./qr_code_img/IOS.png")

                    print(f"{appid} qrcode saves successfully")
                    build_result = [status_value, update_time[5:], apk_type, app_name, app_type, app_version, apk_environment, remark]
                    print(f"{build_result}")
                    return build_result

                elif status_value in ["失败", "中止"]:
                    app_name, app_type, app_version, apk_type, apk_environment, update_time, remark = self.get_build_detail_info()
                    return [status_value, update_time[5:], apk_type, app_name, app_type, app_version, apk_environment, remark]
                                              
                elif status_value in ["未开始", "构建中"]:
                    continue

        except:
            traceback.print_exc()  
        

    # def pack_app_for_gui(self, left_appid=None, right_appid=None):  # 从配置文件 拿 appid
    def pack_app_for_gui(self, left_appid=None, right_appid=None):    # 57是 em 以色列 android, 45 是em以色列 ios
        """为GUI, 执行复制，保存qrcode到本地"""
        
        def copy_and_save_qr_img(appid):
            """封装复制 和 保存 qr img"""
            app_url = APP_BUILD_BASE_URL + appid
            self.click_copy(app_url)
            build_result = self.save_qr_code(appid) 
            # 释放浏览器进程
            self.d.quit()
            return build_result

        if left_appid and right_appid is None:
            left_build_result = copy_and_save_qr_img(left_appid)
            return left_build_result, [""]*7

        elif left_appid is None and right_appid:
            right_build_result = copy_and_save_qr_img(right_appid)
            return [""]*7, right_build_result
        
        else:
            left_app_url = APP_BUILD_BASE_URL + left_appid
            right_app_url = APP_BUILD_BASE_URL + right_appid

            self.click_copy(left_app_url)
            # 打开新的tab并切换过去
            self.d.execute_script("window.open('about:blank', '_blank');")
            self.d.switch_to.window(self.d.window_handles[1])
            # IOS
            self.click_copy(right_app_url)
            right_build_result = self.save_qr_code(right_appid)
            # 关闭这个tab, 只保留左侧的tab, 这样可以不用记录tab 对应的 handle
            self.d.close()

            self.d.switch_to.window(self.d.window_handles[0])
            self.d.refresh()
            time.sleep(2)
            left_build_result = self.save_qr_code(left_appid)
            # 若释放浏览器进程 则当再次Run 会报异常 urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='localhost', port=54638): Max retries exceeded with url: /session/fc521d39a481046e5afae539a47754c8/url (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x000002469CDBA8C0>: Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。'))
            self.d.quit()
            return left_build_result, right_build_result
        
        
# result = Base().pack_app_for_gui(left_appid="23", right_appid="22")
# print(result)
# get_build_info = Base().pack_app_for_gui   # 
# print(get_build_info)