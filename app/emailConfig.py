from pathlib import Path
from typing import Any, Dict, List

from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from .config import Settings


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]

settings = Settings()

conf = ConnectionConfig(
    MAIL_USERNAME =settings.MAIL_USERNAME,
    MAIL_PASSWORD =settings.MAIL_PASSWORD ,
    MAIL_FROM =settings.MAIL_FROM ,
    MAIL_PORT = settings.EMAIL_PORT,
    MAIL_SERVER =settings.MAIL_SERVER ,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
)


async def send_with_template(email: EmailSchema , a : str) -> JSONResponse:

    message = MessageSchema(
        subject="Account Activation",
        recipients=email.dict().get("email"),
        template_body=email.dict().get("body"),
        subtype=MessageType.html,
        )

    fm = FastMail(conf)
    await fm.send_message(message, template_name=a) 
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
 