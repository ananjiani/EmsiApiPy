"""Summary
"""
import requests

from .base import EmsiBaseConnection


class ACSIndicatorsConnection(EmsiBaseConnection):
    """docstring for ACSIndicatorsConnection

    Attributes:
        base_url (str): Description
        scope (str): Description
        token (TYPE): Description
    """

    def __init__(self) -> None:
        """Summary
        """
        super().__init__()
        self.base_url = "https://emsiservices.com/acs/"
        self.scope = "acs"

        self.token = self.get_new_token()

    def querystring_endpoint(self, api_endpoint: str, querystring: dict) -> requests.Response:
        """Summary

        Args:
            api_endpoint (str): Description
            querystring (dict): Description

        Returns:
            requests.Response: Description
        """
        url = self.base_url + api_endpoint

        headers = {'content-type': "application/json", 'authorization': "Bearer {}".format(self.token)}

        response = requests.get(url, headers = headers, params = querystring)
        if response.status_code == 401:
            self.token = self.get_new_token()
            return self.querystring_endpoint(api_endpoint, querystring)

        return response

    def get_status(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = self.base_url + "status"
        response = requests.request("GET", url)

        return response.json()['data']['message']

    def is_healthy(self):
        """
        Summary

        Returns:
            TYPE: Description
        """
        url = self.base_url + "status"
        response = requests.request("GET", url)

        return response.json()['data']['healthy']

    def get_metrics(self, metric_name: str = None) -> dict:
        """
        Summary

        Returns:
            dict: Description

        Args:
            metric_name (str, optional): Description
        """
        if metric_name is None:
            response = self.download_data("meta/metrics")
        else:
            response = self.download_data("meta/metrics/{}".format(metric_name))

        return response.json()['data']

    def get_level(self, level: str, metrics_list: list) -> dict:
        """
        Summary

        Args:
            level (str): Description
            metrics_list (list): Description

        Returns:
            dict: Description
        """
        querystring = {"metrics": ",".join(metrics_list)}
        response = self.querystring_endpoint(level, querystring)

        return response.json()['data']

    def post_level(self, level: str, payload: dict) -> dict:
        """Summary

        Args:
            level (str): Description
            payload (dict): Description

        Returns:
            dict: Description
        """
        response = self.download_data(level, payload)

        return response.json()['data']