from asyncio.locks import Lock
from sqlalchemy.ext.asyncio import AsyncSession
from . import BaseStore
from controllers.employee import EmployeeController


class AdminsStore(BaseStore):
    KEY = "admins"
    LOADING_LOCK = Lock()
    
    @staticmethod
    async def _load_from_db(session: AsyncSession):
        controller = EmployeeController(session)
        return await controller.get_admins_ids()
