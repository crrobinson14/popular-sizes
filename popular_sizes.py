#!/usr/bin/python

import logging
import argparse
import sys
import os
import httplib2
import traceback
import re
import urllib2

from apiclient import discovery
from apiclient import sample_tools
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

import unittest
from selenium import webdriver
from browserstack import browserstack

from config import reportConfig

def main(argv):
    scope='https://www.googleapis.com/auth/analytics.readonly'
    flags = sample_tools.init(argv,
                              'analytics',
                              'v3',
                              __doc__,
                              __file__,
                              scope)

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets('./client_secrets.json',
                                          scope=scope)

    # Credentials storage.
    storage = file.Storage('analytics.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run(flow, storage)

    http = credentials.authorize(http = httplib2.Http())
    service = discovery.build('analytics', 'v3', http=http)

    # Try to make a request to the API. Print the results or handle errors.
    try:
        results = service.data().ga().get(ids='ga:' + reportConfig['viewId'],
                                          metrics='ga:visits',
                                          start_date=reportConfig['startDate'],
                                          end_date=reportConfig['endDate'],
                                          dimensions='ga:screenResolution',
                                          sort='-ga:visits',
                                          max_results='10').execute()
        run_screenshots(results)

    except Exception:
        logging.error(traceback.format_exc())

    except HttpError, error:
        # Handle API errors.
        print ('Arg, there was an API error : %s : %s' %
               (error.resp.status, error._get_reason()))

    except AccessTokenRefreshError:
        # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
               'the application to re-authorize')


def run_screenshots(results):
    command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (
        reportConfig['sauceUser'],
        reportConfig['sauceKey']
    )

    # TODO: In the future we could normalize to the next nearest width, at least
    allowedResolutions = {
        '800x600',
        '1024x768',
        '1280x1024',
        '1440x900',
        '1920x1200'
    }

    for row in results.get('rows'):
        resolution = row[0]
        fields = resolution.split('x')

        print "Taking screenshot at %sx%s" % (fields[0], fields[1])

        # Get it via BrowserStack. Note that this has a very limited set of
        # screen resolutions right now.
        #
        # client = browserstack.BrowserStack(username = reportConfig['browserStackUser'],
        #                                   password = reportConfig['browserStackPass'])
        # wid = client.create_worker(url = reportConfig['testUrl'],
        #                            os = 'win',
        #                            browser = 'chrome',
        #                            version = '32.0')
        #
        # print 'Sending BrowserStack screen shot request for %sx%s...' % (
        #     resolution
        # )
        #
        # Wait for it to complete...
        #
        # while client.get_worker_status(wid['id']) is 'Not Found':
        #     pass
        #
        # data = urllib2.urlopen('http://api.browserstack.com/3/worker/%s/screenshot.png' % wid['id'])
        # output = open('chrome-%s.png' % resolution,'wb')
        # output.write(data.read())
        # output.close()

        # Get it via SauceLabs. Note that screen resolution is in Beta there
        # right now.
        #
        caps = webdriver.DesiredCapabilities.FIREFOX
        caps['platform'] = "Windows XP"
        caps['version'] = "3.6"
        caps['name'] = 'Screenshot at %s in Firefox' % resolution

        if resolution in allowedResolutions:
            caps['screen-resolution'] = resolution

        driver = webdriver.Remote(
            desired_capabilities=caps,
            command_executor=command_executor
        )

        # This is pretty stupid - we could do better. But supposedly you don't
        # go to hell if you ask forgiveness for your sins...
        driver.implicitly_wait(5)

        #try:
        #    driver.maximize_window()
        #except WebDriverException:
        #    pass

        driver.set_window_size(fields[0], fields[1])

        driver.get(reportConfig['testUrl'])

        driver.implicitly_wait(5)
        driver.save_screenshot('firefox-%s.png' % resolution)

        print("Saved chrome-%s.png from https://saucelabs.com/jobs/%s" % (
            resolution,
            driver.session_id)
        )
        driver.quit()


if __name__ == '__main__':
  main(sys.argv)
