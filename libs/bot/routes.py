from os.path import join, isdir
from json import load
from time import sleep
import geckodriver_autoinstaller
from selenium.webdriver import Firefox, FirefoxOptions
gecko = geckodriver_autoinstaller.install(cwd=True)
opts = FirefoxOptions()
opts.headless = False
Firefox().get("https://www.google.com")


class Browser:
    opts = FirefoxOptions()
    opts.headless = False
    driver = None

    @staticmethod
    def set_url(name, page=""):
        return join(f"https://www.{name}.com", page)

    @property
    def status(self):
        if self.driver is None:
            return False
        else:
            return True

    def run(self):
        self.driver = Firefox()

    def close(self):
        if self.status:
            self.driver.close()

    def get(self, url):
        if self.status:
            self.driver.get(url)
            sleep(5)

    def get_element_by_name(self, name):
        return self.driver.find_element("name", name)
    
    def get_element_by_id(self, _id):
        return self.driver.find_element("id", _id)
    
    def get_element_by_class(self, class_name):
        return self.driver.find_element("css selector", class_name)

    def get_element_by_tag_name(self, tag_name):
        return self.driver.find_element("tag name", tag_name)

    def source(self):
        if self.status:
            self.execute("scrolling")
            self.driver.implicitly_wait(1)
            page_source = self.driver.page_source
            return page_source

    def execute(self, script):
        js = {
            "scrolling": lambda: self.driver.set_window_size(
                self.driver.execute_script('return document.body.parentNode.scrollWidth'),
                self.driver.execute_script('return document.body.parentNode.scrollHeight')
            )
        }
        if self.status and js.get(script) is not None:
            js.get(script)()

    def run_script(self, code):
        if self.status:
            self.driver.execute_script(code)
            sleep(5)


class GitHub:
    
    def __init__(self, username="circuitalmynds"):
        self.username = username        
        self.browser = Browser()
        self.browser.run()
        self.login()
    
    def add_member(self, repo, member="alanmatzumiya"):
        self.browser.get(self.browser.set_url("github", join(self.username, repo, "settings/access")))
        self.browser.get_element_by_class("summary.btn.btn-primary.mt-3").click()
        self.browser.get_element_by_name("member").send_keys(member)

    def create_repo(self, *names):
        for repo_name in names:
            self.browser.get(self.browser.set_url("github", "new"))
            code = f'''[r_name, r_desc, r_public, r_readme] = [
                    "name", "description", "visibility_public", "auto_init"
                ].map(
                e => document.querySelector("#repository_" + e)
            );
            [r_name.value, r_desc.value, r_public.checked, r_readme.checked] = [
                "{repo_name}", "{repo_name}", "checked", "checked"
            ];
            btn = document.querySelector('button.btn-primary');
            btn.disabled = false;
            setTimeout( () => btn.click(), 1000);'''
            self.browser.run_script(code)

    def login(self):
        self.browser.get(Browser.set_url("github", "login"))
        for key, value in load(open("/home/alanmatzumiya/credentials.json"))[self.username].items():
            if key == "user":
                self.browser.get_element_by_name("login").send_keys(value)
            elif key == "pwd":
                self.browser.get_element_by_name("password").send_keys(value)
        self.browser.get_element_by_name("commit").click()
