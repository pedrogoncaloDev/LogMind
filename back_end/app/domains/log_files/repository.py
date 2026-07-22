from app.database.session import SessionLocal
from .model import LogFile


def create_log_file(
	user_id,
	original_filename: str,
	stored_filename: str,
	file_size: int,
	status: str = "uploaded",
) -> LogFile:
	try:
		with SessionLocal() as database_session:
			new_log_file = LogFile(
				user_id=user_id,
				original_filename=original_filename,
				stored_filename=stored_filename,
				file_size=file_size,
				status=status,
			)

			database_session.add(new_log_file)
			database_session.commit()
			database_session.refresh(new_log_file)

			return new_log_file
	except Exception as e:
		database_session.rollback()
		raise e
