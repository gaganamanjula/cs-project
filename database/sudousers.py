from . import DB, get_stuff

AL = DB.get("SUDOLIST")
if not AL:
  DB.set("SUDOLIST", "{'USERS':[]}")

def add_sudolist(id):
  mn = get_stuff("SUDOLIST")
  try:
    lt = mn["USERS"]
  except:
    mn.update({"USERS": [id]})
    DB.set("SUDOLIST", str(mn))
    return True
  if not lt:
    lt = []
  if id not in lt:
    lt.append(id)
  mn.update({"USERS": lt})
  DB.set("SUDOLIST", str(mn))


def check_sudolist(id):
  std = get_stuff("SUDOLIST")
  try:
    MNT = std["USERS"]
  except:
    return False
  if MNT and id in MNT:
    return True
  return False


def remove_sudolist(id):
  Bl = get_stuff("SUDOLIST")
  if not (Bl and Bl["USERS"]):
    return "Sudo User List is Empty !"
  if id not in Bl["USERS"]:
    return "User Was Not Sudo !"
  mn = Bl["USERS"]
  mn.remove(id)
  Bl.update({"USERS": mn})
  DB.set("SUDOLIST", str(Bl))
  return "Removed User from SUDOLIST"


def get_sudolisted():
  Bl = get_stuff("SUDOLIST")
  if not Bl:
    return []
  return Bl["USERS"]
