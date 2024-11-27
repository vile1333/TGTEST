from aiogram import Router,F

from .start import start_router
from .hw_dialog import hw_dialog_router




private_router = Router()

private_router.include_router(start_router)
private_router.include_router(hw_dialog_router)

