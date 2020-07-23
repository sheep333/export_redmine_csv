import json
import logging
import numpy as np
from os import getenv
import pandas as pd
from redminelib import Redmine
from redminelib.exceptions import ResourceAttrError

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
        issues = self.redmine.filter_issues(**self.data["merge_check_filter"])

        # Githubのマージされたブランチと比較
        result = []
        git_checker = GitChecker(**self.data["git_data"])
        for issue in issues:
            result.append(git_checker.merge_check(issue.id))
        logger.info("Check of git succeeded!!")

        # CSV化する
        logger.info("Create CSV")
        df = pd.DataFrame(result, columns=["issue_id", "output"])
        df.to_csv(f"./output/merge_check_{self.data['git_data']['branch_name']}.csv")
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

        data_list = []
        for issue in issues:
            try:
                user = issue.assigned_to
            except ResourceAttrError:
                user = "担当者なし"

            try:
                hours = issue.estimated_hours
            except ResourceAttrError:
                hours = 0

            data_list.append([user, hours, issue.tracker["name"], issue.subject])

        df = pd.DataFrame(data_list, columns=["user", "estimated_hours", "tracker", "issue"])
        df.to_csv("./output/check_user_time.csv")

        df_sum = df.groupby("user").agg({"estimated_hour": np.sum})
        df_sum.to_csv("./output/check_user_time_summary.csv")
