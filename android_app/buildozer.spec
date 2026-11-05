
name: Build Nifty Order Flow Android APK

on:
  workflow_dispatch:
  push:
    branches:
      - main
    paths:
      - "android_app/**"
      - ".github/workflows/build-apk.yml"

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-22.04
    timeout-minutes: 60

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Check Android app files
        run: |
          test -f android_app/main.py
          test -f android_app/buildozer.spec

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - name: Install Android build dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            build-essential git zip unzip \
            autoconf automake libtool pkg-config \
            zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 \
            cmake libffi-dev libssl-dev libltdl-dev gettext autopoint

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip setuptools wheel
          python -m pip install "buildozer==1.5.0" "Cython==0.29.33"

      - name: Build debug APK
        working-directory: android_app
        env:
          BUILDOZER_WARN_ON_ROOT: "0"
        run: buildozer -v android debug

      - name: Upload APK artifact
        uses: actions/upload-artifact@v4
        with:
          name: nifty-orderflow-debug-apk
          path: android_app/bin/*.apk
          if-no-files-found: error
          retention-days: 14
