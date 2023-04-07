from git import Repo
from NameGenerator import generate_full_name, get_submission_date
import os


class CommitGenerator:
    def __init__(self, path):
        self.repoPath = path
        self.repo = Repo(path)
        self.repoIndex = self.repo.index

    def _generate_commit_message(self, title, date):
        date_string = date.strftime('%d-%b-%Y, at %X')
        return f'Solution for {title} done on {date_string}'

    def _generate_code_file(self, submission):
        code = submission['code']

        full_name = generate_full_name(submission)
        file_path = os.path.join(self.repoPath, full_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.isfile(file_path):
            with open(file_path, 'w') as new_file:
                new_file.write(code)
            return full_name
        return None

    def _generate_commit(self, file_name, title, date):
        msg = self._generate_commit_message(title, date)
        self.repoIndex.add([file_name])
        self.repoIndex.commit(msg, commit_date=date, author_date=date)

    def submit(self, submission):
        date = get_submission_date(submission)
        file_name = self._generate_code_file(submission)
        if file_name is not None:
            self._generate_commit(file_name, submission['title'], date)
            return True
        return False
