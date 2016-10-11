#!/usr/bin/env python


""" View Wakatime stats """

import json
import os

import base64
import click
import arrow
import requests
import urllib

from pprint import pprint
from tabulate import tabulate
from IPython import embed

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    token_normalize_func=lambda x: x.lower()
    )


class RestAPI:
    def __init__(self, base_url, headers={}):
        self.url = base_url

    def get(self, params, **kwargs):

        url = "{}".format(self.url + params)
        if kwargs:
            url += "?{}".format(urllib.urlencode(kwargs))
        click.secho("getting: {}... "
                    .format(url), fg='blue', nl=False)

        error = None

        try:
            req = requests.get(self.url + params, headers=self.headers)
            if req.ok:
                click.secho("OK", fg='green')
                return json.loads(req.content)
            else:
                click.secho("NOK: {}".format(req.reason), fg='red')
                ret = json.loads(req.content)
                error = ret.get('error') or str(ret)
        except requests.exceptions.ConnectionError, m:
            click.secho("NOK (requests.exceptions.ConnectionError): {}"
                        .format(m), fg='red')
        #except:
            #click.secho("NOK, unknown", fg='red')

        infos = [url, req.status_code, req.reason, error]
        msg = "Errors:\n" + "\n - ".join([str(x) for x in infos if x])
        raise RequestError(msg)
        #raise RequestError("{} // {}/{}/{}"
                           #.format(url, req.status_code, req.reason))

    def post(self, data, params, **kwargs):
        """ send a POST request """
        url = "{}".format(self.url + params)
        click.secho("posting: {} ".format(url), fg='blue', nl=False)

        try:
            req = requests.request('post',
                                   url,
                                   json=data,
                                   headers=self.headers,
                                   **kwargs
                                   )

            if req.ok:
                click.secho("OK", fg='green')
                return json.loads(req.content)
            else:
                click.secho("NOK: {}".format(req.reason), fg='red')
                return json.loads(req.content)

        except requests.exceptions.ConnectionError, m:
            click.secho("NOK: {}".format(m), fg='red')

        raise RequestError("{} // {}/{}"
                           .format(url, req.status_code, req.reason))


class WakatimeAPI(RestAPI):

    def __init__(self, url):
        self.url = url

        self.check_token()
        self.key = base64.b64encode(os.environ.get('WAKATIME_API_KEY'))

        self.headers = {
            "Authorization": 'Basic {}'.format(self.key),
            'Accept': 'application/json',
            }

        RestAPI.__init__(self, url, self.headers)

    def check_token(self):
        if 'WAKATIME_API_KEY' not in os.environ:
            dashboard_url = "https://wakatime.com/settings/account"
            click.secho("No WAKATIME_API_KEY envvar found. ", fg='red')
            msg = ("Retrieve it from the Wakatime settings page:\n")
            msg += click.style(dashboard_url, fg='blue') + "\n"
            msg += ("Once you have it, add it to your bash profile: \n"
                    "export WAKATIME_API_KEY='changeme'")
            click.secho(msg)
            exit()


class RequestError(Exception):
    pass


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@cli.command()
@click.argument('start', required=False)
@click.argument('end', required=False)
def summaries(start, end):
    """
    _start = arrow.get(start) if start else arrow.now().replace(days=-7)
    _end = arrow.get(end) if end else arrow.now()
    #start = _start.format("YYYY-MM-DD")
    #end = _end.format("YYYY-MM-DD")
    start = _start.date().toordinal()
    end = _end.date().toordinal()

    #ret = WAKATIME.get("users/current/summaries", start=start, end=end)
    """
    ret = WAKATIME.get("users/current/stats/last_7_days")
    pprint(ret)

@cli.command()
def whoami():
    ret = WAKATIME.get("users/current")
    data = ret['data']
    pprint(data)


WAKATIME = WakatimeAPI('https://wakatime.com/api/v1/')


if __name__ == '__main__':

    cli(obj={})
