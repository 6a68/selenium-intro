#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# let's jump in the deep end and test account creation with restmail.
# open up 123done
# wait for the spinner to turn into the login button
# click the login button
# switch to the popup, using its title __persona_dialog
# click sign up
# give it a phony restmail.net address and dummy password
# hit submit
# poll against restmail until the verification email arrives
# extract the verification link out of the email
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
