### Author: Dave Yeu <daveyeu@gmail.com>
###
### Collects stats from Heroku's router logs.
###
### Gathers service, connect, and wait times from Heroku's router log lines.
### For each, we calculate the min, max, median, 90th, and 95th percentile.
###
### sudo ./logster --output=stdout HerokuRouterLogster /var/log/heroku.log
###
### For details on Heroku's router log format, check out:
### https://devcenter.heroku.com/articles/http-routing#heroku-router-log-format
###
### Based on MetricLogster in the logster distribution. Thanks.
import re

from logster.parsers import stats_helper

from logster.logster_helper import MetricObject, LogsterParser
from logster.logster_helper import LogsterParsingException

class HerokuRouterLogster(LogsterParser):

    def __init__(self, option_string=None):
        '''Initialize any data structures or variables needed for keeping track
        of the tasty bits we find in the log we are parsing.'''

        self.waits    = []
        self.connects = []
        self.services = []

        self.regex = re.compile('.*heroku\[router\].*wait=(?P<wait>\d+)ms.*connect=(?P<connect>\d+)ms.*service=(?P<service>\d+)ms.*')

    def parse_line(self, line):
        '''This function should digest the contents of one line at a time, updating
        object's state variables. Takes a single argument, the line to be parsed.'''

        matches = self.regex.match(line)

        if matches:
            match_dict = matches.groupdict()
            self.waits.append(int(match_dict['wait']))
            self.connects.append(int(match_dict['connect']))
            self.services.append(int(match_dict['service']))

    def get_state(self, duration):
        '''Run any necessary calculations on the data collected from the logs
        and return a list of metric objects.'''

        if len(self.waits) > 0:
            return [
                MetricObject("wait.min", min(self.waits)),
                MetricObject("wait.max", max(self.waits)),
                MetricObject("wait.mean", stats_helper.find_mean(self.waits)),
                MetricObject("wait.median", stats_helper.find_median(self.waits)),
                MetricObject("wait.90th_percentile", stats_helper.find_percentile(self.waits, 90)),
                MetricObject("wait.95th_percentile", stats_helper.find_percentile(self.waits, 95)),

                MetricObject("connect.min", min(self.connects)),
                MetricObject("connect.max", max(self.connects)),
                MetricObject("connect.mean", stats_helper.find_mean(self.connects)),
                MetricObject("connect.median", stats_helper.find_median(self.connects)),
                MetricObject("connect.90th_percentile", stats_helper.find_percentile(self.connects, 90)),
                MetricObject("connect.95th_percentile", stats_helper.find_percentile(self.connects, 95)),

                MetricObject("service.min", min(self.services)),
                MetricObject("service.max", max(self.services)),
                MetricObject("service.mean", stats_helper.find_mean(self.services)),
                MetricObject("service.median", stats_helper.find_median(self.services)),
                MetricObject("service.90th_percentile", stats_helper.find_percentile(self.services, 90)),
                MetricObject("service.95th_percentile", stats_helper.find_percentile(self.services, 95))
                ]
        else:
            return []
