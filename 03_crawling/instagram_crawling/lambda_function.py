from __future__ import unicode_literals
import argparse
from crawler import InsCrawler


def get_posts_by_user(username, number, detail, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_user_posts(username, number, detail)


def lambda_handler(event):
    parser = argparse.ArgumentParser(description="Instagram Crawler")
    parser.add_argument("--mode", type=str, default="posts")
    parser.add_argument("--number", type=int, default=1)
    parser.add_argument("--username", type=str, default=event['username'])
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()

    print(args)
    get_posts_by_user(args.username, args.number, args.mode , args.debug)


if __name__ == "__main__":
    event = {
        'username' : 'kimdongyeon_dy'
    }
    lambda_handler(event)