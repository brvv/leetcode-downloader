from CommitGenerator import CommitGenerator
from SolutionFetcher import SolutionFetcher
from git import Repo
import time

import settings


cookies = {'csrftoken' : settings.cookie_string}
repo_path = settings.repo_name
delay = settings.api_call_delay
min_offset = settings.min_problem_offset
max_offset = settings.max_problem_offset


repo = Repo.init(repo_path)

if __name__=='__main__':
    fetcher = SolutionFetcher(cookies, min_offset, max_offset)
    generator = CommitGenerator(repo_path)

    while fetcher.has_next_page():
        print('Offset', fetcher.offset)
        page_submissions = fetcher.fetch_next_submissions()
        for submission in page_submissions:
            print('\t', submission['title'])
            generator.submit(submission)
        time.sleep(delay)
    print('Done!')