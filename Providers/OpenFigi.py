import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import config 
import requests
import pandas as pd

class OpenFigi:

    
    
    def __init__(self):
        
        self.api_url=config.OPEN_FIGI_URL
        self.openfigi_key=config.OPEN_FIGI_KEY
        self.openfigi_headers={'Content-Type': 'text/json'}




    def map_jobs(self,jobs):
        '''
        Send an collection of mapping jobs to the API in order to obtain the
        associated FIGI(s).
        Parameters
         ----------
        jobs : list(dict)
            A list of dicts that conform to the OpenFIGI API request structure. See
            https://www.openfigi.com/api#request-format for more information. Note
            rate-limiting requirements when considering length of `jobs`.
        Returns
        -------
        list(dict)
            One dict per item in `jobs` list that conform to the OpenFIGI API
            response structure.  See https://www.openfigi.com/api#response-fomats
            for more information.
        '''

        if self.openfigi_key:
            openfigi_headers['X-OPENFIGI-APIKEY'] = self.openfigi_key
        response = requests.post(url=self.api_url, headers=self.openfigi_headers,
                             json=jobs)
        if response.status_code != 200:
            raise Exception('Bad response code {}'.format(str(response.status_code)))
        jobs=response.json()
        return jobs





