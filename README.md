# flask-chat-app
A real time messaging chat application built with Flask, SocketIO and MongoDB.
Minimal, easy to use and modify web based chat application, built with the power of Flask.
## Prerequisites
* Clone the repository ```git clone https://github.com/mahmouddello/flask-chat-app```
* Cd into the project directory `cd ./flask-chat-app`
### Requirements
Use ```pip install -r requirements.txt``` to install all required modules from [requirements.txt](./requirements.txt).

### Database
  * Create your own Mongo Database either locally or on Mongo Atlas (Preffered).
  * Create sequence value incrementer for ```room_id``` in MongoDB, here is an example:
    
    ```python
    from pymongo import MongoClient

    client = MongoClient('MongoDB_URI')

    # Create or access the sequences collection
    db = client['your_database_name']
    sequences_collection = db['sequences']

    # sequence name can be `room_id`
    def get_next_sequence_value(sequence_name):
    result = sequences_collection.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,  # Create the sequence if it doesn't exist
        return_document=True  # Return the updated document
    )

    return result["sequence_value"]
    
    ```
<hr>
<div align="center">
    <strong>Happy Coding! 💻🎉</strong>
</div>
