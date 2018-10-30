from selenium import webdriver
import time
br = webdriver.Firefox(executable_path='C:\Users\Student\Desktop\geckodriver.exe')
br.implicitly_wait(15) # wait's for the page to get done loading before it does anything with it
br.get('http://www.twitch.tv/')
# to fill out a form
search = br.find_element_by_name('nav-search-input')
search.send_keys('ablemabel')
search.submit()
time.sleep(5)
print(br.title)
