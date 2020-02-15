#!/usr/bin/env python3
# coding: utf-8

import argparse
import itertools
import random
import re
import string
import sys
import json

ALL_EXERCISES = json.load(open("data/integer-exercise.json"))


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
    to_list = lambda x: eval(x) if isinstance(x, str) else list(x)
    var_values = [to_list(exercise["vars"][k]) for k in var_names]
    cases = []
    for trail in itertools.product(*var_values):
        tpl_vars = dict(zip(var_names, trail))
        expr = string.Template(exercise["expr"]).substitute(**tpl_vars)
        valid = True
        for c in exercise["criteria"]:
            cr = string.Template(c).substitute(**tpl_vars)
            valid = valid and eval(cr)
        if valid:
            repr = string.Template(exercise["repr"]).substitute(**tpl_vars)
            cases.append((repr, expr))
    return cases


def make_test_case(exercise):
    while True:
        tpl_vars = dict()
        for k, v in exercise["vars"].items():
            tpl_vars[k] = str(random.choice(v))
        expr = string.Template(exercise["expr"]).substitute(**tpl_vars)
        allowed = True
        for c in exercise["criteria"]:
            cr = string.Template(c).substitute(**tpl_vars)
            allowed = allowed and eval(cr)
        if allowed:
            repr = string.Template(exercise["repr"]).substitute(**tpl_vars)
            return (repr, expr)


def make_test_suite(exercise, count):
    all_cases = make_all_cases(exercise)
    return random.sample(all_cases, count)


def do_exercise(suite):
    count = len(suite)
    oneshot = [True for i in range(count)]
    redo = []
    for i, (repr, expr) in enumerate(suite):
        expected = eval(expr)
        prompt = "✏️  " + repr + " = "
        while read_int(prompt) != expected:
            print("❎ 错了，😢😢😢\n")
            oneshot[i] = False
            redo.append((repr, expr))
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
    parser.add_argument("EXERCISE", help="题库", choices=ALL_EXERCISES.keys())
    parser.add_argument("COUNT", help="题数", type=int)

    args = parser.parse_args()
    run_exercise(ALL_EXERCISES[args.EXERCISE], args.COUNT)


if __name__ == "__main__":
    main()
