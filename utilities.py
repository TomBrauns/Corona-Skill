def formatOutput(output):
    temp = str(float("{:.1f}".format(output)))
    formattedOutput = temp.replace(".", ",")
    return formattedOutput

def saveSessionAttributes(handler_input, data):
    session_attr = handler_input.attributes_manager.session_attributes
    session_attr["data"] = data
    return session_attr

