from logging import getLogger, DEBUG
import sys

from command import Command

logger = getLogger(__name__)
logger.setLevel(DEBUG)


def main():
    # コマンドラインから引数を確認
    logger.info(f"{sys.argv[1]}コマンドを実行")
    command = Command()
    command.execute_command(sys.argv[1])


if __name__ == "__main__":
    main()
