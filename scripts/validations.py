class Validate:
    def chat_id(chat_id) -> None:
        if not chat_id:
            raise ValueError("chat_id cannot be empty!")

        if type(chat_id) is not int:
            raise TypeError("Incorrect chat_id type!")
