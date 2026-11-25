import argparse
import json
import sys
from . import __version__
from .audit import audit


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(1, self.prog + ': error: ' + message + '\n')


def main(argv=None):
    parser = Parser(prog='ismn-validation-claim-audit')
    parser.add_argument('--version', action='version', version=__version__)
    subs = parser.add_subparsers(dest='command', required=True, parser_class=Parser)
    scan = subs.add_parser('audit')
    scan.add_argument('repo', nargs='?', default='.')
    scan.add_argument('--fail-on', choices=('high', 'medium'), default='high')
    scan.add_argument('--ignore', action='append', default=[])
    scan.add_argument('--json', action='store_true')
    scan.add_argument('--verbose', action='store_true')
    args = parser.parse_args(argv)
    try:
        findings = audit(args.repo, args.ignore)
    except (OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({'findings': findings}, indent=2))
    elif findings:
        for finding in findings:
            print(finding['severity'] + ': ' + finding['id'])
    else:
        print('PASS')
    if args.verbose and not args.json:
        print('Audited: ' + args.repo)
    return 2 if any(x['severity'] == 'HIGH' or args.fail_on == 'medium' for x in findings) else 0


if __name__ == '__main__':
    sys.exit(main())
