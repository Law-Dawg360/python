name: Get Channel Info

on:
  push:
    branches:
      - main
  workflow_dispatch:  # Manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v2
      
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
        
    - name: Install dependencies
      run: |
        pip install --upgrade pip
        
    - name: Execute Python script
      run: python 1_YouTube/yt_Scripts/get_channel_info.py
      env:
        API_KEY: ${{ secrets.API_KEY }}
