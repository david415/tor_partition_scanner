
def dump(dict_lines, fh):
    """
    dict_lines: list of dictionaries
    fh: filehandle to write to
    """
    for dict_line in dict_lines:
        line = "%s %s %s %s\n" % (dict_line["path"], dict_line["status"], dict_line["time_start"], dict_line["time_stop"])
        fh.write(line)
    
def load(fh):
    """
    fh: filehandle to read from
    """
    loaded = []
    for line in fh:
        fields = line.split()
        dict_line = {"path": fields[0], "status": fields[1], "time_start": fields[2], "time_stop": fields[3]}
        loaded.append(dict_line)
    return loaded
