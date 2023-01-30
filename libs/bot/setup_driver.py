from os.path import join, isdir
from bs4 import BeautifulSoup
if not isdir('v0.30.0'):
    import geckodriver_autoinstaller
    gecko = geckodriver_autoinstaller.install(cwd=True)
from selenium.webdriver import Firefox, FirefoxOptions
opts = FirefoxOptions()
opts.headless = False
driver = Firefox(
    executable_path=join('v0.30.0', 'geckodriver'), options=opts
)
execute_script = driver.execute_script
set_window_size = driver.set_window_size
get_source = lambda: BeautifulSoup(driver.page_source, 'html.parser').prettify()


def scrolling():
    script = 'return document.body.parentNode.scroll'
    set_window_size(
        execute_script(script + 'Width'),
        execute_script(script + 'Height')
    )


def fb_login():
    driver.get("https://www.facebook.com/login.php")
    scrolling()
    email, password = [driver.find_element_by_id(e) for e in ("email", "pass")]
    email.send_keys(input('email: ')), password.send_keys(input('password: '))
    driver.find_element_by_name("login").click()
    scrolling()
    print(get_source())

fb_login()