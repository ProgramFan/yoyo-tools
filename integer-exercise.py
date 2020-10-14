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
import os

SCRIPT_DIR = os.path.realpath(os.path.dirname(sys.argv[0]))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
ALL_EXERCISES = json.load(open(os.path.join(DATA_DIR,
                                            "integer-exercise.json")))
PROGRESS_CHARS = [
    "🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚", "🕛"
]


def show_progress(v):
    assert v >= 0 and v <= 1
    return PROGRESS_CHARS[int(round(v * (len(PROGRESS_CHARS) - 1)))]


def clear_screen():
    print(chr(27) + '[2j')
    print('\033c')
    print('\x1bc')


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


def sample_n(collection, count):
    if len(collection) < count:
        collection *= (count + len(collection) - 1) // len(collection)
    return random.sample(collection, count)


def make_test_suite(exercises, count):
    result = []
    avg = count // len(exercises)
    last = avg
    if avg * len(exercises) != count:
        last = count - avg * (len(exercises) - 1)
    for e in exercises[:-1]:
        result.extend(sample_n(make_all_cases(e), avg))
    result.extend(sample_n(make_all_cases(exercises[-1]), last))
    random.shuffle(result)
    return result


def do_exercise(suite, feedback):
    count = len(suite)
    oneshot = [True for i in range(count)]
    time = [0 for i in range(count)]
    redo = []
    for i, (repr, expr) in enumerate(suite):
        expected = eval(expr)
        prompt = show_progress(i / count) + " " + repr + " = "
        t0 = datetime.datetime.now()
        if feedback:
            while read_int(prompt) != expected:
                print("❎ 错了，😢😢😢\n")
                oneshot[i] = False
            print("✅ 对了，😁😁😁\n")
        else:
            if read_int(prompt) != expected:
                oneshot[i] = False
        t1 = datetime.datetime.now()
        time[i] = (t1 - t0).total_seconds()
        if oneshot[i] == False:
            redo.append((repr, expr))
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


def run_exercise(exercises, count, dump, feedback):
    used_suites = []
    suite = make_test_suite(exercises, count)
    clear_screen()
    begin = datetime.datetime.now()
    first_time = True
    while suite:
        used_suites.append(list(suite))
        suite = do_exercise(suite, feedback or not first_time)
        print("")
        first_time = False
    end = datetime.datetime.now()
    secs_used = int((end - begin).total_seconds())
    print("⏰⏰⏰ 用时：{}分{}秒\n".format(secs_used // 60, secs_used % 60))
    if dump is not None:
        json.dump(used_suites, open(dump, "w"))


def make_latex(exercises, count, title):
    used_suites = []
    suite = make_test_suite(exercises, count)
    tpl_dir = os.path.join(DATA_DIR, "template")
    tpl = string.Template(open(os.path.join(tpl_dir, "4x24.tex")).read())
    content = ""
    line_segs = []
    for repr, _ in suite:
        line_segs.append(f"{repr} = ")
        if len(line_segs) == 4:
            content += "    " + " & ".join(line_segs) + " \\\\\n"
            line_segs = []
    if line_segs:
        line_segs = line_segs + [" "] * (4 - len(line_segs))
        content += "    " + " & ".join(line_segs) + " \\\\\n"
    tpl_vars = {"title": title, "content": content}
    print(tpl.safe_substitute(**tpl_vars))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e, --exercise",
                        help="题库",
                        nargs="+",
                        choices=ALL_EXERCISES.keys(),
                        dest="EXERCISE",
                        action="append",
                        required=True)
    parser.add_argument("-c, --count",
                        help="题数",
                        type=int,
                        dest="COUNT",
                        required=True)
    parser.add_argument("-d, --dump",
                        help="导出做题过程到文件",
                        dest="DUMP",
                        default="solving.json")
    parser.add_argument("-f, --feedback",
                        help="即时反馈",
                        dest="FEEDBACK",
                        action="store_true")
    parser.add_argument("-l, --to-latex",
                        help="生成 LaTeX 试卷",
                        dest="TITLE",
                        default=None)

    args = parser.parse_args()
    exercises = []
    for e0 in args.EXERCISE:
        exercises.extend(ALL_EXERCISES[e] for e in e0)
    if args.TITLE:
        make_latex(exercises, args.COUNT, args.TITLE)
    else:
        run_exercise(exercises, args.COUNT, args.DUMP, args.FEEDBACK)


if __name__ == "__main__":
    main()
