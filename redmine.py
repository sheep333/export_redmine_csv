class RedmineModule():
    params = ["project_id", "subject", "tracker_id", "description", "status_id", "priority_id",
              "category_id", "fixed_version_id", "is_private", "assigned_to_id", "watcher_user_ids",
              "parent_issue_id", "start_date", "due_date", "estimated_hours", "done_ratio", "custom_fields", "uploads"]

    @classmethod
    def param_checker(cls, **kwargs):
        for key in kwargs:
            if key not in cls.params:
                raise ValueError("存在しないパラメーターです。")
