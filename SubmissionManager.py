import os
from NameGenerator import generate_full_name


class SubmissionManager:
    def __init__(self, repoPath):
        self._submissions = []
        self._shouldFetchNext = True
        self._is_sorted = True
        self.repoPath = repoPath
    
    def shouldFetchNext(self):
        return self._shouldFetchNext

    def _alreadyExists(self, submission):
        full_name = generate_full_name(submission)
        file_path = os.path.join(self.repoPath, full_name)
        exists = os.path.isfile(file_path)
        return exists

    def _updateShouldFetchNext(self, submission):
        self._shouldFetchNext = not self._alreadyExists(submission)
        
    def addSubmission(self, submission):
        self._submissions.append(submission)
        self._is_sorted = False
        self._updateShouldFetchNext(submission)

    def addSubmissions(self, submissions):
        for submission in submissions:
            self.addSubmission(submission)
    
    def sort(self):
        self._submissions = sorted(self._submissions, key=lambda sub : sub.get('timestamp', 0))
        self._is_sorted = True

    def getSortedSubmissions(self):
        if self._is_sorted:
            return self._submissions
        self.sort()
        return self._submissions
