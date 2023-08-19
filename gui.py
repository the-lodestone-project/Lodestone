from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Markdown, TabbedContent, TabPane, LoadingIndicator, OptionList, Select
from pathlib import Path
from textual import on
from importlib_metadata import version
from rich import box
from rich.console import RenderableType
from rich.json import JSON
# from rich.markdown import Markdown
from rich.pretty import Pretty
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from textual.containers import Center

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    RichLog,
    Static,
    Switch,
)


Getting_Started = """
# Open Delivery Bot - Getting Started

Welcome to the Open Delivery Bot project! This open-source initiative empowers users to deploy a self-hosted delivery bot, offering an array of advanced functionalities. Our command-line interface (CLI) or remote web GUI allows effortless control and management, ensuring a seamless experience.

Open Delivery Bot shines with its dynamic features, including pathfinding and optimized elytra flight, accelerating your delivery processes for utmost efficiency. Say goodbye to manual intervention and embrace automation! 📦

## Features

Some of the many features included in Open Delivery Bot

- Ease of use
- Server ready
- Supports all account types
- Pathfinding & Elytra

*And more to come!*

## How to use

To control this interface you can use the arrow keys to move between tabs. Alternatively you can also use the mouse to select and click on tabs.




"""

Commnands = """
# Run remote commands

*Remote commands will be available afer startup*
"""

Live_View = """
# Live view

*Live view will be available afer startup*
"""

Auth = """
# Authentication (microsoft, mojang & cracked)

Please enter your username and password for you mojang or microsoft account.
"""





LINES = """Microsoft account
Mojang account (legacy)
Cracked""".splitlines()





class TabbedApp(App):
    """An example of tabbed content."""
    
    CSS = """
    Select {
        width: 35%;
    }
    
    .label {
        text-align: center;
    }
    
    .login {
        width: auto;
        
        
    }
    """


    BINDINGS = [
        ("1", "show_tab('leto')", "Getting Started"),
        ("2", "show_tab('paul')", "Auth"),
        ("3", "show_tab('Settings')", "Settings"),
        ("4", "show_tab('paul')", "Run Commnands"),
        ("5", "show_tab('paul')", "Live View"),
        ("6", "show_tab('paul')", "Run"),
        
    ]
    

    def compose(self) -> ComposeResult:
        """Compose app with tabbed content."""
        # Footer to show keys
        # yield LoadingIndicator()

        yield Footer()

        # Add the TabbedContent widget
        with TabbedContent():
            
            with TabPane("Getting Started"):  # First tab
                yield Markdown(Getting_Started, classes="label")  # Tab content
            with TabPane("Auth"):
                yield Markdown(Auth)
                with Center():
                    yield Select((line, line) for line in LINES)
                    yield Static("Username", classes="label")
                    yield Input(placeholder="Username")
                    yield Static("Password", classes="label")
                    yield Input(placeholder="Password", password=True)
                    yield Static()
                
                    yield Button("Login", variant="primary", classes="login")
            with TabPane("Settings"):
                yield Markdown(Commnands)
            with TabPane("Run Commnands"):
                yield Markdown(Commnands)
            with TabPane("Live View"):
                yield Markdown(Live_View)
            with TabPane("Run"):
                yield Markdown(Commnands)
                
                
    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)       

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab


if __name__ == "__main__":
    app = TabbedApp()
    app.run()
