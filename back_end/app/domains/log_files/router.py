from fastapi import APIRouter, UploadFile, Depends

from app.domains.users.dependencies import get_current_user
from app.domains.users.model import User
from .schema import LogFileResponse
from .service import LogFileService

router = APIRouter()


@router.post(
	"/upload",
	response_model=LogFileResponse,
	summary="Enviar arquivo de log",
	description="Recebe um arquivo .log (máx. 5MB), armazena e registra no banco",
	responses={
		400: {"description": "Extensão inválida ou arquivo excede o tamanho máximo"},
		401: {"description": "Não autenticado"},
	},
)
async def upload_file(
	file: UploadFile,
	current_user: User = Depends(get_current_user),
):
	return await LogFileService.upload(file, current_user)
