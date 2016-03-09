#!/usr/bin/env python
# encoding: utf-8

"""
test the score game using selenium
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="module")
def firefox(request):
    """
    return a new instance of firefox webdriver
    :param request: see pytest doc
    :return: a new instance of firefox webdriver
    """
    firefox_handler = webdriver.Firefox()

    def end_me():
        """
        We want the firefox frame to be closed at last test call
        """
        firefox_handler.close()
    request.addfinalizer(end_me)
    return firefox_handler


@pytest.mark.skipif(not pytest.config.option.doselenium,
                    reason='you need to specify --selenium to run this test')
def test_index(firefox):
    """
    test the app using selenium
    @param firefox: a firefox instance
    """
    firefox.get("http://localhost:8080")
    assert "GAME STATS" == firefox.title

    __add_play(firefox)
    __delete_all_test_games(firefox)


def __add_play(firefox, players=None, date='21/07/2019', game='test_game'):
    """
    Adds a play using the interface
    :rtype: None
    :param firefox: the firefox instance
    :param game:
    :param date:
    :param players:
    :return: None
    """
    if players is None:
        players = ['test_p1:100', 'test_p2:102']

    firefox.get('http://localhost:8080/new')
    assert "NEW GAME" == firefox.title
    elem = firefox.find_element_by_id('dateId')
    elem.send_keys(date)
    elem = firefox.find_element_by_id('gameId')
    elem.send_keys(game)
    elem = firefox.find_element_by_id('playersId')
    for player in players:
        elem.send_keys(player)
        elem.send_keys(Keys.RETURN)
    elem = firefox.find_element_by_id('sendId')
    elem.click()
    assert 'OK' in firefox.find_element_by_css_selector('p').text


def __delete_all_test_games(firefox):
    """
    delete all the test games
    """
    deleted_a_game = True
    while deleted_a_game:
        firefox.get("http://localhost:8080")
        assert "GAME STATS" == firefox.title
        xpath = '//table[@id="plays_table"]/descendant::tr'
        deleted_a_game = False
        for elem in firefox.find_elements_by_xpath(xpath):
            if 'test_game' in elem.text:
                a_tag = elem.find_element_by_css_selector('a')
                a_tag.click()
                # firefox.get(href)
                deleted_a_game = True
                break
    firefox.get("http://localhost:8080")
    for elem in firefox.find_elements_by_xpath(xpath):
            if 'test_game' in elem.text:
                pytest.fail('Find a test_game in the list of games')
