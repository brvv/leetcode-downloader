import requests 
import json
import time

success_status = 10
json_keys = {'submissions' : 'submissions_dump',
'status' : 'status',
'title' : 'title_slug',
'timestamp' : 'timestamp',
'code' : 'code',
'has_next':'has_next',
'language' : 'lang'}

class SolutionFetcher:
    def __init__(self, cookies, offset=0, max_offset=None):
        self.offset = offset
        self.cookies = cookies

        self._has_next = True
        self._offset_inc = 20
        self._max_offset = max_offset

    def _get_endpoint(self):
        return f'https://leetcode.com/api/submissions/?offset={self.offset}&limit=20&lastkey=' 

    def _is_valid_submission(self, submission):
        return submission[json_keys['status']] == success_status

    def _extract_submission_info(self, submission):
        res = {}
        res['timestamp'] = submission[json_keys['timestamp']]
        res['code'] = submission[json_keys['code']]
        res['language'] = submission[json_keys['language']]
        res['title'] = submission[json_keys['title']]
        return res

    def _parse_submissions(self, page):
        valid = []
        for submission in page.get(json_keys['submissions'], []):
            if self._is_valid_submission(submission):
                valid.append(self._extract_submission_info(submission))
        return valid

    def _fetch_page(self):
        page = requests.get(self._get_endpoint(), cookies=self.cookies)
        page_json = page.json()
        
        return page_json

    def has_next_page(self):
        return self._has_next

    def inc_offset(self, has_next):
        self.offset += self._offset_inc
        self._has_next = has_next

        if self._max_offset is not None and self.offset >= self._max_offset:
            self._has_next = False

    def fetch_next_submissions(self):
        if self.has_next_page():
            next_page = self._fetch_page()
            self.inc_offset(next_page.get(json_keys['has_next'], False))

            next_submissions = self._parse_submissions(next_page)
            return next_submissions
        else:
            return []
