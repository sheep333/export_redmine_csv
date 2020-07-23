import logging
import sys

from command import Command

logger = logging.getLogger(__name__)


def main():
    # コマンドラインから引数を確認
    logger.info(f"{sys.argv[1]}コマンドを実行")
    Command.execute_command(sys.argv[1])


if __name__ == "__main__":
    main()
