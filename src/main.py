from gui import OrderForm
from automation import AutomationHelper

def main():
    # TODO: Implement opening NAVISION

    # Create the OrderForm
    app = OrderForm()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()

