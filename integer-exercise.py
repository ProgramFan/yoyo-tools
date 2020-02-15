#!/usr/bin/env python3
# coding: utf-8

import argparse
import itertools
import random
import re
import string
import sys

ALL_EXERCISES = {
    "add10": {
        "expr": "$a + $b",
        "vars": {
            "a": range(1, 10),
            "b": range(1, 10),
        },
        "criteria": ["$a + $b <= 10"]
    },
    "add15-1d": {
        "expr": "$a + $b",
        "vars": {
            "a": range(1, 10),
            "b": range(1, 10),
        },
        "criteria": ["$a + $b <= 15", "$a + $b >= 7"]
    },
    "add20-1d": {
        "expr": "$a + $b",
        "vars": {
            "a": range(1, 10),
            "b": range(1, 10),
        },
        "criteria": ["$a + $b >= 7"]
    },
    "add20-2d": {
        "expr": "$a + $b",
        "vars": {
            "a": range(1, 20),
            "b": range(1, 20),
        },
        "criteria": ["$a + $b <= 20", "$a + $b >= 7"]
    },
    "sub10": {
        "expr": "$a - $b",
        "vars": {
            "a": range(1, 10),
            "b": range(1, 10),
        },
        "criteria": ["$a - $b > 0"]
    }
}


def read_int(s):
    int_regex = re.compile(r"\d+")
    while True:
        v = input(s)
        if v == "q":
            sys.exit()
        if int_regex.match(v):
            return int(v)


def make_all_cases(exercise):
    var_names = exercise["vars"].keys()
    var_values = [exercise["vars"][k] for k in var_names]
    cases = []
    for trail in itertools.product(*var_values):
        tpl_vars = dict(zip(var_names, trail))
        expr = string.Template(exercise["expr"]).substitute(**tpl_vars)
        valid = True
        for c in exercise["criteria"]:
            cr = string.Template(c).substitute(**tpl_vars)
            valid = valid and eval(cr)
        if valid:
            cases.append(expr)
    return cases


def make_test_case(exercise):
    while True:
        tpl_vars = dict()
        for k, v in exercise["vars"].items():
            tpl_vars[k] = str(random.choice(v))
        expr = string.Template(exercise["expr"]).substitute(**tpl_vars)
        expected = eval(expr)
        allowed = True
        for c in exercise["criteria"]:
            cr = string.Template(c).substitute(**tpl_vars)
            allowed = allowed and eval(cr)
        if allowed:
            return (expr, expected)


def make_test_suite(exercise, count):
    all_cases = make_all_cases(exercise)
    return random.sample(all_cases, count)


def do_exercise(suite):
    count = len(suite)
    oneshot = [True for i in range(count)]
    redo = []
    for i, expr in enumerate(suite):
        expected = eval(expr)
        prompt = "✏️  " + expr + " = "
        while read_int(prompt) != expected:
            print("❎ 错了，😢😢😢\n")
            oneshot[i] = False
            redo.append(expr)
        print("✅ 对了，😁😁😁\n")
    good = oneshot.count(True)
    score = int(good / count * 100)
    print("🎉🎉🎉 恭喜你做完了！")
    print("💛💛💛 做对：{} 道，得 {} 分\n".format(good, score))
    return redo


def run_exercise(exercise, count):
    suite = make_test_suite(exercise, count)
    while suite:
        suite = do_exercise(suite)
        print("")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("EXERCISE", help="练习题类型", choices=ALL_EXERCISES.keys())
    parser.add_argument("COUNT", help="题目数", type=int)

    args = parser.parse_args()
    run_exercise(ALL_EXERCISES[args.EXERCISE], args.COUNT)


if __name__ == "__main__":
    main()
