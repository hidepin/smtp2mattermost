smtp2mattermost
============================================================

概要
------------------------------------------------------------
このツールは、mantis1.18などsmtpでしかチケットの変更を通知することができない
バグトラッキングシステムの変更を、mattermostに出力するツールである。

要求条件
------------------------------------------------------------
- docker
- docker-compose

mattermost設定
------------------------------------------------------------

- WebHookを有効化する(システム管理者)

  1. 左上のメニューから「システムコンソール」を押下する

  2. 「設定」->「統合機能」->「ウェブフックとコマンド」を押下し、下記を設定する

    |メニュー                                                                          |設定値|
    |:---------------------------------------------------------------------------------|:----|
    |内向きのウェブフックを有効化する                                                  |有効 |
    |ウェブフックまたはスラッシュコマンドでのユーザー名を上書きする                    |有効 |
    |プロフィールの画像アイコンを上書きするウェブフックとスラッシュコマンドを有効にする|有効 |

- botからmattermostへのアクセス設定(チーム管理者/システム管理者)

  1. 左上のメニューから「統合機能」を押下する

  2. 「内向きのウェブフック」->「内向きのウェブフックを追加する」を押下する

  3. 下記を設定し、「保存する」を押下する

    |メニュー    |設定値                           |
    |:-----------|:--------------------------------|
    |Display Name|(任意)                           |
    |説明        |(任意)                           |
    |チャネル    |(botを動作させたいチャネルを指定)|

設定
------------------------------------------------------------

docker-compose.ymlファイルの下記パラメータを環境に合わせ変更する

- MATTERMOST_INCOME_URL:         (内向きのウェブフックのURL)
- MATTERMOST_PRIVATE_INCOME_URL: (内向きのウェブフックのURL: privateプロジェクトも出力)
- MATTERMOST_PRIVATE_PROJECT:    (出力対象外のプロジェクト: MATTERMOST_PRIVATE_INCOME_URLには表示)
- MATTERMOST_PRIVATE_PROJECT_HEADER: (mail本文のプロジェクト出力キーワード: デフォルト「プロジェクト:」)
- MATTERMOST_USERNAME:           (表示したいbot名称:デフォルト「subot」)
- MATTERMOST_ADDRESS:            (mattermostのアドレス:mailアドレスからmentionの名前を抽出)
- MATTERMOST_LOGIN_ID:           (mattermostの管理者ID:mailアドレスからmentionの名前を抽出できる権限のあるアカウント)
- MATTERMOST_PASSWORD:           (mattermostの管理者パスワード:mailアドレスからmentionの名前を抽出できる権限のあるアカウント)
- MATTERMOST_PORT:               (mattermostのポート)
- MATTERMOST_EXCLUDE_NOTIFICATE: (mentionで通知しないアカウント:mantisの管理者など)
- MATTERMOST_MESSAGE_MAX:        (mattermostへ通知するメッセージの最大サイズ:デフォルト1000)

起動方法
------------------------------------------------------------

1. ディレクトリに移動する

  ``` shell
  cd smtp2mattermost-docker
  ```

2. 起動する

  - 2回目以降
    ``` shell
    docker-compose start
    ```

  - 初回
    ``` shell
    docker-compose up -d
    ```

3. 起動状態を確認する

  ``` shell
  docker-compose ps
  ```

停止方法
------------------------------------------------------------

1. ディレクトリに移動する

  ``` shell
  cd smtp2mattermost-docker
  ```

2. 起動状態を確認する

  ``` shell
  docker-compose ps
  ```

3. 停止する

  ``` shell
  docker-compose stop
  ```

4. 停止状態を確認する

  ``` shell
  docker-compose ps
  ```

systemdによる自動起動設定
------------------------------------------------------------
host OSにsystemdの自動起動設定を行う
(ansibleのdocker imageが必要)

1. host OSにログインする

2. ansibleの設定を行う

  ``` shell
  ansible-playbook -i "(host OSのIPアドレス)," systemd.yml
  ```

制約条件
------------------------------------------------------------

- mattermost 3.4.0の古いバージョンにしか対応していない
- mantis 1.1.8と、mattermostには同じメールアドレスが登録されていること
- mattermost 3.4のAPIが古く情報取得にログイン情報が必要となる
