from git import Repo
import datetime
import zoneinfo
import os

file_extensions = {'python' : '.py', 'python3' : '.py'}
timezone = "America/Toronto"

class CommitGenerator:
    def __init__(self, path):
        self.repoPath = path
        self.repo = Repo(path)
        self.repoIndex = self.repo.index

    def _get_submission_date(self, submission):
        dt = datetime.datetime.fromtimestamp(submission['timestamp'])
        return dt.replace(tzinfo=zoneinfo.ZoneInfo(key=timezone))


    def _generate_commit_message(self, title, date):
        date_string = date.strftime('%d-%b-%Y, at %X')
        return f'Solution for {title} done on {date_string}'

    def _get_day_suffix(self, day):
        day = int(day)
        if 4 <= day <= 20 or 24 <= day <= 30:
            return "th"
        else:
            return ["st", "nd", "rd"][day % 10 - 1] 

    def _generate_filename(self, title, date):
        day = date.strftime('%d')
        suffix = self._get_day_suffix(day)

        date_string = day + suffix + date.strftime(', at %H %M')
        new_title = title.replace('-', ' ')
        return f'{date_string} - {new_title}'

    def _generate_file_path(self, date):
        year = date.strftime('%Y')
        month = date.strftime('%b')
        return os.path.join(year, month)

    def _generate_full_name(self, submission):
        date = self._get_submission_date(submission)
        filename = self._generate_filename(submission['title'], date)
        extension = file_extensions.get(submission['language'], '')

        path_in_repo = self._generate_file_path(date)

        full_name = os.path.join(path_in_repo, filename + extension)
        return full_name


    def _generate_code_file(self, submission):
        code = submission['code']

        full_name = self._generate_full_name(submission)
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
        date = self._get_submission_date(submission)
        file_name = self._generate_code_file(submission)
        if file_name is not None:
            self._generate_commit(file_name, submission['title'], date)
