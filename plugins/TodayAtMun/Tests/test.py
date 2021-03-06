import sys
import unittest
from unittest.case import TestCase
import pytest


sys.path.append("../")
from datetime import date, datetime, timedelta
from DiaryUtil import DiaryUtil
from DiaryParser import DiaryParser


class TestDateMethods(unittest.TestCase):
    """Testing TodayAtMun Plugin"""

    parse = DiaryParser()
    diary = DiaryUtil(parse.diary)

    def test1_today_is_next(self):
        print("Start today_is_next tests")
        print("Success 1 - Test a formatted date that is not the same")
        self.assertEqual(self.diary.today_is_next("May 31, 2020, Monday"), "")
        print("Success 2 - Test a formatted date that is today")
        self.assertEqual(
            self.diary.today_is_next(self.diary.format_date(datetime.now())), "🔴"
        )
        print("Success 3 - Test a date that is not formatted")
        self.assertNotEqual(datetime.now(), "🔴")

    def test2_time_delta_event(self):
        print("\nStart time_delta_event tests")
        print("Success 1 - Test a date ahead of the current date")
        self.assertEqual(self.diary.time_delta_event(datetime.now()), 0)
        print("Success 2 - Test date with y, m, d")
        self.assertEqual(
            self.diary.time_delta_event(datetime(2022, 10, 2), datetime(2022, 10, 1)), 1
        )
        print("Success 3 - Test date with y, m, d, hr, min")
        self.assertEqual(
            self.diary.time_delta_event(
                datetime(2022, 10, 3, 23, 0), datetime(2022, 10, 2, 22, 59)
            ),
            1,
        )


@pytest.fixture
def parsed_diary():
    return DiaryUtil(DiaryParser().diary)


@pytest.mark.parametrize(
    "date, expected",
    [(date(2021, 10, 22), ""), (datetime.now(), "🔴")],
)
def test_today_is_next(date, expected):
    parse = DiaryParser()
    diary = DiaryUtil(parse.diary)
    date = diary.format_date(diary.truncate_date_time(date))
    assert diary.today_is_next(date) == expected


@pytest.mark.parametrize(
    " today_time, event_time, expected",
    [
        (datetime(2022, 10, 2), datetime(2022, 10, 1), 1),
        (datetime(2022, 10, 2), datetime(2022, 10, 1), 1),
        (datetime(2022, 10, 3, 23, 0), datetime(2022, 10, 2, 22, 59), 1),
        (datetime(2000, 8, 2), datetime(2000, 8, 2), 0),
    ],
)
def test_time_delta_event(today_time, event_time, expected):
    parse = DiaryParser()
    diary = DiaryUtil(parse.diary)
    assert diary.time_delta_event(today_time, event_time) == expected


def test_package_of_events():
    diary_data = {
        "October 23, 2010, Saturday": "Pizza Party",
        "November 20, 2010, Saturday": "Santa Clause parade lol",
        "December 10, 2010, Friday": "December is on the go",
        "December 30, 2010, Thursday": "NYE EVE",
        "December 31, 2010, Friday": "Friday NYE",
        "January 1, 2011, Saturday": "NYD",
    }

    test1_diary_expected = {
        "October 23, 2010, Saturday": "Pizza Party",
        "November 20, 2010, Saturday": "Santa Clause parade lol",
        "December 10, 2010, Friday": "December is on the go",
        "December 30, 2010, Thursday": "NYE EVE",
    }

    test2_diary_expected = {
        "October 23, 2010, Saturday": "Pizza Party",
        "November 20, 2010, Saturday": "Santa Clause parade lol",
        "December 10, 2010, Friday": "December is on the go",
        "December 30, 2010, Thursday": "NYE EVE",
        "December 31, 2010, Friday": "Friday NYE",
        }
    date = datetime(2010, 10, 22)
    diary = DiaryUtil(diary_data)
    TestCase().assertDictEqual(diary.package_of_events(date, 4), test1_diary_expected)
    TestCase().assertDictEqual(diary.package_of_events(date, 5), test2_diary_expected)

def test_find_event(parsed_diary):

    future_date = datetime.now() + timedelta(days=400)
    formatted_future_date = parsed_diary.format_date(future_date)
    diary_data = {f"{formatted_future_date}": "2 years away"}
    diary_util = DiaryUtil(diary_data)
    date = datetime.now()
    assert diary_util.find_event(date) == ""

    future_date2 = datetime.now() + timedelta(days=30)
    formated_date2 = parsed_diary.format_date(future_date2)
    diary_data = {f"{formated_date2}": "40 days away"}
    diary_util = DiaryUtil(diary_data)
    assert diary_data[diary_util.find_event(date)] == "40 days away"

