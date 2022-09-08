# Getting Started  

### Installation

```sh
git clone https://github.com/
python -m venv .venv
pip install -r requirements.txt
```

### Run

```sh
python -m run.py
```

# Pseudocode

### multiprocessing
    Initialize process_List
    create save_url_Process
    append save_url_Process to process_List
    start save_url_Process
    for _ in range(maximum count of processes)
        create get_data_Process
        append get_data_Process to process_List
        start get_data_Process

    for Process in process_List
        join Process

### save url process
    Initialize url_Queue
    for _ in range(maximum count of page)
        go to url
        get elements with an href attribute
        for element in elements
            push element with an href attribute for url_Queue

### get data process
    while url_Queue not empty
        get url for url_Queue
            go to url
            get data
            save data for database