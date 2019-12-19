# -*- coding: utf-8 -*-

"""This module is deprecated."""

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.query import Query
from cloudant.document import Document
import array_comparison as ac
import time


def get_database(dbname, user_name, password, url):
    client = Cloudant(user_name, password, url=url)
    client.connect()
    return client.get(dbname, remote=True)


def add_gamestate_to_database(db, gamestate):
    # Adds a new gamestate to the database.
    print("Creating new entry to db")
    gamestate_dict = {
        "state": gamestate.state.tolist(),
        "rounds": gamestate.rounds_played,
        "weight": 0.7,
        "play_count": 0
    }

    newDocument = db.create_document(gamestate_dict)

    if newDocument.exists():
        print("Document {0} created".format(gamestate.id))


def get_states_for_round(database, round_number):
    # Query that returns all known moves for given round.
    selector = {
        "rounds": round_number
        }
    fields = [
        "_id",
        "state",
        "weight",
        "play_count"
    ]
    query = Query(database, selector=selector, fields=fields)
    return [{
        "_id": res["_id"],
        "state": res["state"],
        "weight": res["weight"],
        "play_count": res["play_count"]
    } for res in query.result]


def get_state_from_database(db, gamestate):
    states = get_states_for_round(db, gamestate.rounds_played)
    for state in states:
        if ac.are_sqr_arrays_equal(state["state"], gamestate.state):
            return state


def update_document(db, state_dict):
    with Document(db, state_dict["_id"]) as doc:
        doc["weight"] = state_dict["weight"]
        doc["play_count"] = state_dict["play_count"]
        time.sleep(1)
