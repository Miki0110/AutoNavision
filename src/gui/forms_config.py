import tkinter as tk

def create_form_configs(order_name_var):
    """
    Returns a dictionary containing all the form configurations.
    Each form is keyed by a form name (e.g., 'Internal commissioning'),
    and the 'fields' list specifies the widgets to display.
    """
    form_configs = {
        # ------------------ Case Work ------------------
        'Internal commissioning': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                {'label': 'Order Name', 'type': 'ordername_combobox', 'var': tk.StringVar()},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring', 'Software Møde'], 'var': tk.StringVar(), 'default': 'Intern Indkøring'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'External commissioning': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                {'label': 'Order Name', 'type': 'ordername_combobox', 'var': tk.StringVar()},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring', 'Kørsel/Rejsetid', 'Software Møde'], 'var': tk.StringVar(), 'default': 'Extern Indkøring'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'Software': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                {'label': 'Order Name', 'type': 'ordername_combobox', 'var': tk.StringVar()},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Software', 'Intern Indkøring', 'Extern Indkøring', 'Kørsel/Rejsetid', 'Software Møde'], 'var': tk.StringVar(), 'default': 'Software'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        # ------------------ Driving ------------------
        'Driving': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'ordernumber_combobox', 'var': tk.StringVar()},
                {'label': 'Order Name', 'type': 'ordername_combobox', 'var': tk.StringVar()},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Kørsel/Rejsetid'], 'var': tk.StringVar(), 'default': 'Kørsel/Rejsetid'},
                {'label': 'Driving Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar()},
                {'label': 'Number plate', 'type': 'platenumber_combobox', 'var': tk.StringVar()},
                {'label': 'Car', 'type': 'car_combobox', 'var': tk.StringVar()},
                {'label': 'From Address', 'type': 'address_combobox', 'var': tk.StringVar()},
                {'label': 'To Address', 'type': 'address_combobox', 'var': tk.StringVar()},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        # ------------------ "Uproduktiv Tid" ------------------
        'Internal meetings': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Intern Møde'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'Internal courses': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Kurses Intern'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'External courses': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Kontor tid', 'Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Kursus Extern'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'Deskwork': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Kontor tid', 'Kurses Intern', 'Kursus Extern', 'Intern Møde'], 'var': tk.StringVar(), 'default': 'Kontor tid'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        # ------------------ Free Days ------------------
        'Holiday': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Ferie'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'Sickday': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Sygdom'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'Childs Sickday': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Barns sygedag'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        },
        'Compensatory Leave': {
            'fields': [
                {'label': 'Order Type', 'type': 'label', 'var': tk.StringVar(), 'default': 'Sag'},
                {'label': 'Date', 'type': 'date_entry', 'var': tk.StringVar()},
                {'label': 'Order Number', 'type': 'label', 'var': tk.StringVar(), 'default': 'Uproduktiv tid'},
                {'label': 'Order Line', 'type': 'combobox', 'options': ['Ferie', 'Sygdom', 'Barns sygedag', 'Afspasering'], 'var': tk.StringVar(), 'default': 'Afspasering'},
                {'label': 'Time (H:M:S)', 'type': 'time_entry', 'var': tk.StringVar(), 'default': '08:00:00'},
                {'label': 'Description', 'type': 'text', 'var': tk.StringVar()},
            ]
        }
    }

    # Append 'Multiple Days' and 'End Date' field to each form
    for form_name, config in form_configs.items():
        config['fields'].append({
            'label': 'Multiple Days',
            'type': 'checkbox',
            'var': tk.BooleanVar(), 
            'default': False
        })
        config['fields'].append({
            'label': 'End Date',
            'type': 'date_entry',
            'var': tk.StringVar(),
            'state': 'disabled'
        })

    return form_configs
