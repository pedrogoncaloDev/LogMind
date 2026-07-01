def create_user(user_data: dict) -> User:
	"""
	Create a new user in the database.

	Args:
		user_data (dict): A dictionary containing user data.

	Returns:
		User: The created User object.
	"""
	new_user = User(**user_data)
	db.session.add(new_user)
	db.session.commit()
	return new_user