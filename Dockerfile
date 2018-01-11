from python:2-slim

run mkdir /app
workdir /app

copy requirements.txt .

run BUILD_DEPS='gcc' \
  && apt-get update \
  && apt-get install -y $BUILD_DEPS \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --no-cache-dir -r requirements.txt \
  && apt-get purge -y --auto-remove $BUILD_DEPS

copy . .

volume /data
run ln -s /data/settings_local.py /app/main/settings_local.py
