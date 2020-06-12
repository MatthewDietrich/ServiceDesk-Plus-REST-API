'''
API wrapper for the ManageEngine ServiceDesk Plus v3 API

Author: Matt Dietrich <mdietrich@ecisolutions.com>
'''


import json

import requests


class SDPAPI:
    def __init__(self, api_key, api_url_base):
        self.api_key = api_key
        self.api_url_base = api_url_base + 'api/v3/'
        self.headers = {'Authtoken': self.api_key}

    def send(self, endpoint, method, input_fields=None):
        params = {'TECHNICIAN_KEY': self.api_key}
        if input_fields:
            params['input_data'] = json.dumps(input_fields)

        res = None

        if method == 'GET':
            res = requests.get(self.api_url_base + endpoint,
                                headers=self.headers,
                                params=params)
        elif method == 'POST':
            res = requests.post(self.api_url_base + endpoint,
                                 headers=self.headers,
                                 params=params)
        elif method == 'PUT':
            res = requests.put(self.api_url_base + endpoint,
                                 headers=self.headers,
                                 params=params)
        elif method == 'DELETE':
            res = requests.delete(self.api_url_base + endpoint,
                                 headers=self.headers,
                                 params=params)

        if res is not None:
            return json.loads(res.text)
        else:
            return None


    def request_view(self, request_id):
        return self.send('requests/' + request_id, 'GET')

    def request_view_all(self, list_info):
        data = {}
        data['list_info'] = list_info
        return self.send('requests', 'GET', data)

    def request_add(self, fields):
        data = {}
        data['request'] = fields
        return self.send('requests', 'POST', data)

    def request_edit(self, request_id, fields):
        data = {}
        data['request'] = fields
        return self.send('requests/' + request_id, 'PUT', data)

    def request_delete(self, request_id):
        return self.send(f'requests/{request_id}/move_to_trash', 'DELETE')

    def request_delete_from_trash(self, request_id):
        return self.send('requests' + request_id, 'DELETE')

    def request_restore_from_trash(self, request_id):
        return self.send(f'requests/{request_id}/restore_from_trash', 'PUT')

    def request_close(self, request_id):
        return self.send(f'requests/{request_id}/close', 'PUT')

    def request_pickup(self, request_id):
        return self.send(f'requests/{request_id}/pickup', 'PUT')

    def request_assign(self, request_id, group, technician):
        data = {'request': {
                    'group': {'name': group},
                    'technician': {'name': technician}}}
        return self.send(f'requests/{request_id}/assign', 'PUT', data)

    def request_get_resolution(self, request_id):
        return self.send(f'requests/{request_id}/resolutions', 'GET')

    def request_add_resolution(self, request_id, content, add_to_linked=False):
        data = {'resolution': {'content': content, 'add_to_linked_requests': add_to_linked}}
        return self.send(f'requests/{request_id}/resolutions', 'POST', data)

    def request_edit_resolution(self, request_id, content):
        data = {'resolution': {'content': content}}
        return self.send(f'requests/{request_id}/resolutions', 'PUT', data)

    def request_get_summary(self, request_id):
        return self.send(f'requests/{request_id}/summary', 'GET')

    def request_associate_problem(self, request_id, problem_id):
        data = {'request_problem_association': {'problem': {'id': problem_id}}}
        return self.send(f'requests/{request_id}/problem', 'POST', data)

    def request_get_problem(self, request_id):
        return self.send(f'requests/{request_id}/problem', 'GET')

    def request_dissociate_problem(self, request_id, problem_id):
        data = {'request_problem_association': {'problem': {'id': problem_id}}}
        return self.send(f'requests/{request_id}/problem', 'DELETE', data)

    def request_associate_initiated_change(self, request_id, change_id):
        data = {'request_initiated_change': {'change': {'id': change_id}}}
        return self.send(f'requests/{request_id}/request_initiated_change', 'POST', data)

    def request_get_initiated_change(self, request_id):
        return self.send(f'requests/{request_id}/request_initiated_change', 'GET')

    def request_dissociate_initiated_change(self, request_id, change_id):
        data = {'request_initiated_change': {'change': {'id': change_id}}}
        return self.send(f'requests/{request_id}/request_initiated_change', 'DELETE', data)

    def request_associate_caused_by_change(self, request_id, change_id):
        data = {'request_caused_by_change' : {'change': {'id': change_id}}}
        return self.send(f'requests/{request_id}/request_caused_by_change', 'POST', data)

    def request_get_caused_by_change(self, request_id):
        return self.send(f'requests/{request_id}/request_caused_by_change', 'GET')

    def request_dissociate_caused_by_change(self, request_id, change_id):
        data = {'request_caused_by_change' : {'change': {'id': change_id}}}
        return self.send(f'requests/{request_id}/request_caused_by_change', 'DELETE', data)

    def request_link_request(self, request_id, link_request_id, comments=''):
        data = {'link_requests': [{'linked_request': {'id': link_request_id},
                                   'comments': comments}]}
        return self.send(f'requests/{request_id}/link_requests', 'POST', data)

    def request_get_linked_requests(self, request_id):
        return self.send(f'requests/{request_id}/link_requests', 'GET')

    def request_unlink_request(self, request_id, link_request_id):
        data = {'link_requests': [{'linked_request': {'id': link_request_id}}]}
        return self.send(f'requests/{request_id}/link_requests', 'DELETE', data)

    def request_add_note(self, request_id, description, show_to_requester=False, notify_technician=False, mark_first_response=False, add_to_linked_requests=False):
        data = {'request_note': {'description': description,
                                 'show_to_requester': show_to_requester,
                                 'notify_technician': notify_technician,
                                 'mark_first_response': mark_first_response,
                                 'add_to_linked_requests': add_to_linked_requests}}
        return self.send(f'requests/{request_id}/notes', 'POST', data)

    def request_edit_note(self, request_id, note_id, description, show_to_requester=False, notify_technician=False):
        data = {'request_note': {'description': description,
                                 'show_to_requester': show_to_requester,
                                 'notify_technician': notify_technician}}
        return self.send(f'requests/{request_id}/notes/{note_id}', 'PUT', data)

    def request_view_note(self, request_id, note_id):
        return self.send(f'requests/{request_id}/notes/{note_id}', 'GET')

    def request_delete_note(self, request_id, note_id):
        return self.send(f'requests/{request_id}/notes/{note_id}', 'DELETE')

    def entity_view_history(self, entity, entity_id):
        return self.send(f'{entity}/{entity_id}/history', 'GET')
