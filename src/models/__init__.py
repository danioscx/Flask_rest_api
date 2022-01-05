from typing import Any


class BaseModel(object):

    @staticmethod
    def object_to_list(lists: Any) -> list:
        """
        convert list object to list serialize
        :param lists:
          response from sqlalchemy query
        :return: list
        """
        result = []
        for value in lists:
            result.append(dict(value))
        return result
