from mongoengine.base import BaseList
from flask_admin.model.typefmt import BASE_FORMATTERS, list_formatter


DEFAULT_FORMATTERS = BASE_FORMATTERS.copy()
DEFAULT_FORMATTERS.update({
    BaseList: list_formatter
})
