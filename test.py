import argparse
import sys
from gevent import monkey
import gevent
import time
import requests

monkey.patch_all()

_stats = []


def clear_stats():
    _stats[:] = []


def print_stats():
    print('')
    print('Successful calls\t\t%r' % len(_stats))
    print('Average          \t\t%.4f' % (sum(_stats) / len(_stats)))
    print('Fastest          \t\t%.4f' % min(_stats))
    print('Slowest          \t\t%.4f' % max(_stats))


def onecall(url):
    start = time.time()
    try:
        requests.get(url)
    finally:
        _stats.append(time.time() - start)

    print _stats
    sys.stdout.write('=')
    # sys.stdout.flush()


def run(url, num, method='GET'):
    # need to be changed to num/concurrency
    for i in range(num):
        onecall(url)


def load(url, requests, concurrency):
    clear_stats()
    sys.stdout.write('Starting the load [')
    try:
        jobs = [gevent.spawn(run, url, requests) for i in range(concurrency)]
        print jobs
        gevent.joinall(jobs)
        print jobs
    finally:
        print('] Done')

    print_stats()


def main():
    parser = argparse.ArgumentParser(description='AB For Humans.')

    parser.add_argument('-n', '--requests', help='Number of requests',
                        default=1,
                        type=int)

    parser.add_argument('-c', '--concurrency', help='Concurrency', default=1,
                        type=int)
    parser.add_argument('url', help='URL to hit')

    args = parser.parse_args()
    print args
    try:
        load(args.url, args.requests, args.concurrency)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
