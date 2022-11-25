import datetime as dt
import re
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    current_year = dt.datetime.now().year
    friends = get_friends(user_id).items
    ages = []
    for friend in friends:
        if (bdate := friend.get("bdate")) is not None:
            if re.findall(r"\d[.]\d[.]\d", bdate):
                year_of_birth = int(bdate.split(".")[-1])
                ages.append(current_year - year_of_birth)
    return statistics.median(ages) if ages else None
