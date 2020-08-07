import json
import logging
from os import getenv

import numpy as np
import pandas as pd
from redminelib import Redmine

from git import GitChecker
from redmine import RedmineModule

logger = logging.getLogger(__name__)


class Command():
    command_list = ["merge_check", "get_issues", "check_user_time"]

    def __init__(self):
        tmp = open("json/settings.json")
        self.data = json.load(tmp)
        self.redmine = Redmine(self.data["redmine_url"], key=getenv("KEY"))

    def execute_command(self, command):
        if not self._check_command(command):
            raise ValueError(f"{command}は存在しないコマンドです")
        elif command == "merge_check":
            self._merge_check()
        elif command == "get_issues":
            self._get_issues()
        elif command == "check_user_time":
            self._check_user_time()

    def _check_command(self, command):
        if command in self.command_list:
            return True
        return False

    def _merge_check(self):
        # RedmineのIssueフィルターをマージしてIssueを検索
        issues = self.redmine.issue.filter(**self.data["merge_check_filter"])

        # Githubのマージされたブランチと比較
        result = []
        git_checker = GitChecker(**self.data["git_data"])
        for issue in issues:
            tmp = git_checker.merge_check(issue.id)
            tmp.insert(0, issue.tracker.name)
            tmp.insert(3, issue.subject)
            result.append(tmp)
        logger.info("Check of git succeeded!!")

        # CSV化する
        logger.info("Create CSV")
        df = pd.DataFrame(result, columns=["tracker", "issue_id", "output", "subject"])
        df.to_csv("./output/merge_check.csv")
        logger.info("Success to create CSV file.")
        return True

    def _get_issues(self):
        # RedmineのIssueフィルターをjsonから取得してIssueを検索
        issues = self.redmine.issue.filter(**self.data["get_issues_filter"])

        # 必要なデータのみを抽出し、CSVとして全て出力
        data_list = RedmineModule.issues_to_list(issues)
        df = pd.DataFrame(data_list, columns=RedmineModule.attributes)
        df.to_csv("./output/get_issues.csv")
        return True

    def _check_user_time(self):
        # RedmineのIssueフィルターをjsonから取得してIssueを検索
        issues = self.redmine.issue.filter(**self.data["check_time_filter"])
        data_list = RedmineModule.create_user_time_list(issues)

        df = pd.DataFrame(data_list, columns=["user", "estimated_hours", "tracker", "issue"])
        df.to_csv("./output/check_user_time.csv")

        df_sum = df.groupby("user").agg({"estimated_hours": np.sum})
        df_sum.to_csv("./output/check_user_time_summary.csv")
