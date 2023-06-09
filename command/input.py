"""
This file contains utilities for handling input from the user and registering specific keys to specific functions,
based on https://github.com/bchao1/bullet
"""
from typing import List

from .keymap import KEYMAP, get_character


def mark(key: str):
    """
    Mark the function with the key code so it can be handled in the register
    """

    def decorator(func):
        handle = getattr(func, "handle_key", [])
        handle += [key]
        setattr(func, "handle_key", handle)
        return func

    return decorator


def mark_multiple(*keys: List[str]):
    """
    Mark the function with the key codes so it can be handled in the register
    """

    def decorator(func):
        handle = getattr(func, "handle_key", [])
        handle += keys
        setattr(func, "handle_key", handle)
        return func

    return decorator


class KeyHandler(type):
    """
    Metaclass that adds the key handlers to the class
    """

    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        if not hasattr(new_cls, "key_handler"):
            setattr(new_cls, "key_handler", {})
        setattr(new_cls, "handle_input", KeyHandler.handle_input)

        for value in attrs.values():
            handled_keys = getattr(value, "handle_key", [])
            for key in handled_keys:
                new_cls.key_handler[key] = value
        return new_cls

    @staticmethod
    def handle_input(cls):
        "Finds and returns the selected character if it exists in the handler"
        char = get_character()
        if char != KEYMAP["undefined"]:
            char = ord(char)
        handler = cls.key_handler.get(char)
        if handler:
            cls.current_selection = char
            return handler(cls)
        else:
            return None


def register(cls):
    """Adds KeyHandler metaclass to the class"""
    return KeyHandler(cls.__name__, cls.__bases__, cls.__dict__.copy())
