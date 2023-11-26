from fastapi import status
from fastapi.responses import JSONResponse
from game import exceptions, schemas, logic
from typing import Union


async def processing_by_item_request(
        game_logic: Union[
            logic.Business, logic.Home, logic.Skill, logic.Transport
        ],
        data: schemas.PerformActionSchema
) -> JSONResponse:
    """ Buy item requests
    :param game_logic:
    :param data:
    :return:
    """
    try:
        await game_logic.buy(data.id)
    except exceptions.NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e)}
        )
    except exceptions.AlreadyExistError as e:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": str(e)}
        )
    except exceptions.PlayerException:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Player not found"}
        )
    except exceptions.NoMoneyError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": str(e)}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Ok"}
    )


async def processing_buy_services_request(
        game_logic: Union[
            logic.Food, logic.Leisure, logic.Health
        ],
        data: schemas.PerformActionSchema
) -> JSONResponse:
    """ Buy services requests
    :param game_logic:
    :param data:
    :return:
    """
    try:
        await game_logic.buy(data.id)
    except exceptions.NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e)}
        )
    except exceptions.PlayerException:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Player not found"}
        )
    except exceptions.NoMoneyError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": str(e)}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Ok"}
    )


async def processing_action_request(
        game_logic: Union[
            logic.StreetAction, logic.Work
        ],
        data: schemas.PerformActionSchema
) -> JSONResponse:
    """ Action requests
    :param game_logic:
    :param data:
    :return:
    """
    try:
        await game_logic.run(data.id)
    except exceptions.NotFoundException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(e)}
        )
    except exceptions.PlayerException:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Player not found"}
        )
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Ok"}
        )
