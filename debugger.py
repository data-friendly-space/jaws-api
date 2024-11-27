from os import getenv

def initialize_debugger_if_needed():
    if getenv("DEBUGGER") == "True":
        import multiprocessing

        if multiprocessing.current_process().pid > 1:
            import debugpy

            debugpy.listen(("0.0.0.0", 8001))
            print("⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳", flush=True)