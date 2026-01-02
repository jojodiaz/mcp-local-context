#!/bin/bash

if test -e ".env"; then 
    echo ".env file already exists."
else
    touch .env
    echo "-----------------------------------------"
    echo ".env file with following keys added\n"
    sleep 0.25
    echo "ANTHROPIC_API_KEY=" | tee -a .env
    sleep 0.25
    echo "DATABASE_USERNAME=" | tee -a .env
    sleep 0.25
    echo "DATABASE_PASSWORD=" | tee -a .env
    sleep 0.25
    
    echo "\nAdding .env file to .gitignore\n"
    sleep 0.25
    if [ -e .gitignore ]; then 
        echo ".env" >> ".gitignore" # TODO: CHECK IF .gitignore HAS .env already set.
        sleep 0.25
        echo ".env added to .gitignore"
    else
        echo "Creating .gitignore, NEVER push changes with .env variables exposed"
        sleep 0.25
        touch .gitignore
        echo ".env" >> ".gitignore"
        sleep 0.25
        echo "\".env\" added to .gitignore"
    fi
    echo "-----------------------------------------"
fi