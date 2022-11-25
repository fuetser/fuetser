import textwrap
import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize
from vkapi import config, session
from vkapi.exceptions import APIError


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    _filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """
    code = f"""
    if ({count} < 100)<
        posts = API.wall.get(
            <
                owner_id:{owner_id},
                domain:{domain},
                offset:{offset},
                "count":"{count}",
                filter:{_filter},
                extended:{extended},
                fields: {fields}
            >
        );
    >
    else <
        posts = [];
        for(var i = 0; i < Math.floor({count} / 100) - 1; i++) <
            p = API.wall.get(
                <
                    owner_id:{owner_id},
                    domain:{domain},
                    offset:{offset}+ i * 100,
                    count: 100,
                    filter:{_filter},
                    extended:{extended},
                    fields: {fields}
                >
            );
            posts.push(...p);
        >
    >
    return posts;
    """.replace(
        "<", "{"
    ).replace(
        ">", "}"
    )
    time.sleep(2)
    resp = session.post(
        "/execute",
        code=code,
        access_token=config.VK_CONFIG["access_token"],
        v=config.VK_CONFIG["version"],
    )
    return json_normalize(resp.json()["response"]["items"])
