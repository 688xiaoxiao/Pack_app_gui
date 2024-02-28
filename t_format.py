from selenium.webdriver.common.by import By

# 通用的 XPath 模板
xpath_template = '//*[contains(text(),"{}")]/following-sibling::div'

# 定义元素名称与对应的定位信息的字典
element_names = ['应用名称', '应用类型', '版本号', '包类型', '环境', '更新时间', '备注', '构建时间']
element_locators = {name: (By.XPATH, xpath_template.format(name)) for name in element_names}

class Base:

    # 定义元素名称与对应的定位信息的字典
    element_locators = element_locators

    def find_element_by_name(self, element_name):
        xpath = self.element_locators[element_name]
        return xpath

base = Base().find_element_by_name("应用名称")
print(base)
