class EventRemove:
    def __init__(self):
        pass

    @staticmethod
    def event_remover(events_dict, events_index):
        remove_event_id = input("Enter the event's ID that you wish to remove: ")
        
        if remove_event_id not in events_index:
            print("Event not found. Please try again.\n")
            return events_dict
        
        date, _ = events_index[remove_event_id]
                
        del events_dict[date][remove_event_id]
        if not events_dict[date] : del events_dict[date]
        
        print(f"Event with event ID '{remove_event_id}' has been successfully removed!")

        return events_dict