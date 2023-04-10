#!/usr/bin/python3

import crdb
import argparse
import logging
import os
import random
import sys


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s:%(funcName)s:%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def cmd_bench(args):
    pass


def cmd_crunch(args):
    """runs a test routine against a test db..."""
    logger.info("start")
    db = crdb.ComicDB('./.de.test-db/ComicDb.xml')
    db.Load()
    logger.info("db loaded")

    # library = db.Library
    # logging.info("crunch: Library unpacked")

    # logging.info("crunch: getting a Book...")
    # book = library[id]
    # logging.debug(f"crunch: UUID={book.Id} AlternateSeries={book.AlternateSeries}")
    # # book.AlternateSeries = str(int(random.random()*1000))
    # # log(f"crunch: set AlternateSeries={book.AlternateSeries}", True)
    # # log("crunch: updating Library...", True)
    # # db.updateLibrary(library)
    # # log("crunch: Library updated", True)

    # logging.info("crunch: saving db...")
    # db.Save()
    logger.info("end")


def cmd_export(args):

    logger.info("prepping for an export...")

    db = crdb.ComicDB(args.crdb)
    fp = args.target
    n = 0

    if args.l_ids is not None:
        logger.info(f"exporting {len(args.l_ids)} books ...")
        for id in args.l_ids:
            n += 1
            db.Export(id, fp)
    else:
        library = db.Library
        logger.info(f"exporting {len(library)} books ...")
        for book in library:
            n += 1
            db.Export(book.Id, fp)

    logger.info(f"{n} completed!")


def cmd_import(args):
    pass


def main():

    logger.debug("starting up...")

    # we are going to be way too smart for our own good...
    parser = argparse.ArgumentParser(description="the DataEngine for ComicRack")
    # TBD - parser.add_argument("--config", nargs='?')
    parser.add_argument("crdb")
    parser.add_argument("-n", "--dry-run",  dest="dryrun", action="store_true")
    mxg = parser.add_mutually_exclusive_group()
    mxg.add_argument("-q", "--quiet", dest="loglevel", action="store_const", const=logging.CRITICAL)
    mxg.add_argument("-V", "--verbose",  dest="loglevel", action="store_const", const=logging.INFO)
    mxg.add_argument("--debugging", dest="loglevel", action="store_const", const=logging.DEBUG)

    # args = parser.parse_args()
    # run parse_args (for the FIRST time) to get the basic config ...
    # and when the cmds are fully plugins, build the list of cmds dynamically

    subparsers = parser.add_subparsers(dest="cmd", title="commands")
    cmd = {}

    subparser_crunch = subparsers.add_parser("crunch")          # pylint: disable=unused-variable
    subparser_crunch.add_argument("--id", nargs="+", action="extend")
    cmd["crunch"] = cmd_crunch

    # once the primitives all work...
    # subparser_bench = subparsers.add_parser("bench")            # pylint: disable=unused-variable
    # cmd["bench"] = cmd_bench

    subparser_export = subparsers.add_parser("export")
    subparser_export.add_argument("target")
    subparser_export.add_argument("--id", nargs="+", action="extend", dest="l_ids", type=str)
    cmd["export"] = cmd_export

    subparser_import = subparsers.add_parser("import")
    subparser_import.add_argument("source")
    subparser_import.add_argument("--id", nargs="+", action="extend", dest="l_ids", type=str)
    cmd["import"] = cmd_import

    logger.debug("parsing cmdline...")

    # and then run parse_args() again, after including the subparsers
    if len(sys.argv) == 1:
        # no arguments at all? you need help.
        parser.parse_args(["--help"])
    else:
        args = parser.parse_args()
        # finally run a command
        cmd[args.cmd](args)
        # log("good exit")


if __name__ == "__main__":
    main()
