import asyncio
import os
import sys
import time

from telethon import TelegramClient
from telethon.tl.types import Channel, User
from telethon.errors import FloodWaitError

from colorama import init, Fore, Style


# ============================================================
# TELESWEEP
# Telegram Account Cleanup & Organization Tool
# Made by Paul
# Telegram: @vibezat1k
# ============================================================

init(autoreset=True)


# ============================================================
# TELEGRAM API CREDENTIALS
# ============================================================

from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    print("ERROR: Telegram API credentials not found.")
    print("Create a .env file with TELEGRAM_API_ID and TELEGRAM_API_HASH.")
    sys.exit(1)

API_ID = int(API_ID)

SESSION_NAME = "telegram_session"

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)


# ============================================================
# COLORS
# ============================================================

CYAN = Fore.CYAN
LIGHT_CYAN = Fore.LIGHTCYAN_EX
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
GREEN = Fore.GREEN
LIGHT_GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.YELLOW
RED = Fore.RED
WHITE = Fore.WHITE
GRAY = Fore.LIGHTBLACK_EX
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT


# ============================================================
# TERMINAL HELPERS
# ============================================================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text="", delay=0.008):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def line(char="─", length=62, color=CYAN):
    print(color + char * length)


def section(title):
    print()
    print(f"{CYAN}╭{'─' * 60}╮")
    print(f"{CYAN}│ {BOLD}{LIGHT_CYAN}{title:<58}{CYAN}│")
    print(f"{CYAN}╰{'─' * 60}╯")


def status(label, value, color=GREEN):
    print(
        f"  {GRAY}│ {WHITE}{label:<20}"
        f"{GRAY}│ {color}{value}"
    )


def pause():
    input(f"\n{GRAY}Press ENTER to continue...{RESET}")


# ============================================================
# BANNER
# ============================================================

def show_banner():

    print()

    print(
        f"{CYAN}╔════════════════════════════════════════════════════════════╗"
    )
    print(
        f"{CYAN}║                                                            ║"
    )
    print(
        f"{CYAN}║   {BOLD}{LIGHT_CYAN}████████╗███████╗██╗     ███████╗███████╗██╗    ██╗{CYAN}   ║"
    )
    print(
        f"{CYAN}║   {BOLD}{LIGHT_CYAN}╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝██║    ██║{CYAN}   ║"
    )
    print(
        f"{CYAN}║   {BOLD}{LIGHT_CYAN}   ██║   █████╗  ██║     █████╗  ███████╗██║ █╗ ██║{CYAN}   ║"
    )
    print(
        f"{CYAN}║   {BOLD}{LIGHT_CYAN}   ██║   ██╔══╝  ██║     ██╔══╝  ╚════██║██║███╗██║{CYAN}   ║"
    )
    print(
        f"{CYAN}║   {BOLD}{LIGHT_CYAN}   ██║   ███████╗███████╗███████╗███████║╚███╔███╔╝{CYAN}   ║"
    )
    print(
        f"{CYAN}║   {BOLD}{LIGHT_CYAN}   ╚═╝   ╚══════╝╚══════╝╚══════╝╚══════╝ ╚══╝╚══╝ {CYAN}   ║"
    )
    print(
        f"{CYAN}║                                                            ║"
    )

    print(
        f"{CYAN}║   {LIGHT_MAGENTA}Telegram Account Cleanup & Organization Tool{CYAN}       ║"
    )

    print(
        f"{CYAN}║                                                            ║"
    )
    print(
        f"{CYAN}║   {GRAY}Made by Paul        {MAGENTA}Telegram: {LIGHT_CYAN}@vibezat1k{CYAN}      ║"
    )
    print(
        f"{CYAN}║   {GRAY}Version 1.0.0                                      {CYAN}║"
    )
    print(
        f"{CYAN}║                                                            ║"
    )
    print(
        f"{CYAN}╚════════════════════════════════════════════════════════════╝"
    )

    print()


# ============================================================
# LOADING ANIMATION
# ============================================================

def loading(text, duration=1.2):

    frames = [
        "⠋",
        "⠙",
        "⠹",
        "⠸",
        "⠼",
        "⠴",
        "⠦",
        "⠧",
        "⠇",
        "⠏"
    ]

    start = time.time()
    i = 0

    while time.time() - start < duration:

        print(
            f"\r{CYAN}{frames[i % len(frames)]} "
            f"{WHITE}{text}",
            end="",
            flush=True
        )

        time.sleep(0.08)

        i += 1

    print(
        f"\r{GREEN}✓ {WHITE}{text}"
    )


# ============================================================
# PARSE NUMBER / RANGE SELECTION
# ============================================================

def parse_selection(text, maximum):

    text = text.replace(" ", "")

    selected = set()

    if not text:
        return []

    for part in text.split(","):

        if not part:
            continue

        try:

            if "-" in part:

                start, end = part.split("-", 1)

                start = int(start)
                end = int(end)

                if start > end:
                    start, end = end, start

                for number in range(start, end + 1):

                    if 1 <= number <= maximum:
                        selected.add(number - 1)

            else:

                number = int(part)

                if 1 <= number <= maximum:
                    selected.add(number - 1)

        except ValueError:
            continue

    return sorted(selected)


# ============================================================
# SCAN ACCOUNT
# ============================================================

async def scan_account():

    groups = []
    channels = []
    bots = []

    loading("Scanning Telegram account...")

    async for dialog in client.iter_dialogs():

        entity = dialog.entity

        # Groups
        if isinstance(entity, Channel):

            if entity.megagroup:
                groups.append(dialog)

            elif entity.broadcast:
                channels.append(dialog)

        # Bots
        elif isinstance(entity, User):

            if entity.bot:
                bots.append(dialog)

    return groups, channels, bots


# ============================================================
# PRINT SECTION
# ============================================================

def print_section(title, items, icon="●"):

    print()

    print(
        f"{MAGENTA}╭{'─' * 60}╮"
    )

    header = f"{icon} {title}  •  {len(items)} found"

    print(
        f"{MAGENTA}│ {BOLD}{LIGHT_MAGENTA}{header:<58}{MAGENTA}│"
    )

    print(
        f"{MAGENTA}╰{'─' * 60}╯"
    )

    if not items:

        print(
            f"  {GRAY}└─ No items found."
        )

        return

    for i, dialog in enumerate(items, 1):

        print(
            f"  {CYAN}{i:>4}{GRAY} │ "
            f"{WHITE}{dialog.name}"
        )


# ============================================================
# ACCOUNT SUMMARY
# ============================================================

def show_summary(groups, channels, bots):

    section("ACCOUNT OVERVIEW")

    status(
        "Groups",
        str(len(groups)),
        LIGHT_CYAN
    )

    status(
        "Channels",
        str(len(channels)),
        LIGHT_MAGENTA
    )

    status(
        "Bot chats",
        str(len(bots)),
        YELLOW
    )

    status(
        "Total manageable",
        str(
            len(groups)
            + len(channels)
            + len(bots)
        ),
        GREEN
    )


# ============================================================
# DISPLAY SELECTION
# ============================================================

def print_selected(items):

    section("SELECTED ITEMS")

    for i, dialog in enumerate(items, 1):

        print(
            f"  {GREEN}{i:>4}{GRAY} │ "
            f"{WHITE}{dialog.name}"
        )

    print()

    print(
        f"  {GRAY}Total selected: "
        f"{WHITE}{len(items)}"
    )


# ============================================================
# CONFIRMATION
# ============================================================

def confirmation_screen(items, action):

    print_selected(items)

    print()

    print(
        f"{YELLOW}╭{'─' * 60}╮"
    )

    print(
        f"{YELLOW}│ {BOLD}{YELLOW}⚠ CONFIRM ACTION{' ' * 43}{YELLOW}│"
    )

    print(
        f"{YELLOW}╰{'─' * 60}╯"
    )

    print(
        f"\n  {WHITE}Action:"
        f" {LIGHT_CYAN}{action}"
    )

    print(
        f"\n  {GRAY}Nothing has been changed yet."
    )

    print(
        f"  {GRAY}Type {BOLD}{YELLOW}LEAVE{RESET}"
        f"{GRAY} to continue."
    )

    print(
        f"  {GRAY}Anything else will cancel the operation."
    )

    print()

    answer = input(
        f"{CYAN}  └─ Confirmation: {WHITE}"
    ).strip().upper()

    return answer == "LEAVE"


# ============================================================
# PROGRESS BAR
# ============================================================

def progress_bar(current, total, width=35):

    if total == 0:
        return

    percentage = current / total

    filled = int(width * percentage)

    bar = "█" * filled + "░" * (width - filled)

    print(
        f"\r  {CYAN}[{bar}] "
        f"{WHITE}{current}/{total}",
        end="",
        flush=True
    )


# ============================================================
# PROCESS ITEMS
# ============================================================

async def process_items(items, action):

    if not items:

        print(
            f"\n{YELLOW}No items available for this operation."
        )

        pause()

        return

    if not confirmation_screen(items, action):

        print(
            f"\n{YELLOW}✕ Operation cancelled."
        )

        pause()

        return

    section(action.upper())

    success = 0
    failed = 0

    total = len(items)

    print()

    for index, dialog in enumerate(items, 1):

        try:

            await client.delete_dialog(
                dialog.entity
            )

            success += 1

            print(
                f"\n  {GREEN}✓{RESET} "
                f"{WHITE}{dialog.name}"
            )

        except FloodWaitError as e:

            print(
                f"\n  {YELLOW}⏳ Flood protection triggered."
            )

            print(
                f"     Waiting {e.seconds} seconds..."
            )

            await asyncio.sleep(e.seconds)

            try:

                await client.delete_dialog(
                    dialog.entity
                )

                success += 1

                print(
                    f"  {GREEN}✓{RESET} "
                    f"{WHITE}{dialog.name}"
                )

            except Exception as retry_error:

                failed += 1

                print(
                    f"  {RED}✗{RESET} "
                    f"{WHITE}{dialog.name}"
                )

                print(
                    f"    {GRAY}{retry_error}"
                )

        except Exception as e:

            failed += 1

            print(
                f"\n  {RED}✗{RESET} "
                f"{WHITE}{dialog.name}"
            )

            print(
                f"    {GRAY}{e}"
            )

        progress_bar(index, total)

        await asyncio.sleep(0.35)

    print("\n")

    section("OPERATION COMPLETE")

    status(
        "Successful",
        str(success),
        GREEN
    )

    status(
        "Failed",
        str(failed),
        RED if failed else GREEN
    )

    status(
        "Processed",
        f"{success + failed}/{total}",
        LIGHT_CYAN
    )

    pause()


# ============================================================
# SEARCH
# ============================================================

def search_items(query, groups, channels, bots):

    query = query.lower()

    matches = []

    for dialog in groups:

        if query in dialog.name.lower():

            matches.append(
                ("GROUP", dialog)
            )

    for dialog in channels:

        if query in dialog.name.lower():

            matches.append(
                ("CHANNEL", dialog)
            )

    for dialog in bots:

        if query in dialog.name.lower():

            matches.append(
                ("BOT", dialog)
            )

    return matches


# ============================================================
# SEARCH MENU
# ============================================================

async def search_menu(groups, channels, bots):

    section("GLOBAL SEARCH")

    query = input(
        f"\n  {CYAN}Search: {WHITE}"
    ).strip()

    if not query:

        print(
            f"\n{YELLOW}Search query cannot be empty."
        )

        pause()

        return

    loading("Searching...")

    matches = search_items(
        query,
        groups,
        channels,
        bots
    )

    if not matches:

        print(
            f"\n{YELLOW}No matches found for "
            f"\"{query}\"."
        )

        pause()

        return

    section(
        f"SEARCH RESULTS • {len(matches)} MATCHES"
    )

    for i, (kind, dialog) in enumerate(
        matches,
        1
    ):

        if kind == "GROUP":
            color = LIGHT_CYAN

        elif kind == "CHANNEL":
            color = LIGHT_MAGENTA

        else:
            color = YELLOW

        print(
            f"  {CYAN}{i:>4}{GRAY} │ "
            f"{color}[{kind:<7}] "
            f"{WHITE}{dialog.name}"
        )

    print()

    print(
        f"  {GRAY}Examples:"
    )

    print(
        f"  {WHITE}2"
    )

    print(
        f"  {WHITE}2,5,8"
    )

    print(
        f"  {WHITE}2-10"
    )

    print(
        f"  {WHITE}2-10,15-20"
    )

    text = input(
        f"\n  {CYAN}Select: {WHITE}"
    )

    indexes = parse_selection(
        text,
        len(matches)
    )

    selected = [
        matches[i][1]
        for i in indexes
    ]

    await process_items(
        selected,
        "Processing selected search results"
    )


# ============================================================
# SPECIFIC ITEM MENU
# ============================================================

async def specific_menu(
    items,
    title,
    action
):

    if not items:

        print(
            f"\n{YELLOW}No {title.lower()} found."
        )

        pause()

        return

    print_section(
        title,
        items
    )

    print()

    print(
        f"  {GRAY}Selection examples:"
    )

    print(
        f"  {WHITE}2"
    )

    print(
        f"  {WHITE}2,5,8"
    )

    print(
        f"  {WHITE}2-19"
    )

    print(
        f"  {WHITE}2-19,21-28,30-87,89-240"
    )

    print()

    text = input(
        f"  {CYAN}Select numbers/ranges: {WHITE}"
    )

    indexes = parse_selection(
        text,
        len(items)
    )

    selected = [
        items[i]
        for i in indexes
    ]

    await process_items(
        selected,
        action
    )


# ============================================================
# MAIN MENU
# ============================================================

def show_menu():

    section("MAIN CONTROL PANEL")

    print(
        f"\n  {CYAN}[01]{WHITE} Leave specific groups"
    )

    print(
        f"  {CYAN}[02]{WHITE} Leave specific channels"
    )

    print(
        f"  {CYAN}[03]{WHITE} Delete specific bot chats"
    )

    print(
        f"  {CYAN}[04]{WHITE} Search group/channel/bot"
    )

    print(
        f"  {CYAN}[05]{RED} Leave ALL groups"
    )

    print(
        f"  {CYAN}[06]{RED} Leave ALL channels"
    )

    print(
        f"  {CYAN}[07]{RED} Delete ALL bot chats"
    )

    print(
        f"  {CYAN}[08]{WHITE} Refresh account"
    )

    print(
        f"  {CYAN}[09]{WHITE} Exit"
    )

    print()


# ============================================================
# MAIN
# ============================================================

async def main():

    clear_screen()

    show_banner()

    section("SYSTEM STATUS")

    status(
        "Application",
        "TELESWEEP",
        LIGHT_CYAN
    )

    status(
        "Session",
        SESSION_NAME,
        GREEN
    )

    status(
        "Mode",
        "Account Cleanup",
        LIGHT_MAGENTA
    )

    print()

    loading(
        "Connecting to Telegram..."
    )

    if not client.is_connected():

        print(
            f"\n{RED}✗ Unable to connect to Telegram."
        )

        return

    print(
        f"{GREEN}✓ Telegram connection established."
    )

    await asyncio.sleep(0.5)

    while True:

        clear_screen()

        show_banner()

        groups, channels, bots = (
            await scan_account()
        )

        show_summary(
            groups,
            channels,
            bots
        )

        print_section(
            "GROUPS",
            groups,
            "◆"
        )

        print_section(
            "CHANNELS",
            channels,
            "◆"
        )

        print_section(
            "BOT CHATS",
            bots,
            "◆"
        )

        show_menu()

        choice = input(
            f"{CYAN}  └─ Select option {GRAY}(1-9){CYAN}: "
            f"{WHITE}"
        ).strip()

        # ----------------------------------------------------
        # 1 - SPECIFIC GROUPS
        # ----------------------------------------------------

        if choice == "1":

            await specific_menu(
                groups,
                "GROUPS",
                "Leaving selected groups"
            )

        # ----------------------------------------------------
        # 2 - SPECIFIC CHANNELS
        # ----------------------------------------------------

        elif choice == "2":

            await specific_menu(
                channels,
                "CHANNELS",
                "Leaving selected channels"
            )

        # ----------------------------------------------------
        # 3 - SPECIFIC BOTS
        # ----------------------------------------------------

        elif choice == "3":

            await specific_menu(
                bots,
                "BOT CHATS",
                "Deleting selected bot chats"
            )

        # ----------------------------------------------------
        # 4 - SEARCH
        # ----------------------------------------------------

        elif choice == "4":

            await search_menu(
                groups,
                channels,
                bots
            )

        # ----------------------------------------------------
        # 5 - ALL GROUPS
        # ----------------------------------------------------

        elif choice == "5":

            await process_items(
                groups,
                "Leaving ALL groups"
            )

        # ----------------------------------------------------
        # 6 - ALL CHANNELS
        # ----------------------------------------------------

        elif choice == "6":

            await process_items(
                channels,
                "Leaving ALL channels"
            )

        # ----------------------------------------------------
        # 7 - ALL BOTS
        # ----------------------------------------------------

        elif choice == "7":

            await process_items(
                bots,
                "Deleting ALL bot chats"
            )

        # ----------------------------------------------------
        # 8 - REFRESH
        # ----------------------------------------------------

        elif choice == "8":

            print(
                f"\n{CYAN}Refreshing account..."
            )

            await asyncio.sleep(1)

        # ----------------------------------------------------
        # 9 - EXIT
        # ----------------------------------------------------

        elif choice == "9":

            clear_screen()

            print(
                f"\n{CYAN}╔════════════════════════════════════════════════════════════╗"
            )

            print(
                f"{CYAN}║                                                            ║"
            )

            print(
                f"{CYAN}║       {GREEN}{BOLD}✓ TELESWEEP SESSION CLOSED{CYAN}                       ║"
            )

            print(
                f"{CYAN}║                                                            ║"
            )

            print(
                f"{CYAN}║       {GRAY}Made by Paul                                      {CYAN}║"
            )

            print(
                f"{CYAN}║       {GRAY}Telegram: {LIGHT_CYAN}@vibezat1k{CYAN}                         ║"
            )

            print(
                f"{CYAN}║                                                            ║"
            )

            print(
                f"{CYAN}╚════════════════════════════════════════════════════════════╝"
            )

            print()

            break

        # ----------------------------------------------------
        # INVALID
        # ----------------------------------------------------

        else:

            print(
                f"\n{RED}✗ Invalid option."
            )

            await asyncio.sleep(1)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    try:

        with client:

            client.loop.run_until_complete(
                main()
            )

    except KeyboardInterrupt:

        print(
            f"\n\n{YELLOW}⚠ TELESWEEP stopped by user."
        )

        print(
            f"{GRAY}No further operations were performed."
        )

    except Exception as e:

        print(
            f"\n{RED}✗ Fatal error:"
        )

        print(
            f"{GRAY}{e}"
        )

        input(
            "\nPress ENTER to exit..."
        )