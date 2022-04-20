import argparse

from src.storage import get_previous_character, initialize_death_file, print_all_characters, \
    print_previous_character


def make_argparser():
    """
    Setup argparse arguments.
    """
    parser = argparse.ArgumentParser(prog='youdied',
                                     description="A motivational Elden Ring death counter.\n\n"
                                                 "Uses screen capture to detect deaths.\n"
                                                 "Will output motivational quotes and proverbs on detection.\n",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="Good luck, Tarnished!")
    parser.add_argument("-v", "--version", action="store_true", help="Print version and exit.")

    parser.add_argument("character_name", nargs='*', default=None,
                        help="Name of character to register stats on. " 
                             "If omitted the last used character is used, if any")

    parser.add_argument("-l", "--list", action="store_true",
                        help="List all characters.")
    parser.add_argument("-p", "--previous", action="store_true",
                        help="Print out previous character, i.e. the last one used.")

    # parser.add_argument("--clear", action="store_true",
    #                     help="Delete all existing records for the character and start from zero.")
    return parser


def start_detecting(character):
    from capture_and_detect import run_forever
    run_forever(character)


def run_from_cli():
    parser = make_argparser()
    args = parser.parse_args()
    if args.version:
        from pkg_resources import get_distribution, DistributionNotFound
        try:
            __version__ = get_distribution(__name__).version
            print(__version__)
        except DistributionNotFound:
            # package is not installed
            print('Cannot print version. Package not installed')
            pass
        return

    if args.list:
        print_all_characters()
        return

    if args.previous:
        print_previous_character()
        return

    character = ' '.join(args.character_name) or get_previous_character()
    initialize_death_file(character)
    print(f'You chose {character}. Starting...\n')
    start_detecting(character)
