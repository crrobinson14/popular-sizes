Popular Sizes
=============

Extract screen shots of a Web site at sizes reported to be popular by Google
Analytics.

Setup
-----

Unfortunately this is a multi-step process - there is no wizard for getting API
access to Google Analytics reports (Google: hint, hint!)

1.  Clone this repository into a local working directory.
1.  Go to the Google API Console at https://cloud.google.com/console/project,
    make sure you are logged in as the correct user ID (if you have more than
    one), and select or create the project you want to work in.
1.  Select "APIs & Auth" > "APIs" and make sure "Analytics API" is turned on.
1.  Select "APIs & Auth" > "Credentials" and select "Create New Client ID" under
    OAuth. If you have already generated an ID you can skip this step. **YOU
    MUST SELECT "INSTALLED APPLICATION" THEN "OTHER" IN THE NEXT STEP!**
1.  Select "APIs & Auth" > "Consent Screen". If "Product name" is blank, you
    must fill this in before proceeding - it doesn't matter what you put here.
    (Select an appropriate e-mail address too.)
1.  Copy the file this process sends you to this directory and call it
    "client_secrets.json".
1.  Go to your Analytics account and the profile you want to work with. Go to
    "Admin" > "Profile Settings" and make note of the "View ID" on this screen.
1.  Copy config_sample.py to config.py and edit to suit. At the very least you
    need to put the Account ID from the step above
1.  Make sure you have Python 2.7 installed, and this project's dependencies
    (yeah, yeah, requirements.txt - feel free to send a Pull Request):

        python --version
        sudo easy_install https://gdata-python-client.googlecode.com/files/gdata-2.0.18.tar.gz
        sudo easy_install https://httplib2.googlecode.com/files/httplib2-0.8.tar.gz
        sudo easy_install urllib3
        sudo easy_install --upgrade google-api-python-client
        sudo easy_install -U selenium

Authorizing
-----------
The first time you run this application, Google's API client library needs to go
through an authentication flow. If you've followed the steps above properly, you
should be able to run the following command:

    python popular_sizes.py

This should open a browser window that asks you to authenticate and approve the
app's access to your Analytics data. After you do this the first time, the
credentials will be cached in an analytics.dat file in this folder. You won't
have to enter it again. You should then see:

    The authentication flow has completed.

You can close the browser tab at this point.

NOTE: If you can't get past this step, repeat the Setup instructions above
carefully, especially the Credentials procedure. Also, clear your browser
cookies. Google caches these so it's hard to re-test - sometimes you can fix the
problem without realizing it!


Sauce Labs
----------
I've been using Sauce Labs for some time for cross-browser testing so I used it
for this project as well. I'm not a shill for the company but I do like the
service. If you prefer something else, feel free to send a Pull Request to add
more vendors (BrowserStack stub code is included to get you started).

There is an advantage to this route, though. This project was built on Selenium
WebDriver. It is therefore a cool "stub" for working into a data-driven
Continuous Integration tool. Instead of running your CI build tests against the
browsers you THINK users are actually using, why not run it against what your
reports SAY they are using? How cool is that? Now if a new screen resolution
suddenly becomes popular (new phone release, anyone?) your build tool will warn
you about this proactively!

Note that Sauce Labs' support for different screen resolutions is in Beta right
now. A limited number of resolutions is supported. But since this uses Selenium
to create its screen shots, you could easily use the same code to set up a
Selenium Grid cluster of your own - just change the URL it calls to send its
requests and you should be good to go.
