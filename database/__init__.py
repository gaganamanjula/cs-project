import ast
import redis
import os

REDIS_URI = "redis-13013.c284.us-east1-2.gce.cloud.redislabs.com:13013"
REDIS_PASS = "dM38N28dpBpL5rXSo3qHYHdm3h9MIhIX"

INFO = REDIS_URI.split(":")

DB = redis.StrictRedis(
    host=INFO[0],
    port=INFO[1],
    password=REDIS_PASS,
    charset="utf-8",
    decode_responses=True,
)


def get_stuff(WHAT):
  n = []
  cha = DB.get(WHAT)
  if not cha:
    cha = "{}"
  n.append(ast.literal_eval(cha))
  return n[0]
