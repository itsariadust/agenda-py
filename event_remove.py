class EventRemove:
    def __init__(self):
        pass

    @staticmethod
    def event_remover(event_id, events_dict, events_index):
        if event_id not in events_index:
            print("Event not found. Please try again.\n")
            return events_dict
        
        date, _ = events_index[event_id]
                
        del events_dict[date][event_id]
        if not events_dict[date] : del events_dict[date]
        
        print(f"Event with event ID '{event_id}' has been successfully removed!")

        return events_dict