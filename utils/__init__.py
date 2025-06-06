def format_message(message) -> object:
    if "output" in message:
        message = message['output']
    return {"message": message}
