from asyncio.locks import Lock
from . import BaseStore
from sqlalchemy.ext.asyncio import AsyncSession
from controllers.employee import EmployeeController


class EmployeeStore(BaseStore):
    LOADING_LOCK = Lock()
    KEY = "employees"
    
    @staticmethod
    async def _load_from_db(session: AsyncSession):
        controller = EmployeeController(session)
        return await controller.get_all_ids()
