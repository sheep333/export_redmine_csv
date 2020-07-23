from redminelib.exceptions import ResourceAttrError
from redminelib.resources import BaseResource


class RedmineModule():
    params = ["project_id", "subject", "tracker_id", "description", "status_id", "priority_id",
              "category_id", "fixed_version_id", "is_private", "assigned_to_id", "watcher_user_ids",
              "parent_issue_id", "start_date", "due_date", "estimated_hours", "done_ratio", "custom_fields", "uploads"]

    attributes = ["id", "project", "tracker", "status", "priority", "author", "assigned_to", "fixed_version",
                  "subject", "start_date", "due_date", "done_ratio", "is_private", "estimated_hours",
                  "created_on", "updated_on", "closed_on"]

    @classmethod
    def param_checker(cls, **kwargs):
        for key in kwargs:
            if key not in cls.params:
                raise ValueError("存在しないパラメーターです。")

    @classmethod
    def issues_to_list(cls, issues):
        data_list = []
        for issue in issues:
            issue_data = []
            for attr in cls.attributes:
                # attritbuteが取得できない場合はNoneをいれる
                try:
                    attr_data = getattr(issue, attr)
                except Exception:
                    attr_data = None
                # attributeのデータが辞書の場合には
                if isinstance(attr_data, (BaseResource)):
                    data = attr_data.name
                else:
                    data = attr_data
                issue_data.append(data)
            data_list.append(issue_data)
        return data_list

    @classmethod
    def create_user_time_list(cls, issues):
        data_list = []
        for issue in issues:
            try:
                user = issue.assigned_to.name
            except ResourceAttrError:
                user = "担当者なし"

            try:
                hours = issue.estimated_hours
            except ResourceAttrError:
                hours = 0

            data_list.append([user, hours, issue.tracker.name, issue.subject])
        return data_list
