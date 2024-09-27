# Converts request size based on request parameters into some size based on server speed. Formula given by user
def sizeConversion(size, reqType):
    if reqType == "LOG_IN":
        return 0.001
    reqSize = size/10000000 + 0.0095
    return reqSize