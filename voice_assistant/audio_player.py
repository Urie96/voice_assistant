#!/usr/bin/env python3

import subprocess


class RealtimeMp3Player:
    def __init__(self):
        self.ffmpeg_process = subprocess.Popen(
            [
                "ffplay",
                "-autoexit",
                "-nodisp",
                "-i",
                "-",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )  # initialize ffmpeg to decode mp3
        print("mp3 audio player is started")

    def stop(self):
        try:
            print("stopping mp3 audio player")
            self.ffmpeg_process.stdin.close()
            self.ffmpeg_process.wait()
            if self.ffmpeg_process:
                self.ffmpeg_process.terminate()
            print("mp3 audio player is stopped")
        except subprocess.CalledProcessError as e:
            # Capturing ffmpeg exceptions, printing error details
            print(f"An error occurred: {e}")

    def write(self, data: bytes) -> None:
        # print('write audio data:', len(data))
        try:
            self.ffmpeg_process.stdin.write(data)
            self.ffmpeg_process.stdin.flush()
        except subprocess.CalledProcessError as e:
            # Capturing ffmpeg exceptions, printing error details
            print(f"An error occurred: {e}")
