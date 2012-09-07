#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# this needs to be explained
from unittestzero import Assert

# let's jump in the deep end and test account creation with restmail.
# first, get a browser webdriver
driver = webdriver.Firefox()
# open up 123done
driver.get('http://dev.123done.org/')
# wait for the login button to appear.
# we can do this by waiting for the spinner to disappear:
# (honestly, this is how the code works now, but I'd rather wait for what I do want, not wait for what I don't want to disappear.)
WebDriverWait(driver, 5000).until(
    lambda driver: not driver.find_element_by_css_selector('li.loading img').is_displayed()
# check the page title as a sanity check
Assert.equal(driver.title, '123done - your tasks, simplified')

# find and click sign up
driver.find_element_by_css_selector('#loggedout > button').click()
# switch to the popup, using its title __persona_dialog
# seems like we should wait for the window to open up? todo
WebDriverWait(driver, 8000).until(
    lambda driver: '__persona_dialog' in driver.window_handles)
driver.switch_to_window('__persona_dialog')
# check the page title, again, as a sanity check
Assert.equal(driver.title, 'Mozilla Persona: A Better Way to Sign In')
# give it a phony restmail.net address and click 'next'
emailInput = driver.find_element_by_id('email')
emailInput.clear()

# here's how we generate some test user creds
import time
testuser_email = '123donetest_%s@restmail.net' % repr(time.time())
testuser_password = 'Password12345'

email.send_keys(testuser_email)
# hit 'next'
driver.find_element_by_css_selector('button.start').click()
# wait for the page to reload by checking the #password el is displayed.
# todo is there a way to watch for page load event?
WebDriverWait(driver, 5000).until(
    lambda driver: driver.find_element_by_id('password').is_displayed())
# fill in the two password fields
passwordInput = driver.find_element_by_id('password')
passwordInput.clear()
passwordInput.send_keys(testuser_password)
verifyPasswordInput = driver.find_element_by_id('vpassword')
verifyPasswordInput.clear()
verifyPasswordInput.send_keys(testuser_password)
# hit 'done' button
driver.find_element_by_id('verify_user').click()

# verify you see the 'check your email' screen last.
WebDriverWait(driver, 5000).until(lambda driver: 
    driver.find_element_by_css_selector('#wait .contents h2 + p strong').is_displayed())

# I kind of think this isn't worth it from here on out.
# nah, let's make it epic in scale.

# now we have to wait for the email round trip:
# poll against restmail until the verification email arrives
import requests
import json
import re
from time import sleep
timer = 0
timeout = 30
restmail_url = 'https://restmail.net/mail/' + testuser_email.split('@')[0]
response_json = []
while timer < timeout:
    sleep(1)
    timer += 1
    response = requests.get(restmail_url, verify=False)
    response_json = json.loads(response.content)
    if response.json != []:
        break
Assert.not_equal(timer, timeout, "restmail timed out")

# ok, we got the inbox, assume the email is the first message.
# grab the first message and find the verify link
verify_regex = 'https:\/\/.*verify_email_address\?token=.{48}'
verify_link = re.search(verify_regex, response_json[0]['text']).group(0)
Assert.not_none(verify_link, "verify link not found in acct creation email")
        
# switch to the main window and open up that link


# verify that the page says success message
# verify that the redirect happens
# verify that the dialog got dismissed
# verify that you're actually logged in
# go ahead and log out :-) it's all good now

# problems to talk about -- maybe move this to the next file.
#  - first off, you can't, ever, use XPaths to find elements. so brittle.
#  - you don't want to hard-code selectors, since the class names could change.
#  - but beyond that, what you really want is to abstract out, not just
#    selectors, but all the low-level page interactions: abstract out the 
#    sequence of steps needed to log in, or log out, or select an email from the list
#    shown in the dialog.
#  - this is the page object model thing.
#  - what you wind up with is isolated selectors inside the POMs, 
#    and the tests themselves become really short and use a real user-centric DSL
#    to describe steps: here's the entirety of test_sign_in.py:

class TestSignIn:

    @pytest.mark.nondestructive
    def test_that_user_can_sign_in(self, mozwebqa):
        home_pg = HomePage(mozwebqa)
        home_pg.go_to_home_page()
        home_pg.sign_in()
        Assert.true(home_pg.is_logged_in)
