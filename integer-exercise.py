#!/usr/bin/env python3
# coding: utf-8

import argparse
import itertools
import random
import re
import string
import sys
import json
import datetime
import math

ALL_EXERCISES = json.load(open("data/integer-exercise.json"))
PROGRESS_CHARS = [
    "🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"
]


def show_progress(v):
    assert v >= 0 and v <= 1
    return PROGRESS_CHARS[int(round(v * (len(PROGRESS_CHARS) - 1)))]


def read_int(s):
    int_regex = re.compile(r"\s*^\d+\s*$")
    while True:
        v = input(s)
        if v == "quit":
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


def make_test_suite(exercises, count):
    all_cases = []
    for e in exercises:
        all_cases.extend(make_all_cases(e))
    if len(all_cases) < count:
        all_cases *= (count + len(all_cases) - 1) // len(all_cases)
    return random.sample(all_cases, count)


def do_exercise(suite):
    count = len(suite)
    oneshot = [True for i in range(count)]
    time = [0 for i in range(count)]
    redo = []
    for i, (repr, expr) in enumerate(suite):
        expected = eval(expr)
        prompt = show_progress(i / count) + " " + repr + " = "
        t0 = datetime.datetime.now()
        while read_int(prompt) != expected:
            print("❎ 错了，😢😢😢\n")
            oneshot[i] = False
        t1 = datetime.datetime.now()
        time[i] = (t1 - t0).total_seconds()
        if oneshot[i] == False:
            redo.append((repr, expr))
        print("✅ 对了，😁😁😁\n")
    good = oneshot.count(True)
    score = int(good / count * 100)
    print("🎉🎉🎉 恭喜你做完了！")
    print("💛💛💛 做对：{} 道，得 {} 分\n".format(good, score))
    # Add those takes extremely long to finish into next round so that they can
    # be memorized. Here we use the technique of z-score for outlier detection
    # and the exercise over 2.5 std derivations are considered too slow and
    # added to the redo list.
    if count == 1:
        return redo
    avg = sum(time) / len(time)
    std = math.sqrt(1.0 / len(time) * sum((v - avg)**2 for v in time))
    if std / avg < 0.05:
        return redo
    for i, v in enumerate(suite):
        if (time[i] - avg) / std > 2.5 and v not in redo:
            redo.append(v)
    return redo


def run_exercise(exercises, count):
    begin = datetime.datetime.now()
    suite = make_test_suite(exercises, count)
    while suite:
        suite = do_exercise(suite)
        print("")
    end = datetime.datetime.now()
    secs_used = int((end - begin).total_seconds())
    print("⏰⏰⏰ 用时：{}分{}秒\n".format(secs_used // 60, secs_used % 60))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e, --exercise",
                        help="题库",
                        nargs="+",
                        choices=ALL_EXERCISES.keys(),
                        dest="EXERCISE",
                        required=True)
    parser.add_argument("-c, --count",
                        help="题数",
                        type=int,
                        dest="COUNT",
                        required=True)

    args = parser.parse_args()
    exercises = [ALL_EXERCISES[e] for e in args.EXERCISE]
    run_exercise(exercises, args.COUNT)


if __name__ == "__main__":
    main()
