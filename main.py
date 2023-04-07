from CommitGenerator import CommitGenerator
from SolutionFetcher import SolutionFetcher
from SubmissionManager import SubmissionManager
from dotenv import dotenv_values
from git import Repo
import time

import settings

def getCookie():
    try:
        config = dotenv_values('.env')
        cookie_string = config['COOKIE_STRING']
        if len(cookie_string) > 0:
            return {'csrftoken' : cookie_string}
    except:
        return None
    return None


repo_path = settings.repo_name
delay = settings.api_call_delay
min_offset = settings.min_problem_offset
max_offset = settings.max_problem_offset


repo = Repo.init(repo_path)

if __name__=='__main__':
    cookie = getCookie()

    if cookie is None:
        print('Cookie string not provided')
        exit()


    fetcher = SolutionFetcher(cookie, min_offset, max_offset)
    manager = SubmissionManager(repo_path)
    generator = CommitGenerator(repo_path)

    while fetcher.has_next_page() and manager.shouldFetchNext():
        print('fetching offset', fetcher.offset)
        page_submissions = fetcher.fetch_next_submissions()
        for submission in page_submissions:
            print('\t', submission['title'])
        manager.addSubmissions(page_submissions)
        time.sleep(delay)

    if not manager.shouldFetchNext():
        print('Found existing submission and aborted fetching.')

    print('sorting submissions')
    sorted_submissions = manager.getSortedSubmissions()
    print('generating commits')

    for submission in sorted_submissions:
        status = generator.submit(submission)
        if status:
            print('commit for', submission['title'])


    print('Done!')