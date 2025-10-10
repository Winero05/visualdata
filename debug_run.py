"""
Debug runner for PyQt5_Complete_App.py
Runs the app and writes any exception traceback to debug_traceback.txt so you can paste it here.

Usage (PowerShell):
& C:/path/to/python.exe debug_run.py
# After it exits (or if it crashes), open debug_traceback.txt
Get-Content debug_traceback.txt -Raw
"""
import traceback
import sys

def run():
    try:
        import PyQt5_Complete_App as app
        # call main() so the same startup sequence runs; exceptions will be caught below
        try:
            app.main()
        except Exception:
            # write traceback when main raises
            with open('debug_traceback.txt', 'w', encoding='utf-8') as f:
                traceback.print_exc(file=f)
            print("Traceback written to debug_traceback.txt")
    except Exception:
        # import-time errors
        with open('debug_traceback.txt', 'w', encoding='utf-8') as f:
            traceback.print_exc(file=f)
        print("Import-time traceback written to debug_traceback.txt")

if __name__ == '__main__':
    run()
