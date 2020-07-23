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
- "./output/get_issues.csv"
  - チケットID｜マージ履歴

### get_issues
#### 機能
- RedmineのIssueを条件で絞り込んで取得

#### 指定するパラメータ
- issue_filter

#### 出力内容
- "./output/merge_check_{ブランチ名}.csv"
  - [RemineAPIで取得できる情報一覧](https://www.redmine.org/projects/redmine/wiki/Rest_Issues#Creating-an-issue)

### check_user_time
#### 機能
- RedmineのIssueを条件で絞り込み、ユーザ毎のチケット消化に必要な時間を出力する

#### 指定するパラメータ
- issue_filter

#### 出力内容
- "./output/check_user_time.csv"を出力
  - ユーザ名|Issueの時間数|Issueタイトル|トラッカー

- "./output/check_user_time_summary.csv"を出力
  - ユーザ名|総時間数
