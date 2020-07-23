import logging
import subprocess

logger = logging.getLogger(__name__)


class GitChecker():

    def __init__(self, **kwargs):
        if "branch_name" not in kwargs or "directory" not in kwargs:
            raise ValueError("gitの取得に必要な値が設定されていません。")

        self.branch_name = kwargs["branch_name"]
        self.directory = kwargs["directory"]
        self._checkout_branch()

    def _checkout_branch(self):
        try:
            subprocess.run(["git", "checkout", f"{self.branch_name}"], cwd=self.directory)
        except Exception:
            logger.error(f"Can't checkout branch: {self.branch_name}")
            raise ValueError(f"{self.branch_name}をチェックアウトできません")

        try:
            subprocess.run("git pull", shell=True, cwd=self.directory)
        except Exception:
            logger.error(f"Can't pull branch: {self.branch_name}")
            raise ValueError(f"{self.branch_name}のプルに失敗しました。")

    def merge_check(self, id):
        # FIXME: 毎回データを取得するよりもtmpファイルを作ってgrepかける方が負担が少ないかも。
        logger.info(f"Check whether merged issue_id: {id}")
        p1 = subprocess.Popen(["git", "log", "--merges", "--oneline"], cwd=self.directory,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", f"{id}"], stdin=p1.stdout, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True)
        p1.stdout.close()
        output = p2.communicate()[0]

        if output is not None:
            return [id, output]
        else:
            return [id, ""]
