import logging
import sys

from .command import Command

logger = logging.getLogger(__name__)


def main():
    # コマンドラインから引数を確認
    Command.execute_command(sys.argv[1])
