import pandas as pd
import logging

from .redmine import RedmineModule
from .git import GitChecker

logger = logging.getLogger(__name__)


class Command():
    command_list = ['merge_check', 'get_issues']

    def __init__(self):
        self.data = pd.read_json('json/settings.json')
        self.redmine = RedmineModule(**self.data['redmine_auth'])

    @classmethod
    def execute_command(cls, command):
        if not cls._check_command(command):
            raise ValueError('存在しないコマンドです')
        elif command == 'merge_check':
            cls._merge_check()
        elif command == 'get_issues':
            cls._get_issues()

    def _check_command(self, command):
        if command in self.command_list:
            return True
        return False

    def _merge_check(self):
        # RedmineのIssueフィルターをマージしてIssueを検索
        issues = self.redmine.filter_issues(**self.data['issue_filter'])

        # Githubのマージされたブランチと比較
        result = []
        git_checker = GitChecker(**self.data['git_data'])
        for issue in issues:
            result.append(git_checker.merge_check(issue.id))
        logger.info(f'Check of git succeeded!!')

        # CSV化する
        logger.info('Create CSV')
        df = pd.DataFrame(result, columns=['issue_id', 'output'])
        df.to_csv(f"./output/merge_check_{self.data['git_data']['branch_name']}.csv")
        logger.info(f'Success to create CSV file.')
        return True

    def _get_issues(self):
        # RedmineのIssueフィルターをjsonから取得してIssueを検索
        issues = self.redmine.filter_issues(**self.data['issue_filter'])

        # IssueをCSVとして全て出力
        issues.export('csv', savepath='./output/get_issues.csv', columns='all')
        return True
