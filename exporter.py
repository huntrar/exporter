#!/usr/bin/python3
import requests
import json
import os

import appdirs

class ClubhouseExporter:
    def __init__(self):
        self.BASE_URL = 'https://api.clubhouse.io/api/v2'
        self.TOKEN = os.environ.get('CLUBHOUSE_API_TOKEN')
        self.DATA_DIR = appdirs.user_data_dir('clubhouse')
        os.makedirs(self.DATA_DIR, exist_ok=True)
        self.DEBUG = False

    def get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['token'] = self.TOKEN
        headers = {'Content-Type': 'application/json'}
        if self.DEBUG:
            print('curl -X GET -H "Content-Type: application/json" \'{}/{}?{}\''.format(self.BASE_URL, endpoint.lstrip('/'), '&'.join('{}={}'.format(k, v) for k, v in params.items())))
        r = requests.get('{}/{}'.format(self.BASE_URL, endpoint.lstrip('/')), params=params, headers=headers)
        r.raise_for_status()
        return r

    def get_story(self, story_id, params=None):
        """Get Story returns information about a chosen Story."""
        if params is None:
            params = {}
        return self.get('stories/{}'.format(str(story_id).lstrip('/')), params).json()

    def search_stories(self, params):
        """Search Stories lets you search Stories based on desired parameters."""
        return self.get('search/stories', params).json()['data']

    def export(self):
        story_ids = [x['id'] for x in self.search_stories({"query": "is:story"})]
        fields = ['categories', 'epic-workflow', 'epics', 'files', 'labels', 'linked-files', 'members',
                  'milestones', 'projects', 'repositories', 'stories', 'teams', 'workflows']

        for field in fields:
            filename = os.path.join(self.DATA_DIR, field + '.json')

            if field == 'stories':
                resp = [self.get_story(x) for x in story_ids]
            else:
                resp = self.get(field).json()
            with open(filename, 'w') as f:
                print(filename)
                f.write(json.dumps(resp))


if __name__ == '__main__':
    exporter = ClubhouseExporter()
    exporter.export()
