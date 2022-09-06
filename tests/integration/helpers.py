from random import randint

ALL = ["create_threads", "generate_pairs", "generate_pair"]


def create_threads(client, count=2):
    return [client.create_thread() for _ in range(count)]


def generate_pairs(count=2):
    return [generate_one_pair() for _ in range(count)]


def generate_one_pair():
    return randint(0, 10), randint(0, 10)
