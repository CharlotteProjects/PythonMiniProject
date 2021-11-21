# For Customer Color

def Color(color = ""):
    if color == "BLACK":
        return (  0,   0,   0)
    elif color == "WHITE":
        return (255, 255, 255)
    elif color == "BLUE":
        return (255,   0,   0)
    elif color == "GREEN":
        return (  0, 255,   0)
    elif color == "RED":
        return (  0,   0, 255)
    elif color == "CYAN":
        return (255, 255,   0)
    elif color == "MAGENTA":
        return (255,   0, 255)
    elif color == "YELLOW":
        return (  0, 255, 255)
    else:
        return (  0,   0,   0)