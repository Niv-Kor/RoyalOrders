def perform(root, func, *args):
    root.after(0, func, args=args)
