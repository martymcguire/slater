#!/usr/bin/env python

def main():
    from slater.app import create_app
    app = create_app()
    app.run(debug=True, port=5001)

main()
