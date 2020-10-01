## Description
This repository contains main data service. This service is an interface to interact with data base and face recognition service. 

## API
End-points:
- /analyze_face - endpoint receives image that contains face of unknown criminal. If face was recognized, image and face embeddings will be added to database and associated with recognized criminal. User will get back information about this criminal. If face wasn't recognized, image will be automatically added to data base as unknown criminal.
- /add_data - endpoint receives data about known criminal (with photo or without) and add this data to data base. If images are attached, then these images with their face embeddings also will be added to database.
- /update_data - endpoint allows users to update existing entries in the data base. For example, user can add photo to description of previously known but unseen criminal. Or add text info to previously unknown photo. 
- /check_entity - check if there is criminal with entered name or data base id. Service need this type of request to allow update information about existing entries.
- /get_info - get information about criminal by data base id, location or name.


## DBConnector
Bunch of scripts, that allows to interact with PostgreSQL database.