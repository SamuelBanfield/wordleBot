if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'solver':
        from bot.wordle_solver_ui import main
    else:
        from bot.wordle import main
    main()