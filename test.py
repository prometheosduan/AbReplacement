import argparse
import sys
from gevent import monkey
import time
import requests
from gevent.pool import Pool

monkey.patch_all()

_stats = []
_VERBS = ['GET', 'POST', 'DELETE', 'PUT', 'HEAD', ]


def clear_stats():
    _stats[:] = []


def print_stats(total):
    print('')
    print('Successful calls\t\t%r' % len(_stats))
    print('Total time       \t\t%.4f s' % total)
    print('Average          \t\t%.4f' % (sum(_stats) / len(_stats)))
    print('Fastest          \t\t%.4f' % min(_stats))
    print('Slowest          \t\t%.4f' % max(_stats))


def onecall(url, method):
    method = getattr(requests, method.lower())
    start = time.time()
    try:
        method(url)
    finally:
        _stats.append(time.time() - start)

    sys.stdout.write('=')
    sys.stdout.flush()


def run(url, num, method, concurrency):
    '''
    Maintain a group of greenlets that are still running with the maximum
    amount of active ones that will be allowed
    '''
    pool = Pool(concurrency)
    for i in range(num):
        '''
        Begin a new greenlet & add it to the collection
        of greenlets this group is monitoring
        '''
        pool.spawn(onecall, url, method)
    # Wait for this group to become empty at least once
    pool.join()


def load(url, requests, concurrency, method):
    clear_stats()
    sys.stdout.write('Starting the load [')
    try:
        run(url, requests, method, concurrency)
    finally:
        print('] Done')



def main():
    parser = argparse.ArgumentParser(description='AB For Humans.')

    parser.add_argument('-n', '--requests', help='Number of requests',
                        default=1,
                        type=int)

    parser.add_argument('-m', '--method', help='Concurrency',
                        type=str, default='GET', choices=_VERBS)

    parser.add_argument('-c', '--concurrency', help='Concurrency', default=1,
                        type=int)

    parser.add_argument('url', help='URL to hit')

    args = parser.parse_args()
    print args

    start = time.time()
    try:
        load(args.url, args.requests, args.concurrency, args.method)
    except KeyboardInterrupt:
        sys.exit(0)
    finally:
        total = time.time() - start
        print_stats(total)


if __name__ == '__main__':
    main()
