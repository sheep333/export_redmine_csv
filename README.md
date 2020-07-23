# WIP

## 使い方
python main.py {コマンド名}

## 使用できるコマンド

### merge_check
#### 機能
- RedmineのIssueを取得して、gitの特定のブランチにマージされているかを確認するCSVを出力する

#### 指定するパラメータ
- git_data
- issue_filter

#### 出力内容
チケットID｜マージ履歴

### get_issues
#### 機能
- RedmineのIssueを条件で絞り込んで取得

#### 指定するパラメータ
- issue_filter

#### 出力内容
- [RemineAPIで取得できる情報一覧](https://www.redmine.org/projects/redmine/wiki/Rest_Issues#Creating-an-issue)

### check_user_handle_time
#### 機能
- RedmineのIssueを条件で絞り込み、ユーザ毎のチケット消化に必要な時間を出力する

#### 指定するパラメータ
- issue_filter
