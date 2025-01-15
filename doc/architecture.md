   # Application Architecture

   ProxyPulse is designed with a modular architecture to ensure scalability and maintainability. The main components are:

   - **src/proxy_tester.py**: Contains the core logic for testing proxies asynchronously.
   - **src/gui_app.py**: Implements the Tkinter-based graphical user interface.
   - **tests/tests.py**: Contains unit tests for the proxy testing functionality.
   - **data/**: Stores input (`proxies.txt`) and output (`proxies.json`) files.
   - **config/**: Contains configuration settings (`config.json`).
   - **logs/**: Stores application logs (`app.log`).

   The application follows a clear separation of concerns, with the GUI and proxy testing logic kept independent for easier updates and debugging.
