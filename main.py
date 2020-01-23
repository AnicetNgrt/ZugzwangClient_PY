import asyncio
import socketio
import flore1 as f1

loop = asyncio.get_event_loop()
sio = socketio.Client()

@sio.on('game created')
def game_create(data):
  game_name = data["game_name"]
  f1.clear_screen()
  print(f'Game \"{game_name}\" created !')
  print("Waiting for players to join ...")


@sio.on('available boards')
def available_boards(data):
  boards = data["boards"]
  chosen = False
  while not chosen:
    n = 0
    bd = []
    f1.clear_screen()
    print("== Choose board ==")
    for cat in boards.keys():
      for el in boards[cat].keys():
        n += 1
        bd.append((boards[cat][el], cat, el))
        print(f"{n} -- {cat} - {el}")
    print("\n")
    n = input("board to select: ")
    n = int(n)-1
    if not 0 <= n < len(bd):
      continue

    b, c, e = bd[n]
    f1.clear_screen()
    print("================")
    print(f"Displaying: {c} - {e}\n")
    print(b)
    print("\n1 - select\n2 - back\n")
    choice = input("choice: ")
    if choice == "1":
      chosen = True
      sio.emit("board chosen", {"cat":c, "el":e})


@sio.on('available rules')
def available_rules(data):
  rules = data["rules"]
  chosen = False
  while not chosen:
    n = 0
    rl = []
    f1.clear_screen()
    print("== Choose rules ==")
    for cat in rules.keys():
      for el in rules[cat].keys():
        n += 1
        rl.append((rules[cat][el], cat, el))
        print(f"{n} -- {cat} - {el}")
    print("\n")
    n = input("rules to select: ")
    n = int(n)-1
    if not 0 <= n < len(rl):
      continue

    r, c, e = rl[n]
    f1.clear_screen()
    print("================")
    print(f"Displaying: {c} - {e}\n")
    for field in r.keys():
      print(f"{field}: {r[field]}")
    print("\n1 - select\n2 - back\n")
    choice = input("choice: ")
    if choice == "1":
      chosen = True
      sio.emit("rules chosen", {"cat":c, "el":e})


@sio.event
def connect():
  sio.emit('test', {})

  print("connected to the Zugzwang server !")
  name = input("choose username: ")
  sio.emit("my name is", {"name":name})

  f1.clear_screen()
  print("===== MENU =====")
  print("1 - join game")
  print("2 - create game\n")
  c = input("?")

  if c == "2":
    sio.emit("create game", data={})

  if c == "1":
    game_name = input("game_name: ")
    sio.emit("join game", game_name)

def start_server():
  sio.connect('https://zugzwang-core.anicetn.repl.co')
  sio.wait()

if __name__ == '__main__':
  print('loading...')
  start_server()